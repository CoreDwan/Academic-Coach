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
  <a href="#usage"><img src="https://img.shields.io/badge/%F0%9F%93%98-Usage-black?style=for-the-badge" alt="Usage"></a>
  <a href="#notes"><img src="https://img.shields.io/badge/%F0%9F%A7%B1-Notes-black?style=for-the-badge" alt="Notes"></a>
</p>

</div>

Academic Coach is a reusable academic tutoring protocol for long-term course learning, exam readiness, and persistent study-state management across sessions.

## What it is

Academic Coach treats a course like a maintained study system rather than a one-off Q&A session.

It currently supports:
- Hermes skill usage through this repository as a custom tap
- mixed materials such as textbooks, PPT/PPTX, PDFs, notes, images, lab reports, homework, and past exams
- multi-session progress tracking
- one-knowledge-point-at-a-time teaching rounds
- mistake tracking, spaced review, and exam-mode workflows
- Obsidian-first or external-markdown workspaces
- chat, doc, and hybrid interaction modes

Current reality:
- usable now
- protocol-first
- pure skill workflow, not a native Hermes slash command
- best with Hermes, adaptable to other agent systems manually

## Quick install

### Hermes repository tap (recommended)

```bash
hermes skills tap add CoreDwan/Academic-Coach
hermes skills install CoreDwan/Academic-Coach/academic-coach
hermes skills list
```

### Hermes manual clone/copy

```bash
git clone https://github.com/CoreDwan/Academic-Coach.git
mkdir -p ~/.hermes/skills/note-taking
cp -R Academic-Coach/skills/note-taking/academic-coach ~/.hermes/skills/note-taking/
```

For manual adaptation or non-Hermes usage, clone the repo and start from `SKILL.md`.

## Usage

### 1. Load the skill
Start Hermes, then load or invoke `academic-coach` in natural language or pseudo-command form.

Useful entry patterns:
- start Hermes normally, then type `/skill academic-coach`
- or start with the skill preloaded: `hermes -s academic-coach`

Typical forms:
- `academic-coach help`
- `academic-coach init`
- `academic-coach continue`
- `/academic-coach review`
- `use academic-coach to help me study digital electronics`

### 2. Initialize a course
Use `academic-coach init` when you want the skill to build a persistent study system for a subject.

The init flow will confirm key facts before creating files, including:
- course/subject name
- preferred teaching language
- workspace mode (`obsidian` or `external-markdown`)
- interaction mode (`chat`, `doc`, or `hybrid`)
- target folder
- available materials
- exam timing and current goal

### 3. Run daily study rounds
After init, the main commands are:
- `academic-coach status` — show current progress and next action
- `academic-coach continue` — teach exactly one knowledge point
- `academic-coach review` — run one spaced-review round
- `academic-coach weak` — focus on fragile topics
- `academic-coach exam` — enter mock-exam mode
- `academic-coach audit` — check whether the study system drifted

### 4. Use bootstrap when full init is too early
If you ask for `continue`, `review`, or another study action before a course has been initialized, Academic Coach should not fake state.

Instead, it should enter bootstrap mode:
- ask the minimum clarification questions
- decide between full init and lightweight bootstrap
- optionally create a partial study system
- let you start one real task immediately

## Notes

- This repo is a custom Hermes tap source, not an official built-in Hermes skill.
- The skill is designed to teach in Chinese, English, bilingual Chinese+English, or another requested language.
- Managed study documents use uppercase English filenames.
- Cron-based reminders are supported, but schedule changes should still be confirmed before creation.
- The protocol is optimized for persistent course coaching, not casual one-shot Q&A.

## Further reading

If you want to inspect the protocol internals, start with:
- `SKILL.md`
- `docs/COMMAND_AND_TARGET_MODEL.md`
- `docs/INIT_SCAFFOLDING_SPEC.md`
- `docs/DOC_INTERACTION_PROTOCOL.md`
- `docs/INSTALLATION.md`
