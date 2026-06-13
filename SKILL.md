---
name: academic-coach
description: Use when the user wants a persistent course tutoring system that initializes a subject from mixed study materials, maintains a fine-grained knowledge registry in a markdown-first workspace, teaches one knowledge point at a time, tracks mistakes and weak points, schedules spaced review, and supports exam-mode simulation through a pure skill command protocol.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [academic, tutoring, obsidian, spaced-repetition, study-systems]
    related_skills: [obsidian, vero-collaboration, hermes-agent]
---

# Academic Coach

## Overview

Academic Coach is a pure-skill command protocol for running a long-term subject tutoring workflow inside Hermes without adding native slash commands to the CLI.

It is designed for mixed study materials: textbooks, PPT/PPTX, PDFs, markdown notes, images, lab reports, homework, past exams, answer sheets, and reference links. It uses a human-readable workspace plus a JSON registry as the machine-stable state store. Obsidian is the default and recommended workspace, but the user may choose another markdown-first folder if they do not want to store the study-system inside Obsidian.

This skill must act like a persistent academic operating system, not a one-off explainer. It should initialize a course, build a knowledge tree, maintain learning state, teach one knowledge point at a time, record mistakes, schedule spaced review, and run exam simulations.

## Interaction Surfaces

Academic Coach has a stable protocol core and one or more interaction surfaces.

Current supported / intended surfaces:
- chat or pseudo-command interaction inside Hermes
- document-first interaction inside Obsidian or another markdown workspace

These surfaces should reuse the same mode semantics (`init`, `continue`, `review`, `exam`, etc.) and the same state model rather than behaving like separate tutoring systems.

## Deterministic Companion Layer

Academic Coach now includes a Python companion library (`companion/`) that handles deterministic operations so the LLM only needs to do creative work.

### What the companion handles (read-only — Phase 1)
- Registry operations: `list_courses()`, `resolve_course(course_id)`
- State detection: `detect_state()`, `find_active_session()`, `get_inbox_ui_mode()`
- Knowledge queries: `get_progress()`, `find_due_reviews()`, `find_eligible_next_kps()`, `find_weak_points()`
- INBOX parsing: `parse_inbox()`, `validate_request()`
- State machine enforcement: `validate_transition()`, `transition_state()`

### When to use the companion
- `academic-coach courses` → use `list_courses()` first (registry-first, no filesystem scan)
- `academic-coach status` → use `get_progress()` + `detect_state()`
- `academic-coach continue` → use `find_eligible_next_kps()` for the KP shortlist
- `academic-coach review` → use `find_due_reviews()` for the due review queue
- `academic-coach inbox` → use `parse_inbox()` + `validate_request()` before processing

### Companion execution rule
When the companion is available (files exist in `companion/`), prefer it for all read operations. The LLM should receive pre-computed structured context, not raw file contents. Fall back to manual file reading only if the companion module is unavailable or raises an error.

For the full design, see the internal specs in `docs/internal/` (not tracked in git).

The command surface must also be alias-friendly. The stable contract is the mode vocabulary, not the literal skill name. If the user invokes this system as `/academic-coach init`, `/subject-coach review`, `/course-tutor continue`, or another wrapper-specific alias, normalize it to the same underlying study modes as long as the intent is clearly this tutoring system rather than Hermes configuration.

For reuse boundaries and the document-first evolution path, consult:
- `references/reuse-map.md`
- `references/doc-interaction-protocol.md`
- `references/command-and-target-model.md`

## Protocol Documentation Hygiene

When evolving this skill's protocol, keep the documentation stack small and role-separated.

Treat these four as the canonical control-plane docs:
- `references/command-and-target-model.md` — command taxonomy, course identity, target resolution, `workspace_mode` vs `interaction_mode`
- `references/COMMAND_ROUTING_MATRIX.md` — initialized vs no-state vs lightweight-bootstrap routing
- `references/init-scaffolding-spec.md` — full init vs lightweight bootstrap artifact rules and template filling
- `references/doc-interaction-protocol.md` — doc-first artifacts and persistence semantics

Treat these as secondary operator/support docs:
- `references/request-routing-examples.md` — worked normalization examples
- `references/help-and-commands.md` — concise operator command help
- `references/init-response-skeleton.md` — first-turn reply shape for fresh/no-state starts
- `references/reuse-map.md` and `references/user-journey.md` — design anchors, not parallel specs

Documentation maintenance rules:
1. Do not create new top-level protocol docs when an existing canonical doc can absorb the rule.
2. `OPERATOR_GUIDE`-style docs should explain practical usage, not re-specify routing or target resolution already defined elsewhere.
3. `INIT_CHECKLIST`-style docs should stay compact checklists; the full creation logic belongs in the init scaffolding spec.
4. If a workflow doc is fully absorbed by the operator guide, remove the standalone duplicate instead of keeping two drifting versions.
5. When chat/doc/hybrid behavior changes, update the canonical control-plane docs first, then refresh operator/support docs to point back to them.


## Command Protocol

This is a pure skill protocol, not a native Hermes slash command. The user may write commands in natural language or pseudo-command form.

Core study modes:
- `academic-coach help`
- `academic-coach init`
- `academic-coach status`
- `academic-coach continue`
- `academic-coach review`
- `academic-coach weak`
- `academic-coach plan`
- `academic-coach exam`
- `academic-coach sync`
- `academic-coach mistakes`
- `academic-coach schedule`
- `academic-coach audit`

Surface helpers:
- `academic-coach courses`
- `academic-coach use <course_id>`
- `academic-coach dashboard`
- `academic-coach inbox`

If the user writes `/academic-coach init`, interpret it as the same protocol command unless they explicitly say they are modifying Hermes itself.
Likewise, `/academic-coach help` and `/academic-coach audit` should be interpreted as pseudo-command invocations of this skill, not as native Hermes slash commands.

For the command taxonomy, course-targeting rules, and `workspace_mode` versus `interaction_mode`, consult `references/command-and-target-model.md`.

For helper intents like `academic-coach courses`, prefer the explicit registry-first behavior: read `~/.hermes/academic-coach/COURSE_REGISTRY.json` before any filesystem discovery, and only fall back to broad scanning when the registry is missing or broken.

Design the protocol so the surface name can be re-skinned later. The stable part is the mode vocabulary (`init`, `continue`, `review`, `weak`, `exam`, `status`, `audit`, `schedule`, `mistakes`, `sync`), not the literal skill name. This keeps the skill reusable as a generic subject-coach template and compatible with future doc-first or automation surfaces.

## Hard Rules

1. Teach exactly one knowledge point at a time.
2. Never jump to the next knowledge point without waiting for the user's answer.
3. Every teaching round must follow: explain → ask user to restate → ask questions → score → update state.
4. Every reply during active course mode must begin with:
   - 当前课程：
   - 当前知识点：
   - 总体进度：
   - 已掌握：
   - 学习中：
   - 薄弱项：
5. Use the user's preferred teaching/output language. If unknown, confirm it during initialization; preserve technical terms in English when useful.
6. Before creating course notes, first confirm the workspace mode. Default is Obsidian, but a non-Obsidian markdown workspace is allowed if the user explicitly prefers it.
7. If workspace mode is Obsidian, always align with the existing Obsidian vault structure, naming conventions, and course-folder organization before creating or updating files. If the `vero-collaboration` skill is also in play for that workspace, reuse its collaboration rules instead of inventing a parallel study-system layout.
8. File names for academic-coach managed documents must use uppercase English names.
9. By default, use a `study-system/` subdirectory under the chosen course folder.
10. Use markdown for human-facing files and JSON for the authoritative state registry.
11. Do not begin initialization until required information has been clarified.
12. During `init`, use a superpower-style clarification gate: actively gather course name, exam context, workspace target, available materials, desired mode, and missing-but-important constraints before creating files or a study plan.
13. Mixed materials are normal, not an edge case. The initialization workflow must be able to ingest PDFs, PPT/PPTX, markdown/text notes, images/screenshots, homework, lab reports, past exams, answer sheets, and reference links in one course setup.
14. Cron/review scheduling changes require confirmation before creating or changing jobs.
15. When evidence is missing, say so clearly rather than inventing coverage or mastery.
16. Never create synthetic study materials, fake chapter notes, demo textbooks, or placeholder content files to make `init` look complete. Only inventory or transform user-provided materials; if materials are missing, scaffold an honest partial state instead.
17. The terminal/chat surface is preserved as a first-class interaction surface; doc-first mode does not replace it.
18. If the course workspace includes doc-first artifacts (`DASHBOARD.md`, `INBOX.md`, `OUTBOX.md`, `SESSIONS/`, or `TOPICS/`), then chat/pseudo-command interactions are not a bypass: each executed teaching/review/exam/audit transaction must also be persisted into the same documentation layer, especially `SESSIONS/` and `OUTBOX.md`, and into `INBOX.md` when a normalized request record is needed.
19. In a hybrid workflow, terminal chat is just another request-entry surface. Persistence rules must stay identical across chat, note, and cron-originated runs.
20. For `continue`, do not score or update persistent learning state until the user has answered the assessment questions for that round, unless the user explicitly asks for a rough provisional score.
21. Only one active instructional thread per course. If a session note is in `awaiting_user_answer`, new teaching actions must not silently replace it. Surface the conflict and let the user choose: resume or cancel-and-restart.
22. Every interactive teaching/review/exam session must create a session note in `SESSIONS/`. Read-only actions (`status`, `help`) are exempt.
23. `INBOX.md` is a UI projection driven by course interaction state. Its layout (command-entry, clarification, answer-entry, post-completion) is determined by the current state, not by a static template.
24. `academic-coach inbox` is valid in both `hybrid` and `doc` modes. Do not reject an inbox request just because the user is currently interacting via chat — hybrid mode means both surfaces are active. Check the course's registered `interaction_mode` before deciding whether INBOX.md is available.

## When to Use

Use this skill when the user wants any of the following:

- A long-term tutoring workflow for a course or exam
- A course initialized from mixed study materials
- Knowledge-tree construction and progress tracking
- A one-knowledge-point-at-a-time teaching loop
- Weak-point analysis, mistake tracking, and spaced review
- Exam simulation based on past papers and high-frequency topics
- Obsidian-based study records that persist across sessions
- External markdown-based study records when the user does not want the workflow inside Obsidian
- A markdown-first study workspace outside Obsidian, when the user wants the same protocol without storing files in the vault

Do not use this skill for:

- One-off factual questions with no long-term tracking
- Generic brainstorming unrelated to a concrete course
- Pure document conversion with no tutoring workflow

## Workspace Layout

First determine the workspace mode:

- `obsidian` (default, recommended)
- `external-markdown` (allowed when the user prefers a non-Obsidian folder)

If workspace mode is `obsidian`, resolve the correct Obsidian course folder first.
If workspace mode is `external-markdown`, resolve the user-specified course folder outside the vault.

### `<course-folder>/study-system/` (state and knowledge files)

Required files:

- `COURSE_OVERVIEW.md`
- `PROGRESS.md`
- `KNOWLEDGE_TREE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `EXAM_FOCUS.md`
- `REVIEW_SCHEDULE.md`
- `SYLLABUS_ASSETS.md`
- `KNOWLEDGE_REGISTRY.json`

Recommended optional files:

- `STATUS.md`
- `TEACHING_LOG.md`
- `EXAM_SIMULATIONS.md`
- `COURSE_CONFIG.json`

### `<course-folder>/` (doc-first collaboration surface — at course root, NOT inside study-system/)

These files live directly under the course folder, alongside `study-system/`:

- `DASHBOARD.md` — human-facing control panel and summary
- `INBOX.md` — current interaction surface / input console
- `OUTBOX.md` — latest agent responses / summaries
- `SESSIONS/` — one note per teaching/review/exam transaction
- `TOPICS/` — durable concept notes mapped to knowledge points

**Important:** When checking for INBOX.md, look at `<course-folder>/INBOX.md`, NOT `<course-folder>/study-system/INBOX.md`. The registry's `inbox_path` field (if set) points to the correct location.

## Supporting Files Included With This Skill

References:
- `references/packaging-and-distribution.md` — how to package and publish Academic Coach as a public repo; includes Hermes tap layout, manual clone/copy paths for other agents, and the current multilingual README strategy (`README.md` as the primary English homepage plus `README.zh-CN.md` for Chinese)
- `references/reuse-map.md` — what to keep, lightly adapt, or redesign when evolving Academic Coach from chat-first to doc-first
- `references/doc-interaction-protocol.md` — the document-first / Obsidian-first interaction layer built on top of the same Academic Coach protocol core
- `references/doc-first-template-contract.md` — canonical responsibilities and creation rules for `DASHBOARD.md`, `INBOX.md`, `OUTBOX.md`, `SESSION` notes, and `TOPIC` notes in the doc-first surface
- `references/user-journey.md` — timeline-first statement of how users discover, bootstrap, use, and grow with Academic Coach over the life of a course

Templates:
- `templates/COURSE_OVERVIEW.template.md`
- `templates/PROGRESS.template.md`
- `templates/KNOWLEDGE_TREE.template.md`
- `templates/WEAK_POINTS.template.md`
- `templates/MISTAKES.template.md`
- `templates/EXAM_FOCUS.template.md`
- `templates/STATUS.template.md`
- `templates/TEACHING_LOG.template.md`
- `templates/EXAM_SIMULATIONS.template.md`
- `templates/COURSE_CONFIG.template.json`
- `templates/KNOWLEDGE_REGISTRY.template.json`
- `templates/REVIEW_SCHEDULE.template.md`
- `templates/DASHBOARD.template.md`
- `templates/INBOX.template.md`
- `templates/OUTBOX.template.md`
- `templates/SESSION.template.md`
- `templates/TOPIC.template.md`

References:
- `references/init-questionnaire.md`
- `references/init-response-skeleton.md` — standardized first-turn reply shape for fresh/no-state starts and implicit bootstrap cases
- `references/cron-prompt-patterns.md`
- `references/review-history-schema.md`
- `references/help-and-commands.md`
- `references/material-extraction-recipes.md` — image-PDF extraction, knowledge mapping detection, PPT↔textbook alignment
- `references/post-teaching-update-recipe.md` — exact field-level update recipe for Step 7 (post-teaching file consistency)
- `references/digital-electronics-teaching-notes.md` — domain-specific teaching patterns, analogies, assessment banks, and score tracking for 数字电子技术基础
- `references/command-and-target-model.md` — command taxonomy, course identity model, and target-resolution priority across chat/doc/hybrid workflows
- `references/request-routing-examples.md` — canonical request schema plus routing/normalization examples across chat, notes, and cron surfaces
- `references/init-scaffolding-spec.md` — exact full-init vs lightweight-bootstrap artifact matrix, file creation order, and template variable filling rules
- `references/hybrid-chat-doc-persistence.md` — hybrid workflow rule: terminal/chat remains first-class, but chat-originated runs must still write back into `SESSIONS/`, `OUTBOX.md`, and related study-system records when doc-first artifacts exist

Use the template files as starting points during initialization instead of inventing file layouts from scratch.
Use the reference files to standardize the clarification phase and cron prompt construction.

## Data Model

### Knowledge status values

Use exactly these states:

- `unseen` → □ 未学习
- `learning` → ◐ 学习中
- `mastered` → ✓ 已掌握
- `weak` → ⚠ 薄弱
- `forgotten` → ✗ 遗忘

### `KNOWLEDGE_REGISTRY.json`

Maintain one record per fine-grained knowledge point. Recommended fields:

```json
{
  "course": "Machine Learning",
  "last_updated": "2026-06-13",
  "knowledge_points": [
    {
      "id": "ch01-module02-kp03",
      "chapter": "Chapter 1",
      "module": "Linear Regression",
      "knowledge_point": "Normal Equation",
      "aliases": ["least squares closed-form"],
      "status": "unseen",
      "dependencies": ["matrix multiplication", "transpose"],
      "importance": 5,
      "difficulty": 3,
      "evidence_sources": ["textbook p.12-14", "ppt week2 slide 8-10"],
      "exam_frequency": 4,
      "mastery_score": null,
      "mistake_count": 0,
      "last_studied": null,
      "next_review": null,
      "review_history": [],
      "notes": ""
    }
  ]
}
```

Guidelines:

- Knowledge points must be as fine-grained as practical.
- Prefer stable IDs.
- `importance` and `exam_frequency` use a 1-5 scale.
- `mastery_score` is the most recent 0-100 evaluation.
- `next_review` must be recomputed after each learning or review event.

## Help Protocol: `academic-coach help`

Use this command to explain how the protocol works before any course-specific action.

It should:
- explain that `academic-coach` is usable now as a pure skill protocol
- explain that `/academic-coach ...` is pseudo-command input, not a native Hermes slash command
- list all supported commands
- explain the standard initialization → audit → plan → continue/review workflow
- explain what happens when the user starts with `/academic-coach ...` or natural language before initialization: the skill should enter an implicit bootstrap gate rather than fabricate state
- mention exam-oriented and deadline-driven use as optional scenarios, not the default framing
- point to `references/help-and-commands.md` for the operator manual

## Initialization Protocol: `academic-coach init`

Do not start by blindly processing files. First run a structured clarification phase.

### Clarification checklist

Before initialization, gather or confirm:

1. Course name
2. Academic term / semester
3. Workspace mode: `obsidian` or `external-markdown`
4. Interaction mode for this course: `chat`, `doc`, or `hybrid`
5. Course folder path inside Obsidian, or an external markdown course folder, or permission to create it
6. Preferred teaching/output language
7. Exam date if known
8. Target score or target mastery level
9. User's current foundation level
10. Available materials and their paths or links
11. Whether there are labs, homework, or project components
12. Whether past exams and answer keys are available
13. Time budget per day / per week
14. Whether to create cron review reminders
15. Whether materials may include images/scans needing OCR or vision help

Missing critical information must be asked before proceeding.

Important target-resolution rule for explicit `init`:
- do not open by assuming the request belongs to an already-known course unless the user clearly targeted that course
- if the user is creating a new test course or gives a different folder/workspace than an existing course, that explicit new target wins
- only inspect an existing study-system after the target course has been confirmed

For a reusable question flow, consult `references/init-questionnaire.md`.

Reference files:
- `references/COMMAND_ROUTING_MATRIX.md` — normalization rules for pseudo-commands, natural-language triggers, no-state bootstrap, and lightweight-vs-full-init routing

### Implicit Initialization Gate

If the user invokes any `academic-coach` command other than `init` in a workspace with no known `study-system/` or no established course state, do not fabricate progress, mastery, review queues, or audit results.

Instead:
1. acknowledge the requested intent
2. state that no initialized course state has been detected yet
3. enter the minimum clarification phase needed to bootstrap the workflow
4. after clarification, either run full `academic-coach init` or perform a lightweight bootstrap if the user explicitly wants immediate teaching before complete archive setup

Command-specific behavior when no study-system exists:
- `status`: explain that there is no initialized course state yet, then offer/initiate bootstrap
- `audit`: explain that there is nothing to audit yet, then offer/initiate bootstrap
- `continue`, `review`, `weak`: do not pretend there are due items or stored progress; bootstrap first
- `exam`: may proceed only as an ad-hoc mock session if the user explicitly wants that, but should still explain that persistent tracking requires bootstrap
- natural-language requests such as `/academic-coach 帮我复习 xxx` or `use academic-coach to study ...`: treat them as intent triggers and route them through this gate when no state exists

### Lightweight Bootstrap

Use lightweight bootstrap only when all of the following are true:
- there is no established `study-system/` yet
- the user did not explicitly ask for a full archival init first
- the user wants immediate teaching, review, or exam help before the full system is built
- enough minimum context is available to avoid fabricating the subject or scope

Minimum required clarification for lightweight bootstrap:
1. course or subject name
2. preferred teaching/output language
3. workspace mode
4. interaction mode (`chat`, `doc`, or `hybrid`)
5. intended target folder, or explicit permission to defer file creation temporarily
6. immediate goal for this session (e.g. review one topic, debug one homework concept, run one mock question)
7. currently available materials or evidence, even if partial

Lightweight bootstrap behavior:
1. create or reserve the target course context if the user wants persistence now
2. create a minimal state footprint instead of the full archive when appropriate
3. record unknowns explicitly rather than guessing missing chapters, assets, or exam weights
4. allow exactly one immediate teaching/review/exam task after the minimal clarification is done
5. clearly mark the session as partially initialized until full `academic-coach init` or `academic-coach sync` completes the archive

Minimal artifacts for lightweight bootstrap when persistence is requested:
- `COURSE_CONFIG.json`
- `STATUS.md`
- `PROGRESS.md`
- `KNOWLEDGE_REGISTRY.json` with only confirmed knowledge points or placeholders clearly marked as provisional
- `SYLLABUS_ASSETS.md` with partial-inventory notes

Rules:
- do not fabricate a full knowledge tree from thin evidence
- do not generate comprehensive exam-focus rankings without supporting materials
- do not silently upgrade lightweight bootstrap into full init without saying so
- recommend full `academic-coach init` or `academic-coach sync` once enough materials are available

### Initialization steps

After clarification:

1. Resolve the target course folder according to workspace mode.
2. If workspace mode is `obsidian`, find the matching course folder in the vault and align with existing academic-path structure.
3. If the target folder is absent, create it only after permission is clear.
4. Create `study-system/`.
5. **Scan material directory for pre-existing knowledge mapping files** (e.g., `knowledge_ppt_mapping.json`). If found, use it as the primary source for knowledge point extraction — skip manual material analysis.
6. Build `SYLLABUS_ASSETS.md` with a source inventory and coverage notes.
7. Analyze only the materials the user actually provided (or use a detected mapping file). If materials are missing, record that honestly; do not invent substitute course content.
8. Construct the course knowledge tree at course → chapter → module → knowledge point granularity, but only to the degree the evidence supports.
9. Create `KNOWLEDGE_TREE.md`.
10. Create `KNOWLEDGE_REGISTRY.json` with default statuses.
11. Create the remaining markdown files. **Prefer batch-creating all files via `execute_code`** rather than individual `write_file` calls.
12. Generate a learning route with dependency order and exam weighting.
13. Offer cron setup confirmation if scheduling is desired.
14. When creating the first set of course files, prefer the bundled templates for `COURSE_OVERVIEW.md`, `PROGRESS.md`, `KNOWLEDGE_TREE.md`, `WEAK_POINTS.md`, `MISTAKES.md`, `EXAM_FOCUS.md`, `KNOWLEDGE_REGISTRY.json`, and `REVIEW_SCHEDULE.md`.
15. If the workflow uses optional execution files, prefer the bundled templates for `STATUS.md`, `TEACHING_LOG.md`, `EXAM_SIMULATIONS.md`, and `COURSE_CONFIG.json`.
16. **If exam is <7 days away**, set `intensive_mode: true` in COURSE_CONFIG.json and use compressed review intervals in KNOWLEDGE_REGISTRY.json settings.
17. For smoke tests, the honest path is: create minimal/partial scaffolding with real empty-state notes, or use one small real user-provided file. Never fabricate demo chapters or fake source materials.

### Required initialization outputs

`COURSE_OVERVIEW.md` should include:
- course identity
- scope
- assessment structure if known
- target outcomes
- material summary
- study strategy summary

`PROGRESS.md` should include:
- overall counts by status
- latest studied point
- next recommended point
- latest score
- recent updates log

`KNOWLEDGE_TREE.md` should include:
- nested tree view
- dependency notes
- high-frequency exam markers

`WEAK_POINTS.md` should include:
- current weak topics ranking
- why each is weak
- linked mistakes / symptoms

`MISTAKES.md` should include a structured log table with:
- date
- question
- user answer
- correct answer
- error reason
- related knowledge point
- occurrence count

`EXAM_FOCUS.md` should include:
- likely high-weight topics
- observed patterns from past papers
- ranking by frequency and importance

`REVIEW_SCHEDULE.md` should include:
- due today
- due soon
- long-term cadence
- cron status if configured

## Daily Teaching Protocol: `academic-coach continue`

### Step 0: state header

Every active teaching reply begins with the fixed status header.
**Prefer using `companion.get_progress()` and `companion.detect_state()`** to populate these values rather than manually reading and counting from raw files:

- 当前课程：...
- 当前知识点：...
- 总体进度：...%
- 已掌握：...
- 学习中：...
- 薄弱项：...

### Step 1: choose the next knowledge point

**Prefer `companion.find_eligible_next_kps()`** to get the dependency-safe, weight-sorted shortlist. Then use LLM judgment to pick from the top candidates considering:

1. exam weight (from companion priority score)
2. review urgency (from `companion.find_due_reviews()`)
3. continuity (prefer learning over unseen when scores are close)
4. recent mistake concentration
5. user hint if provided

Explain the choice briefly if helpful.

### Step 2: teach

Teaching must include:

- core principle or mechanism
- intuitive explanation
- at least one example
- connection to already learned knowledge
- common misunderstanding if relevant

Do not only recite definitions.

### Step 3: ask for restatement

Always ask the user to explain the concept in their own words.

### Step 4: assess with questions

Ask at least:

- 1 concept question
- 1 understanding question
- 1 application question

Add calculation or derivation questions when appropriate for the subject.

Assessment-turn rule:
- after asking the assessment questions, stop and wait for the user's answer
- if the user answers only part of the assessment, ask the remaining unanswered question(s) before scoring
- do not treat a good restatement alone as sufficient to finalize the round

### Step 5: score

Score 0-100 using:

- conceptual understanding
- accuracy of expression
- application ability
- knowledge linkage

### Step 6: classify mastery

- 90-100 → `mastered`
- 70-89 → `learning`
- below 70 → `weak`

If the user previously mastered the point but now fails badly in review, downgrade to `forgotten` or `weak` depending on severity.

### Step 7: update records

After evaluation, update all state files. **Prefer batching updates via `execute_code`** using `patch()` calls. The companion's write operations (Phase 2) will handle this deterministically; until then, update these files manually in one batch:

- `PROGRESS.md`
- `WEAK_POINTS.md` (add/update/remove as score dictates)
- `MISTAKES.md` (append any new errors with cause + linked KP)
- `REVIEW_SCHEDULE.md` (schedule +1d/+3d/+7d/+14d/+30d from today)
- `KNOWLEDGE_REGISTRY.json` (update status, score, last_session, next_review)
- `TEACHING_LOG.md` (append session entry)
- If doc-surface enabled: update `OUTBOX.md` with completion summary + next action
- If doc-surface enabled: update `SESSIONS/` session note to `completed`

Then stop and wait. Do not auto-start the next point.

## Status Protocol: `academic-coach status`

Report the current course state. Use `companion.get_progress()` for accurate counts.

Output:
- course name + course_id
- interaction mode + workspace mode
- current interaction state (from `companion.detect_state()`)
- progress: mastered/total (percentage), plus learning/weak/unseen/forgotten counts
- due reviews today and within 3 days (from `companion.find_due_reviews()`)
- weak points summary
- next recommended action
- active session if any (from `companion.find_active_session()`)

## Inbox Protocol: `academic-coach inbox`

**CRITICAL: When the user invokes `academic-coach inbox`, you MUST read and dispatch INBOX.md. Do NOT fall through to chat-mode teaching. Do NOT treat `inbox` as equivalent to `continue`.**

Step 0 — mandatory first action:
1. Resolve the course context (use `companion.resolve_course()`).
2. Check `ctx.interaction_mode` — if `chat`, explain inbox is not available and suggest `continue`. If `doc` or `hybrid`, proceed.
3. Read INBOX.md from `ctx.inbox_path` (or `<course-folder>/INBOX.md`). It exists at the course root, NOT in study-system/.
4. Parse it with `companion.parse_inbox(ctx)`.
5. If the parsed action is valid, execute it. If not, report the validation errors.

This is the primary doc-mode entry point. **It works in both `doc` and `hybrid` interaction modes.** Only pure `chat` mode courses have no INBOX.md.

Execution flow:
1. Parse INBOX.md via `companion.parse_inbox(ctx)` — extracts action, details, context
2. Validate via `companion.validate_request(parsed)` — rejects multi-select, empty action
3. Detect current state via `companion.detect_state(ctx)`
4. **Conflict check**: if state is `awaiting_user_answer` and the user is starting a new instructional action, surface the conflict. Offer: resume current thread OR cancel and start new.
5. If valid and no conflict, normalize into the corresponding internal mode (`continue`, `review`, `exam`, etc.) and execute
6. Create/update session note in `SESSIONS/`
7. After completion, update `OUTBOX.md` with result + next action
8. Reset `INBOX.md` projection according to the state machine (post-completion → command-entry)

The inbox is a projection surface, not the canonical state store. Session notes are the durable record.

## Review Protocol: `academic-coach review`

Use spaced repetition. Default intervals: 1d / 3d / 7d / 14d / 30d.

**Use `companion.find_due_reviews()`** to get the due review queue. Do not manually scan KNOWLEDGE_REGISTRY.json.

Review flow:
1. Get due items from `companion.find_due_reviews(ctx, days=0)`
2. Ask recall / transfer questions before re-explaining
3. Rescore the knowledge point
4. If failure is substantial, downgrade status (use `companion.apply_mastery_changes()`)
5. Recompute the next review date (use `companion.schedule_reviews()`)
6. Update review history and markdown summaries

When multiple items are due, still handle one knowledge point at a time unless the user explicitly asks for a batch review summary.

If nothing is due yet:
- say so explicitly
- do not pretend the review queue is non-empty just to keep the flow moving
- offer the user a clear choice among: strict no-op review, early review of a not-yet-due point, or switching to `continue`

## Weak-Point Protocol: `academic-coach weak`

Use this mode to focus on fragile knowledge.

Prioritize knowledge points with:
- repeated mistakes
- low mastery scores
- recent downgrades
- high exam frequency

Provide short targeted repair sessions rather than broad lectures.

## Planning Protocol: `academic-coach plan`

Generate:

1. full learning route
2. recommended learning order
3. estimated study time
4. high-frequency topic ranking
5. exam weight analysis

Use dependencies plus evidence from past exams and assignments when available.

### Priority scoring formula

When building the learning route, score each knowledge point with:

```
priority = (importance × exam_frequency × 2) / difficulty
```

Higher score = study first. This naturally surfaces high-weight, low-difficulty points for early study while pushing hard-but-low-frequency points later.

### Time estimation

Estimate per-KP study time from difficulty: 1→15min, 2→20min, 3→30min, 4→45min, 5→60min. Sum all to get total study time, then compare against available days × daily budget.

### Study plan output

Create `STUDY_PLAN.md` in the study-system directory with:
- Priority ranking table (all KPs sorted by score)
- Day-by-day schedule with time slots
- Chapter breakdown with average priority
- Tier-based exam weight analysis (Tier 1/2/3 by combined importance×frequency)
- Score projection table (what coverage level → what expected score)
- Review strategy specific to the timeline

## Exam Protocol: `academic-coach exam`

When the user enters exam mode:

1. infer likely重点 from past papers, assignments, and teacher emphasis
2. generate a mock paper
3. optionally set a time limit
4. collect answers in chat or in a companion Obsidian file
5. score the result
6. produce an analysis covering:
   - coverage
   - weak points
   - score loss reasons
   - estimated real-exam score

Recommended artifacts:
- append summary to `EXAM_SIMULATIONS.md`
- update `WEAK_POINTS.md`, `MISTAKES.md`, and `EXAM_FOCUS.md`

## Sync Protocol: `academic-coach sync`

Use when new files appear or existing materials change.

Tasks:
- rescan assets
- refresh `SYLLABUS_ASSETS.md`
- add newly discovered knowledge points
- update evidence sources
- revise exam focus if new papers appear
- preserve existing mastery history unless the new material invalidates it

## Audit Protocol: `academic-coach audit`

**Use `companion.audit(ctx)`** for a comprehensive automated audit. The companion runs 7 checks:
1. Registry cross-reference with filesystem
2. Required file existence
3. Doc surface file existence
4. SESSIONS/ directory health
5. Single-thread enforcement
6. Progress consistency (registry vs PROGRESS.md)
7. Naming convention compliance

The companion returns a structured report with status (`healthy`/`warnings`/`broken`), a list of issues, and repair recommendations. Supplement with manual inspection for subject-matter concerns (exam focus freshness, material coverage).

## Mistake Logging Rules

Every substantive error should record:
- question
- user answer
- correct answer
- error reason
- linked knowledge point
- occurrence count

Error reasons should be normalized where possible, e.g.:
- concept confusion
- formula misuse
- missing prerequisite
- careless arithmetic
- incomplete reasoning
- memorized but not understood

## Scheduling Protocol: `academic-coach schedule`

This skill may recommend cron jobs but must confirm before creation or modification.

Typical schedules:
- daily review reminder
- every 3 days weak-point drill
- weekly mock exam
- pre-exam intensified review

When creating a cron job, make the prompt self-contained and include:
- course name
- target folder
- command mode (`review`, `continue`, or `exam`)
- expected output style
- reminder vs autonomous generation behavior

## Recommended Cron Patterns

Examples to adapt, not literal hardcoded defaults:

- Daily review: `0 20 * * *`
- Weekly mock exam: `0 14 * * 0`
- Intensified pre-exam review: `0 19 * * 1-5`

Always confirm first.

For self-contained cron wording, adapt the prompt patterns in `references/cron-prompt-patterns.md`.

## Mixed-Material Handling

Material may include text, PDFs, PPTX, images, screenshots, and scans.

Preferred approach:
1. Use extracted text where possible.
2. If the material is image-heavy, use OCR/vision-capable tools.
3. For lecture slides, preserve chapter/slide provenance in evidence fields.
4. For past exams, map each question to knowledge points and frequency.
5. For handwritten notes, mark uncertain extraction explicitly.

### Pre-existing knowledge mapping files (CRITICAL)

Before manually constructing the knowledge tree, **always check the material directory for pre-existing mapping files** such as:
- `knowledge_ppt_mapping.json`
- `index.json`, `outline.json`, `syllabus.json`
- Any JSON/YAML mapping knowledge points to slides/chapters/pages

If a mapping file exists and is well-structured, use it as the primary source for KNOWLEDGE_REGISTRY.json entries. Transform its keys into `id`, `knowledge_point`, `module`, and `evidence_sources` fields. This avoids hours of manual material analysis.

### Image-based PDF extraction pipeline

Many Chinese technical textbooks are scanned PDFs (image-only, no extractable text). Use this pipeline:
1. Try `pypdf` first (fastest — `PdfReader(path).pages[i].extract_text()`)
2. If empty, install `pymupdf` (`pip3 install pymupdf`) and convert pages to PNG: `page.get_pixmap(dpi=200).save(f'/tmp/page_{i}.png')`
3. Use `vision_analyze` on each PNG to extract text
4. For long PDFs, prioritize the table of contents pages first to establish scope, then extract only exam-relevant sections

### PPT-to-textbook chapter mapping

When PPTs and textbook use different chapter numbers, build a cross-reference early:
- Match PPT titles (e.g., "ch5 触发器") to textbook sections (e.g., "第五章 半导体存储电路 §5.2-5.3")
- Note the mapping in `SYLLABUS_ASSETS.md` so the teaching loop can cite both sources

## Output Style

During course-mode replies:
- concise but educational
- use the user's preferred teaching/output language
- preserve technical terms in English or bilingual form when useful
- no flooding with unrelated extras
- explain reasoning and intuition, not just final statements
- use public-facing, reusable wording rather than personal or one-off exam-cram framing unless the user explicitly asks for that style

## Teaching Technique Notes

When teaching technical subjects, these patterns consistently produce high comprehension:

### Physical Intuition Anchors
- **Complement / two's complement**: Clock analogy (mod-12 for mod-2^N). "往回拨5小时 = 往前拨7小时"
- **De Morgan's theorem**: Series-parallel switch circuit analogy. "破坏串联断一个就够；破坏并联全部都断"
- **Gray code**: Rotary encoder / angle measurement context. Show intermediate glitch states explicitly.
- **BCD +6 correction**: "十六进位 vs 十进位差6个空洞" — frame as skipping invalid codes, not arbitrary magic number.
- **Logical vs arithmetic "+"**: Explicitly show 1+1=1 (OR) vs 1+1=10 (binary add) side by side on day one.

### Assessment Question Patterns That Work
- **Concept question**: "Why does X exist / why is X asymmetric / why not just use Y?"
- **Understanding question**: Step-by-step calculation with explicit theorem citations per step
- **Application question**: Real-world scenario (encoder, insurance box, door access) → write expression → draw circuit
- **Verification bonus**: Ask student to verify result by reverse operation (e.g., Gray→binary→Gray, or complement→original)

### Score Calibration Notes
- Students who explain "why" (not just "what") deserve 95+ on concept questions
- Step-by-step with theorem citations per step = 100 on understanding questions
- Alternative proof methods (formula + exhaustive) on same question = bonus credit
- Non-standard but internally consistent notation (e.g., Gray MSB=0) should be noted but not penalized

## Common Pitfalls

1. Starting `init` before collecting enough metadata.
2. Teaching multiple knowledge points in one turn.
3. Forgetting to wait for the user's answer.
4. Letting markdown files and JSON state drift apart.
5. Using vague knowledge points that are too coarse to track.
6. Failing to record evidence sources from materials.
7. Creating cron jobs without confirmation.
8. Overwriting historical mistakes instead of incrementally logging them.
9. Ignoring prerequisite gaps when choosing the next topic.
10. Treating exam frequency as the only priority and skipping fundamentals.
11. **Not checking for pre-existing knowledge mappings.** When materials include PPT-to-HTML conversions, always check for a `knowledge_ppt_mapping.json` or similar mapping file first. If it exists, use it directly as the primary source for knowledge point extraction instead of manually scanning all materials. This can turn a multi-hour analysis into minutes.
12. **PPT chapter numbering ≠ textbook chapter numbering.** Chinese textbook PPTs often use their own chapter numbering that diverges from the textbook. For example, PPT "ch10 波形产生和整形" may correspond to textbook Chapter 7. Always cross-reference PPT titles with the textbook table of contents rather than assuming numbering alignment.
13. **Creating study-system files one at a time.** During init, use `execute_code` to batch-create all 12+ files in a single script. Individual `write_file` calls are slow and create unnecessary tool-call overhead.
14. **Using standard review intervals for near-exam courses.** When the exam is <7 days away, use compressed intervals (e.g., 4h / 12h / 24h) instead of the default 1d / 3d / 7d / 14d / 30d. Set `intensive_mode: true` in COURSE_CONFIG.json and override `settings.default_review_intervals` in KNOWLEDGE_REGISTRY.json.
15. **Vague question format in MISTAKES.md.** When logging mistakes, write the question exactly as the user heard it during the assessment round — not a paraphrased or abstracted version. This makes later review rounds more effective because the user recognizes the framing.
16. **Step 7 file updates done inconsistently.** After each teaching round, multiple files must be patched atomically (PROGRESS, STATUS, MISTAKES, TEACHING_LOG, REVIEW_SCHEDULE, KNOWLEDGE_REGISTRY, optionally WEAK_POINTS and KNOWLEDGE_TREE). Use `execute_code` with `patch()` to update all in one block. See `references/post-teaching-update-recipe.md` for the exact field-level recipe and consistency contract.
17. **Fabricating demo materials during init.** Never write fake chapter notes, synthetic course content, or made-up source files just to make extraction/audit look successful. Honest empty or partial scaffolding is correct; fabricated materials are a protocol failure.
18. **Scoring before the assessment is actually answered.** If the user only restated the concept or only answered one of several assessment questions, the round is not complete yet. Ask the remaining question(s) first; only then score and update state.

## Verification Checklist

- [ ] Course folder located or created correctly for the chosen workspace mode
- [ ] `study-system/` created under the course folder
- [ ] Uppercase English filenames used for all managed documents
- [ ] `KNOWLEDGE_REGISTRY.json` exists and is the authoritative state store
- [ ] `KNOWLEDGE_TREE.md` uses fine-grained knowledge points
- [ ] Teaching loop handles exactly one knowledge point at a time
- [ ] Status header appears at the start of active teaching replies
- [ ] Mistakes are logged with causes and linked knowledge points
- [ ] Review intervals are updated after each teaching/review event
- [ ] Cron changes only happen after confirmation
