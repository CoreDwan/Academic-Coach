"""State detection — derive course interaction state from on-disk artifacts."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .models import (
    CourseContext,
    InteractionState,
    InboxUIMode,
    SessionStatus,
)
from .errors import InvalidStateTransitionError


# ── State detection ──────────────────────────────────────────────────────


def detect_state(ctx: CourseContext) -> InteractionState:
    """Derive the current course interaction state from filesystem artifacts.

    Priority order for detection:
    1. Check for active session notes (awaiting_user_answer → session exists)
    2. Check INBOX.md content for mode markers
    3. Default to idle if nothing is in progress
    """
    active = find_active_session(ctx)
    if active is not None:
        # A session note is waiting for the user → answer-entry mode
        return InteractionState.AWAITING_USER_ANSWER

    inbox = ctx.inbox_path
    if inbox and inbox.exists():
        content = inbox.read_text(encoding="utf-8")

        # Check footer for explicit mode
        if "Mode: clarification" in content:
            return InteractionState.AWAITING_CLARIFICATION
        if "Mode: answer-entry" in content:
            return InteractionState.AWAITING_USER_ANSWER
        if "Mode: post-completion" in content:
            return InteractionState.COMPLETED_PENDING_RESET
        if "Mode: blocked" in content:
            return InteractionState.BLOCKED

        # Check for prepared request (checked checkbox or non-empty details)
        if _has_prepared_request(content):
            return InteractionState.REQUEST_PREPARED

    return InteractionState.IDLE


def get_inbox_ui_mode(ctx: CourseContext) -> InboxUIMode:
    """Map the current interaction state to the INBOX.md UI mode."""
    state = detect_state(ctx)
    mapping = {
        InteractionState.IDLE: InboxUIMode.COMMAND_ENTRY,
        InteractionState.REQUEST_PREPARED: InboxUIMode.COMMAND_ENTRY,
        InteractionState.PROCESSING: InboxUIMode.COMMAND_ENTRY,  # transient, no special UI
        InteractionState.AWAITING_CLARIFICATION: InboxUIMode.CLARIFICATION,
        InteractionState.AWAITING_USER_ANSWER: InboxUIMode.ANSWER_ENTRY,
        InteractionState.COMPLETED_PENDING_RESET: InboxUIMode.POST_COMPLETION,
        InteractionState.BLOCKED: InboxUIMode.CLARIFICATION,  # treat as clarification-like
    }
    return mapping[state]


def find_active_session(ctx: CourseContext) -> Optional[Path]:
    """Find a session note that is currently awaiting_user_answer.

    Returns the path to the session note, or None.
    """
    sessions = ctx.sessions_dir
    if not sessions or not sessions.exists():
        return None

    for sf in sorted(sessions.glob("*.md"), reverse=True):
        content = sf.read_text(encoding="utf-8")
        if "status: awaiting_user_answer" in content:
            return sf

    return None


# ── State machine validation ─────────────────────────────────────────────


# Allowed transitions (current → {valid next states})
_TRANSITIONS: dict[InteractionState, set[InteractionState]] = {
    InteractionState.IDLE: {
        InteractionState.REQUEST_PREPARED,
        InteractionState.BLOCKED,
    },
    InteractionState.REQUEST_PREPARED: {
        InteractionState.PROCESSING,
        InteractionState.AWAITING_CLARIFICATION,
        InteractionState.IDLE,
        InteractionState.BLOCKED,
    },
    InteractionState.PROCESSING: {
        InteractionState.COMPLETED_PENDING_RESET,
        InteractionState.AWAITING_CLARIFICATION,
        InteractionState.AWAITING_USER_ANSWER,
        InteractionState.BLOCKED,
    },
    InteractionState.AWAITING_CLARIFICATION: {
        InteractionState.REQUEST_PREPARED,
        InteractionState.IDLE,
        InteractionState.BLOCKED,
    },
    InteractionState.AWAITING_USER_ANSWER: {
        InteractionState.PROCESSING,
        InteractionState.COMPLETED_PENDING_RESET,
        InteractionState.IDLE,
    },
    InteractionState.COMPLETED_PENDING_RESET: {
        InteractionState.IDLE,
        InteractionState.REQUEST_PREPARED,
    },
    InteractionState.BLOCKED: {
        InteractionState.IDLE,
        InteractionState.REQUEST_PREPARED,
    },
}


def validate_transition(
    current: InteractionState, proposed: InteractionState
) -> bool:
    """Return True if the proposed transition is allowed by the state machine."""
    allowed = _TRANSITIONS.get(current, set())
    return proposed in allowed


def transition_state(ctx: CourseContext, to: InteractionState) -> None:
    """Validate and record a state transition.

    Currently validates only.  In future phases this will also write
    the state to a persistent marker so it survives restarts.

    Raises InvalidStateTransitionError if the transition is illegal.
    """
    current = detect_state(ctx)
    if not validate_transition(current, to):
        raise InvalidStateTransitionError(
            f"Illegal transition: {current.value} → {to.value}"
        )
    # Phase 1: validate-only.  Phase 2+: persist marker.


# ── Internal helpers ─────────────────────────────────────────────────────


def _has_prepared_request(inbox_content: str) -> bool:
    """Heuristic: does the inbox have a user-prepared (but unsubmitted) request?"""
    # A checked checkbox under the Action section suggests a prepared request
    if "- [x]" in inbox_content:
        return True
    # Non-trivial content in the details section also suggests prepared
    # (but we can't reliably parse without the full parser; keep simple for now)
    return False
