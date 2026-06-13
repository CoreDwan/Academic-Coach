"""Safety and validation — guardrails that prevent invalid state.

Phase 3: cross-reference checks, single-thread enforcement, session schema
validation, and full audit capability.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import CourseContext, InteractionState
from .state import detect_state, find_active_session
from .knowledge import get_all_kps, get_progress, load_knowledge_registry


# ── Registry validation ──────────────────────────────────────────────────


def validate_registry(ctx: CourseContext) -> list[str]:
    """Cross-reference the global registry entry with the actual filesystem.

    Returns a list of issue strings (empty = healthy).
    """
    issues: list[str] = []

    # Check study-system root exists
    if not ctx.study_system_root.exists():
        issues.append(f"study-system root missing: {ctx.study_system_root}")
        return issues  # Can't check further

    # Required files
    required = [
        "COURSE_OVERVIEW.md",
        "PROGRESS.md",
        "KNOWLEDGE_TREE.md",
        "WEAK_POINTS.md",
        "MISTAKES.md",
        "EXAM_FOCUS.md",
        "REVIEW_SCHEDULE.md",
        "KNOWLEDGE_REGISTRY.json",
    ]
    for f in required:
        if not (ctx.study_system_root / f).exists():
            issues.append(f"missing required file: study-system/{f}")

    # JSON validity
    kr_path = ctx.study_system_root / "KNOWLEDGE_REGISTRY.json"
    if kr_path.exists():
        try:
            kr = json.loads(kr_path.read_text(encoding="utf-8"))
            if "knowledge_points" not in kr:
                issues.append("KNOWLEDGE_REGISTRY.json missing 'knowledge_points' key")
            else:
                kps = kr["knowledge_points"]
                if not isinstance(kps, list):
                    issues.append("KNOWLEDGE_REGISTRY.json 'knowledge_points' is not a list")
                elif len(kps) == 0:
                    issues.append("KNOWLEDGE_REGISTRY.json has zero knowledge points")
        except json.JSONDecodeError as e:
            issues.append(f"KNOWLEDGE_REGISTRY.json is invalid JSON: {e}")

    # Config
    cfg_path = ctx.study_system_root / "COURSE_CONFIG.json"
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            issues.append(f"COURSE_CONFIG.json is invalid JSON: {e}")

    # Progress consistency
    try:
        progress = get_progress(ctx)
        progress_path = ctx.study_system_root / "PROGRESS.md"
        if progress_path.exists():
            content = progress_path.read_text(encoding="utf-8")
            if str(progress.total) not in content:
                issues.append(f"PROGRESS.md total may be stale (registry says {progress.total})")
    except Exception as e:
        issues.append(f"Could not compute progress: {e}")

    return issues


# ── Single-thread enforcement ───────────────────────────────────────────


def check_single_thread(ctx: CourseContext) -> Optional[Path]:
    """Check for duplicate active sessions.

    Returns the path to a conflicting session if one exists, or None.
    Also returns None if the active session is the expected one (single).
    """
    sessions = ctx.sessions_dir
    if not sessions or not sessions.exists():
        return None

    active_sessions: list[Path] = []
    for sf in sorted(sessions.glob("*.md")):
        # Skip templates
        if sf.name.startswith("_") or sf.name.startswith("TEMPLATE"):
            continue
        content = sf.read_text(encoding="utf-8")
        if "status: awaiting_user_answer" in content:
            active_sessions.append(sf)

    if len(active_sessions) > 1:
        # Return the older one as the "conflict" — the newer one is presumably current
        return active_sessions[0]

    return None


# ── Session schema validation ────────────────────────────────────────────


def validate_session_schema(session_path: Path) -> list[str]:
    """Validate a session note's frontmatter and structure.

    Returns a list of issue strings (empty = valid).
    """
    issues: list[str] = []
    content = session_path.read_text(encoding="utf-8")

    # Check for YAML frontmatter
    if not content.startswith("---"):
        issues.append("Missing YAML frontmatter")
        return issues

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        issues.append("Malformed frontmatter delimiters")
        return issues

    fm_text = parts[1].strip()
    body = parts[2] if len(parts) > 2 else ""

    # Required frontmatter fields
    required_fields = ["type", "session_type", "status", "course", "course_id", "created"]
    for field in required_fields:
        if field not in fm_text:
            issues.append(f"Missing required frontmatter field: {field}")

    # type must be 'academic-coach-session'
    if "type: academic-coach-session" not in fm_text:
        issues.append("Frontmatter 'type' must be 'academic-coach-session'")

    # Required body sections
    required_sections = ["## Status", "## Assessment", "## Evaluation", "## State Changes"]
    for section in required_sections:
        if section not in body:
            issues.append(f"Missing required body section: {section}")

    return issues


# ── Full audit ───────────────────────────────────────────────────────────


def audit(ctx: CourseContext) -> dict:
    """Run a full consistency audit and return a structured report.

    Returns a dict with:
    - status: 'healthy' | 'warnings' | 'broken'
    - issues: list of issue strings
    - recommendations: list of repair suggestions
    - checks: dict of check_name -> passed (bool)
    """
    report: dict = {
        "course": ctx.course_name,
        "course_id": ctx.course_id,
        "status": "healthy",
        "issues": [],
        "recommendations": [],
        "checks": {},
    }

    # 1. Registry validation
    reg_issues = validate_registry(ctx)
    report["checks"]["registry"] = len(reg_issues) == 0
    report["issues"].extend(reg_issues)

    # 2. File existence
    required_files = [
        ctx.study_system_root / "COURSE_OVERVIEW.md",
        ctx.study_system_root / "PROGRESS.md",
        ctx.study_system_root / "KNOWLEDGE_TREE.md",
        ctx.study_system_root / "WEAK_POINTS.md",
        ctx.study_system_root / "MISTAKES.md",
        ctx.study_system_root / "EXAM_FOCUS.md",
        ctx.study_system_root / "REVIEW_SCHEDULE.md",
        ctx.study_system_root / "KNOWLEDGE_REGISTRY.json",
        ctx.study_system_root / "COURSE_CONFIG.json",
    ]
    missing = [str(f) for f in required_files if not f.exists()]
    report["checks"]["required_files"] = len(missing) == 0
    if missing:
        report["issues"].append(f"Missing files: {', '.join(missing)}")
        report["recommendations"].append("Run academic-coach sync to restore missing files")

    # 3. Doc surface files
    doc_files = [
        ctx.inbox_path,
        ctx.outbox_path,
        ctx.dashboard_path,
    ]
    missing_doc = [str(f) for f in doc_files if f and not f.exists()]
    report["checks"]["doc_surface"] = len(missing_doc) == 0
    if missing_doc:
        report["issues"].append(f"Missing doc-surface files: {', '.join(missing_doc)}")
        report["recommendations"].append("Run academic-coach init with doc mode to create doc surface")

    # 4. SESSIONS/ directory
    if ctx.sessions_dir and ctx.sessions_dir.exists():
        sessions = [f for f in ctx.sessions_dir.glob("*.md") if not f.name.startswith("_")]
        report["checks"]["sessions_dir"] = True
        report["checks"]["session_count"] = len(sessions)
    else:
        report["checks"]["sessions_dir"] = False
        report["issues"].append("SESSIONS/ directory missing")

    # 5. Single-thread check
    conflict = check_single_thread(ctx)
    report["checks"]["single_thread"] = conflict is None
    if conflict:
        report["issues"].append(f"Multiple active sessions detected: {conflict.name}")
        report["recommendations"].append("Review and close duplicate active sessions")

    # 6. Progress consistency
    try:
        progress = get_progress(ctx)
        report["checks"]["progress_computed"] = True
        # Check for drift
        kps = get_all_kps(ctx)
        registry_count = len(kps)
        if registry_count != progress.total:
            report["issues"].append(
                f"KP count mismatch: registry has {registry_count}, progress says {progress.total}"
            )
    except Exception as e:
        report["checks"]["progress_computed"] = False
        report["issues"].append(f"Could not compute progress: {e}")

    # 7. Naming convention
    naming_ok = True
    for f in ctx.study_system_root.glob("*.md"):
        if f.name != f.name.upper() and not f.name.startswith("_"):
            naming_ok = False
            report["issues"].append(f"Non-uppercase filename: study-system/{f.name}")
    for f in ctx.study_system_root.glob("*.json"):
        if f.name != f.name.upper() and not f.name.startswith("_"):
            naming_ok = False
            report["issues"].append(f"Non-uppercase filename: study-system/{f.name}")
    report["checks"]["naming"] = naming_ok

    # Determine overall status
    if not report["issues"]:
        report["status"] = "healthy"
    elif any("missing" in i.lower() for i in report["issues"]):
        report["status"] = "broken"
    else:
        report["status"] = "warnings"

    return report
