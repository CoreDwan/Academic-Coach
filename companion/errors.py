"""Custom exceptions for the Academic Coach companion."""


class CompanionError(Exception):
    """Base exception for all companion errors."""


class RegistryNotFoundError(CompanionError):
    """COURSE_REGISTRY.json is missing or unreadable."""


class CourseNotFoundError(CompanionError):
    """The requested course_id is not in the registry."""


class ConfigNotFoundError(CompanionError):
    """COURSE_CONFIG.json is missing for a registered course."""


class KnowledgeRegistryNotFoundError(CompanionError):
    """KNOWLEDGE_REGISTRY.json is missing."""


class InboxNotFoundError(CompanionError):
    """INBOX.md not found at the expected path."""


class InvalidStateTransitionError(CompanionError):
    """Attempted an illegal state machine transition."""


class ParseError(CompanionError):
    """Failed to parse a user-facing file."""


class ValidationError(CompanionError):
    """Request or state validation failed."""
