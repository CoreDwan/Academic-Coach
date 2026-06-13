"""Knowledge point operations — queries on KNOWLEDGE_REGISTRY.json."""

from __future__ import annotations

import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from .models import (
    CourseContext,
    EligibleKP,
    KPInfo,
    KPStatus,
    ProgressSnapshot,
    _read_json,
)
from .errors import KnowledgeRegistryNotFoundError


# ── Public API ────────────────────────────────────────────────────────────


def load_knowledge_registry(ctx: CourseContext) -> dict:
    """Read the KNOWLEDGE_REGISTRY.json for a course."""
    kr_path = ctx.study_system_root / "KNOWLEDGE_REGISTRY.json"
    if not kr_path.exists():
        raise KnowledgeRegistryNotFoundError(
            f"KNOWLEDGE_REGISTRY.json not found at {kr_path}"
        )
    return _read_json(kr_path)


def get_all_kps(ctx: CourseContext) -> list[KPInfo]:
    """Return all knowledge points for the course."""
    kr = load_knowledge_registry(ctx)
    kps: list[KPInfo] = []
    for raw in kr.get("knowledge_points", []):
        kps.append(_kp_from_dict(raw))
    return kps


def get_progress(ctx: CourseContext) -> ProgressSnapshot:
    """Compute progress snapshot from the knowledge registry."""
    kps = get_all_kps(ctx)
    counts: dict[str, int] = {}
    for kp in kps:
        s = kp.status.value
        counts[s] = counts.get(s, 0) + 1

    return ProgressSnapshot(
        total=len(kps),
        mastered=counts.get("mastered", 0),
        learning=counts.get("learning", 0),
        weak=counts.get("weak", 0),
        unseen=counts.get("unseen", 0),
        forgotten=counts.get("forgotten", 0),
    )


def find_due_reviews(
    ctx: CourseContext, days: int = 0
) -> list[KPInfo]:
    """Return KPs whose next_review date is on or before (today + days)."""
    kps = get_all_kps(ctx)
    today = date.today()
    due: list[KPInfo] = []

    for kp in kps:
        if not kp.next_review:
            continue
        try:
            # Handle both "2026-06-13" and "2026-06-13T17:00:00"
            nr_str = kp.next_review[:10]  # take date part only
            nr_date = date.fromisoformat(nr_str)
            if nr_date <= today:
                due.append(kp)
        except (ValueError, IndexError):
            continue

    return due


def find_weak_points(ctx: CourseContext) -> list[KPInfo]:
    """Return all KPs with status == weak."""
    return [kp for kp in get_all_kps(ctx) if kp.status == KPStatus.WEAK]


def find_eligible_next_kps(
    ctx: CourseContext, limit: int = 5
) -> list[EligibleKP]:
    """Return a ranked shortlist of KPs that are safe to learn next.

    Ranking factors (in order):
    1. Dependencies satisfied (hard gate — unsatisfied = excluded)
    2. Exam weight (higher = higher priority)
    3. Not already mastered
    4. Prefer learning over unseen (continuity)

    Returns up to `limit` eligible KPs, sorted by priority descending.
    """
    all_kps = get_all_kps(ctx)
    kp_map: dict[str, KPInfo] = {kp.kp_id: kp for kp in all_kps}

    def _deps_satisfied(kp: KPInfo) -> bool:
        for dep_id in kp.dependencies:
            dep = kp_map.get(dep_id)
            if dep is None:
                continue  # unknown dependency — assume satisfied
            if dep.status != KPStatus.MASTERED:
                return False
        return True

    eligible: list[EligibleKP] = []
    for kp in all_kps:
        if kp.status == KPStatus.MASTERED:
            continue
        if not _deps_satisfied(kp):
            continue

        # Compute priority score
        score = kp.exam_weight * 10.0
        if kp.status == KPStatus.LEARNING:
            score += 5.0  # continuity bonus
        if kp.status == KPStatus.WEAK:
            score += 7.0  # remediation bonus
        if kp.status == KPStatus.FORGOTTEN:
            score += 3.0

        reason_parts = []
        if kp.exam_weight > 0:
            reason_parts.append(f"exam weight {kp.exam_weight}%")
        if kp.status == KPStatus.LEARNING:
            reason_parts.append("in progress")
        if kp.status == KPStatus.WEAK:
            reason_parts.append("needs remediation")

        eligible.append(
            EligibleKP(
                kp=kp,
                priority_score=score,
                reason=", ".join(reason_parts) if reason_parts else "eligible",
            )
        )

    eligible.sort(key=lambda e: e.priority_score, reverse=True)
    return eligible[:limit]


def get_kp_by_id(ctx: CourseContext, kp_id: str) -> Optional[KPInfo]:
    """Look up a single knowledge point by its ID."""
    for kp in get_all_kps(ctx):
        if kp.kp_id == kp_id:
            return kp
    return None


# ── Internal helpers ─────────────────────────────────────────────────────


def _kp_from_dict(raw: dict) -> KPInfo:
    """Parse a raw KP dict from KNOWLEDGE_REGISTRY.json into a KPInfo."""
    status_str = raw.get("status", "unseen")
    try:
        status = KPStatus(status_str)
    except ValueError:
        status = KPStatus.UNSEEN

    return KPInfo(
        kp_id=raw.get("id", raw.get("kp_id", "")),
        name=raw.get("name", raw.get("topic", "")),
        chapter=raw.get("chapter", ""),
        status=status,
        score=raw.get("score"),
        last_session=raw.get("last_session"),
        next_review=raw.get("next_review"),
        review_count=raw.get("review_count", 0),
        exam_weight=raw.get("exam_weight", raw.get("weight", 0.0)),
        dependencies=raw.get("dependencies", raw.get("prerequisites", [])),
    )
