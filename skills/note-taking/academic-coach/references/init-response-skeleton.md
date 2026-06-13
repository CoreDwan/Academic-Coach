# INIT RESPONSE SKELETON

Use this reference when `academic-coach` is invoked in a fresh workspace, a no-state workspace, or an ambiguous new-course context.

## Goals

- recognize user intent without forcing rigid command syntax
- avoid fabricating course state
- choose between full init and lightweight bootstrap explicitly
- confirm teaching/output language before course-mode replies
- keep the first reply structured and reusable

## Trigger Scenarios

Apply this when any of the following is true:
- the user says `academic-coach init` or `/academic-coach init`
- the user invokes a non-`init` academic-coach command in a workspace with no known `study-system/`
- the user uses natural language such as `/academic-coach 帮我复习线性代数`
- the agent cannot verify that an initialized course state already exists

## First-Response Structure

1. Acknowledge the intent.
   - Example: "I can take this course in academic-coach mode."
2. State the current state truthfully.
   - If no state exists, say no initialized `study-system/` or course state has been detected.
   - Do not imply that progress, review queues, weak points, or audit results already exist.
3. Choose the bootstrap path explicitly.
   - Full init: if the user wants a full long-term system now.
   - Lightweight bootstrap: if the user wants immediate teaching/review help before a full archive exists.
4. Ask the minimum clarification questions.
   - Full init: use the full structured questionnaire.
   - Lightweight bootstrap: at least course/subject name, preferred teaching/output language, workspace mode, target folder or file-creation deferral, immediate goal, and available materials.
5. Explain what happens next.
   - Full init: build the course workspace and initialize the study-system files.
   - Lightweight bootstrap: create the minimum state needed and start exactly one teaching/review/exam task.

## Tone Rules

- calm and operator-like
- no fake urgency unless the user brings urgency
- public-facing wording, not a private cram-session tone
- concise, but explicit about state and next steps

## Do Not Do This

- do not jump straight into teaching while pretending a registry already exists
- do not show fake progress headers before state exists
- do not skip language confirmation when it is unknown
- do not silently choose full init when the user clearly wants an immediate lightweight start
- do not silently choose lightweight bootstrap when the user explicitly asked for a full persistent setup
