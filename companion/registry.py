"""Registry operations — read and resolve the global COURSE_REGISTRY.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .models import (
    CourseContext,
    CourseInfo,
    _read_json,
    _resolve_registry_path,
)
from .errors import (
    CourseNotFoundError,
    ConfigNotFoundError,
    RegistryNotFoundError,
)


# ── Public API ────────────────────────────────────────────────────────────


def load_registry(path: str | Path | None = None) -> dict:
    """Read and return the raw COURSE_REGISTRY.json dict.

    Raises RegistryNotFoundError if the file is missing.
    """
    p = _resolve_registry_path(str(path) if path else None)
    if not p.exists():
        raise RegistryNotFoundError(f"Registry not found at {p}")
    return _read_json(p)


def list_courses(path: str | Path | None = None) -> list[CourseInfo]:
    """Return all registered courses as CourseInfo objects."""
    registry = load_registry(path)
    courses: list[CourseInfo] = []
    for entry in registry.get("courses", []):
        sr_root = Path(entry["study_system_root"])
        cr_root = Path(entry["course_root"])

        courses.append(
            CourseInfo(
                course_id=entry["course_id"],
                course_name=entry.get("course_name", entry["course_id"]),
                course_root=cr_root,
                study_system_root=sr_root,
                interaction_mode=entry.get("interaction_mode", "chat"),
                workspace_mode=entry.get("workspace_mode", "obsidian"),
                status=entry.get("status", "active"),
                last_active=entry.get("last_active"),
                exam_date=entry.get("exam_date"),
                dashboard_path=entry.get("dashboard_path"),
                inbox_path=entry.get("inbox_path"),
            )
        )
    return courses


def resolve_course(
    course_id: str, registry_path: str | Path | None = None
) -> CourseContext:
    """Resolve a course_id into a fully-populated CourseContext.

    Reads the global registry and the per-course COURSE_CONFIG.json.
    Raises CourseNotFoundError or ConfigNotFoundError on failure.
    """
    registry = load_registry(registry_path)
    entry: dict | None = None
    for c in registry.get("courses", []):
        if c["course_id"] == course_id:
            entry = c
            break

    if entry is None:
        raise CourseNotFoundError(
            f"Course '{course_id}' not found in registry. "
            f"Available: {[c['course_id'] for c in registry.get('courses', [])]}"
        )

    sr_root = Path(entry["study_system_root"])
    cr_root = Path(entry["course_root"])
    config_path = sr_root / "COURSE_CONFIG.json"

    if not config_path.exists():
        # Not fatal — some courses may not have config yet.
        config: dict = {}
    else:
        config = _read_json(config_path)

    ctx = CourseContext(
        course_id=course_id,
        course_name=entry.get("course_name", course_id),
        course_root=cr_root,
        study_system_root=sr_root,
        interaction_mode=entry.get("interaction_mode", config.get("interaction_mode", "chat")),
        workspace_mode=entry.get("workspace_mode", config.get("workspace_mode", "obsidian")),
        config=config,
        registry_entry=entry,
    )

    # Derive doc-surface paths
    dp = entry.get("dashboard_path")
    ctx.dashboard_path = Path(dp) if dp else (cr_root / "DASHBOARD.md")

    ip = entry.get("inbox_path")
    ctx.inbox_path = Path(ip) if ip else (cr_root / "INBOX.md")

    ctx.outbox_path = cr_root / "OUTBOX.md"
    ctx.sessions_dir = cr_root / "SESSIONS"
    ctx.topics_dir = cr_root / "TOPICS"

    return ctx


def find_registry_path() -> Path:
    """Return the default registry path without reading it."""
    return _resolve_registry_path()
