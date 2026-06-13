# Academic Coach Operator Guide

## Purpose

This is the human-facing operating guide for Academic Coach.
It explains how to use the protocol in practice after the control-plane docs define routing and targeting.

Core protocol docs:
- `docs/COMMAND_AND_TARGET_MODEL.md` — command taxonomy, helper taxonomy, course identity, and target resolution
- `docs/COMMAND_ROUTING_MATRIX.md` — initialized vs no-state vs lightweight-bootstrap routing
- `docs/INIT_SCAFFOLDING_SPEC.md` — full-init vs lightweight-bootstrap file creation rules
- `docs/DOC_INTERACTION_PROTOCOL.md` — document-first surface and persistence model

Supporting docs:
- `docs/REQUEST_ROUTING_EXAMPLES.md`
- `docs/INIT_CHECKLIST.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/USER_JOURNEY.md`
- `docs/REUSE_MAP.md`

## Can It Be Used Right Now?

Yes.

But with one important caveat:
`academic-coach` is currently usable as a pure skill protocol, not as a native Hermes slash command.

Its default workspace is Obsidian, but that should be treated as a default rather than a hard requirement. The user may choose an external markdown-first course folder and still use the same protocol. During `academic-coach init`, workspace mode and target folder should be confirmed explicitly.

Valid usage patterns:
- `academic-coach help`
- `academic-coach init`
- `academic-coach continue`
- `academic-coach review`
- `academic-coach exam`
- `academic-coach audit`

The pseudo-slash form can also be used conversationally:
- `/academic-coach help`
- `/academic-coach audit`

That works because the agent interprets them as protocol commands. It does not mean Hermes has a real registered `/academic-coach` command.

## Interaction Surfaces

Academic Coach is a protocol core with multiple surfaces:
- terminal chat / pseudo-command
- document-first collaboration in Obsidian or another markdown workspace
- cron-originated reminders or queued requests

These surfaces must reuse the same internal study modes and the same persistent course state.
They must not become separate tutoring systems.

For the concrete doc-first contract, see `docs/DOC_INTERACTION_PROTOCOL.md`.
For the user-timeline product anchor, see `docs/USER_JOURNEY.md`.

## Command Summary

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

For the command taxonomy, helper taxonomy, target resolution, and `workspace_mode` versus `interaction_mode`, see `docs/COMMAND_AND_TARGET_MODEL.md`.
For worked request normalization examples, see `docs/REQUEST_ROUTING_EXAMPLES.md`.

## What `audit` Is For

`academic-coach audit` is the repair-and-consistency pass for an existing `study-system/`.

Use it when:
- you initialized with partial materials
- you added new files later
- progress counts feel wrong
- markdown files and JSON state may have drifted
- you want to clean up the study-system before an intensive review cycle

It should verify at least:
1. required files exist
2. uppercase naming is respected
3. `KNOWLEDGE_REGISTRY.json` is valid and readable
4. `PROGRESS.md` is consistent with registry counts
5. `STATUS.md` is consistent if present
6. `REVIEW_SCHEDULE.md` roughly matches due reviews
7. `WEAK_POINTS.md` and `MISTAKES.md` reflect current weak/error state
8. stale or missing files are called out explicitly

## Pre-Init Execution

Before the first real `academic-coach init`:
- use `docs/INIT_CHECKLIST.md` as the short execution checklist
- use `docs/INIT_SCAFFOLDING_SPEC.md` as the canonical init/create-files spec
- use `docs/INIT_RESPONSE_SKELETON.md` for the first-turn shape in fresh or no-state workspaces

Do not create study-system files before the clarification summary is confirmed.

## Fresh Workspace / No-State Behavior

If the user starts with `/academic-coach ...` but there is no existing `study-system/` or course state yet, the protocol should not pretend that progress, due reviews, or auditable records already exist.

Instead, route the request through the implicit bootstrap gate:
1. recognize the requested intent
2. state that no initialized course state has been detected yet
3. ask the minimum clarification questions needed to bootstrap
4. then choose full init or lightweight bootstrap honestly

This applies both to pseudo-commands and natural-language triggers such as:
- `/academic-coach review`
- `/academic-coach audit`
- `/academic-coach 帮我复习概率论`
- `use academic-coach to study operating systems`

For the exact routing rules, see `docs/COMMAND_ROUTING_MATRIX.md`.

## Lightweight Bootstrap vs Full Init

Use lightweight bootstrap when the user wants immediate help in a fresh workspace and there is not enough evidence yet for a full archive-quality initialization.

Lightweight bootstrap should:
1. confirm the minimum needed context
2. avoid fabricating a full knowledge tree or exam ranking
3. optionally create only the minimal persistent files
4. permit one immediate teaching / review / exam task
5. leave the workspace clearly marked as partially initialized

Use full `academic-coach init` when the user wants the complete long-term study-system built now.
Use `academic-coach sync` later if the first session started lightweight and more materials arrive.

For exact artifact rules, see `docs/INIT_SCAFFOLDING_SPEC.md`.

## Recommended First-Time Usage

A pragmatic first-use sequence is:
1. `academic-coach help`
2. `academic-coach init`
3. `academic-coach audit`
4. `academic-coach plan`
5. `academic-coach continue`
6. `academic-coach review`
7. `academic-coach exam`

This prioritizes a functioning study loop over perfect archive completeness.

## Near-Exam Minimal Operating Loop

When materials are incomplete but finals pressure is real, do not wait for the perfect archive.
Use this loop:
1. establish the course context and run init honestly
2. mark unknowns instead of guessing coverage
3. run `academic-coach audit`
4. use `academic-coach plan` to rank high-value topics
5. alternate `academic-coach continue` and `academic-coach review`
6. use `academic-coach exam` to pressure-test retention
7. sync new materials later with `academic-coach sync`

A realistic finals cadence can be:
- daytime: `academic-coach continue`
- evening: `academic-coach review`
- every few days: `academic-coach audit`
- weekly or pre-exam: `academic-coach exam`

## True Slash Command vs Pure Skill

If you later want a true Hermes-native `/academic-coach` slash command, that requires Hermes code changes in the CLI command registry. That is intentionally separate from the current skill-based design.
