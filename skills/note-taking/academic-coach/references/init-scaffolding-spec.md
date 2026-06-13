# Academic Coach Init Scaffolding Spec

## Purpose

This document defines what initialization must physically create and how template variables should be filled.
Use it to keep full init, lightweight bootstrap, and later sync behavior consistent.

## Two Initialization Levels

### 1. Full init
Use when:
- the user explicitly asks for `academic-coach init`
- the user wants the long-term course system now
- enough material/context exists to build a meaningful archive

### 2. Lightweight bootstrap
Use when:
- there is no established state yet
- the user wants immediate help before full archive setup
- enough context exists to ground one focused session, but not enough for a full knowledge-map build

## Artifact Matrix

| Artifact | Full init | Lightweight bootstrap | Notes |
|---|---|---|---|
| `study-system/` | required | required if persistence is requested now | may be deferred only if user explicitly permits no files yet |
| `COURSE_OVERVIEW.md` | required | optional/deferred | avoid fake scope claims |
| `PROGRESS.md` | required | required | must clearly show partial initialization if bootstrap |
| `KNOWLEDGE_TREE.md` | required | optional/deferred | only create when evidence supports a real tree |
| `WEAK_POINTS.md` | required | optional | can remain placeholder if no real weak evidence yet |
| `MISTAKES.md` | required | optional | create when assessment starts or user wants persistence now |
| `EXAM_FOCUS.md` | required | optional/deferred | do not rank without evidence |
| `REVIEW_SCHEDULE.md` | required | optional/minimal | can hold "not enough history yet" during bootstrap |
| `SYLLABUS_ASSETS.md` | required | required | record both confirmed and missing assets |
| `KNOWLEDGE_REGISTRY.json` | required | required | only confirmed KPs in bootstrap; placeholders must be marked provisional |
| `STATUS.md` | recommended | required | best place to signal partial state clearly |
| `TEACHING_LOG.md` | recommended | optional | create once a real teaching/review round happens |
| `EXAM_SIMULATIONS.md` | optional | optional | create when exam mode is used |
| `COURSE_CONFIG.json` | recommended | required | must mark workspace mode and initialization level |
| `DASHBOARD.md` | recommended for doc-first | recommended for doc-first | human control panel |
| `INBOX.md` | recommended for doc-first | recommended for doc-first | request queue |
| `OUTBOX.md` | recommended for doc-first | recommended for doc-first | concise summaries |
| `SESSIONS/` | recommended for doc-first | recommended for doc-first | actual interaction records |
| `TOPICS/` | recommended for doc-first | optional | create when topic notes are actually used |

## Scaffolding Order

### Full init order
1. resolve workspace mode and target course folder
2. verify permission to create or modify files
3. create course folder if needed
4. create `study-system/`
5. create doc-first surface files/folders if this course should use them
6. build `SYLLABUS_ASSETS.md`
7. inspect for pre-existing mapping files such as `knowledge_ppt_mapping.json`
8. derive the first real knowledge tree from actual user-provided evidence only
9. create `KNOWLEDGE_REGISTRY.json`
10. create all required markdown state files from templates
11. create recommended optional files as appropriate
12. run sanity verification

### Lightweight bootstrap order
1. resolve course identity and immediate goal
2. resolve target folder or explicit file-deferral permission
3. if persistence is requested now, create `study-system/`
4. create minimum files only
5. mark initialization level as partial in `COURSE_CONFIG.json` and `STATUS.md`
6. create one focused request/session surface if doc-first flow is being used
7. execute exactly one grounded teaching/review/exam task
8. recommend full init or sync later

## Required Metadata for Template Filling

Before rendering templates, capture these normalized values whenever available:
- `DATE`
- `TIMESTAMP`
- `COURSE_NAME`
- `ACADEMIC_TERM`
- `WORKSPACE_MODE`
- `INTERACTION_MODE`
- `WORKSPACE_ROOT_OR_NULL`
- `COURSE_FOLDER`
- `STUDY_SYSTEM_FOLDER`
- `COURSE_ID`
- `COURSE_ALIASES_JSON`
- `PREFERRED_LANGUAGE`
- `REVIEW_INTERVALS_JSON`
- `DOC_SURFACE_ENABLED`
- `FILE_CREATION_DEFERRED`
- `INTENSIVE_MODE`
- `REVIEW_INTERVALS_LABEL`
- `EXAM_DATE_OR_TBD`
- `TARGET_GOAL`
- `FOUNDATION_LEVEL`
- `CURRENT_PHASE`
- `INITIALIZATION_LEVEL` (`full` or `lightweight`)
- `PARTIAL_STATE_NOTE`
- `COURSE_STATUS` (`partial` or `full`)

## Template Variable Strategy

### Fill directly from confirmed facts
Examples:
- `COURSE_NAME`
- `ACADEMIC_TERM`
- `WORKSPACE_MODE`
- `INTERACTION_MODE`
- `COURSE_FOLDER`
- `EXAM_DATE_OR_TBD`
- `PREFERRED_LANGUAGE`
- `REVIEW_INTERVALS_JSON`

### Fill with explicit null/unknown markers when evidence is missing
Examples:
- `INSTRUCTOR_OR_UNKNOWN`
- `WORKSPACE_ROOT_OR_NULL`
- `EXAM_DATE_OR_TBD`
- `TOP_DUE_ITEM` when there is no schedule yet
- `COURSE_ALIASES_JSON` when no aliases have been confirmed yet

Do not leave ambiguous blanks that look like accidental omission.

### Fill with bootstrap-safe placeholders when the file must exist before real evidence is available
Examples:
- `CURRENT_PHASE`: `bootstrap` or `partial-initialization`
- `SELECTION_REASON`: `Not enough confirmed state yet; waiting for first real teaching/review transaction.`
- `DUE_TODAY_SUMMARY`: `No reliable due queue yet.`
- `REVIEW_INTERVALS_LABEL`: `1d / 3d / 7d / 14d / 30d` until a different confirmed policy is chosen

## File-Specific Requirements

### `COURSE_CONFIG.json`
Must record:
- workspace mode
- interaction mode
- target folder
- initialization level
- whether intensive mode is enabled
- whether doc-first surface is enabled
- whether file creation was deferred at any stage

### `STATUS.md`
For bootstrap, it must visibly state:
- that the course is only partially initialized
- what is already known
- what is still missing
- what the next valid command should be

### `PROGRESS.md`
During bootstrap:
- counts may be partial
- must not imply complete course coverage
- should explicitly note whether totals are provisional

### `KNOWLEDGE_REGISTRY.json`
During bootstrap:
- include only confirmed knowledge points or explicit provisional placeholders
- each provisional entry should be tagged in `notes` or a similar field
- do not fabricate chapter counts from intuition

### `SYLLABUS_ASSETS.md`
Always distinguish:
- confirmed assets with paths/links
- promised but missing assets
- extraction risks such as scan/OCR needs
- pre-existing mapping files detected

Never create fake assets to populate this file. Missing materials should stay missing and be recorded as such.

### `DASHBOARD.md`
If created during bootstrap:
- show that the course is in partial state
- link toward `INBOX.md`, `OUTBOX.md`, and the first active session if one exists

### `INBOX.md`
If bootstrap starts from a request:
- preserve that request rather than rewriting history
- append clarification blocks or status changes in place

### `SESSION.template.md` consumers
A session note should only be created once there is a real executed teaching/review/exam/audit transaction.
Do not create fake empty session notes just because scaffolding began.

## Variable Fill Examples

### Example: full init
```yaml
COURSE_NAME: Digital Electronics
ACADEMIC_TERM: 2025-2026-2
WORKSPACE_MODE: obsidian
INTERACTION_MODE: hybrid
COURSE_ID: digital-electronics-2025s2
COURSE_ALIASES_JSON: ["数电", "数字电子技术基础"]
PREFERRED_LANGUAGE: zh-CN
DOC_SURFACE_ENABLED: true
FILE_CREATION_DEFERRED: false
INTENSIVE_MODE: false
REVIEW_INTERVALS_JSON: ["1d", "3d", "7d", "14d", "30d"]
REVIEW_INTERVALS_LABEL: 1d / 3d / 7d / 14d / 30d
COURSE_STATUS: full
COURSE_FOLDER: /Users/cheriwen/Documents/Obsidian/01-Academic/2025-2026-2/Major/Digital Electronics
STUDY_SYSTEM_FOLDER: /Users/cheriwen/Documents/Obsidian/01-Academic/2025-2026-2/Major/Digital Electronics/study-system
CURRENT_PHASE: initialization
INITIALIZATION_LEVEL: full
PARTIAL_STATE_NOTE: none
```

### Example: lightweight bootstrap
```yaml
COURSE_NAME: Signals and Systems
ACADEMIC_TERM: unknown
WORKSPACE_MODE: obsidian
INTERACTION_MODE: chat
COURSE_ID: signals-and-systems-bootstrap
COURSE_ALIASES_JSON: []
PREFERRED_LANGUAGE: zh-CN
DOC_SURFACE_ENABLED: false
FILE_CREATION_DEFERRED: false
INTENSIVE_MODE: false
REVIEW_INTERVALS_JSON: ["1d", "3d", "7d", "14d", "30d"]
REVIEW_INTERVALS_LABEL: 1d / 3d / 7d / 14d / 30d
COURSE_STATUS: partial
COURSE_FOLDER: /vault/.../Signals and Systems
STUDY_SYSTEM_FOLDER: /vault/.../Signals and Systems/study-system
CURRENT_PHASE: partial-initialization
INITIALIZATION_LEVEL: lightweight
PARTIAL_STATE_NOTE: Full archive not built yet; only minimum persistence exists.
```

## Sanity Checks After Scaffolding

- the chosen workspace path is real and matches user intent
- required files for the chosen init level exist
- uppercase naming convention is respected for managed study-system files
- `KNOWLEDGE_REGISTRY.json` parses cleanly
- `COURSE_CONFIG.json` marks `initialization_level` correctly
- near-exam courses (<7 days) set `intensive_mode: true` and use compressed `REVIEW_INTERVALS_JSON` values such as `["4h", "12h", "24h"]`
- bootstrap files explicitly declare provisional state where needed
- no file claims due reviews, weak rankings, or exam focus without evidence

## Upgrade Path: Bootstrap -> Full Init

When more materials arrive later:
1. preserve existing `PROGRESS.md`, `STATUS.md`, and `KNOWLEDGE_REGISTRY.json` history
2. enrich `SYLLABUS_ASSETS.md`
3. replace provisional placeholders with confirmed knowledge points
4. create deferred files such as `KNOWLEDGE_TREE.md` and `EXAM_FOCUS.md`
5. update `COURSE_CONFIG.json` from `lightweight` to `full` only after the real expansion is complete

## Hard Rules

Do not:
- create archive-looking files full of invented content
- fill template variables from assumptions the user never confirmed
- create `KNOWLEDGE_TREE.md` with fake completeness during bootstrap
- populate `EXAM_FOCUS.md` with rankings unsupported by real materials
- mark bootstrap state as full init just because files now exist
- create synthetic textbook chapters, fake lecture notes, or demo materials to make initialization appear grounded

## Bottom Line

Initialization quality is not about creating the most files.
It is about creating the right files with truthful scope and clear upgrade paths.
