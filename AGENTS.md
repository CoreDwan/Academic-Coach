# AGENTS.md

This file is the continuation handoff for future Hermes sessions, subagents, or other coding agents working on `Academic-Coach`.

## Project Identity

- Repo: `CoreDwan/Academic-Coach`
- Primary goal: evolve Academic Coach into a reusable, open-source, multilingual academic tutoring protocol with persistent study-state management.
- Current public repo URL: `https://github.com/CoreDwan/Academic-Coach`
- Current distribution model: GitHub-hosted custom Hermes tap + manual clone/adaptation for other agents.

## What This Project Is

Academic Coach is not a one-shot prompt. It is a protocol package for long-term course learning.

Core behaviors already established:
- initialize a course from mixed materials
- maintain a persistent `study-system/`
- teach one knowledge point at a time
- track mistakes, weak points, review schedule, exam focus
- support `init`, `continue`, `review`, `weak`, `exam`, `audit`, `sync`, etc.
- support both explicit pseudo-commands and natural-language triggers
- support no-state startup through an implicit bootstrap gate
- support lightweight bootstrap before full archival init

## Current Repo Shape

Human-facing source tree:
- `README.md` — primary GitHub homepage README, English by default
- `README.zh-CN.md` — Chinese version
- `SKILL.md` — main protocol definition
- `templates/` — managed file templates
- `references/` — questionnaires and supporting reference docs
- `docs/` — operator/protocol docs
- `LICENSE` — MIT
- `skill.json` — project metadata manifest

Hermes-installable mirror:
- `skills/note-taking/academic-coach/`

Important: when changing protocol content, keep root files and the mirrored Hermes install subtree aligned.

## Key Docs To Read First

Future agents should read these before making non-trivial changes:
1. `README.md`
2. `SKILL.md`
3. `docs/OPERATOR_GUIDE.md`
4. `docs/COMMAND_ROUTING_MATRIX.md`
5. `docs/INIT_RESPONSE_SKELETON.md`
6. `docs/INSTALLATION.md`
7. `references/help-and-commands.md`

## Protocol Rules Already Locked In

Do not casually change these without explicit user approval:
- English is the default public README language; Chinese lives in `README.zh-CN.md`
- teaching/output language must be confirmed during init if unknown
- managed study document filenames use uppercase English
- each teaching round covers exactly one knowledge point
- never fabricate progress, review queues, weak-point history, or audit results
- `cron`-related changes require confirmation
- non-`init` first contact in a no-state workspace must go through the implicit bootstrap gate
- lightweight bootstrap is allowed, but must stay explicitly partial and must not silently become full init
- Academic Coach is currently a pure-skill protocol, not a native Hermes slash command
- Hermes distribution is via custom GitHub tap, not an official Hermes built-in skill

## Current Installation Story

Hermes custom tap:
```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills search academic-coach --source CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
```

Manual Hermes install:
```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
mkdir -p ~/.hermes/skills/note-taking
cp -R Academic-Coach/skills/note-taking/academic-coach ~/.hermes/skills/note-taking/
```

Other agents:
- clone repo
- adapt `SKILL.md` + `templates/` + `references/` + `docs/`

## Important Recently Added Pieces

These were added during the recent build-out and are central to the current protocol:
- `docs/COMMAND_ROUTING_MATRIX.md`
- `docs/INIT_RESPONSE_SKELETON.md`
- `docs/INSTALLATION.md`
- `docs/INIT_CHECKLIST.md`
- `docs/AUDIT_SPEC.md`
- `LICENSE`
- centered README hero with badges and quick navigation
- clarification in README that the tap source is the GitHub repo itself

## Current Git / Status Baseline

At the time this handoff file was created, the latest public commits included:
- `0113e86` — docs: polish readme hero and centered badges
- `987feef` — docs: add github badges and clarify custom tap source
- `555aa08` — docs: default homepage to english and add routing matrix
- `abe730a` — docs: add installation paths and open-source license

If later sessions drift far beyond this, update this section.

## Recommended Next Work

High-value next steps, in roughly recommended order:
1. Add a `STATE_MODEL.md` document explaining the responsibilities and synchronization boundaries of:
   - `KNOWLEDGE_REGISTRY.json`
   - `PROGRESS.md`
   - `STATUS.md`
   - `REVIEW_SCHEDULE.md`
   - `WEAK_POINTS.md`
2. Consider a more showcase-style README section for:
   - core highlights
   - use cases
   - adoption paths
3. Decide whether to normalize future git author identity if the user wants contributors to map differently on GitHub.
4. Consider packaging improvements later:
   - better cross-agent manifests
   - possible well-known endpoint or other discovery model
   - maybe future installer tooling, but only after protocol stabilizes
5. If implementing protocol changes, update both:
   - root docs/source files
   - mirrored `skills/note-taking/academic-coach/` tree

## Editing Guidance For Future Agents

When making changes:
- prefer small, explicit commits
- keep README public-facing and readable; avoid turning it into an internal dump
- do not claim Hermes-official status unless that becomes factually true
- verify wording against actual repo structure and actual Hermes docs
- when changing install or protocol docs, re-check `README.md`, `docs/INSTALLATION.md`, and `docs/OPERATOR_GUIDE.md` together
- if you add new protocol-critical docs, link them from `README.md` and usually from `docs/OPERATOR_GUIDE.md`

## Suggested Verification Routine

Before finalizing future doc/protocol changes:
```bash
git status --short --branch
```
Read back changed files, then if appropriate:
```bash
git add <files>
git commit -m "docs: ..."
git push origin main
```

## If You Are A Fresh Agent With No Conversation Context

Start here:
1. Read `AGENTS.md`
2. Read `README.md`
3. Read `SKILL.md`
4. Read `docs/OPERATOR_GUIDE.md`
5. Read `docs/COMMAND_ROUTING_MATRIX.md`
6. Inspect git status and recent commits
7. Only then continue development

If the user asks for protocol evolution, preserve existing invariants unless they explicitly want a redesign.
