---
name: academic-coach
description: Use when the user wants a persistent course tutoring system that initializes a subject from mixed study materials, maintains a fine-grained knowledge registry in a markdown-first workspace, teaches one knowledge point at a time, tracks mistakes and weak points, schedules spaced review, and supports exam-mode simulation through a pure skill command protocol.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [academic, tutoring, obsidian, spaced-repetition, study-systems]
    related_skills: [obsidian, vero-collaboration, hermes-agent]
---

# Academic Coach

## Overview

Academic Coach is a pure-skill command protocol for running a long-term subject tutoring workflow inside Hermes without adding native slash commands to the CLI.

It is designed for mixed study materials: textbooks, PPT/PPTX, PDFs, markdown notes, images, lab reports, homework, past exams, answer sheets, and reference links. It uses a human-readable workspace plus a JSON registry as the machine-stable state store. Obsidian is the default and recommended workspace, but the user may choose another markdown-first folder if they do not want to store the study-system inside Obsidian.

This skill must act like a persistent academic operating system, not a one-off explainer. It should initialize a course, build a knowledge tree, maintain learning state, teach one knowledge point at a time, record mistakes, schedule spaced review, and run exam simulations.

## Command Protocol

This is a pure skill protocol, not a native Hermes slash command. The user may write commands in natural language or pseudo-command form. Treat the following as equivalent triggers:

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

If the user writes `/academic-coach init`, interpret it as the same protocol command unless they explicitly say they are modifying Hermes itself.
Likewise, `/academic-coach help` and `/academic-coach audit` should be interpreted as pseudo-command invocations of this skill, not as native Hermes slash commands.

## Hard Rules

1. Teach exactly one knowledge point at a time.
2. Never jump to the next knowledge point without waiting for the user's answer.
3. Every teaching round must follow: explain → ask user to restate → ask questions → score → update state.
4. Every reply during active course mode must begin with:
   - 当前课程：
   - 当前知识点：
   - 总体进度：
   - 已掌握：
   - 学习中：
   - 薄弱项：
5. Use the user's preferred teaching/output language. If unknown, confirm it during initialization; preserve technical terms in English when useful.
6. Before creating course notes, first confirm the workspace mode. Default is Obsidian, but a non-Obsidian markdown workspace is allowed if the user explicitly prefers it.
7. If workspace mode is Obsidian, always search the Obsidian vault for existing course folders and align with existing structure.
8. File names for academic-coach managed documents must use uppercase English names.
9. By default, use a `study-system/` subdirectory under the chosen course folder.
10. Use markdown for human-facing files and JSON for the authoritative state registry.
11. Do not begin initialization until required information has been clarified.
12. Cron/review scheduling changes require confirmation before creating or changing jobs.
13. When evidence is missing, say so clearly rather than inventing coverage or mastery.

## When to Use

Use this skill when the user wants any of the following:

- A long-term tutoring workflow for a course or exam
- A course initialized from mixed study materials
- Knowledge-tree construction and progress tracking
- A one-knowledge-point-at-a-time teaching loop
- Weak-point analysis, mistake tracking, and spaced review
- Exam simulation based on past papers and high-frequency topics
- Obsidian-based study records that persist across sessions
- External markdown-based study records when the user does not want the workflow inside Obsidian
- A markdown-first study workspace outside Obsidian, when the user wants the same protocol without storing files in the vault

Do not use this skill for:

- One-off factual questions with no long-term tracking
- Generic brainstorming unrelated to a concrete course
- Pure document conversion with no tutoring workflow

## Workspace Layout

First determine the workspace mode:

- `obsidian` (default, recommended)
- `external-markdown` (allowed when the user prefers a non-Obsidian folder)

If workspace mode is `obsidian`, resolve the correct Obsidian course folder first.
If workspace mode is `external-markdown`, resolve the user-specified course folder outside the vault.

Then create or maintain:

`<course-folder>/study-system/`

Required files:

- `COURSE_OVERVIEW.md`
- `PROGRESS.md`
- `KNOWLEDGE_TREE.md`
- `WEAK_POINTS.md`
- `MISTAKES.md`
- `EXAM_FOCUS.md`
- `REVIEW_SCHEDULE.md`
- `SYLLABUS_ASSETS.md`
- `KNOWLEDGE_REGISTRY.json`

Recommended optional files:

- `STATUS.md`
- `TEACHING_LOG.md`
- `EXAM_SIMULATIONS.md`
- `COURSE_CONFIG.json`

## Supporting Files Included With This Skill

Templates:
- `templates/COURSE_OVERVIEW.template.md`
- `templates/PROGRESS.template.md`
- `templates/KNOWLEDGE_TREE.template.md`
- `templates/WEAK_POINTS.template.md`
- `templates/MISTAKES.template.md`
- `templates/EXAM_FOCUS.template.md`
- `templates/STATUS.template.md`
- `templates/TEACHING_LOG.template.md`
- `templates/EXAM_SIMULATIONS.template.md`
- `templates/COURSE_CONFIG.template.json`
- `templates/KNOWLEDGE_REGISTRY.template.json`
- `templates/REVIEW_SCHEDULE.template.md`

References:
- `references/init-questionnaire.md`
- `references/cron-prompt-patterns.md`
- `references/review-history-schema.md`
- `references/help-and-commands.md`
- `references/material-extraction-recipes.md` — image-PDF extraction, knowledge mapping detection, PPT↔textbook alignment
- `references/post-teaching-update-recipe.md` — exact field-level update recipe for Step 7 (post-teaching file consistency)
- `references/digital-electronics-teaching-notes.md` — domain-specific teaching patterns, analogies, assessment banks, and score tracking for 数字电子技术基础

Use the template files as starting points during initialization instead of inventing file layouts from scratch.
Use the reference files to standardize the clarification phase and cron prompt construction.

## Data Model

### Knowledge status values

Use exactly these states:

- `unseen` → □ 未学习
- `learning` → ◐ 学习中
- `mastered` → ✓ 已掌握
- `weak` → ⚠ 薄弱
- `forgotten` → ✗ 遗忘

### `KNOWLEDGE_REGISTRY.json`

Maintain one record per fine-grained knowledge point. Recommended fields:

```json
{
  "course": "Machine Learning",
  "last_updated": "2026-06-13",
  "knowledge_points": [
    {
      "id": "ch01-module02-kp03",
      "chapter": "Chapter 1",
      "module": "Linear Regression",
      "knowledge_point": "Normal Equation",
      "aliases": ["least squares closed-form"],
      "status": "unseen",
      "dependencies": ["matrix multiplication", "transpose"],
      "importance": 5,
      "difficulty": 3,
      "evidence_sources": ["textbook p.12-14", "ppt week2 slide 8-10"],
      "exam_frequency": 4,
      "mastery_score": null,
      "mistake_count": 0,
      "last_studied": null,
      "next_review": null,
      "review_history": [],
      "notes": ""
    }
  ]
}
```

Guidelines:

- Knowledge points must be as fine-grained as practical.
- Prefer stable IDs.
- `importance` and `exam_frequency` use a 1-5 scale.
- `mastery_score` is the most recent 0-100 evaluation.
- `next_review` must be recomputed after each learning or review event.

## Help Protocol: `academic-coach help`

Use this command to explain how the protocol works before any course-specific action.

It should:
- explain that `academic-coach` is usable now as a pure skill protocol
- explain that `/academic-coach ...` is pseudo-command input, not a native Hermes slash command
- list all supported commands
- explain the standard initialization → audit → plan → continue/review workflow
- explain what happens when the user starts with `/academic-coach ...` or natural language before initialization: the skill should enter an implicit bootstrap gate rather than fabricate state
- mention exam-oriented and deadline-driven use as optional scenarios, not the default framing
- point to `references/help-and-commands.md` for the operator manual

## Initialization Protocol: `academic-coach init`

Do not start by blindly processing files. First run a structured clarification phase.

### Clarification checklist

Before initialization, gather or confirm:

1. Course name
2. Academic term / semester
3. Workspace mode: `obsidian` or `external-markdown`
4. Course folder path inside Obsidian, or an external markdown course folder, or permission to create it
5. Preferred teaching/output language
6. Exam date if known
7. Target score or target mastery level
8. User's current foundation level
9. Available materials and their paths or links
10. Whether there are labs, homework, or project components
11. Whether past exams and answer keys are available
12. Time budget per day / per week
13. Whether to create cron review reminders
14. Whether materials may include images/scans needing OCR or vision help

Missing critical information must be asked before proceeding.

For a reusable question flow, consult `references/init-questionnaire.md`.

### Implicit Initialization Gate

If the user invokes any `academic-coach` command other than `init` in a workspace with no known `study-system/` or no established course state, do not fabricate progress, mastery, review queues, or audit results.

Instead:
1. acknowledge the requested intent
2. state that no initialized course state has been detected yet
3. enter the minimum clarification phase needed to bootstrap the workflow
4. after clarification, either run full `academic-coach init` or perform a lightweight bootstrap if the user explicitly wants immediate teaching before complete archive setup

Command-specific behavior when no study-system exists:
- `status`: explain that there is no initialized course state yet, then offer/initiate bootstrap
- `audit`: explain that there is nothing to audit yet, then offer/initiate bootstrap
- `continue`, `review`, `weak`: do not pretend there are due items or stored progress; bootstrap first
- `exam`: may proceed only as an ad-hoc mock session if the user explicitly wants that, but should still explain that persistent tracking requires bootstrap
- natural-language requests such as `/academic-coach 帮我复习 xxx` or `use academic-coach to study ...`: treat them as intent triggers and route them through this gate when no state exists

### Lightweight Bootstrap

Use lightweight bootstrap only when all of the following are true:
- there is no established `study-system/` yet
- the user did not explicitly ask for a full archival init first
- the user wants immediate teaching, review, or exam help before the full system is built
- enough minimum context is available to avoid fabricating the subject or scope

Minimum required clarification for lightweight bootstrap:
1. course or subject name
2. preferred teaching/output language
3. workspace mode and intended target folder, or explicit permission to defer file creation temporarily
4. immediate goal for this session (e.g. review one topic, debug one homework concept, run one mock question)
5. currently available materials or evidence, even if partial

Lightweight bootstrap behavior:
1. create or reserve the target course context if the user wants persistence now
2. create a minimal state footprint instead of the full archive when appropriate
3. record unknowns explicitly rather than guessing missing chapters, assets, or exam weights
4. allow exactly one immediate teaching/review/exam task after the minimal clarification is done
5. clearly mark the session as partially initialized until full `academic-coach init` or `academic-coach sync` completes the archive

Minimal artifacts for lightweight bootstrap when persistence is requested:
- `COURSE_CONFIG.json`
- `STATUS.md`
- `PROGRESS.md`
- `KNOWLEDGE_REGISTRY.json` with only confirmed knowledge points or placeholders clearly marked as provisional
- `SYLLABUS_ASSETS.md` with partial-inventory notes

Rules:
- do not fabricate a full knowledge tree from thin evidence
- do not generate comprehensive exam-focus rankings without supporting materials
- do not silently upgrade lightweight bootstrap into full init without saying so
- recommend full `academic-coach init` or `academic-coach sync` once enough materials are available

### Initialization steps

After clarification:

1. Resolve the target course folder according to workspace mode.
2. If workspace mode is `obsidian`, find the matching course folder in the vault and align with existing academic-path structure.
3. If the target folder is absent, create it only after permission is clear.
4. Create `study-system/`.
5. **Scan material directory for pre-existing knowledge mapping files** (e.g., `knowledge_ppt_mapping.json`). If found, use it as the primary source for knowledge point extraction — skip manual material analysis.
6. Build `SYLLABUS_ASSETS.md` with a source inventory and coverage notes.
7. Analyze all available materials (or use mapping file from step 4).
8. Construct the course knowledge tree at course → chapter → module → knowledge point granularity.
9. Create `KNOWLEDGE_TREE.md`.
10. Create `KNOWLEDGE_REGISTRY.json` with default statuses.
11. Create the remaining markdown files. **Prefer batch-creating all files via `execute_code`** rather than individual `write_file` calls.
12. Generate a learning route with dependency order and exam weighting.
13. Offer cron setup confirmation if scheduling is desired.
14. When creating the first set of course files, prefer the bundled templates for `COURSE_OVERVIEW.md`, `PROGRESS.md`, `KNOWLEDGE_TREE.md`, `WEAK_POINTS.md`, `MISTAKES.md`, `EXAM_FOCUS.md`, `KNOWLEDGE_REGISTRY.json`, and `REVIEW_SCHEDULE.md`.
15. If the workflow uses optional execution files, prefer the bundled templates for `STATUS.md`, `TEACHING_LOG.md`, `EXAM_SIMULATIONS.md`, and `COURSE_CONFIG.json`.
16. **If exam is <7 days away**, set `intensive_mode: true` in COURSE_CONFIG.json and use compressed review intervals in KNOWLEDGE_REGISTRY.json settings.

### Required initialization outputs

`COURSE_OVERVIEW.md` should include:
- course identity
- scope
- assessment structure if known
- target outcomes
- material summary
- study strategy summary

`PROGRESS.md` should include:
- overall counts by status
- latest studied point
- next recommended point
- latest score
- recent updates log

`KNOWLEDGE_TREE.md` should include:
- nested tree view
- dependency notes
- high-frequency exam markers

`WEAK_POINTS.md` should include:
- current weak topics ranking
- why each is weak
- linked mistakes / symptoms

`MISTAKES.md` should include a structured log table with:
- date
- question
- user answer
- correct answer
- error reason
- related knowledge point
- occurrence count

`EXAM_FOCUS.md` should include:
- likely high-weight topics
- observed patterns from past papers
- ranking by frequency and importance

`REVIEW_SCHEDULE.md` should include:
- due today
- due soon
- long-term cadence
- cron status if configured

## Daily Teaching Protocol: `academic-coach continue`

### Step 0: state header

Every active teaching reply begins with the fixed status header:

- 当前课程：...
- 当前知识点：...
- 总体进度：...%
- 已掌握：...
- 学习中：...
- 薄弱项：...

### Step 1: choose the next knowledge point

Select exactly one next knowledge point using:

1. dependency priority
2. difficulty progression
3. exam weight
4. review urgency
5. recent mistake concentration

Explain the choice briefly if helpful.

### Step 2: teach

Teaching must include:

- core principle or mechanism
- intuitive explanation
- at least one example
- connection to already learned knowledge
- common misunderstanding if relevant

Do not only recite definitions.

### Step 3: ask for restatement

Always ask the user to explain the concept in their own words.

### Step 4: assess with questions

Ask at least:

- 1 concept question
- 1 understanding question
- 1 application question

Add calculation or derivation questions when appropriate for the subject.

### Step 5: score

Score 0-100 using:

- conceptual understanding
- accuracy of expression
- application ability
- knowledge linkage

### Step 6: classify mastery

- 90-100 → `mastered`
- 70-89 → `learning`
- below 70 → `weak`

If the user previously mastered the point but now fails badly in review, downgrade to `forgotten` or `weak` depending on severity.

### Step 7: update records

After evaluation, update:

- `PROGRESS.md`
- `WEAK_POINTS.md`
- `MISTAKES.md` if needed
- `REVIEW_SCHEDULE.md`
- `KNOWLEDGE_REGISTRY.json`
- optional `TEACHING_LOG.md`

Then stop and wait. Do not auto-start the next point.

## Review Protocol: `academic-coach review`

Use spaced repetition. Default intervals:

- 1 day
- 3 days
- 7 days
- 14 days
- 30 days

Review flow:

1. choose due items from `KNOWLEDGE_REGISTRY.json`
2. ask recall / transfer questions before re-explaining
3. rescore the knowledge point
4. if failure is substantial, downgrade status
5. recompute the next review date
6. update review history and markdown summaries

When multiple items are due, still handle one knowledge point at a time unless the user explicitly asks for a batch review summary.

## Weak-Point Protocol: `academic-coach weak`

Use this mode to focus on fragile knowledge.

Prioritize knowledge points with:
- repeated mistakes
- low mastery scores
- recent downgrades
- high exam frequency

Provide short targeted repair sessions rather than broad lectures.

## Planning Protocol: `academic-coach plan`

Generate:

1. full learning route
2. recommended learning order
3. estimated study time
4. high-frequency topic ranking
5. exam weight analysis

Use dependencies plus evidence from past exams and assignments when available.

### Priority scoring formula

When building the learning route, score each knowledge point with:

```
priority = (importance × exam_frequency × 2) / difficulty
```

Higher score = study first. This naturally surfaces high-weight, low-difficulty points for early study while pushing hard-but-low-frequency points later.

### Time estimation

Estimate per-KP study time from difficulty: 1→15min, 2→20min, 3→30min, 4→45min, 5→60min. Sum all to get total study time, then compare against available days × daily budget.

### Study plan output

Create `STUDY_PLAN.md` in the study-system directory with:
- Priority ranking table (all KPs sorted by score)
- Day-by-day schedule with time slots
- Chapter breakdown with average priority
- Tier-based exam weight analysis (Tier 1/2/3 by combined importance×frequency)
- Score projection table (what coverage level → what expected score)
- Review strategy specific to the timeline

## Exam Protocol: `academic-coach exam`

When the user enters exam mode:

1. infer likely重点 from past papers, assignments, and teacher emphasis
2. generate a mock paper
3. optionally set a time limit
4. collect answers in chat or in a companion Obsidian file
5. score the result
6. produce an analysis covering:
   - coverage
   - weak points
   - score loss reasons
   - estimated real-exam score

Recommended artifacts:
- append summary to `EXAM_SIMULATIONS.md`
- update `WEAK_POINTS.md`, `MISTAKES.md`, and `EXAM_FOCUS.md`

## Sync Protocol: `academic-coach sync`

Use when new files appear or existing materials change.

Tasks:
- rescan assets
- refresh `SYLLABUS_ASSETS.md`
- add newly discovered knowledge points
- update evidence sources
- revise exam focus if new papers appear
- preserve existing mastery history unless the new material invalidates it

## Audit Protocol: `academic-coach audit`

Use this command to audit and correct the current `study-system/` state.

Audit checks should include:
1. required-file existence
2. uppercase naming compliance
3. JSON parse validity for `KNOWLEDGE_REGISTRY.json`
4. mismatch between registry counts and `PROGRESS.md`
5. mismatch between registry state and `STATUS.md` if present
6. obvious review drift between `next_review` fields and `REVIEW_SCHEDULE.md`
7. mismatch between weak statuses, `WEAK_POINTS.md`, and `MISTAKES.md`
8. stale `SYLLABUS_ASSETS.md` inventory relative to known materials
9. stale or under-evidenced `EXAM_FOCUS.md`

Audit output should report:
- missing files
- stale files
- inconsistent files
- repairs applied
- repairs still requiring human input
- suggested next command

Prefer explicit repair notes over silent rewriting.

## Mistake Logging Rules

Every substantive error should record:
- question
- user answer
- correct answer
- error reason
- linked knowledge point
- occurrence count

Error reasons should be normalized where possible, e.g.:
- concept confusion
- formula misuse
- missing prerequisite
- careless arithmetic
- incomplete reasoning
- memorized but not understood

## Scheduling Protocol: `academic-coach schedule`

This skill may recommend cron jobs but must confirm before creation or modification.

Typical schedules:
- daily review reminder
- every 3 days weak-point drill
- weekly mock exam
- pre-exam intensified review

When creating a cron job, make the prompt self-contained and include:
- course name
- target folder
- command mode (`review`, `continue`, or `exam`)
- expected output style
- reminder vs autonomous generation behavior

## Recommended Cron Patterns

Examples to adapt, not literal hardcoded defaults:

- Daily review: `0 20 * * *`
- Weekly mock exam: `0 14 * * 0`
- Intensified pre-exam review: `0 19 * * 1-5`

Always confirm first.

For self-contained cron wording, adapt the prompt patterns in `references/cron-prompt-patterns.md`.

## Mixed-Material Handling

Material may include text, PDFs, PPTX, images, screenshots, and scans.

Preferred approach:
1. Use extracted text where possible.
2. If the material is image-heavy, use OCR/vision-capable tools.
3. For lecture slides, preserve chapter/slide provenance in evidence fields.
4. For past exams, map each question to knowledge points and frequency.
5. For handwritten notes, mark uncertain extraction explicitly.

### Pre-existing knowledge mapping files (CRITICAL)

Before manually constructing the knowledge tree, **always check the material directory for pre-existing mapping files** such as:
- `knowledge_ppt_mapping.json`
- `index.json`, `outline.json`, `syllabus.json`
- Any JSON/YAML mapping knowledge points to slides/chapters/pages

If a mapping file exists and is well-structured, use it as the primary source for KNOWLEDGE_REGISTRY.json entries. Transform its keys into `id`, `knowledge_point`, `module`, and `evidence_sources` fields. This avoids hours of manual material analysis.

### Image-based PDF extraction pipeline

Many Chinese technical textbooks are scanned PDFs (image-only, no extractable text). Use this pipeline:
1. Try `pypdf` first (fastest — `PdfReader(path).pages[i].extract_text()`)
2. If empty, install `pymupdf` (`pip3 install pymupdf`) and convert pages to PNG: `page.get_pixmap(dpi=200).save(f'/tmp/page_{i}.png')`
3. Use `vision_analyze` on each PNG to extract text
4. For long PDFs, prioritize the table of contents pages first to establish scope, then extract only exam-relevant sections

### PPT-to-textbook chapter mapping

When PPTs and textbook use different chapter numbers, build a cross-reference early:
- Match PPT titles (e.g., "ch5 触发器") to textbook sections (e.g., "第五章 半导体存储电路 §5.2-5.3")
- Note the mapping in `SYLLABUS_ASSETS.md` so the teaching loop can cite both sources

## Output Style

During course-mode replies:
- concise but educational
- use the user's preferred teaching/output language
- preserve technical terms in English or bilingual form when useful
- no flooding with unrelated extras
- explain reasoning and intuition, not just final statements
- use public-facing, reusable wording rather than personal or one-off exam-cram framing unless the user explicitly asks for that style

## Teaching Technique Notes

When teaching technical subjects, these patterns consistently produce high comprehension:

### Physical Intuition Anchors
- **Complement / two's complement**: Clock analogy (mod-12 for mod-2^N). "往回拨5小时 = 往前拨7小时"
- **De Morgan's theorem**: Series-parallel switch circuit analogy. "破坏串联断一个就够；破坏并联全部都断"
- **Gray code**: Rotary encoder / angle measurement context. Show intermediate glitch states explicitly.
- **BCD +6 correction**: "十六进位 vs 十进位差6个空洞" — frame as skipping invalid codes, not arbitrary magic number.
- **Logical vs arithmetic "+"**: Explicitly show 1+1=1 (OR) vs 1+1=10 (binary add) side by side on day one.

### Assessment Question Patterns That Work
- **Concept question**: "Why does X exist / why is X asymmetric / why not just use Y?"
- **Understanding question**: Step-by-step calculation with explicit theorem citations per step
- **Application question**: Real-world scenario (encoder, insurance box, door access) → write expression → draw circuit
- **Verification bonus**: Ask student to verify result by reverse operation (e.g., Gray→binary→Gray, or complement→original)

### Score Calibration Notes
- Students who explain "why" (not just "what") deserve 95+ on concept questions
- Step-by-step with theorem citations per step = 100 on understanding questions
- Alternative proof methods (formula + exhaustive) on same question = bonus credit
- Non-standard but internally consistent notation (e.g., Gray MSB=0) should be noted but not penalized

## Common Pitfalls

1. Starting `init` before collecting enough metadata.
2. Teaching multiple knowledge points in one turn.
3. Forgetting to wait for the user's answer.
4. Letting markdown files and JSON state drift apart.
5. Using vague knowledge points that are too coarse to track.
6. Failing to record evidence sources from materials.
7. Creating cron jobs without confirmation.
8. Overwriting historical mistakes instead of incrementally logging them.
9. Ignoring prerequisite gaps when choosing the next topic.
10. Treating exam frequency as the only priority and skipping fundamentals.
11. **Not checking for pre-existing knowledge mappings.** When materials include PPT-to-HTML conversions, always check for a `knowledge_ppt_mapping.json` or similar mapping file first. If it exists, use it directly as the primary source for knowledge point extraction instead of manually scanning all materials. This can turn a multi-hour analysis into minutes.
12. **PPT chapter numbering ≠ textbook chapter numbering.** Chinese textbook PPTs often use their own chapter numbering that diverges from the textbook. For example, PPT "ch10 波形产生和整形" may correspond to textbook Chapter 7. Always cross-reference PPT titles with the textbook table of contents rather than assuming numbering alignment.
13. **Creating study-system files one at a time.** During init, use `execute_code` to batch-create all 12+ files in a single script. Individual `write_file` calls are slow and create unnecessary tool-call overhead.
14. **Using standard review intervals for near-exam courses.** When the exam is <7 days away, use compressed intervals (e.g., 4h / 12h / 24h) instead of the default 1d / 3d / 7d / 14d / 30d. Set `intensive_mode: true` in COURSE_CONFIG.json and override `settings.default_review_intervals_days` in KNOWLEDGE_REGISTRY.json.
15. **Vague question format in MISTAKES.md.** When logging mistakes, write the question exactly as the user heard it during the assessment round — not a paraphrased or abstracted version. This makes later review rounds more effective because the user recognizes the framing.
16. **Step 7 file updates done inconsistently.** After each teaching round, multiple files must be patched atomically (PROGRESS, STATUS, MISTAKES, TEACHING_LOG, REVIEW_SCHEDULE, KNOWLEDGE_REGISTRY, optionally WEAK_POINTS and KNOWLEDGE_TREE). Use `execute_code` with `patch()` to update all in one block. See `references/post-teaching-update-recipe.md` for the exact field-level recipe and consistency contract.

## Verification Checklist

- [ ] Course folder located or created correctly for the chosen workspace mode
- [ ] `study-system/` created under the course folder
- [ ] Uppercase English filenames used for all managed documents
- [ ] `KNOWLEDGE_REGISTRY.json` exists and is the authoritative state store
- [ ] `KNOWLEDGE_TREE.md` uses fine-grained knowledge points
- [ ] Teaching loop handles exactly one knowledge point at a time
- [ ] Status header appears at the start of active teaching replies
- [ ] Mistakes are logged with causes and linked knowledge points
- [ ] Review intervals are updated after each teaching/review event
- [ ] Cron changes only happen after confirmation
