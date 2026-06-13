---
tags: [academic/dashboard, academic/doc-surface]
created: "{{DATE}}"
source: "self"
source_title: "{{COURSE_NAME}} Dashboard"
source_url: ""
status: wip
---

# DASHBOARD

## COURSE SUMMARY
- Course: {{COURSE_NAME}}
- Academic term: {{ACADEMIC_TERM}}
- Workspace mode: {{WORKSPACE_MODE}}
- Course folder: {{COURSE_FOLDER}}
- Study-system folder: {{STUDY_SYSTEM_FOLDER}}
- Current phase: {{CURRENT_PHASE}}
- Exam date: {{EXAM_DATE_OR_TBD}}

## PROGRESS SNAPSHOT
- Overall progress: {{OVERALL_PROGRESS_PERCENT}}%
- Mastered: {{MASTERED_COUNT}}
- Learning: {{LEARNING_COUNT}}
- Weak: {{WEAK_COUNT}}
- Forgotten: {{FORGOTTEN_COUNT}}
- Unseen: {{UNSEEN_COUNT}}

## DUE TODAY
- Review due count: {{DUE_TODAY_COUNT}}
- Highest-priority due item: {{TOP_DUE_ITEM}}
- Review urgency note: {{REVIEW_URGENCY_NOTE}}

## WEAK-POINT FOCUS
- Top weak knowledge point: {{TOP_WEAK_POINT}}
- Main error pattern: {{MAIN_ERROR_PATTERN}}
- Repair priority: {{REPAIR_PRIORITY_NOTE}}

## ACTIVE REQUEST
- Active request ID: {{ACTIVE_REQUEST_ID_OR_NONE}}
- Active mode: {{ACTIVE_MODE_OR_NONE}}
- Active request status: {{ACTIVE_REQUEST_STATUS_OR_NONE}}
- Blocking question summary: {{BLOCKING_QUESTION_SUMMARY}}

## LATEST SESSION
- Latest session note: {{LATEST_SESSION_NOTE_OR_NONE}}
- Current knowledge point: {{CURRENT_KNOWLEDGE_POINT}}
- Latest score: {{LATEST_SCORE}}
- Next review at: {{NEXT_REVIEW_AT}}

## QUICK ACTIONS
- `academic-coach status`
- `academic-coach continue`
- `academic-coach review`
- `academic-coach weak`
- `academic-coach exam`
- Add a structured request to `INBOX.md`

## NAVIGATION
- Study system: `study-system/`
- Request queue: `INBOX.md`
- Latest summaries: `OUTBOX.md`
- Session history: `SESSIONS/`
- Topic notes: `TOPICS/`

## LAST UPDATED
- {{DATE}}: dashboard initialized
