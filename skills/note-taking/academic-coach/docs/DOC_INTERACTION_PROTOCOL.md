# Academic Coach Document Interaction Protocol

## Purpose

This document defines a doc-first / Obsidian-first interaction surface for Academic Coach.

It does not replace the existing Academic Coach protocol core.
Instead, it adds a new collaboration surface that lets the user and agent work through markdown notes rather than relying only on live terminal chat turns.

The intended model is:

- Academic Coach core = state machine + tutoring rules
- document interaction protocol = request/response workflow inside markdown notes

## Core design principle

Do not build a second tutoring system.

The document workflow must reuse the existing Academic Coach core:
- same mode semantics
- same state model
- same mastery logic
- same bootstrap rules
- same one-knowledge-point teaching rule

Only the interaction surface changes.

### Related design specs (local, not tracked)

The full state machine and inbox UI design are defined in companion specs under `docs/internal/`:
- `2026-06-13-DOC-STATE-MACHINE-SPEC.md` — 7 course interaction states + transition rules
- `2026-06-13-INBOX-UI-SPEC.md` — 4 inbox UI modes with concrete markdown layouts
- `2026-06-13-DOC-SESSION-LIFECYCLE.md` — session note creation, structure, and lifecycle
- `2026-06-13-RUNTIME-COMPANION-BOUNDARY.md` — what's code vs what's LLM

These are implementation-authoritative for inbox behavior and session management.

## Supported surfaces

Academic Coach should now be thought of as supporting at least two surfaces:

1. Chat / pseudo-command surface
   - `academic-coach init`
   - `/academic-coach review`
   - natural-language requests in chat

2. Document-first surface
   - request entries inside `INBOX.md`
   - structured note frontmatter
   - dashboard-driven requests
   - cron-generated requests

All of these must normalize into the same internal routing modes.

Important: adding the document-first surface does not remove the terminal/chat surface.
Chat, pseudo-command, and natural-language terminal interactions remain first-class entry points.
When a course already uses the doc-first workspace, those chat-originated runs must also leave the same persistent paper trail as note-originated runs.

## Recommended workspace structure

Within the chosen course folder, keep the existing state area and add a collaboration area.

```text
<course-folder>/
├── DASHBOARD.md
├── INBOX.md
├── OUTBOX.md
├── SESSIONS/
├── TOPICS/
└── study-system/
    ├── COURSE_OVERVIEW.md
    ├── PROGRESS.md
    ├── KNOWLEDGE_TREE.md
    ├── WEAK_POINTS.md
    ├── MISTAKES.md
    ├── EXAM_FOCUS.md
    ├── REVIEW_SCHEDULE.md
    ├── SYLLABUS_ASSETS.md
    ├── KNOWLEDGE_REGISTRY.json
    ├── STATUS.md
    ├── TEACHING_LOG.md
    ├── EXAM_SIMULATIONS.md
    └── COURSE_CONFIG.json
```

### Folder responsibilities

- `study-system/`
  - authoritative course state and projections
- `DASHBOARD.md`
  - human-facing control panel and summary
- `INBOX.md`
  - pending requests / clarifications / queued tasks
- `OUTBOX.md`
  - latest agent responses / summaries / reminders
- `SESSIONS/`
  - one note per teaching/review/exam/audit transaction
- `TOPICS/`
  - durable concept notes mapped to knowledge points

## Request entry points

A request may originate from any of these places:

### 1. `INBOX.md`

Recommended for most user requests.

Example:

```md
## Request: 2026-06-13-continue-logic-functions
status: open
mode: continue
course: Digital Electronics
topic_hint: Logic function representation
source: user

请继续学习，优先处理今天该复习的内容；如果没有到期复习项，就选下一个前置依赖完整的知识点。
```

### 2. Structured frontmatter inside a note

Useful for topic-specific work.

```yaml
---
type: academic-coach-request
status: open
mode: review
course: Digital Electronics
topic_hint: Gray code
created: 2026-06-13
source_note: TOPICS/Gray-Code.md
---
```

### 3. Pseudo-command text inside a note

Still supported for compatibility.

Examples:
- `/academic-coach continue`
- `/academic-coach review`
- `/academic-coach exam`

These should be normalized to the same request schema, not treated as a separate execution path.

### 4. Cron-generated request

A scheduled job may append a request or write a due summary into `INBOX.md` / `OUTBOX.md`.

## Normalized request schema

Whether the request comes from chat or markdown, normalize it into the same logical fields:

- `request_id`
- `status`
- `mode`
- `course`
- `topic_hint` (optional)
- `goal` (optional)
- `source`
- `source_note` (optional)
- `created_at`
- `updated_at`
- `blocking_questions` (optional)
- `session_note` (optional after creation)

Recommended status values:
- `open`
- `needs_clarification`
- `ready`
- `awaiting_user_answer`
- `completed`
- `cancelled`

## Routing rules

### 1. Normalize first

Every trigger should route into one internal mode:
- `init`
- `help`
- `status`
- `continue`
- `review`
- `weak`
- `plan`
- `exam`
- `sync`
- `mistakes`
- `schedule`
- `audit`

### 2. Preserve no-state bootstrap rules

If there is no initialized course state yet, non-`init` requests must not fabricate progress or due items.
The document workflow must still use:
- implicit bootstrap gate
- lightweight bootstrap when appropriate

### 3. Clarify before acting when required

For document requests, unanswered blocking questions should move the request to `needs_clarification` rather than allowing guesswork.

### 4. Only one active teaching thread per course

If a request is already in `awaiting_user_answer` for a course, new teaching requests should usually queue behind it rather than opening multiple simultaneous knowledge-point sessions.

## Session note contract

Each executed request should create or update one session note.
This applies regardless of surface origin:
- request came from `INBOX.md`
- request came from note frontmatter
- request came from cron
- request came from terminal chat / pseudo-command inside Hermes

Terminal chat is an input surface, not a non-persistent bypass.
If the course workspace has doc-first artifacts enabled, a chat-originated teaching/review/exam/audit run must still create or update the corresponding `SESSIONS/...md` record.

Recommended path pattern:

```text
SESSIONS/YYYY-MM-DD-HHMM-<mode>-<slug>.md
```

Recommended frontmatter:

```yaml
---
type: academic-coach-session
status: awaiting_user_answer
mode: continue
course: Digital Electronics
knowledge_point: Logic function representation
request_id: 2026-06-13-continue-logic-functions
created: 2026-06-13 20:10
updated: 2026-06-13 20:18
linked_topic:
  - TOPICS/Logic-Function-Representation.md
---
```

Recommended body structure:

1. status header
2. request context
3. explanation block
4. prompt for user restatement
5. assessment questions
6. user answer area
7. evaluation block
8. score / mastery decision
9. state updates applied
10. next recommended action

### Status header rule

Keep the same information fields as the chat protocol, but allow them to render as note content:
- 当前课程：
- 当前知识点：
- 总体进度：
- 已掌握：
- 学习中：
- 薄弱项：

The information contract stays the same even if the visual layout changes.

## Topic note contract

Each durable topic note in `TOPICS/` should map to one knowledge point or a tightly bounded cluster of knowledge points.

Recommended contents:
- canonical concept summary
- intuition / mechanism explanation
- prerequisites
- common mistakes
- linked sessions
- source evidence
- current mastery snapshot
- next review date

Recommended frontmatter:

```yaml
---
type: academic-coach-topic
course: Digital Electronics
knowledge_point_id: ch02-module03-kp01
status: learning
importance: 4
exam_frequency: 5
next_review: 2026-06-14
---
```

## Dashboard contract

`DASHBOARD.md` should act as the human control panel.

Recommended sections:
- current course summary
- progress snapshot
- due today
- weak points
- active request
- latest session link
- quick actions

Quick actions may be rendered as plain text conventions such as:
- `/academic-coach continue`
- `/academic-coach review`
- `create request in INBOX`

## Inbox / outbox behavior

### `INBOX.md`

Use for:
- new requests
- clarification questions awaiting user input
- queued review prompts
- cron-created reminders

### `OUTBOX.md`

Use for:
- latest agent summary
- concise review reminder
- session completion summary
- audit result summary
- next recommended action

`OUTBOX.md` should be short and navigational.
The full detail belongs in session notes and study-system files.
For hybrid use, chat-originated completed runs should also append or refresh the relevant `OUTBOX.md` summary so terminal work and note work do not diverge.

## Transaction model

A doc-first Academic Coach run should be treated as a transaction.
The same transaction contract should also be used for terminal/chat-originated runs whenever the course already has a doc-first workspace.
In other words: different intake surface, same persistence contract.

### Phase 1: intake
1. read request
2. normalize mode
3. detect course/workspace context
4. check whether initialized state exists

### Phase 2: gating
5. run bootstrap gate if needed
6. ask clarifying questions if critical information is missing
7. move request to `ready` only when action is grounded

### Phase 3: execution
8. create/update session note
9. teach/review/exam/audit exactly according to mode semantics
10. wait for user answer when the pedagogical step requires it

### Phase 4: commit
11. update `KNOWLEDGE_REGISTRY.json`
12. update projection markdown files
13. update `DASHBOARD.md` / `OUTBOX.md` summary if needed
14. update request status
15. link artifacts together

## One-knowledge-point rule in doc-first mode

The move to markdown must not weaken the teaching discipline.

For `continue`, `review`, and `weak`:
- one active teaching session should focus on one knowledge point
- do not pre-open a second topic in the same teaching transaction
- stop after asking or evaluating, then wait for the user's answer

## Cron integration

Cron should be able to support the doc-first workflow in two main ways.

### 1. Reminder mode

The cron job delivers a reminder message to the user and points them to:
- `DASHBOARD.md`
- `INBOX.md`
- latest due items

### 2. Document-update mode

The cron job writes or triggers:
- a due-review request in `INBOX.md`
- an updated due summary in `OUTBOX.md`
- a weekly mock-exam request

Cron must still require explicit confirmation when being created or changed.

## Conflict-handling rules

When conflicts appear, prefer explicitness over silent merging.

### Multiple open requests
- sort by urgency, explicit user priority, and blocking status
- only one request should normally become `awaiting_user_answer` per course at a time

### Freeform user text without mode
- infer the mode if obvious
- otherwise move to clarification

### Topic note vs inbox disagreement
- request entry should win for immediate execution intent
- topic note remains context, not the execution order source

### User edits an old session after completion
- do not silently rewrite history
- create a follow-up request or follow-up session when the edit changes state-relevant meaning

## Minimal adoption path

A practical first implementation can stay simple:

1. keep current `study-system/` unchanged
2. add `DASHBOARD.md`, `INBOX.md`, `OUTBOX.md`, `SESSIONS/`, `TOPICS/`
3. normalize doc requests into existing mode semantics
4. create one session note per executed request
5. patch state files atomically after evaluation

This gives a real doc-first workflow without rewriting the entire protocol.

## Recommended next implementation steps

1. add these docs to the repo and skill references
2. update `SKILL.md` to recognize multiple interaction surfaces
3. document `DASHBOARD.md` / `INBOX.md` / `OUTBOX.md` as recommended artifacts
4. define a canonical request template
5. later add execution helpers for scanning inbox notes and updating session links

## Bottom line

Academic Coach should evolve from:
- a terminal-first tutoring protocol

to:
- a protocol core with a document-first collaboration surface

The protocol remains the same tutor.
The notebook becomes the room where the tutoring happens.
