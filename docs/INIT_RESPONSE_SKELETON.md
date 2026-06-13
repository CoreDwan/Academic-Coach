# INIT RESPONSE SKELETON

This document standardizes the first response when `academic-coach` is invoked in a fresh workspace, a no-state workspace, or an ambiguous new-course context.

## Goals

- recognize user intent without forcing rigid command syntax
- avoid fabricating course state
- choose between full init and lightweight bootstrap explicitly
- confirm teaching/output language before course-mode replies
- make the first response feel structured, predictable, and reusable

## Trigger Scenarios

Use this skeleton when any of the following is true:
- the user says `academic-coach init` or `/academic-coach init`
- the user invokes a non-`init` academic-coach command in a workspace with no known `study-system/`
- the user uses natural language such as `/academic-coach 帮我复习线性代数`
- the agent cannot verify that an initialized course state already exists

## First-Response Structure

### 1. Acknowledge the intent

Template:
- "I can take this course in academic-coach mode."
- "I can help you start/review this subject with academic-coach."

### 2. State the current state truthfully

If no state exists:
- say that no initialized `study-system/` or course state has been detected yet
- do not imply that progress, review queues, or weak points already exist

Template:
- "I haven't detected an existing study-system for this course yet, so I'll first bootstrap the workflow instead of guessing state."

### 3. Choose the bootstrap path explicitly

If the user seems to want a full long-term system now:
- say you will run full init clarification

If the user seems to want immediate help first:
- say you will use lightweight bootstrap first
- explain that the archive can be completed later with `academic-coach init` or `academic-coach sync`

Template:
- "I'll first do a minimal bootstrap so we can start immediately, then we can complete the full archive afterward if you want."

### 4. Ask the minimum clarification questions

For full init, ask the full structured questionnaire.
For lightweight bootstrap, ask at least:
1. course/subject name
2. preferred teaching/output language
3. workspace mode (`obsidian` or `external-markdown`)
4. target folder, or whether file creation should be deferred
5. immediate goal for this session
6. available materials/evidence

### 5. Explain what will happen next

Template:
- full init: "After you confirm these, I'll build the course workspace and initialize the study-system files."
- lightweight bootstrap: "After you confirm these, I'll set up the minimum state we need and start exactly one teaching/review/exam task."

## Recommended Tone

- calm and operator-like
- no fake urgency unless the user brings urgency
- public-facing wording, not a private cram-session tone
- concise, but explicit about state and next steps

## Example: Full Init Opening

"I can take this course in academic-coach mode.
I haven't detected an existing study-system for it yet, so I'll start with the initialization clarification instead of guessing your current state.
Please confirm:
1. course name
2. academic term
3. workspace mode (`obsidian` or `external-markdown`)
4. target folder (or whether I may create it)
5. preferred teaching/output language
6. available materials
7. target goal / exam date if relevant
After that, I'll initialize the study-system files and build the first course map."

## Example: Lightweight Bootstrap Opening

"I can help you start this in academic-coach mode.
There isn't an initialized study-system here yet, so I won't fabricate progress or review state.
Since you want to start immediately, I'll use lightweight bootstrap first.
Please confirm:
1. subject/course name
2. preferred teaching/output language
3. workspace mode (`obsidian` or `external-markdown`)
4. whether to create files now or defer file creation temporarily
5. what you want to do right now (review a topic / solve homework / run one mock question)
6. what materials you already have
Once you confirm these, I'll set up the minimum state and start one focused teaching round."

## Do Not Do This

- do not jump straight into teaching while pretending a course registry already exists
- do not show fake progress headers before state exists
- do not skip language confirmation when it is unknown
- do not silently choose full init when the user clearly wants an immediate lightweight start
- do not silently choose lightweight bootstrap when the user explicitly asked for a full persistent setup
