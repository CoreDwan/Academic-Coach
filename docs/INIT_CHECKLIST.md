# Init Checklist

Short execution checklist for the first real `academic-coach init` in a fresh course workspace.

Canonical spec:
- `docs/INIT_SCAFFOLDING_SPEC.md` = what gets created and how templates are filled
This file = compact preflight checklist only.

## 1. Confirm intent
- The user is actually asking for `academic-coach init`
- Not `help`, `audit`, a one-off tutoring answer, or Hermes slash-command development

## 2. Confirm workspace target
- `workspace_mode` is known: `obsidian` or `external-markdown`
- target course folder is known
- permission to create the folder/files is clear

## 3. Confirm course basics
- exact course name
- term / semester
- exam date or exam window
- target score or mastery goal
- current foundation level
- study budget

## 4. Confirm materials
- confirmed assets are listed with paths/links
- promised-but-missing assets are separated from confirmed ones
- OCR / scan / image risk is noted if relevant
- pre-existing mapping files were checked for

## 5. Confirm mode decision
- normal mode or near-exam intensive mode
- whether cron should be proposed later
- whether doc-first artifacts are desired now

## 6. Show confirmation summary
Before creating files, reflect back:
- course
- workspace mode
- target folder
- exam timing
- goal
- available materials
- missing materials
- risks / unknowns

If the summary is not approved, do not create files.

## 7. Create only after all preconditions pass
Create files only when:
- intent is `academic-coach init`
- workspace target is unambiguous
- minimum metadata exists
- some usable evidence exists
- summary approval is explicit

## 8. Immediate post-init sanity check
- `study-system/` exists in the correct location
- uppercase naming is respected
- required files exist for the chosen init level
- `KNOWLEDGE_REGISTRY.json` parses cleanly
- provisional state is marked honestly if bootstrap-like gaps remain
- next recommended command is usually `academic-coach audit`

## Stop and ask instead of guessing when
- workspace mode is missing
- target folder is ambiguous
- materials were mentioned but not actually provided
- exam timing is unknown and the user wants a sprint plan
- course folder structure conflicts with the stated workspace choice
