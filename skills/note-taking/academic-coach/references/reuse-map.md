# Academic Coach Reuse Map

## Purpose

This document classifies which parts of the current `academic-coach` protocol should be reused as-is, reused with light adaptation, or redesigned when evolving from a terminal-first/chat-first workflow into a document-first Obsidian workflow.

The main conclusion is simple:

- keep the protocol core
- keep the state model
- keep the teaching constraints
- replace the interaction surface

Academic Coach should become a protocol core with multiple surfaces, not two separate tutoring systems.

## A. Reuse directly

These parts are already strong and should stay conceptually unchanged.

### 1. Command vocabulary / mode semantics

Keep these mode names and meanings:

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

Even in a document-first workflow, these should remain the internal routing vocabulary.
The user may trigger them from chat, pseudo-commands, dashboard buttons, inbox notes, or cron-created requests, but the protocol meaning should stay stable.

### 2. State model

Keep the existing authoritative state split:

- machine-stable source of truth: `KNOWLEDGE_REGISTRY.json`
- human-facing projections: markdown files such as `PROGRESS.md`, `WEAK_POINTS.md`, `REVIEW_SCHEDULE.md`, `MISTAKES.md`, `EXAM_FOCUS.md`

This separation is still the right architecture for Obsidian.
Markdown is readable and pleasant to browse; JSON is easier to validate and synchronize.

### 3. Knowledge-point mastery states

Keep the existing five-state model:

- `unseen`
- `learning`
- `mastered`
- `weak`
- `forgotten`

The labels and downgrade/upgrade behavior already match the intended long-term tutoring workflow.

### 4. One-knowledge-point teaching invariant

Keep this as a hard rule:

- one teaching round = one knowledge point
- no automatic jump to the next point
- wait for the user's answer before evaluation and progression

This remains essential in document-first mode. The interaction surface changes, but the pedagogical unit should not.

### 5. Teaching loop

Keep the current teaching sequence:

1. explain
2. ask the user to restate
3. ask concept / understanding / application questions
4. score
5. classify mastery
6. update records

This is one of the strongest parts of the protocol and should stay intact.

### 6. Bootstrap / no-state rules

Keep these exactly in spirit:

- no fabricated progress
- no fabricated weak-point history
- no fabricated review queue
- no fabricated audit result
- non-`init` first contact in a fresh workspace must go through the implicit bootstrap gate
- lightweight bootstrap remains explicitly partial

These rules matter even more in document workflows, because the presence of files can create a false sense of initialized state.

### 7. Audit and sync concepts

Keep both:

- `audit` = consistency / repair pass
- `sync` = rescan new materials and refresh evidence/state

A document-first system is more vulnerable to state drift, so these concepts become more valuable, not less.

### 8. Mixed-material ingestion assumptions

Keep support for:

- PDFs
- PPT/PPTX
- markdown notes
- images / scans
- homework
- past exams
- answer keys
- references / links

Also keep the rule that existing mapping files should be checked before manual extraction.

## B. Reuse with light adaptation

These parts should survive, but their presentation or execution model should change.

### 1. Pseudo-command triggers -> request normalization layer

Current form:
- `academic-coach continue`
- `/academic-coach review`

Document-first form:
- request item in `INBOX.md`
- frontmatter block in a note
- dashboard action request
- cron-generated request entry

The mapping should still normalize to the same internal mode (`continue`, `review`, etc.).

### 2. Reply header -> dashboard/session header

Current chat-oriented rule:
- 当前课程：
- 当前知识点：
- 总体进度：
- 已掌握：
- 学习中：
- 薄弱项：

Adaptation:
- keep the same information fields
- render them as a session-note header, dashboard summary block, or topic-note status block
- do not require a literal chat-style prefix in every medium

### 3. `study-system/` outputs -> study-system + collaboration surface

Keep `study-system/` as the protocol state area, but add a document collaboration surface around it.
Suggested addition:

- `DASHBOARD.md`
- `INBOX.md`
- `OUTBOX.md`
- `SESSIONS/`
- `TOPICS/`

The `study-system/` remains the managed academic state core; the new notes become the interaction surface.

### 4. Teaching log -> session notes

Current `TEACHING_LOG.md` can remain useful, but in a doc-first workflow the richer artifact is the individual session note.

Recommended adaptation:
- `TEACHING_LOG.md` remains a compact index or summary
- `SESSIONS/*.md` hold the full teaching transaction history

### 5. Cron jobs -> request producers

The current schedule idea still works, but instead of assuming a live chat turn, cron can create or trigger:

- a review reminder
- a generated inbox request
- a dashboard due-item refresh
- an autonomous review brief written into `OUTBOX.md`

The important change is that cron should target the document workflow explicitly.

### 6. Weak-mode and exam-mode artifacts

These modes should keep their existing logic, but the output destination changes:

- chat output -> session note / outbox note
- score summary -> `EXAM_SIMULATIONS.md` and session artifacts
- weak-point repair -> topic note plus state updates

## C. Redesign / create new protocol pieces

These pieces do not exist fully in the current terminal-first design and should be designed explicitly.

### 1. Document request lifecycle

Need a formal lifecycle such as:

- `open`
- `needs_clarification`
- `ready`
- `awaiting_user_answer`
- `completed`
- `cancelled`

This is the document equivalent of turn-taking in chat.

### 2. Request schema

Need a normalized schema for requests written in markdown, for example:

- request id
- mode
- course
- topic hint
- user goal
- status
- created / updated timestamps
- source note
- blocking questions

Without this, document-first routing will become inconsistent.

### 3. Session-note contract

Need a standard structure for teaching/review/exam session notes:

- status header
- request context
- explanation block
- user answer area
- assessment block
- score / mastery decision
- file updates applied
- next action

### 4. Topic-note contract

Need a durable structure for one knowledge point or topic note, including:

- canonical concept summary
- prerequisites
- linked mistakes
- linked sessions
- evidence sources
- current mastery summary
- next review

### 5. Document transaction model

A doc-first run should behave like a transaction:

1. read request
2. load current state
3. clarify if needed
4. create/update session note
5. wait for user answer when appropriate
6. evaluate
7. patch study-system files atomically
8. mark request status

This is more precise than a generic “reply in markdown” rule.

### 6. Multi-surface synchronization contract

Need an explicit contract for keeping these aligned:

- `KNOWLEDGE_REGISTRY.json`
- `PROGRESS.md`
- `STATUS.md`
- `REVIEW_SCHEDULE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `DASHBOARD.md`
- `INBOX.md` / `OUTBOX.md`
- `SESSIONS/` / `TOPICS/`

This is broader than the current sync model.

### 7. Conflict and ambiguity handling

Need rules for situations like:

- multiple open requests
- a topic note and inbox request disagree
- the user writes freeform text without a mode
- the user edits an old session after evaluation
- cron creates a request while another teaching round is already awaiting the user's answer

### 8. Obsidian-native ergonomics

Need conventions for:

- file naming
- wiki-links between topic notes and session notes
- callout usage
- frontmatter fields
- dashboard blocks
- where the user should type answers

## Recommended architecture

### Protocol core (stable)

Keep Academic Coach as the stable tutoring core:
- mode semantics
- state model
- teaching constraints
- bootstrap logic
- scoring and review logic
- exam / weak / audit / sync logic

### Interaction surfaces (replaceable)

Support multiple surfaces over the same core:
- chat / pseudo-command surface
- document-first Obsidian surface
- future web surface if needed

This means the correct evolution path is:
- not “replace Academic Coach”
- but “add a doc-first interaction protocol on top of Academic Coach core”

## Migration guidance

When evolving the repo, prefer this order:

1. write the doc-first interaction protocol
2. define request/session/topic schemas
3. update operator docs and references
4. keep existing command vocabulary stable
5. sync repo source, tap mirror, and live Hermes skill together

## Bottom line

Reuse the brain.
Replace the mouth, hands, and inbox.
