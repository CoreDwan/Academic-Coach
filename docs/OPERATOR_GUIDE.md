# Academic Coach Operator Guide

## Can It Be Used Right Now?

Yes.

But with one important caveat:

`academic-coach` is currently usable as a pure skill protocol, not as a native Hermes slash command.

Its default workspace is Obsidian, but that should be treated as a default rather than a hard requirement. The user may choose an external markdown-first course folder and still use the same protocol. During `academic-coach init`, workspace mode and target folder should be confirmed explicitly.

In practice, these inputs are valid usage patterns for the agent:
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

## Command List

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

## What `audit` Is For

`academic-coach audit` is the repair-and-consistency pass for an existing `study-system/`.

Use it when:
- you initialized with partial materials
- you added new files later
- progress counts feel wrong
- markdown files and JSON state may have drifted
- you want to clean up the study-system before an intensive review cycle

## What `audit` Should Verify

1. required files exist
2. uppercase naming is respected
3. `KNOWLEDGE_REGISTRY.json` is valid and readable
4. `PROGRESS.md` is consistent with registry counts
5. `STATUS.md` is consistent if present
6. `REVIEW_SCHEDULE.md` roughly matches due reviews
7. `WEAK_POINTS.md` and `MISTAKES.md` reflect current weak/error state
8. stale or missing files are called out explicitly

## Pre-Init Execution Note

Before the first real `academic-coach init`, follow `docs/INIT_CHECKLIST.md` so workspace mode, target folder, material readiness, and summary confirmation are all checked before file creation.

## Starting From a Fresh Directory or No-State Workspace

If the user starts with `/academic-coach ...` but there is no existing `study-system/` or course state yet, the protocol should not pretend that progress, due reviews, or auditable records already exist.

Instead, route the request through an implicit bootstrap gate:
1. recognize the requested intent
2. state that no initialized course state has been detected yet
3. ask the minimum clarification questions needed to bootstrap
4. then either run full init or a lightweight bootstrap path if the user explicitly wants immediate teaching first

This applies both to pseudo-commands and natural-language triggers such as:
- `/academic-coach review`
- `/academic-coach audit`
- `/academic-coach 帮我复习概率论`
- `use academic-coach to study operating systems`

## Recommended First-Time Usage

When you do not yet have every textbook, PPT, lab report, and past paper, the repo should still be used in a pragmatic order:

1. `academic-coach help`
2. `academic-coach init`
3. `academic-coach audit`
4. `academic-coach plan`
5. `academic-coach continue`
6. `academic-coach review`
7. `academic-coach exam`

This prioritizes a functioning study loop over perfect archive completeness.

## True Slash Command vs Pure Skill

If you later want a true Hermes-native `/academic-coach` slash command, that requires Hermes code changes in the CLI command registry. That is intentionally separate from the current skill-based design.
