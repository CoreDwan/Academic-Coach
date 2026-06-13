"""Comprehensive tests for Phase 1 companion — covers all modules, edge cases, and error paths."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from companion import *
from companion.errors import *

passed = 0
failed = 0

def check(name, condition, detail=''):
    global passed, failed
    if condition:
        passed += 1
        print(f'  ✓ {name}')
    else:
        failed += 1
        print(f'  ✗ {name}  {detail}')

def check_raises(name, exc_type, fn, *args):
    global passed, failed
    try:
        fn(*args)
        failed += 1
        print(f'  ✗ {name} — expected {exc_type.__name__}, but no exception')
    except exc_type:
        passed += 1
        print(f'  ✓ {name}')
    except Exception as e:
        failed += 1
        print(f'  ✗ {name} — expected {exc_type.__name__}, got {type(e).__name__}: {e}')

# ── 1. Registry ──

print('=== 1. Registry operations ===')
courses = list_courses()
check('list_courses returns list', isinstance(courses, list))
check('>= 2 courses', len(courses) >= 2)
check('digital-electronics present', any(c.course_id == 'digital-electronics' for c in courses))
check('srp-phat present', any(c.course_id == 'srp-phat' for c in courses))
for c in courses:
    check(f'{c.course_id} course_root exists', c.course_root.exists())
    check(f'{c.course_id} study_system_root exists', c.study_system_root.exists())
    check(f'{c.course_id} has interaction_mode', c.interaction_mode in ('chat', 'doc', 'hybrid'))

ctx_de = resolve_course('digital-electronics')
check('resolve DE returns CourseContext', isinstance(ctx_de, CourseContext))
check('DE interaction_mode', ctx_de.interaction_mode == 'hybrid')
check('DE inbox_path exists', ctx_de.inbox_path and ctx_de.inbox_path.exists())
check('DE outbox_path set', ctx_de.outbox_path is not None)
check('DE sessions_dir set', ctx_de.sessions_dir is not None)
check_raises('resolve unknown raises', CourseNotFoundError, resolve_course, 'nonexistent-xyz')
rp = find_registry_path()
check('registry path ends with COURSE_REGISTRY.json', rp.name == 'COURSE_REGISTRY.json')

# ── 2. State ──

print('\n=== 2. State detection ===')
state = detect_state(ctx_de)
check('DE state is idle', state == InteractionState.IDLE)
check('DE state is enum', isinstance(state, InteractionState))
ui = get_inbox_ui_mode(ctx_de)
check('DE UI mode is command_entry', ui == InboxUIMode.COMMAND_ENTRY)
active = find_active_session(ctx_de)
check('DE no active session', active is None)

ctx_srp = resolve_course('srp-phat')
check('SRP state is idle', detect_state(ctx_srp) == InteractionState.IDLE)

check('idle→request_prepared valid', validate_transition(InteractionState.IDLE, InteractionState.REQUEST_PREPARED))
check('idle→processing INVALID', not validate_transition(InteractionState.IDLE, InteractionState.PROCESSING))
check('idle→awaiting_user_answer INVALID', not validate_transition(InteractionState.IDLE, InteractionState.AWAITING_USER_ANSWER))
check('processing→completed_pending_reset valid', validate_transition(InteractionState.PROCESSING, InteractionState.COMPLETED_PENDING_RESET))
check('processing→awaiting_user_answer valid', validate_transition(InteractionState.PROCESSING, InteractionState.AWAITING_USER_ANSWER))
check('awaiting_user_answer→processing valid', validate_transition(InteractionState.AWAITING_USER_ANSWER, InteractionState.PROCESSING))
check('completed_pending_reset→idle valid', validate_transition(InteractionState.COMPLETED_PENDING_RESET, InteractionState.IDLE))
check('completed_pending_reset→request_prepared valid', validate_transition(InteractionState.COMPLETED_PENDING_RESET, InteractionState.REQUEST_PREPARED))
check('completed_pending_reset→processing INVALID', not validate_transition(InteractionState.COMPLETED_PENDING_RESET, InteractionState.PROCESSING))
check('blocked→idle valid', validate_transition(InteractionState.BLOCKED, InteractionState.IDLE))
check_raises('transition idle→processing raises', InvalidStateTransitionError, transition_state, ctx_de, InteractionState.PROCESSING)
try:
    transition_state(ctx_de, InteractionState.REQUEST_PREPARED)
    check('transition idle→request_prepared succeeds', True)
except Exception as e:
    check('transition idle→request_prepared succeeds', False, str(e))

# ── 3. Knowledge ──

print('\n=== 3. Knowledge operations ===')
prog = get_progress(ctx_de)
check('progress total=42', prog.total == 42)
check('progress mastered=12', prog.mastered == 12)
check('progress learning=1', prog.learning == 1)
check('progress weak=0', prog.weak == 0)
check('progress unseen=29', prog.unseen == 29)
check('progress percent=28.6', prog.percent == 28.6)
check('progress sum matches total', prog.mastered + prog.learning + prog.weak + prog.unseen + prog.forgotten == prog.total)

due = find_due_reviews(ctx_de, days=0)
check('due reviews is list', isinstance(due, list))
check('due reviews has ch1-1', any(d.kp_id == 'ch1-1' for d in due))
check('due reviews KP is KPInfo', all(isinstance(d, KPInfo) for d in due))
check('due 3d includes due 0d', len(find_due_reviews(ctx_de, days=3)) >= len(due))
check('weak points is list', isinstance(find_weak_points(ctx_de), list))

eligible = find_eligible_next_kps(ctx_de, limit=5)
check('eligible <= 5', len(eligible) <= 5)
check('eligible >= 1', len(eligible) >= 1)
check('first eligible is ch1-1', eligible[0].kp.kp_id == 'ch1-1')
check('eligible have priority_score', all(e.priority_score >= 0 for e in eligible))
check('eligible have reason', all(len(e.reason) > 0 for e in eligible))

kp = get_kp_by_id(ctx_de, 'ch1-1')
check('get_kp_by_id ch1-1 found', kp is not None and kp.status == KPStatus.LEARNING)
check('get_kp_by_id nonexistent returns None', get_kp_by_id(ctx_de, 'nonexistent-kp') is None)
check('get_all_kps returns 42', len(get_all_kps(ctx_de)) == 42)

kr = load_knowledge_registry(ctx_de)
check('load_knowledge_registry returns dict', isinstance(kr, dict))
check('registry KP count matches', len(kr.get('knowledge_points', [])) == 42)

prog_srp = get_progress(ctx_srp)
check('SRP total=18', prog_srp.total == 18)
check('SRP mastered=0', prog_srp.mastered == 0)
check('SRP percent=0.0', prog_srp.percent == 0.0)

# ── 4. INBOX parser ──

print('\n=== 4. INBOX parsing ===')
parsed = parse_inbox(ctx_de)
check('parse_inbox returns ParsedRequest', isinstance(parsed, ParsedRequest))
check('DE inbox action=None (idle)', parsed.action is None)
check('DE inbox not valid (no action)', not parsed.is_valid)

pr = ParsedRequest(action=None)
pr = validate_request(pr)
check('validate no-action has error', len(pr.errors) == 1 and 'No action selected' in pr.errors[0])

pr2 = ParsedRequest(action=None, raw_action_text='- [x] continue\n- [x] review')
pr2 = validate_request(pr2)
check('validate multi-action has error', len(pr2.errors) == 1 and 'Multiple actions' in pr2.errors[0])

from companion.models import ActionMode
pr3 = ParsedRequest(action=ActionMode.CONTINUE)
pr3 = validate_request(pr3)
check('validate valid action is valid', pr3.is_valid and len(pr3.errors) == 0)

# ── 5. Error paths ──

print('\n=== 5. Error paths ===')
check_raises('registry not found', (RegistryNotFoundError, FileNotFoundError),
    load_registry, '/nonexistent/path/registry.json')
check_raises('KP registry not found', KnowledgeRegistryNotFoundError,
    load_knowledge_registry, CourseContext(
        course_id='test', course_name='test', course_root=Path('/tmp'),
        study_system_root=Path('/tmp/nonexistent'), interaction_mode='chat', workspace_mode='obsidian'))
check_raises('inbox not found', InboxNotFoundError,
    parse_inbox, CourseContext(
        course_id='test', course_name='test', course_root=Path('/tmp/nonexistent'),
        study_system_root=Path('/tmp/nonexistent'), interaction_mode='chat',
        workspace_mode='obsidian', inbox_path=Path('/tmp/nonexistent/INBOX.md')))

# ── 6. Model integrity ──

print('\n=== 6. Model integrity ===')
check('InteractionState has 7 values', len(InteractionState) == 7)
check('SessionStatus has 7 values', len(SessionStatus) == 7)
check('KPStatus has 5 values', len(KPStatus) == 5)
check('SessionType has 7 values', len(SessionType) == 7)
check('InboxUIMode has 4 values', len(InboxUIMode) == 4)
check('ActionMode has 8 values', len(ActionMode) == 8)

ps = ProgressSnapshot(total=10, mastered=7, learning=1, weak=1, unseen=1, forgotten=0)
check('ProgressSnapshot.percent', ps.percent == 70.0)
check('ProgressSnapshot zero div', ProgressSnapshot(total=0, mastered=0, learning=0, weak=0, unseen=0, forgotten=0).percent == 0.0)

check('ParsedRequest valid when action set', ParsedRequest(action=ActionMode.CONTINUE).is_valid)
check('ParsedRequest invalid when None', not ParsedRequest(action=None).is_valid)
check('ParsedRequest invalid with errors', not ParsedRequest(action=ActionMode.CONTINUE, errors=['err']).is_valid)

print(f'\n{"="*40}')
print(f'{passed} passed, {failed} failed')
if failed:
    print('SOME TESTS FAILED')
    sys.exit(1)
else:
    print('ALL TESTS PASSED')
