"""Write operations — create and update files in the course workspace.

Phase 2: all file-mutating operations.  Each function is idempotent where
possible and validates inputs before writing.
"""

from __future__ import annotations

import json
import shutil
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Optional

from .models import (
    ActionMode,
    CourseContext,
    InboxUIMode,
    InteractionState,
    KPInfo,
    KPStatus,
    ParsedRequest,
    ProgressSnapshot,
    SessionType,
)
from .registry import resolve_course
from .knowledge import get_all_kps, get_progress, load_knowledge_registry
from .state import detect_state, get_inbox_ui_mode


# ── Session notes ────────────────────────────────────────────────────────


def create_session_note(
    ctx: CourseContext,
    session_type: SessionType,
    kp_list: list[KPInfo],
    request: ParsedRequest | None = None,
) -> Path:
    """Create a new session note in SESSIONS/ and return its path.

    Does NOT overwrite existing notes.  Returns the path to the new file.
    """
    sessions_dir = ctx.sessions_dir
    if not sessions_dir:
        sessions_dir = ctx.course_root / "SESSIONS"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).astimezone()
    ts = now.strftime("%Y-%m-%d-%H%M")
    slug = _slug_for_session(session_type, kp_list)
    filename = f"{ts}-{session_type.value}-{slug}.md"
    path = sessions_dir / filename

    # Build frontmatter
    fm = {
        "type": "academic-coach-session",
        "session_type": session_type.value,
        "status": "draft",
        "course": ctx.course_name,
        "course_id": ctx.course_id,
        "created": now.isoformat(),
        "updated": now.isoformat(),
        "knowledge_points": [
            {
                "id": kp.kp_id,
                "name": kp.name,
                "status_before": kp.status.value,
            }
            for kp in kp_list
        ],
        "source": "inbox" if request else "chat",
    }
    if request:
        fm["request_details"] = request.details[:200] if request.details else ""

    # Build body
    progress = get_progress(ctx)
    body_parts = [
        "## Status",
        "",
        f"| 当前课程 | {ctx.course_name} |",
        f"| 当前知识点 | {kp_list[0].kp_id} — {kp_list[0].name if kp_list[0].name else kp_list[0].kp_id} |" if kp_list else "",
        f"| 总体进度 | {progress.percent}% ({progress.mastered}/{progress.total} mastered) |",
        "",
        "## Request",
        "",
        f"- Source: {fm['source']}",
        f"- Mode: {session_type.value}",
        "",
    ]
    if request and request.details:
        body_parts.append(f'- Details: "{request.details[:200]}"')
        body_parts.append("")

    body_parts += [
        "## Pre-Session State",
        "",
    ]
    for kp in kp_list:
        body_parts.append(f"- {kp.kp_id}: {kp.status.value}" + (f" (score: {kp.score})" if kp.score else ""))
    body_parts += [
        "",
        "## Teaching",
        "",
        "[agent writes here]",
        "",
        "## Assessment",
        "",
        "[agent writes questions here; user answers are copied in after each submit]",
        "",
        "## Evaluation",
        "",
        "[completed after all questions scored]",
        "",
        "## State Changes",
        "",
        "[completed after evaluation]",
        "",
        "## Next Steps",
        "",
        "[completed after evaluation]",
        "",
    ]

    body = "\n".join(body_parts)

    # Write file
    yaml_fm = _dump_yaml_frontmatter(fm)
    path.write_text(f"---\n{yaml_fm}---\n\n{body}", encoding="utf-8")
    return path


def append_answer(session_path: Path, q_num: int, answer: str) -> None:
    """Append the user's answer to an existing session note."""
    content = session_path.read_text(encoding="utf-8")
    marker = f"### Question {q_num}"
    if marker not in content:
        content += f"\n\n{marker}\n"
    content += f"\n**Your Answer:**\n{answer}\n"
    session_path.write_text(content, encoding="utf-8")


def finalize_session(
    session_path: Path,
    total_score: float,
    max_score: float,
    mastery_decisions: dict[str, KPStatus],
    feedback: str = "",
) -> None:
    """Mark a session as completed and write the evaluation summary."""
    content = session_path.read_text(encoding="utf-8")
    now = datetime.now(timezone.utc).astimezone().isoformat()

    # Update frontmatter status
    content = content.replace("status: draft", "status: completed")
    content = content.replace("status: active", "status: completed")
    content = content.replace("status: awaiting_user_answer", "status: completed")
    content = content.replace("status: evaluating", "status: completed")
    content = content.replace(
        "updated: ", f"updated: {now}\n# original_updated: "
    )

    # Replace Evaluation placeholder
    eval_block = f"""## Evaluation

| Metric | Value |
|---|---|
| Total score | {total_score}/{max_score} |
| Percentage | {round(total_score / max_score * 100, 1)}% |
| Mastery decisions | {', '.join(f'{kpid}→{s.value}' for kpid, s in mastery_decisions.items())} |

{feedback}
"""
    content = content.replace(
        "## Evaluation\n\n[completed after all questions scored]",
        eval_block.strip(),
    )

    session_path.write_text(content, encoding="utf-8")


def cancel_session(session_path: Path, reason: str = "") -> None:
    """Mark a session as cancelled."""
    content = session_path.read_text(encoding="utf-8")
    content = content.replace("status: draft", "status: cancelled")
    content = content.replace("status: active", "status: cancelled")
    content = content.replace("status: awaiting_user_answer", "status: cancelled")
    if reason:
        content += f"\n\n## Cancellation Note\n{reason}\n"
    session_path.write_text(content, encoding="utf-8")


# ── INBOX rendering ──────────────────────────────────────────────────────


def render_inbox(ctx: CourseContext, mode: InboxUIMode | None = None) -> None:
    """Render INBOX.md in the correct UI mode for the current state."""
    if mode is None:
        mode = get_inbox_ui_mode(ctx)

    # Progress may not be available (e.g. fresh workspace) — use defaults
    try:
        progress = get_progress(ctx)
    except Exception:
        progress = ProgressSnapshot(total=0, mastered=0, learning=0, weak=0, unseen=0, forgotten=0)
    inbox_path = ctx.inbox_path
    if not inbox_path:
        inbox_path = ctx.course_root / "INBOX.md"

    exam_str = ctx.config.get("exam_date", "") or (
        ctx.registry_entry.get("exam_date", "") if hasattr(ctx, "registry_entry") else ""
    )
    exam_line = ""
    if exam_str:
        try:
            ed = date.fromisoformat(exam_str[:10])
            days = (ed - date.today()).days
            if days <= 14:
                exam_line = f"> **Exam:** {exam_str[:10]} ({days} days)"
        except (ValueError, IndexError):
            pass

    content = _render_mode(ctx, mode, progress, exam_line)
    inbox_path.parent.mkdir(parents=True, exist_ok=True)
    inbox_path.write_text(content, encoding="utf-8")


def _render_mode(
    ctx: CourseContext,
    mode: InboxUIMode,
    progress: ProgressSnapshot,
    exam_line: str,
) -> str:
    """Render a specific inbox UI mode."""
    base = f"""# INBOX — {ctx.course_name}

> **Status:** {_status_banner(mode)}
> **Progress:** {progress.percent}% ({progress.mastered}/{progress.total} mastered) | {progress.learning} learning | {progress.weak} weak | {progress.unseen} unseen
{exam_line}

"""

    if mode == InboxUIMode.COMMAND_ENTRY:
        return base + _render_command_entry()

    elif mode == InboxUIMode.CLARIFICATION:
        # Clarification mode is populated by the LLM during processing.
        # We just ensure the shell exists.
        return base + _render_clarification_shell()

    elif mode == InboxUIMode.ANSWER_ENTRY:
        return base + _render_answer_entry_shell()

    elif mode == InboxUIMode.POST_COMPLETION:
        return base + _render_post_completion_shell()

    return base


def _render_command_entry() -> str:
    return """## ▶ Action

- [ ] **continue** — 继续学习下一个知识点
- [ ] **review** — 复习到期内容
- [ ] **weak** — 针对性强化薄弱项
- [ ] **exam** — 进入考试/模拟考试模式
- [ ] **plan** — 生成/更新学习计划
- [ ] **sync** — 同步新资料（PPT/PDF/笔记）
- [ ] **audit** — 检查学习系统一致性
- [ ] **status** — 查看完整进度报告

## ✏ Request Details

<!-- 在这里写你的要求。随意写，不用纠结格式。 -->

（在此处写下你的学习请求，或在终端输入 academic-coach inbox 处理已选动作）

## 📎 Optional Context

<!-- 贴链接、话题提示、材料路径、图片等（可选） -->

---

<!-- 以下由系统维护，请勿手动编辑 -->
_Last processed: — | Mode: command-entry | Course: {{course_id}}_
"""


def _render_clarification_shell() -> str:
    return """## ❓ Agent needs more info

_The system needs answers to these questions before it can proceed._

[agent writes clarification questions here]

## ✏ Your Answers

[answer each question here]

---

<!-- 以下由系统维护，请勿手动编辑 -->
_Last processed: — | Mode: clarification_
"""


def _render_answer_entry_shell() -> str:
    return """## 📖 What the agent taught

[agent writes brief summary here — full content in session note]

## ❓ Current Question

[agent writes current question here]

## ✏ Your Answer

[write your answer here — use LaTeX $$, Mermaid, or images as needed]

---

<!-- 以下由系统维护，请勿手动编辑 -->
_Last processed: — | Mode: answer-entry_
"""


def _render_post_completion_shell() -> str:
    return """## 📊 Result

[completion summary — score, mastery decision, time]

## 📝 Feedback

[strengths and areas to improve]

## 🔜 Next

[recommended next action]

---

## ▶ New Action

- [ ] **continue** — 继续学习
- [ ] **review** — 复习到期内容
- [ ] **weak** — 针对性强化
- [ ] **exam** — 进入考试模式
- [ ] **plan** — 更新学习计划

## ✏ Request Details

<!-- Ready for your next request -->

---

<!-- 以下由系统维护，请勿手动编辑 -->
_Last processed: — | Mode: post-completion_
"""


# ── OUTBOX rendering ─────────────────────────────────────────────────────


def render_outbox(
    ctx: CourseContext,
    summary: str,
    next_action: str = "",
    session_path: str | None = None,
) -> None:
    """Write a concise result summary to OUTBOX.md."""
    outbox = ctx.outbox_path or (ctx.course_root / "OUTBOX.md")
    outbox.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    parts = [
        f"# OUTBOX — {ctx.course_name}",
        "",
        f"> Updated: {now}",
        "",
        "## Result",
        "",
        summary,
        "",
    ]
    if session_path:
        parts.append(f"**Session:** [[{session_path}]]")
        parts.append("")
    if next_action:
        parts.append("## Next")
        parts.append("")
        parts.append(next_action)
        parts.append("")

    outbox.write_text("\n".join(parts), encoding="utf-8")


# ── DASHBOARD refresh ────────────────────────────────────────────────────


def refresh_dashboard(ctx: CourseContext) -> None:
    """Update DASHBOARD.md with current progress and status."""
    dash = ctx.dashboard_path or (ctx.course_root / "DASHBOARD.md")
    dash.parent.mkdir(parents=True, exist_ok=True)

    progress = get_progress(ctx)
    state = detect_state(ctx)
    due = _get_due_ids(ctx)

    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    content = f"""# DASHBOARD — {ctx.course_name}

> Updated: {now} | Mode: {ctx.interaction_mode} / {ctx.workspace_mode}
> State: {state.value}

## Progress

| Status | Count |
|---|---|
| ✓ mastered | {progress.mastered} |
| ◐ learning | {progress.learning} |
| ⚠ weak | {progress.weak} |
| □ unseen | {progress.unseen} |
| ✗ forgotten | {progress.forgotten} |
| **Total** | **{progress.total}** |

**Overall: {progress.percent}%**

## Due Reviews

"""
    if due:
        for d in due:
            content += f"- {d}\n"
    else:
        content += "None due today.\n"

    content += f"""
## Quick Actions

- `academic-coach continue` — keep learning
- `academic-coach review` — handle due reviews
- `academic-coach inbox` — open inbox control panel
- `academic-coach status` — full status report
"""
    dash.write_text(content, encoding="utf-8")


# ── State changes ────────────────────────────────────────────────────────


def apply_mastery_changes(
    ctx: CourseContext, changes: list[dict]
) -> None:
    """Apply mastery/score changes to KNOWLEDGE_REGISTRY.json.

    Each change dict should have:
    - kp_id: str
    - status: KPStatus (or str value)
    - score: float | None
    - last_session: str | None (optional)
    """
    kr_path = ctx.study_system_root / "KNOWLEDGE_REGISTRY.json"
    kr = json.loads(kr_path.read_text(encoding="utf-8"))

    for ch in changes:
        kp_id = ch["kp_id"]
        for kp in kr.get("knowledge_points", []):
            if kp.get("id") == kp_id:
                new_status = ch["status"]
                kp["status"] = new_status.value if isinstance(new_status, KPStatus) else new_status
                if ch.get("score") is not None:
                    kp["score"] = ch["score"]
                if ch.get("last_session"):
                    kp["last_session"] = ch["last_session"]
                break

    kr["last_updated"] = date.today().isoformat()
    kr_path.write_text(json.dumps(kr, ensure_ascii=False, indent=2), encoding="utf-8")


def schedule_reviews(
    ctx: CourseContext,
    kp_id: str,
    base_date: date | None = None,
    intervals: list[int] | None = None,
) -> None:
    """Schedule spaced-repetition reviews for a knowledge point."""
    if base_date is None:
        base_date = date.today()
    if intervals is None:
        # Check config for intensive mode
        settings = ctx.config.get("settings", {})
        if settings.get("intensive_mode"):
            intervals = settings.get("default_review_intervals_days", [1, 3, 7, 14, 30])
        else:
            intervals = [1, 3, 7, 14, 30]

    kr_path = ctx.study_system_root / "KNOWLEDGE_REGISTRY.json"
    kr = json.loads(kr_path.read_text(encoding="utf-8"))

    next_date = None
    for interval in intervals:
        d = base_date
        # Simple date addition
        import datetime as _dt
        next_date = d + _dt.timedelta(days=interval)
        break  # Only set the first (earliest) review

    for kp in kr.get("knowledge_points", []):
        if kp.get("id") == kp_id:
            if next_date:
                kp["next_review"] = next_date.isoformat()
            kp["review_count"] = kp.get("review_count", 0) + 1
            break

    kr_path.write_text(json.dumps(kr, ensure_ascii=False, indent=2), encoding="utf-8")

    # Also update REVIEW_SCHEDULE.md
    schedule_path = ctx.study_system_root / "REVIEW_SCHEDULE.md"
    if schedule_path.exists():
        content = schedule_path.read_text(encoding="utf-8")
        entry = f"- {kp_id}: next review {next_date.isoformat() if next_date else 'TBD'} (interval: {intervals[0]}d)"
        if "## Due Today" in content:
            content = content.replace("## Due Today", f"## Upcoming\n{entry}\n\n## Due Today")
        schedule_path.write_text(content, encoding="utf-8")


def log_mistakes(
    ctx: CourseContext,
    kp_id: str,
    question: str,
    user_answer: str,
    correct_answer: str,
    error_reason: str,
) -> None:
    """Append a mistake entry to MISTAKES.md."""
    mistakes_path = ctx.study_system_root / "MISTAKES.md"
    if not mistakes_path.exists():
        mistakes_path.write_text(
            "# Mistakes Log\n\n| Date | KP | Question | Your Answer | Correct | Reason | Count |\n|---|---|---|---|---|---|---|\n",
            encoding="utf-8",
        )

    today = date.today().isoformat()
    # Escape pipes in cell content
    q = question.replace("|", "\\|").replace("\n", " ")
    ua = user_answer.replace("|", "\\|").replace("\n", " ")
    ca = correct_answer.replace("|", "\\|").replace("\n", " ")
    er = error_reason.replace("|", "\\|").replace("\n", " ")

    row = f"| {today} | {kp_id} | {q[:80]} | {ua[:80]} | {ca[:80]} | {er} | 1 |\n"
    content = mistakes_path.read_text(encoding="utf-8")
    content += row
    mistakes_path.write_text(content, encoding="utf-8")


def update_progress(ctx: CourseContext) -> None:
    """Rewrite PROGRESS.md with current progress snapshot."""
    progress = get_progress(ctx)
    progress_path = ctx.study_system_root / "PROGRESS.md"
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")

    content = f"""# Progress — {ctx.course_name}

> Updated: {now}

## Overall

- **Total knowledge points:** {progress.total}
- **Mastered:** {progress.mastered} ({progress.percent}%)
- **Learning:** {progress.learning}
- **Weak:** {progress.weak}
- **Unseen:** {progress.unseen}
- **Forgotten:** {progress.forgotten}

## Status Distribution

| Status | Count | Percentage |
|---|---|---|
| ✓ mastered | {progress.mastered} | {round(progress.mastered/progress.total*100, 1) if progress.total else 0}% |
| ◐ learning | {progress.learning} | {round(progress.learning/progress.total*100, 1) if progress.total else 0}% |
| ⚠ weak | {progress.weak} | {round(progress.weak/progress.total*100, 1) if progress.total else 0}% |
| □ unseen | {progress.unseen} | {round(progress.unseen/progress.total*100, 1) if progress.total else 0}% |
| ✗ forgotten | {progress.forgotten} | {round(progress.forgotten/progress.total*100, 1) if progress.total else 0}% |
"""
    progress_path.write_text(content, encoding="utf-8")


def append_teaching_log(ctx: CourseContext, kp_id: str, score: float, new_status: str) -> None:
    """Append a one-line entry to TEACHING_LOG.md."""
    log_path = ctx.study_system_root / "TEACHING_LOG.md"
    if not log_path.exists():
        log_path.write_text(
            "# Teaching Log\n\n| Date | KP | Score | New Status |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    row = f"| {now} | {kp_id} | {score} | {new_status} |\n"
    content = log_path.read_text(encoding="utf-8")
    content += row
    log_path.write_text(content, encoding="utf-8")


# ── Helpers ──────────────────────────────────────────────────────────────


def _slug_for_session(session_type: SessionType, kp_list: list[KPInfo]) -> str:
    """Generate a short slug for a session filename."""
    if not kp_list:
        return session_type.value
    if len(kp_list) == 1:
        kp_id = kp_list[0].kp_id.replace(" ", "-").lower()
        return kp_id[:40]
    return f"{len(kp_list)}kps"[:40]


def _dump_yaml_frontmatter(d: dict, indent: int = 0) -> str:
    """Simple YAML frontmatter dumper for dicts. Not a full YAML serializer."""
    lines = []
    for key, value in d.items():
        prefix = "  " * indent
        if isinstance(value, dict):
            lines.append(f"{prefix}{key}:")
            lines.append(_dump_yaml_frontmatter(value, indent + 1))
        elif isinstance(value, list):
            lines.append(f"{prefix}{key}:")
            for item in value:
                if isinstance(item, dict):
                    lines.append(f"{prefix}  - {_dump_yaml_frontmatter(item, indent + 2).strip()}")
                else:
                    lines.append(f"{prefix}  - {item}")
        elif isinstance(value, str):
            if ":" in value or "#" in value:
                lines.append(f'{prefix}{key}: "{value}"')
            else:
                lines.append(f"{prefix}{key}: {value}")
        elif isinstance(value, bool):
            lines.append(f"{prefix}{key}: {'true' if value else 'false'}")
        else:
            lines.append(f"{prefix}{key}: {value}")
    return "\n".join(lines)


def _status_banner(mode: InboxUIMode) -> str:
    """Human-readable status banner for each UI mode."""
    banners = {
        InboxUIMode.COMMAND_ENTRY: "Ready for next action",
        InboxUIMode.CLARIFICATION: "⚠ Needs clarification before proceeding",
        InboxUIMode.ANSWER_ENTRY: "⏳ Awaiting your answer",
        InboxUIMode.POST_COMPLETION: "✓ Session complete",
    }
    return banners.get(mode, "Unknown")


def _get_due_ids(ctx: CourseContext) -> list[str]:
    """Get list of due review KP IDs."""
    from .knowledge import find_due_reviews
    due = find_due_reviews(ctx)
    return [f"{d.kp_id} ({d.name})" if d.name else d.kp_id for d in due]
