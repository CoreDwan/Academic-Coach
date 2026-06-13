"""INBOX.md parser — extract action, details, and context from user-facing markdown."""

from __future__ import annotations

import re
from pathlib import Path

from .models import ActionMode, CourseContext, ParsedRequest
from .errors import InboxNotFoundError, ParseError


# ── Public API ────────────────────────────────────────────────────────────


# Map checkbox label text → ActionMode
_ACTION_LABEL_MAP: dict[str, ActionMode] = {
    "continue": ActionMode.CONTINUE,
    "review": ActionMode.REVIEW,
    "weak": ActionMode.WEAK,
    "exam": ActionMode.EXAM,
    "plan": ActionMode.PLAN,
    "sync": ActionMode.SYNC,
    "audit": ActionMode.AUDIT,
    "status": ActionMode.STATUS,
}


def parse_inbox(ctx: CourseContext) -> ParsedRequest:
    """Parse the current INBOX.md and return a normalized ParsedRequest.

    Extracts:
    - action: which checkbox is checked under the ▶ Action section
    - details: freeform text under ✏ Request Details
    - context: optional text under 📎 Optional Context

    Raises InboxNotFoundError if INBOX.md doesn't exist.
    """
    inbox_path = ctx.inbox_path
    if not inbox_path or not inbox_path.exists():
        raise InboxNotFoundError(
            f"INBOX.md not found at {inbox_path}. "
            f"Run 'academic-coach init' with doc mode enabled to create one."
        )

    content = inbox_path.read_text(encoding="utf-8")
    return _parse_inbox_content(content)


def validate_request(parsed: ParsedRequest) -> ParsedRequest:
    """Validate a ParsedRequest and populate its errors list.

    Returns the same object with .errors populated (empty = valid).
    """
    errors: list[str] = []

    if parsed.action is None:
        # Check if there are multiple checked boxes
        checked = _find_checked_actions(parsed.raw_action_text or "")
        if len(checked) == 0:
            errors.append(
                "No action selected. Check exactly one box under ▶ Action."
            )
        elif len(checked) > 1:
            names = ", ".join(checked)
            errors.append(
                f"Multiple actions selected: {names}. Please pick exactly one."
            )

    parsed.errors = errors
    return parsed


# ── Internal helpers ─────────────────────────────────────────────────────


def _parse_inbox_content(content: str) -> ParsedRequest:
    """Parse raw INBOX.md content into a ParsedRequest."""
    action_text = _extract_section(content, "▶ Action")
    details = _extract_section(content, "✏ Request Details")
    context = _extract_section(content, "📎 Optional Context")

    # If the old-style header exists, try it too
    if not action_text:
        action_text = _extract_section(content, "Action")
    if not details:
        details = _extract_section(content, "Request Details")
    if not context:
        context = _extract_section(content, "Optional Context")

    action = _resolve_action(action_text)

    return ParsedRequest(
        action=action,
        details=details.strip() if details else "",
        context=context.strip() if context else "",
        raw_action_text=action_text,
    )


def _extract_section(content: str, heading: str) -> str:
    """Extract the content under a markdown heading until the next heading or footer.

    Handles both '## Heading' and '## ▶ Heading' style headers.
    """
    # Build a regex that matches the heading (with optional emoji prefix)
    escaped = re.escape(heading)
    # Allow optional emoji/decoration before the heading text
    pattern = rf"^#{1,3}\s+(?:[▶❓✏📎]\s*)?{escaped}\s*\n(.*?)(?=^#{1,3}\s|\n---\n|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def _find_checked_actions(action_text: str) -> list[str]:
    """Find all checked checkbox labels in the action section."""
    checked: list[str] = []
    for m in re.finditer(r"- \[x\]\s+\*?\*?(\w+)\*?\*?", action_text, re.IGNORECASE):
        label = m.group(1).lower().strip()
        if label in _ACTION_LABEL_MAP:
            checked.append(label)
    return checked


def _resolve_action(action_text: str) -> ActionMode | None:
    """Resolve the first checked checkbox to an ActionMode.

    Returns None if no checkbox is checked or the label is unrecognized.
    """
    checked = _find_checked_actions(action_text)
    if len(checked) == 1:
        return _ACTION_LABEL_MAP.get(checked[0])
    return None
