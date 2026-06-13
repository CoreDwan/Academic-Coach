# Command and Target Model

## Purpose

This is the control-plane document for Academic Coach.
Use it to answer four questions before any teaching logic runs:

1. what kind of action is being requested
2. which course the request targets
3. which interaction surface the request came from
4. whether the request should run in chat, doc, or hybrid persistence mode

This document exists to reduce duplication across routing, doc-first, and init documents.
If another document needs command taxonomy or course-targeting rules, it should point here rather than restating them.

## Design Principle

Do not split Academic Coach into separate chat and doc products.
Keep one protocol core and let multiple interaction surfaces feed into it.

That means:
- command semantics stay stable
- course state stays stable
- only request entry and persistence behavior vary by interaction mode

## Three Layers

### 1. Core study modes
These answer: what does the user want to do to the course?

- `help`
- `init`
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

These are the real protocol modes.
They should work the same whether the request came from chat, notes, or cron.

### 2. Surface helpers
These answer: how does the operator enter, inspect, or steer the workspace?

Recommended helper intents:
- `courses` — list known courses / study-systems
- `use` — set or confirm the active course for the current session
- `dashboard` — open or summarize the current course dashboard surface
- `inbox` — inspect or process queued course requests

These are navigation / control helpers, not teaching modes.
They may be expressed as pseudo-commands, natural language, or note actions, but they should not be confused with `continue` / `review` / `exam`.

### 3. Target resolution
These answer: which course should receive the request?

This layer must run before any course action is executed.
Without it, multi-course workflows and fresh-agent sessions become unreliable.

## Workspace Mode vs Interaction Mode

Do not mix these concepts.

### `workspace_mode`
Where files live:
- `obsidian`
- `external-markdown`

### `interaction_mode`
How the course is operated:
- `chat`
- `doc`
- `hybrid`

Examples:
- `obsidian + chat` = files live in Obsidian, but terminal/chat is the primary surface
- `obsidian + doc` = files live in Obsidian and doc artifacts are the primary surface
- `obsidian + hybrid` = both chat and docs are first-class, with mandatory persistence across both
- `external-markdown + hybrid` = non-Obsidian markdown workspace, but still with doc artifacts and chat writeback

## Required Course Identity Fields

Every initialized or partially initialized course should carry these fields in `COURSE_CONFIG.json` or equivalent metadata:

- `course_id`
- `course_name`
- `aliases`
- `workspace_mode`
- `interaction_mode`
- `course_root`
- `study_system_root`
- `doc_surface_enabled`
- `initialization_level`
- `status`

Recommended semantics:
- `course_id` should be stable and unique
- `aliases` should include Chinese/English short names users are likely to type
- `status` may distinguish `partial` vs `full`

## Global Course Registry

When multiple courses may exist, keep a lightweight registry outside any single course.
Default Hermes location: `~/.hermes/academic-coach/COURSE_REGISTRY.json`.
If a deployment needs something else, override it explicitly rather than leaving the path implicit.

Suggested fields:

```json
{
  "courses": [
    {
      "course_id": "digital-electronics-2025s2",
      "course_name": "Digital Electronics",
      "aliases": ["数电", "数字电子技术基础"],
      "workspace_mode": "obsidian",
      "interaction_mode": "hybrid",
      "course_root": "/path/to/course",
      "study_system_root": "/path/to/course/study-system",
      "dashboard_path": "/path/to/course/DASHBOARD.md",
      "status": "full",
      "last_active": "2026-06-13T20:00:00"
    }
  ]
}
```

Purpose of the registry:
- help fresh agents find known courses
- support multi-course selection
- preserve `course_id` to path mapping
- avoid guessing from vague requests like “继续学习”

## Active Course Rules

A session may have one active course context.
That context should be used only when course resolution is already unambiguous.

Recommended behavior:
1. `use <course_id>` sets the active course for the current session
2. subsequent core study modes may omit the course selector while that session remains valid
3. fresh sessions should not assume the same active course unless the system explicitly reloads it from state
4. if the request conflicts with the active course, explicit request data wins

## Course Target Resolution Priority

Before executing any non-`help` request, resolve the target course in this order:

1. explicit `course_id`
2. current-session active course
3. request payload `course` field
4. request text matching `course_name` or `aliases`
5. only one candidate in the global course registry
6. otherwise ask for clarification

Never guess when multiple real candidates remain.

Special rule for `init` and smoke tests:
- explicit new-course setup data beats ambient history
- if the user supplies a new course name, new folder, new workspace mode, or says this is a smoke test / temporary test, treat that as a new target unless they explicitly say to reuse an existing course
- existing study-systems may be mentioned as optional context, but they must not hijack an explicit new initialization flow

## Surface Routing Rules

### Chat / pseudo-command
Examples:
- `academic-coach continue`
- `/academic-coach review`
- `继续学习数电`

Behavior:
- normalize to core mode
- resolve course target
- execute using the current course's `interaction_mode`

### Doc-first request
Examples:
- `INBOX.md` entries
- note frontmatter
- dashboard action blocks

Behavior:
- normalize to the same core mode
- resolve course from metadata first
- if the course is doc or hybrid, keep the paper trail inside workspace artifacts

### Cron request
Examples:
- reminder prompts
- scheduled review nudges
- cron-created inbox requests

Behavior:
- cron is a trigger source, not a separate tutoring mode
- it must still resolve a specific course
- state changes happen only when a real transaction executes

## Interaction Mode Execution Rules

### `chat`
- terminal/chat is the primary interaction surface
- doc artifacts are optional
- if doc artifacts do not exist, no doc writeback is required

### `doc`
- document artifacts are the primary interaction surface
- terminal may still be used operationally, but execution should read/write through doc artifacts
- the course should remain understandable to a fresh agent from files alone

### `hybrid`
- chat and docs are both first-class entry points
- chat-originated runs are not a bypass
- executed `continue` / `review` / `exam` / `audit` transactions must also update the doc trail when doc artifacts exist

## Helper Intent Semantics

### `courses`
Use to list known courses, their IDs, modes, and status.
Recommended output fields:
- `course_id`
- `course_name`
- `interaction_mode`
- `workspace_mode`
- `status`
- `last_active`

Default data source:
- `~/.hermes/academic-coach/COURSE_REGISTRY.json`

### `use`
Use to bind the current session to a chosen course.
It should never silently switch if multiple plausible candidates exist.

### `dashboard`
Use to read the course's summary/control surface.
In `chat` mode it may summarize `STATUS.md` or `PROGRESS.md` instead.
In `doc` or `hybrid` mode it should prefer the course-root `DASHBOARD.md` when present.

### `inbox`
Use to inspect or process queued requests.
Mostly meaningful in `doc` or `hybrid` mode.
Default target file is the course-root `INBOX.md`.

## Fresh-Agent Start Sequence

When a new agent/session receives an Academic Coach request:

1. load the command/target model
2. inspect the global course registry if available
3. resolve whether the request refers to an existing course or a new one
4. if existing, load that course's `COURSE_CONFIG.json`
5. determine `workspace_mode` and `interaction_mode`
6. only then route into `init`, `continue`, `review`, etc.

## Relationship to Other Docs

- `COMMAND_ROUTING_MATRIX.md` explains no-state vs initialized vs lightweight routing
- `REQUEST_ROUTING_EXAMPLES.md` shows normalized request examples across chat/doc/cron
- `DOC_INTERACTION_PROTOCOL.md` defines the doc-surface artifacts and persistence behavior
- `INIT_SCAFFOLDING_SPEC.md` defines which files get created and how templates are filled
- `OPERATOR_GUIDE.md` explains how an operator should use the protocol in practice

This document should remain the single source of truth for:
- command taxonomy
- helper taxonomy
- course identity model
- target resolution priority
- `workspace_mode` vs `interaction_mode`
