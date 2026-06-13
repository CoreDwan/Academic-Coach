---
tags: [academic/inbox, academic/doc-surface]
created: "{{DATE}}"
source: "self"
source_title: "{{COURSE_NAME}} Inbox"
source_url: ""
status: wip
---

# INBOX

Use this file for:
- new study requests
- clarification questions
- queued review prompts
- cron-generated reminders

## QUEUE RULES
- Keep newest open requests near the top.
- Prefer one active teaching request per course at a time.
- Use normalized status values: `open`, `needs_clarification`, `ready`, `awaiting_user_answer`, `completed`, `cancelled`.
- When a request turns into a teaching/review/exam run, link the corresponding session note.

## ACTIVE / OPEN REQUESTS

## REQUEST TEMPLATE
```md
## Request: {{REQUEST_ID}}
status: open
mode: {{MODE}}
course: {{COURSE_NAME}}
topic_hint: {{TOPIC_HINT_OR_NONE}}
goal: {{GOAL_OR_NONE}}
source: user
source_note: {{SOURCE_NOTE_OR_NONE}}
created_at: {{TIMESTAMP}}
updated_at: {{TIMESTAMP}}
blocking_questions: {{BLOCKING_QUESTIONS_OR_NONE}}
session_note: {{SESSION_NOTE_OR_NONE}}

{{REQUEST_BODY}}
```

## CLARIFICATION BLOCK TEMPLATE
```md
## Clarification: {{REQUEST_ID}}
status: needs_clarification
mode: {{MODE}}
course: {{COURSE_NAME}}
blocking_questions:
- {{QUESTION_1}}
- {{QUESTION_2}}

Pending user answer here.
```

## READY / QUEUED REQUESTS

## COMPLETED / ARCHIVED POINTERS
- Move detailed outcomes to `OUTBOX.md` and `SESSIONS/`.
