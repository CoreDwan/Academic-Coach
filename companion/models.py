"""Data models for the Academic Coach deterministic companion layer.

All entities that flow between companion modules are defined here as
dataclasses, enums, and typed dictionaries.  No file I/O or logic lives here.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


# ── Enums ────────────────────────────────────────────────────────────────


class InteractionState(str, Enum):
    """Course-level interaction state — what the user is currently seeing/doing."""

    IDLE = "idle"
    REQUEST_PREPARED = "request_prepared"
    PROCESSING = "processing"
    AWAITING_CLARIFICATION = "awaiting_clarification"
    AWAITING_USER_ANSWER = "awaiting_user_answer"
    COMPLETED_PENDING_RESET = "completed_pending_reset"
    BLOCKED = "blocked"


class SessionStatus(str, Enum):
    """Lifecycle status of a single session note."""

    DRAFT = "draft"
    ACTIVE = "active"
    AWAITING_USER_ANSWER = "awaiting_user_answer"
    EVALUATING = "evaluating"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ABANDONED = "abandoned"


class KPStatus(str, Enum):
    """Knowledge point mastery status."""

    UNSEEN = "unseen"
    LEARNING = "learning"
    MASTERED = "mastered"
    WEAK = "weak"
    FORGOTTEN = "forgotten"


class SessionType(str, Enum):
    """Type of instructional session."""

    CONTINUE = "continue"
    REVIEW = "review"
    WEAK = "weak"
    EXAM = "exam"
    AUDIT = "audit"
    PLAN = "plan"
    SYNC = "sync"


class InboxUIMode(str, Enum):
    """Which UI layout INBOX.md should render."""

    COMMAND_ENTRY = "command_entry"
    CLARIFICATION = "clarification"
    ANSWER_ENTRY = "answer_entry"
    POST_COMPLETION = "post_completion"


class ActionMode(str, Enum):
    """Parsed action from INBOX.md checkbox or chat command."""

    CONTINUE = "continue"
    REVIEW = "review"
    WEAK = "weak"
    EXAM = "exam"
    PLAN = "plan"
    SYNC = "sync"
    AUDIT = "audit"
    STATUS = "status"


# ── Dataclasses ───────────────────────────────────────────────────────────


@dataclass
class CourseInfo:
    """Lightweight course entry from the global registry."""

    course_id: str
    course_name: str
    course_root: Path
    study_system_root: Path
    interaction_mode: str  # "chat", "doc", "hybrid"
    workspace_mode: str   # "obsidian", "external-markdown", etc.
    status: str
    last_active: str | None = None
    exam_date: str | None = None
    dashboard_path: str | None = None
    inbox_path: str | None = None


@dataclass
class CourseContext:
    """Fully resolved course with all relevant paths materialised."""

    course_id: str
    course_name: str
    course_root: Path
    study_system_root: Path
    interaction_mode: str
    workspace_mode: str
    config: dict = field(default_factory=dict)
    registry_entry: dict = field(default_factory=dict)

    # Derived paths (lazily computed by resolve_course)
    dashboard_path: Path | None = None
    inbox_path: Path | None = None
    outbox_path: Path | None = None
    sessions_dir: Path | None = None
    topics_dir: Path | None = None


@dataclass
class KPInfo:
    """One knowledge point from KNOWLEDGE_REGISTRY.json."""

    kp_id: str
    name: str = ""
    chapter: str = ""
    status: KPStatus = KPStatus.UNSEEN
    score: float | None = None
    last_session: str | None = None
    next_review: str | None = None
    review_count: int = 0
    exam_weight: float = 0.0
    dependencies: list[str] = field(default_factory=list)


@dataclass
class ProgressSnapshot:
    """Aggregated progress across all knowledge points."""

    total: int
    mastered: int
    learning: int
    weak: int
    unseen: int
    forgotten: int

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return round(self.mastered / self.total * 100, 1)


@dataclass
class EligibleKP:
    """A knowledge point that is safe to learn next, with a priority score."""

    kp: KPInfo
    priority_score: float = 0.0
    reason: str = ""


@dataclass
class ParsedRequest:
    """Normalized request extracted from INBOX.md or chat."""

    action: ActionMode | None
    details: str = ""
    context: str = ""
    raw_action_text: str = ""
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return self.action is not None and len(self.errors) == 0


# ── JSON helpers ──────────────────────────────────────────────────────────


def _read_json(path: Path) -> dict:
    """Read and parse a JSON file.  Raises FileNotFoundError / JSONDecodeError."""
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _resolve_registry_path(explicit: str | None = None) -> Path:
    """Return the path to COURSE_REGISTRY.json.

    Default: ~/.hermes/academic-coach/COURSE_REGISTRY.json
    Override via explicit path or HERMES_HOME env var.
    """
    if explicit:
        return Path(explicit).expanduser()
    import os

    hermes = os.environ.get("HERMES_HOME", os.path.expanduser("~/.hermes"))
    return Path(hermes) / "academic-coach" / "COURSE_REGISTRY.json"
