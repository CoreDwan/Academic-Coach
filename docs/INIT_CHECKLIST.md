# Init Checklist

This checklist is for the first real execution of `academic-coach init` in a fresh study session.

## Goal

Prevent bad initialization caused by wrong workspace selection, unclear target folder, partial materials, or premature file creation.

## Rule Zero

Do not create any study-system files until the clarification summary has been shown back to the user and confirmed.

## Phase 1: Confirm Command Intent

Before doing anything else, confirm that the user is actually asking for:
- `academic-coach init`

Not:
- `academic-coach help`
- `academic-coach audit`
- a one-off tutoring answer
- Hermes native slash-command development

## Phase 2: Confirm Workspace Decision

The init flow must explicitly capture:
- workspace mode: `obsidian` or `external-markdown`
- target course folder
- whether folder creation is allowed if missing

Checks:
- If `obsidian`, locate the course inside the vault and align with existing note structure.
- If `external-markdown`, use the user-specified markdown-first folder and do not assume any Obsidian path rules.
- Do not silently default to Obsidian if the user asked for something else.

## Phase 3: Confirm Course Basics

Required:
- exact course name
- academic term / semester
- exam date or approximate exam window
- target score / mastery goal
- current foundation level
- daily / weekly study budget

Do not proceed if the time horizon and goal are too vague to drive planning.

## Phase 4: Confirm Materials

Gather paths or links for whatever currently exists:
- textbook
- PPT / slides
- notes
- homework
- labs / reports
- past exams
- answer keys / rubrics
- references

Checks:
- separate confirmed materials from promised-but-missing materials
- identify whether image-only PDFs / screenshots / handwriting may need OCR or vision
- check for pre-existing mapping files such as `knowledge_ppt_mapping.json`, `outline.json`, or similar structured indexes

## Phase 5: Confirm Execution Mode

Before file creation, decide whether init should run in:
- normal mode
- intensive near-exam mode

Use intensive mode when the exam is very near and review intervals should be compressed.

## Phase 6: Confirmation Summary

Before creating files, show a summary containing:
- course name
- term
- workspace mode
- target folder
- exam timing
- target goal
- foundation level
- available materials
- missing materials
- OCR / vision risk
- whether cron should be proposed later

If the user corrects anything, revise the summary first.

## Phase 7: File-Creation Preconditions

Only create files when all of the following are true:
- command intent is `academic-coach init`
- workspace mode is known
- target folder is known
- folder creation permission is clear
- minimum course metadata is known
- at least some usable materials exist
- confirmation summary has been approved

## Phase 8: Post-Creation Sanity Check

Immediately after initialization, verify:
- `study-system/` exists in the correct location
- uppercase filenames were used
- required files exist
- `KNOWLEDGE_REGISTRY.json` is valid JSON
- `COURSE_CONFIG.json` records workspace mode correctly if present
- the generated knowledge tree is not obviously empty or too coarse
- `academic-coach audit` can be the next recommended command

## Fast Failure Conditions

Stop and ask instead of guessing when:
- workspace mode is missing
- target folder is ambiguous
- materials were referenced but not actually provided
- exam timing is unknown and the user wants a sprint plan
- the user’s course folder structure conflicts with their stated workspace choice

## Recommended First Real Flow

1. `academic-coach help`
2. `academic-coach init`
3. clarification summary
4. file creation
5. `academic-coach audit`
6. `academic-coach plan`
