# Academic Coach

Academic Coach is a reusable academic tutoring protocol for long-term course learning, exam readiness, and persistent study-state management across sessions.

This repository is multilingual by design:
- the protocol can teach in Chinese, English, bilingual Chinese+English, or another user-requested language
- during `academic-coach init`, the agent should explicitly confirm the preferred teaching/output language
- technical terms may remain bilingual when that improves clarity

Current status:
- protocol-first
- pure skill workflow, not a native Hermes slash command
- Hermes repository-tap install supported via `skills/note-taking/academic-coach/`
- Obsidian-default workspace design, with support for a user-chosen external markdown workspace
- explicit `workspace_mode` selection during init (`obsidian` or `external-markdown`)
- mixed-material support for textbooks, PPT/PPTX, PDFs, notes, images, lab reports, homework, and past exams

Core idea:
Academic Coach treats a course like a persistent study system rather than a one-off Q&A session.

Quick install (Hermes):
```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

See `docs/INSTALLATION.md` for manual clone/copy and cross-agent adaptation paths.

Repository layout:
- `SKILL.md` — main protocol definition
- `templates/` — reusable markdown/json templates
- `references/` — operational references such as the init questionnaire and cron prompt patterns
- `docs/` — operator and protocol documentation tracked as part of the public contract

Managed study-system files:
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

Command protocol:
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

Important bootstrap rule:
If the user starts with any non-`init` command or a natural-language `academic-coach` request in a workspace with no known study-system yet, the protocol should enter an implicit bootstrap gate rather than fabricate state.

Lightweight bootstrap:
When the user wants immediate help in a fresh workspace but there is not enough evidence yet for a full archive-quality initialization, the protocol may use lightweight bootstrap.
It should:
- confirm the minimum context first
- avoid inventing a full knowledge tree or exam ranking
- optionally create only minimal persistent files
- allow one immediate teaching/review/exam task
- leave the workspace clearly marked as partially initialized

Design constraints:
- one knowledge point per teaching round
- must wait for user response before moving on
- teaching/output language must be confirmed during init if unknown
- uppercase English filenames for managed study documents
- cron changes require confirmation
- no fake mastery, no fake coverage, no invented evidence

See also:
- `docs/INSTALLATION.md`
- `docs/OPERATOR_GUIDE.md`
- `docs/INIT_CHECKLIST.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/MINIMAL_WORKFLOW.md`
- `docs/AUDIT_SPEC.md`
