# Audit Specification

## Purpose

`academic-coach audit` is the study-system consistency and repair pass.

It exists because study workflows often start with partial materials, repeated manual updates, and evolving evidence. That creates drift risk between markdown summaries and the JSON registry.

## Inputs

The audit command should inspect the current course folder and its `study-system/` contents.
It should also respect the recorded workspace mode from `COURSE_CONFIG.json` when present, so the audit does not assume the course lives inside Obsidian.

Primary artifacts to inspect:
- `COURSE_OVERVIEW.md`
- `PROGRESS.md`
- `KNOWLEDGE_TREE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `EXAM_FOCUS.md`
- `REVIEW_SCHEDULE.md`
- `SYLLABUS_ASSETS.md`
- `KNOWLEDGE_REGISTRY.json`

Optional artifacts:
- `STATUS.md`
- `TEACHING_LOG.md`
- `EXAM_SIMULATIONS.md`
- `COURSE_CONFIG.json`

## Checks

1. existence checks
2. uppercase filename convention checks
3. JSON parse checks
4. stale-summary checks
5. weak-point consistency checks
6. mistake-log consistency checks
7. due-review consistency checks
8. asset-inventory freshness checks
9. optional-file consistency checks

## Output Shape

Recommended output:
- audit status: healthy / warnings / broken
- missing files
- inconsistent files
- stale files
- repair actions taken
- repair actions still needed
- recommended next command

## Repair Philosophy

The audit should prefer explicit repair over silent rewriting.

Good behavior:
- say what is wrong
- say what was repaired
- say what still needs human input
- say what cannot be inferred because source materials are missing

Bad behavior:
- inventing state to make files look complete
- overwriting history without reason
- pretending uncertain exam focus is certain
