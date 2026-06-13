# Academic Coach Init Questionnaire

Use this as the default clarification script before running `academic-coach init`.

## Goal
Collect enough structured information to avoid starting initialization with ambiguous scope, missing assets, or the wrong workspace location.

## Mandatory Questions

1. What is the exact course name?
2. Which academic term / semester is this for?
3. Which workspace mode do you want for this course?
   - `obsidian` (default, recommended)
   - `external-markdown` (a non-Obsidian markdown-first folder)
4. Which interaction mode should this course use?
   - `chat` (terminal/chat-first)
   - `doc` (document-first / Obsidian-first)
   - `hybrid` (chat plus durable doc write-back)
5. What is your preferred teaching/output language?
   - Examples: Chinese, English, bilingual Chinese+English, or another language
6. What is the target course folder?
   - If workspace mode is `obsidian`: where is the existing course folder in Obsidian? If it does not exist, may I create it?
   - If workspace mode is `external-markdown`: what folder should hold the study-system? If it does not exist, may I create it?
7. What is the exam date or approximate exam window?
8. What is your target score, rank, or mastery goal?
9. What is your current foundation level for this course?
10. What materials do you already have? Please provide paths or links for textbooks, PPTs, notes, homework, labs, past papers, and reference material.
11. Are there any image-only scans, screenshots, or handwritten notes that may need OCR/vision?
12. Does this course contain labs, projects, or reports that affect grading?
13. Do you have past exams, answer keys, grading rubrics, or teacher emphasis notes?
14. How much time can you invest per day and per week?
15. Do you want me to prepare cron-based review reminders after initialization?

## Recommended Follow-up Questions

Ask these when helpful, but not necessarily all at once:

- Do you want the teaching language and document commentary to be fully localized, or should key technical terms stay bilingual?
- Which chapters already feel familiar?
- Which topics currently feel hardest?
- Is the teacher more proof-heavy, calculation-heavy, or concept-heavy?
- Do you want the learning route optimized for passing, high score, or full mastery?
- Should the system prioritize exam performance, assignment performance, or both?
- If workspace mode is `obsidian`, are there existing notes in your vault whose format I should mirror?
- If workspace mode is `external-markdown`, do you want the study-system to stay standalone or coexist with a repo/project structure?

## Stop Conditions

Do not proceed to initialization if any of these are unresolved:

- Course identity is unclear
- Workspace mode is unknown
- Teaching/output language preference is unknown
- Target folder is unknown and user has not approved creation
- Materials are promised later but not yet available in any usable form
- Time horizon and goal are too vague to plan around

## Output of Clarification Phase

Before creating files, summarize back to the user:

- course name
- term
- workspace mode
- interaction mode
- teaching/output language
- target folder
- available materials
- missing materials
- exam timing
- target goal
- weekly study budget
- whether cron setup should be proposed

Only begin file creation after the user confirms or corrects the summary.
