# Minimal Workflow for Final Exam Sprint

This document is the practical path for using Academic Coach before you have a full clean archive of course materials.

## Goal

Serve final-exam preparation first.

Do not wait for the perfect dataset. Start with partial materials, establish the study-system, audit it, and iterate.

## Minimum Inputs

You do not need every asset on day one.

Good enough to start:
- course name
- academic term
- workspace mode: Obsidian or external markdown folder
- target course folder
- exam date or approximate exam window
- target score / goal
- at least some of the following:
  - one textbook or chapter list
  - partial PPTs
  - class notes
  - homework sets
  - one past paper or topic memory

## Recommended Command Sequence

### Step 1: help
Use:
`academic-coach help`

Purpose:
- confirm the protocol
- see the command set
- understand the difference between pseudo-slash use and real Hermes slash commands

### Step 2: init
Use:
`academic-coach init`

Before running the real initialization pass, follow `docs/INIT_CHECKLIST.md`.

Purpose:
- create the course `study-system/`
- establish required markdown files
- create `KNOWLEDGE_REGISTRY.json`
- record known materials in `SYLLABUS_ASSETS.md`

Important:
Even with partial materials, init should still proceed once the key basics are clarified and the confirmation summary is approved.
Unknown coverage must be marked explicitly rather than guessed.

### Step 3: audit
Use:
`academic-coach audit`

Purpose:
- verify the generated study-system is internally consistent
- catch missing files, stale counts, drift, or weak summaries
- repair the working state before heavy study begins

### Step 4: plan
Use:
`academic-coach plan`

Purpose:
- rank high-value topics for finals
- identify dependencies
- generate a practical learning order under time pressure

In sprint mode, the plan should optimize for:
- exam weight
- prerequisite bottlenecks
- repeated mistake risk
- limited time budget

### Step 5: continue
Use:
`academic-coach continue`

Purpose:
- start actual one-knowledge-point teaching rounds
- build understanding and collect mastery signals quickly

### Step 6: review
Use:
`academic-coach review`

Purpose:
- pull due items back into short-term memory
- downgrade overestimated mastery when needed

### Step 7: exam
Use:
`academic-coach exam`

Purpose:
- pressure-test what is really retained
- expose score-loss sources before the real final

## Operating Principle Under Incomplete Materials

When materials are incomplete:
- do not fabricate knowledge-tree coverage
- do not fake exam-focus confidence
- do not mark mastery without evidence
- do keep the workflow moving

The correct behavior is:
- initialize what is known
- label uncertainty clearly
- keep syncing new materials later with `academic-coach sync`
- re-run `academic-coach audit` after meaningful updates

## Suggested Near-Term Loop

A realistic finals loop can be:
1. morning or afternoon: `academic-coach continue`
2. evening: `academic-coach review`
3. every few days: `academic-coach audit`
4. weekly or pre-exam: `academic-coach exam`

## What Success Looks Like

Even before you own every course asset, success means:
- a working `study-system/` exists
- the knowledge registry is alive and being updated
- weak points are visible
- mistakes are being logged
- review pressure is scheduled
- exam preparation is becoming evidence-driven instead of vague
