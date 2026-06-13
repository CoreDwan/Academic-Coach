---
type: academic-coach-session
status: {{SESSION_STATUS}}
mode: {{MODE}}
course: {{COURSE_NAME}}
knowledge_point: {{KNOWLEDGE_POINT}}
request_id: {{REQUEST_ID}}
created: {{TIMESTAMP}}
updated: {{TIMESTAMP}}
linked_topic:
  - {{LINKED_TOPIC_PATH_OR_NONE}}
---

# SESSION: {{SESSION_TITLE}}

## STATUS HEADER
- 当前课程：{{COURSE_NAME}}
- 当前知识点：{{KNOWLEDGE_POINT}}
- 总体进度：{{OVERALL_PROGRESS_PERCENT}}%
- 已掌握：{{MASTERED_COUNT}}
- 学习中：{{LEARNING_COUNT}}
- 薄弱项：{{WEAK_SUMMARY}}

## REQUEST CONTEXT
- Mode: {{MODE}}
- Request ID: {{REQUEST_ID}}
- Source: {{REQUEST_SOURCE}}
- Goal: {{REQUEST_GOAL_OR_NONE}}
- Topic hint: {{TOPIC_HINT_OR_NONE}}

## EXPLANATION
- Core principle / mechanism:
- Intuition:
- Example:
- Linked prerequisite:
- Common misunderstanding:

## USER RESTATEMENT PROMPT
请用自己的话解释这个知识点，并说明它为什么重要。

## ASSESSMENT QUESTIONS
1. Concept question:
2. Understanding question:
3. Application question:
4. Optional calculation / derivation:

## USER ANSWER AREA
- Restatement:
- Q1:
- Q2:
- Q3:
- Q4:

## EVALUATION
- Conceptual understanding:
- Accuracy of expression:
- Application ability:
- Knowledge linkage:

## SCORE / MASTERY DECISION
- Score: {{SCORE_OR_PENDING}}
- New status: {{NEW_STATUS_OR_PENDING}}
- Error reason category: {{ERROR_REASON_OR_NONE}}

## STATE UPDATES APPLIED
- `KNOWLEDGE_REGISTRY.json`:
- `PROGRESS.md`:
- `WEAK_POINTS.md`:
- `MISTAKES.md`:
- `REVIEW_SCHEDULE.md`:
- `TEACHING_LOG.md`:

## NEXT RECOMMENDED ACTION
- {{NEXT_ACTION_NOTE}}
