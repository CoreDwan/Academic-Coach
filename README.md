<div align="center">

# Academic Coach

<p><a href="README.zh-CN.md">中文说明 / Chinese version</a></p>

<p><strong>Persistent academic tutoring protocol for Hermes and beyond.</strong></p>

<p>Turn a course into a maintained study system with structured teaching, review loops, mistake tracking, and exam preparation.</p>

<p>
  <a href="https://github.com/CoreDwan/Academic-Coach/stargazers"><img src="https://img.shields.io/github/stars/CoreDwan/Academic-Coach?style=for-the-badge&logo=github" alt="Stars"></a>
  <a href="https://github.com/CoreDwan/Academic-Coach/network/members"><img src="https://img.shields.io/github/forks/CoreDwan/Academic-Coach?style=for-the-badge&logo=github" alt="Forks"></a>
  <a href="https://github.com/CoreDwan/Academic-Coach/graphs/contributors"><img src="https://img.shields.io/github/contributors/CoreDwan/Academic-Coach?style=for-the-badge" alt="Contributors"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/CoreDwan/Academic-Coach?style=for-the-badge" alt="License"></a>
  <img src="https://img.shields.io/github/last-commit/CoreDwan/Academic-Coach?style=for-the-badge" alt="Last Commit">
</p>

<p>
  <a href="#quick-install"><img src="https://img.shields.io/badge/%F0%9F%9A%80-Quick%20Start-black?style=for-the-badge" alt="Quick Start"></a>
  <a href="#what-it-is"><img src="https://img.shields.io/badge/%F0%9F%A7%AD-Overview-black?style=for-the-badge" alt="Overview"></a>
  <a href="#command-protocol"><img src="https://img.shields.io/badge/%F0%9F%93%98-Command%20Protocol-black?style=for-the-badge" alt="Command Protocol"></a>
  <a href="#key-docs"><img src="https://img.shields.io/badge/%F0%9F%93%9A-Key%20Docs-black?style=for-the-badge" alt="Key Docs"></a>
</p>

</div>

Academic Coach is a reusable academic tutoring protocol for long-term course learning, exam readiness, and persistent study-state management across sessions.

This repository is multilingual by design:
- the protocol can teach in Chinese, English, bilingual Chinese+English, or another user-requested language
- during `academic-coach init`, the agent should explicitly confirm the preferred teaching/output language
- technical terms may remain bilingual when that improves clarity

## What it is

Academic Coach treats a course like a persistent study system rather than a one-off Q&A session.

It is designed for mixed study materials such as:
- textbooks
- PPT / PPTX slides
- PDFs
- markdown notes
- images
- lab reports
- homework
- past exams
- reference links

Current status:
- protocol-first
- pure skill workflow, not a native Hermes slash command
- Hermes custom-tap install supported via this GitHub repository
- Obsidian-default workspace design, with support for a user-chosen external markdown workspace
- explicit `workspace_mode` selection during init (`obsidian` or `external-markdown`)
- doc-first / Obsidian-first collaboration surface documented for the next evolution stage

## Quick install

### Hermes repository tap (recommended)

```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills search academic-coach --source CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

### Hermes manual clone/copy

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
mkdir -p ~/.hermes/skills/note-taking
cp -R Academic-Coach/skills/note-taking/academic-coach ~/.hermes/skills/note-taking/
```

### Other agents

Clone the repository and adapt the protocol manually:

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
cd Academic-Coach
```

Start with:
- `SKILL.md`
- `references/`
- `templates/`
- `docs/`

## How Hermes tap works

This repo has not been uploaded to Hermes official built-in skills.

The tap source is this GitHub repository itself:
- repo source: `CoreDwan/Academic-Coach`
- installable skill path inside the repo: `skills/note-taking/academic-coach/`

What Hermes does:
1. `hermes skills tap add CoreDwan/Academic-Coach` registers the GitHub repo as a custom skill source
2. Hermes scans the repo for installable skill layouts
3. `hermes skills install CoreDwan/Academic-Coach/academic-coach` installs the skill from that repo

In other words:
- official/bundled skill: shipped by Hermes itself
- skills hub publish: pushed through the Hermes publish flow
- tap: your own GitHub repo used as a custom skill source

Academic Coach currently uses the third model: a custom GitHub tap, not an official Hermes-bundled skill.

## Repository layout

Source tree:
- `SKILL.md` — main protocol definition
- `templates/` — reusable markdown/json templates, including doc-first workspace artifacts such as dashboard/inbox/session/topic notes
- `references/` — operational references such as the init questionnaire, routing examples, scaffolding rules, and cron prompt patterns
- `docs/` — operator and protocol documentation tracked as part of the public contract

Installable Hermes layout:
- `skills/note-taking/academic-coach/`

## Managed study-system files

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

Doc-first collaboration artifacts:
- `DASHBOARD.md`
- `INBOX.md`
- `OUTBOX.md`
- `SESSIONS/`
- `TOPICS/`

## Command protocol

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

These may also appear as pseudo-commands like `/academic-coach review` or as natural-language requests such as `help me review calculus with academic-coach`.

## Bootstrap rules

### Implicit bootstrap gate

If the user starts with any non-`init` command or a natural-language `academic-coach` request in a workspace with no known study-system yet, the protocol should enter an implicit bootstrap gate rather than fabricate state.

That means:
1. recognize the requested intent
2. state that no initialized course state has been detected yet
3. ask the minimum clarification questions needed
4. choose either full `init` or lightweight bootstrap

### Lightweight bootstrap

When the user wants immediate help in a fresh workspace but there is not enough evidence yet for a full archive-quality initialization, the protocol may use lightweight bootstrap.

It should:
- confirm the minimum context first
- avoid inventing a full knowledge tree or exam ranking
- optionally create only minimal persistent files
- allow one immediate teaching/review/exam task
- leave the workspace clearly marked as partially initialized

## Design constraints

- one knowledge point per teaching round
- must wait for user response before moving on
- teaching/output language must be confirmed during init if unknown
- uppercase English filenames for managed study documents
- cron changes require confirmation
- no fake mastery, no fake coverage, no invented evidence

## Key docs

Core protocol docs:
- `docs/COMMAND_AND_TARGET_MODEL.md`
- `docs/COMMAND_ROUTING_MATRIX.md`
- `docs/INIT_SCAFFOLDING_SPEC.md`
- `docs/DOC_INTERACTION_PROTOCOL.md`

Operator and supporting docs:
- `docs/OPERATOR_GUIDE.md`
- `docs/REQUEST_ROUTING_EXAMPLES.md`
- `docs/INIT_CHECKLIST.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/AUDIT_SPEC.md`
- `docs/REUSE_MAP.md`
- `docs/USER_JOURNEY.md`
- `docs/INSTALLATION.md`
- `LICENSE`
