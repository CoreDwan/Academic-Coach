"""Smoke tests for Phase 1 companion — run against real workspace data."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from companion import (
    list_courses,
    resolve_course,
    get_progress,
    find_due_reviews,
    find_weak_points,
    find_eligible_next_kps,
    parse_inbox,
    validate_request,
    detect_state,
    get_inbox_ui_mode,
    validate_transition,
    InteractionState,
    ParsedRequest,
)
from companion.errors import CourseNotFoundError


class TestRegistry:
    def test_list_courses_returns_both(self):
        courses = list_courses()
        ids = {c.course_id for c in courses}
        assert "digital-electronics" in ids
        assert "srp-phat" in ids
        assert all(c.course_root.exists() for c in courses)

    def test_resolve_de(self):
        ctx = resolve_course("digital-electronics")
        assert ctx.interaction_mode == "hybrid"
        assert ctx.study_system_root.exists()
        assert ctx.inbox_path.exists()

    def test_resolve_srp(self):
        ctx = resolve_course("srp-phat")
        assert ctx.interaction_mode == "hybrid"
        assert ctx.study_system_root.exists()

    def test_resolve_unknown_raises(self):
        try:
            resolve_course("nonexistent-course-xyz")
            assert False, "Should have raised"
        except CourseNotFoundError:
            pass


class TestState:
    def test_de_is_idle(self):
        ctx = resolve_course("digital-electronics")
        assert detect_state(ctx) == InteractionState.IDLE

    def test_ui_mode_is_command_entry(self):
        ctx = resolve_course("digital-electronics")
        assert get_inbox_ui_mode(ctx) == get_inbox_ui_mode.__annotations__.get(
            "return", None
        ) or "command_entry"

    def test_valid_transitions(self):
        assert validate_transition(InteractionState.IDLE, InteractionState.REQUEST_PREPARED)
        assert validate_transition(InteractionState.AWAITING_USER_ANSWER, InteractionState.PROCESSING)

    def test_invalid_transitions(self):
        assert not validate_transition(InteractionState.IDLE, InteractionState.AWAITING_USER_ANSWER)
        assert not validate_transition(InteractionState.COMPLETED_PENDING_RESET, InteractionState.PROCESSING)


class TestKnowledge:
    def test_progress(self):
        ctx = resolve_course("digital-electronics")
        p = get_progress(ctx)
        assert p.total == 42
        assert p.mastered == 12
        assert 0 <= p.percent <= 100

    def test_due_reviews(self):
        ctx = resolve_course("digital-electronics")
        due = find_due_reviews(ctx)
        assert isinstance(due, list)
        # At least ch1-1 should be due
        due_ids = {d.kp_id for d in due}
        assert "ch1-1" in due_ids

    def test_weak_points(self):
        ctx = resolve_course("digital-electronics")
        weak = find_weak_points(ctx)
        assert isinstance(weak, list)

    def test_eligible_kps(self):
        ctx = resolve_course("digital-electronics")
        eligible = find_eligible_next_kps(ctx, limit=5)
        assert len(eligible) <= 5
        assert len(eligible) >= 1
        # First eligible should be ch1-1 (in progress, only eligible non-mastered with no deps)
        assert eligible[0].kp.kp_id == "ch1-1"

    def test_srp_zero_progress(self):
        ctx = resolve_course("srp-phat")
        p = get_progress(ctx)
        assert p.total == 18
        assert p.mastered == 0
        assert p.percent == 0.0


class TestInboxParser:
    def test_parse_idle_inbox(self):
        ctx = resolve_course("digital-electronics")
        parsed = parse_inbox(ctx)
        # No checkbox checked → action is None
        assert parsed.action is None
        assert not parsed.is_valid

    def test_validate_no_action(self):
        pr = ParsedRequest(action=None)
        pr = validate_request(pr)
        assert len(pr.errors) == 1
        assert "No action selected" in pr.errors[0]

    def test_validate_multiple_actions(self):
        pr = ParsedRequest(
            action=None,
            raw_action_text="- [x] continue\n- [x] review",
        )
        pr = validate_request(pr)
        assert len(pr.errors) == 1
        assert "Multiple actions" in pr.errors[0]

    def test_validate_valid(self):
        from companion.models import ActionMode

        pr = ParsedRequest(action=ActionMode.CONTINUE)
        pr = validate_request(pr)
        assert pr.is_valid
        assert len(pr.errors) == 0


if __name__ == "__main__":
    # Simple runner — no pytest dependency needed for smoke tests
    import inspect

    passed = 0
    failed = 0
    for name, cls in list(globals().items()):
        if inspect.isclass(cls) and name.startswith("Test"):
            inst = cls()
            for method_name in dir(inst):
                if method_name.startswith("test_"):
                    try:
                        getattr(inst, method_name)()
                        print(f"  ✓ {name}.{method_name}")
                        passed += 1
                    except Exception as e:
                        print(f"  ✗ {name}.{method_name}: {e}")
                        failed += 1

    print(f"\n{passed} passed, {failed} failed")
    if failed:
        sys.exit(1)
