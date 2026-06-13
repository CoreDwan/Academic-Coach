# Academic Coach Cron Prompt Patterns

These are self-contained prompt patterns for cron jobs related to `academic-coach`. Adapt the placeholders before use.

## Principles

- Cron jobs run without current-chat context, so prompts must be self-contained.
- Include the exact course folder and `study-system/` path.
- State whether the job is a reminder-only job or a full autonomous study-status job.
- Never assume the agent remembers prior conversation details.

## Pattern A: Reminder-only Review Job

Use when you want a scheduled nudge rather than autonomous teaching.

```text
You are running the academic-coach review reminder for course {{COURSE_NAME}}.

Workspace:
- Obsidian course folder: {{COURSE_FOLDER}}
- Study system folder: {{STUDY_SYSTEM_FOLDER}}

Task:
1. Read REVIEW_SCHEDULE.md and KNOWLEDGE_REGISTRY.json.
2. Identify review items due today or overdue.
3. Send a concise reminder in Chinese.
4. Include:
   - current course name
   - number of due items
   - the top 1-3 due knowledge points
   - a suggested next command: academic-coach review
5. Do not fabricate due items if the files are incomplete; state the blocker instead.
```

## Pattern B: Daily Status Job

Use when you want a lightweight daily summary.

```text
You are running a daily academic-coach status check for {{COURSE_NAME}}.

Workspace:
- Obsidian course folder: {{COURSE_FOLDER}}
- Study system folder: {{STUDY_SYSTEM_FOLDER}}

Task:
1. Read PROGRESS.md, REVIEW_SCHEDULE.md, and KNOWLEDGE_REGISTRY.json.
2. Summarize current progress in Chinese.
3. Report:
   - overall progress percent if available
   - mastered / learning / weak counts
   - next recommended knowledge point
   - due-today review items
4. Keep the message concise and actionable.
```

## Pattern C: Weekly Mock Exam Reminder

```text
You are running a weekly academic-coach exam reminder for {{COURSE_NAME}}.

Workspace:
- Obsidian course folder: {{COURSE_FOLDER}}
- Study system folder: {{STUDY_SYSTEM_FOLDER}}

Task:
1. Read EXAM_FOCUS.md, WEAK_POINTS.md, and PROGRESS.md.
2. Produce a concise Chinese reminder that recommends starting `academic-coach exam`.
3. Mention:
   - the most important exam-focus topics
   - the most dangerous weak points
   - one recommended exam duration
4. If evidence is thin, say that the exam focus needs refinement.
```

## Pattern D: Pre-Exam Intensified Review Reminder

```text
You are running a pre-exam intensified review reminder for {{COURSE_NAME}}.

Workspace:
- Obsidian course folder: {{COURSE_FOLDER}}
- Study system folder: {{STUDY_SYSTEM_FOLDER}}
- Exam date: {{EXAM_DATE}}

Task:
1. Read REVIEW_SCHEDULE.md, EXAM_FOCUS.md, WEAK_POINTS.md, and KNOWLEDGE_REGISTRY.json.
2. Produce a focused Chinese reminder for today.
3. Prioritize:
   - overdue review items
   - high-frequency exam topics
   - weak items with repeated mistakes
4. End with the suggested next action: academic-coach review or academic-coach weak.
```

## Scheduling Examples

- Daily review reminder: `0 20 * * *`
- Weekly mock exam reminder: `0 14 * * 0`
- Pre-exam weekday reminder: `0 19 * * 1-5`

Always confirm the schedule with the user before creation.
