# Academic Coach Help and Commands

This is the operator manual for the `academic-coach` protocol.

## Important Reality Check

`academic-coach` is usable now, but it is a pure skill protocol, not a native Hermes slash command.

That means these forms should be treated as protocol invocations by the agent:
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

The pseudo-slash form is also acceptable as user input:
- `/academic-coach help`
- `/academic-coach init`

But this is interpretation by the agent, not a registered Hermes CLI slash command.

## Command Summary

### `academic-coach help`
Show the operator guide, command list, and practical usage notes.

### `academic-coach init`
Start a new course study-system.
Use when you have enough basic course information and at least partial materials.
The agent should first run the clarification phase before creating files.

### `academic-coach status`
Show the current course header, progress counts, next recommended action, and urgent review items.

### `academic-coach continue`
Run one teaching round for exactly one knowledge point.
Must stop and wait after the user replies and is evaluated.

### `academic-coach review`
Run spaced review for one due knowledge point at a time.

### `academic-coach weak`
Focus on fragile or repeatedly failed knowledge points.

### `academic-coach plan`
Generate or refresh the overall learning route, ordering, time estimate, and exam-weight analysis.

### `academic-coach exam`
Enter mock-exam mode and write results into exam-focused artifacts.

### `academic-coach sync`
Refresh the study-system after new files or new evidence appear.

### `academic-coach mistakes`
Inspect the error log and summarize repeated mistake patterns.

### `academic-coach schedule`
Propose or update cron-based review/exam reminders. Must confirm first.

### `academic-coach audit`
Audit the current `study-system/` for consistency.
Use when the user suspects drift, missing files, stale status summaries, or mismatch between markdown files and `KNOWLEDGE_REGISTRY.json`.

## What `audit` Should Check

1. Required files exist.
2. Optional files are either present or intentionally absent.
3. Uppercase naming convention is respected.
4. `KNOWLEDGE_REGISTRY.json` parses correctly.
5. Counts in `PROGRESS.md` and `STATUS.md` do not obviously disagree with the registry.
6. `REVIEW_SCHEDULE.md` due items are not wildly inconsistent with `next_review` fields.
7. `WEAK_POINTS.md` and `MISTAKES.md` are aligned with recorded weak statuses and mistake counts.
8. `EXAM_FOCUS.md` still matches the latest available exam evidence.
9. `SYLLABUS_ASSETS.md` reflects the actual known material inventory.
10. Missing or stale artifacts are listed with concrete repair actions.

## Suggested `audit` Output Shape

- Course folder:
- Study-system path:
- Audit result: healthy / warnings / broken
- Missing files:
- Stale files:
- Inconsistencies:
- Recommended repairs:
- Suggested next command:

## What Happens If You Start Without `init`

If the user invokes `academic-coach` from a fresh directory or a workspace with no known `study-system/`, the skill should not fabricate progress, due reviews, weak points, or audit results.

Instead it should:
1. acknowledge the requested intent
2. explain that no initialized course state has been detected yet
3. enter a minimal bootstrap clarification phase
4. after clarification, either run full `academic-coach init` or perform a lightweight bootstrap if the user explicitly wants immediate teaching before complete archive setup

Examples:
- `/academic-coach review` in a fresh workspace → do not invent due items; bootstrap first
- `/academic-coach audit` in a fresh workspace → explain there is nothing to audit yet; bootstrap first
- `/academic-coach 帮我复习线性代数` → treat as a valid intent trigger; extract the course/topic and route into bootstrap

## Recommended First-Time Flow

If you are starting with partial materials or incomplete course assets:
1. `academic-coach help`
2. `academic-coach init`
3. `academic-coach audit`
4. `academic-coach plan`
5. `academic-coach continue` or `academic-coach review`

## Limitations

- Without full materials, the system can still work, but evidence coverage and exam-focus confidence will be lower.
- `academic-coach audit` repairs by updating files and summaries; it does not magically infer missing source materials.
- If you want a true `/academic-coach` Hermes slash command, Hermes itself must be extended in code.
