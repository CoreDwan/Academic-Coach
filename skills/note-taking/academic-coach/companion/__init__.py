"""Academic Coach Companion — deterministic orchestration layer.

This package provides read, write, and safety operations that handle
file I/O, state management, and input normalization so the LLM only
needs to do creative work: teaching, assessment, and planning.

Phases:
  1 — read-only (safe, no state mutation)
  2 — write operations (file creation/mutation)
  3 — safety and validation (guardrails)
"""

from .models import (
    ActionMode,
    CourseContext,
    CourseInfo,
    EligibleKP,
    InboxUIMode,
    InteractionState,
    KPInfo,
    KPStatus,
    ParsedRequest,
    ProgressSnapshot,
    SessionStatus,
    SessionType,
)
from .errors import (
    CompanionError,
    ConfigNotFoundError,
    CourseNotFoundError,
    InboxNotFoundError,
    InvalidStateTransitionError,
    KnowledgeRegistryNotFoundError,
    ParseError,
    RegistryNotFoundError,
    ValidationError,
)
from .registry import (
    find_registry_path,
    list_courses,
    load_registry,
    resolve_course,
)
from .state import (
    detect_state,
    find_active_session,
    get_inbox_ui_mode,
    transition_state,
    validate_transition,
)
from .knowledge import (
    find_due_reviews,
    find_eligible_next_kps,
    find_weak_points,
    get_all_kps,
    get_kp_by_id,
    get_progress,
    load_knowledge_registry,
)
from .inbox_parser import (
    parse_inbox,
    validate_request,
)
from .write_ops import (
    append_answer,
    append_teaching_log,
    apply_mastery_changes,
    cancel_session,
    create_session_note,
    finalize_session,
    log_mistakes,
    refresh_dashboard,
    render_inbox,
    render_outbox,
    schedule_reviews,
    update_progress,
)
from .safety import (
    audit,
    check_single_thread,
    validate_registry,
    validate_session_schema,
)

__all__ = [
    # Models
    "ActionMode",
    "CourseContext",
    "CourseInfo",
    "EligibleKP",
    "InboxUIMode",
    "InteractionState",
    "KPInfo",
    "KPStatus",
    "ParsedRequest",
    "ProgressSnapshot",
    "SessionStatus",
    "SessionType",
    # Errors
    "CompanionError",
    "ConfigNotFoundError",
    "CourseNotFoundError",
    "InboxNotFoundError",
    "InvalidStateTransitionError",
    "KnowledgeRegistryNotFoundError",
    "ParseError",
    "RegistryNotFoundError",
    "ValidationError",
    # Registry
    "find_registry_path",
    "list_courses",
    "load_registry",
    "resolve_course",
    # State
    "detect_state",
    "find_active_session",
    "get_inbox_ui_mode",
    "validate_transition",
    "transition_state",
    # Knowledge
    "find_due_reviews",
    "find_eligible_next_kps",
    "find_weak_points",
    "get_all_kps",
    "get_kp_by_id",
    "get_progress",
    "load_knowledge_registry",
    # Inbox
    "parse_inbox",
    "validate_request",
    # Write ops
    "append_answer",
    "append_teaching_log",
    "apply_mastery_changes",
    "cancel_session",
    "create_session_note",
    "finalize_session",
    "log_mistakes",
    "refresh_dashboard",
    "render_inbox",
    "render_outbox",
    "schedule_reviews",
    "update_progress",
    # Safety
    "audit",
    "check_single_thread",
    "validate_registry",
    "validate_session_schema",
]
