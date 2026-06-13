"""Academic Coach Companion — deterministic orchestration layer.

This package provides read-only and (in later phases) write operations
that handle file I/O, state management, and input normalization so the
LLM only needs to do creative work: teaching, assessment, and planning.

Phase 1: read-only operations (safe, no state mutation).
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
    validate_transition,
    transition_state,
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
]
