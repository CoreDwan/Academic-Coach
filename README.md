# Academic Coach

Academic Coach is a reusable academic tutoring protocol designed for long-term course learning, exam readiness, and persistent study-state management across sessions.

Primary documentation in this repo is currently written in English for portability, but the protocol itself is multilingual. During initialization, the agent should confirm the user's preferred teaching/output language and keep technical terms in whichever bilingual mix is most helpful.

Current status:
- protocol-first
- pure skill workflow, not native slash commands
- Obsidian-default workspace design, with support for a user-chosen external markdown workspace
- explicit workspace_mode selection during init (`obsidian` or `external-markdown`)
- mixed-material support planned for real courses
- currently optimized for real-world early validation before public examples are added

## Core Idea

Academic Coach treats a course like a persistent study system rather than a one-off Q&A session.

It is built around four layers:

1. Protocol
   - command contract such as `academic-coach init`, `continue`, `review`, `exam`
2. State
   - `KNOWLEDGE_REGISTRY.json` as machine-readable ground truth
3. Human-facing study files
   - uppercase English markdown files inside `study-system/`
4. Reusable assets
   - templates and references that make behavior consistent across agents

## Repository Layout

- `SKILL.md` — main protocol definition
- `templates/` — reusable markdown/json file templates
- `references/` — operational references such as init questionnaire and cron prompt patterns
- `docs/` — repo-facing design and roadmap notes

## Managed Study-System Files

Required:
- `COURSE_OVERVIEW.md`
- `PROGRESS.md`
- `KNOWLEDGE_TREE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `EXAM_FOCUS.md`
- `REVIEW_SCHEDULE.md`
- `SYLLABUS_ASSETS.md`
- `KNOWLEDGE_REGISTRY.json`

Optional but recommended:
- `STATUS.md`
- `TEACHING_LOG.md`
- `EXAM_SIMULATIONS.md`
- `COURSE_CONFIG.json`

## Command Protocol

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

See also:
- `docs/OPERATOR_GUIDE.md`
- `docs/INIT_CHECKLIST.md`
- `docs/MINIMAL_WORKFLOW.md`
- `docs/AUDIT_SPEC.md`

## Design Constraints

- one knowledge point per teaching round
- must wait for user response before moving on
- Chinese-first teaching by default in this seed repo, but the protocol itself is multilingual and should confirm the user's preferred teaching/output language during init
- uppercase English filenames for managed study documents
- cron changes require confirmation
- no fake mastery, no fake coverage, no invented evidence

## Why No Public Example Yet

This repo is being prepared before a full real-course corpus is available.

The immediate goal is practical validation on real study workflows. Because of that, the repo currently prioritizes:
- protocol clarity
- reusable templates
- stable state schemas
- agent portability

instead of publishing a polished course example too early.

## Next Development Directions

1. real-course validation on one live course workflow
2. public example course once full materials exist
3. repository cleanup for broader open-source use
4. cron and automation presets for review / exam reminders
