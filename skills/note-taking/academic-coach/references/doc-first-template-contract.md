# Doc-First Template Contract

Use this reference when Academic Coach is operating through the document-first / Obsidian-first surface.

## Purpose

These templates are not decorative extras. They define the minimum collaboration surface that lets the same Academic Coach protocol run outside a live terminal turn while keeping state legible to both the user and the agent.

## Canonical doc-first template set

### Workspace control layer
- `templates/DASHBOARD.template.md`
- `templates/INBOX.template.md`
- `templates/OUTBOX.template.md`

### Execution / knowledge layer
- `templates/SESSION.template.md`
- `templates/TOPIC.template.md`

## Responsibilities

### `DASHBOARD.md`
Human control panel.
Should show:
- course summary
- progress snapshot
- due-today summary
- weak-point focus
- active request
- latest session link
- quick actions

### `INBOX.md`
Request intake queue.
Use for:
- new requests
- clarification blocks
- queued review prompts
- cron-generated reminders

Keep normalized request fields visible in the template so future sessions can reconstruct state without guessing.

### `OUTBOX.md`
Short navigational summary.
Use for:
- latest result summary
- due / reminder summary
- recent transaction pointers
- next recommended action

Do not turn `OUTBOX.md` into a second session log. Full detail belongs in session notes and study-system files.

### `SESSION.template.md`
One transaction = one teaching/review/exam/audit note.
Must preserve the same status-header contract as chat mode:
- 当前课程：
- 当前知识点：
- 总体进度：
- 已掌握：
- 学习中：
- 薄弱项：

The template should also preserve the pedagogical sequence:
- explanation
- user restatement prompt
- assessment questions
- evaluation
- score / mastery decision
- state updates applied

### `TOPIC.template.md`
Durable per-knowledge-point note.
Should capture:
- canonical summary
- intuition / mechanism
- prerequisites
- common mistakes
- examples / applications
- source evidence
- linked sessions
- mastery snapshot

## When to create these files

### Full init
During a full `academic-coach init`, create or prepare the doc-first layer when the user wants Obsidian-first or markdown-first collaboration rather than chat-only operation.

Recommended set:
- `DASHBOARD.md`
- `INBOX.md`
- `OUTBOX.md`
- `SESSIONS/`
- `TOPICS/`

### Lightweight bootstrap
Do not force the entire doc-first collaboration layer if the user only wants immediate teaching and has not committed to the workspace shape yet.

Minimum acceptable behavior:
- confirm workspace intent first
- if persistence is requested, create only the minimal files needed for grounded continuity
- explicitly mark missing doc-first artifacts as deferred rather than silently pretending they exist

## Agent discipline

1. Keep study-system files authoritative for course state.
2. Treat dashboard/inbox/outbox/session/topic files as the collaboration surface, not an alternate source of truth.
3. Prefer explicit links between requests, sessions, topics, and study-system updates.
4. When adding doc-first support, update both the template inventory and the skill instructions so future agents know the files are first-class.
5. If the user asks for a reusable template-style skill rather than a one-off workflow, prioritize bundled templates and references over burying structure only in prose.
