# Academic Coach

[中文说明 / Chinese version](README.zh-CN.md)

Academic Coach is a reusable academic tutoring protocol for long-term course learning, exam readiness, and persistent study-state management across sessions.

This repository is multilingual by design:
- the protocol can teach in Chinese, English, bilingual Chinese+English, or another user-requested language
- during `academic-coach init`, the agent should explicitly confirm the preferred teaching/output language
- technical terms may remain bilingual when that improves clarity

[![Stars](https://img.shields.io/github/stars/CoreDwan/Academic-Coach?style=for-the-badge&logo=github)](https://github.com/CoreDwan/Academic-Coach/stargazers)
[![Forks](https://img.shields.io/github/forks/CoreDwan/Academic-Coach?style=for-the-badge&logo=github)](https://github.com/CoreDwan/Academic-Coach/network/members)
[![Contributors](https://img.shields.io/github/contributors/CoreDwan/Academic-Coach?style=for-the-badge)](https://github.com/CoreDwan/Academic-Coach/graphs/contributors)
[![License](https://img.shields.io/github/license/CoreDwan/Academic-Coach?style=for-the-badge)](LICENSE)
![Last Commit](https://img.shields.io/github/last-commit/CoreDwan/Academic-Coach?style=for-the-badge)

[![Quick Start](https://img.shields.io/badge/%F0%9F%9A%80-Quick%20Start-black?style=for-the-badge)](#quick-install)
[![Protocol](https://img.shields.io/badge/%F0%9F%93%98-Command%20Protocol-black?style=for-the-badge)](#command-protocol)
[![Docs](https://img.shields.io/badge/%F0%9F%93%9A-Key%20Docs-black?style=for-the-badge)](#key-docs)

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
- `templates/` — reusable markdown/json templates
- `references/` — operational references such as the init questionnaire and cron prompt patterns
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

## Command protocol

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

- `docs/INSTALLATION.md`
- `docs/OPERATOR_GUIDE.md`
- `docs/INIT_CHECKLIST.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/COMMAND_ROUTING_MATRIX.md`
- `docs/MINIMAL_WORKFLOW.md`
- `docs/AUDIT_SPEC.md`
- `LICENSE`
