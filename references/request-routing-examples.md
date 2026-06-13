# Academic Coach Request Routing Examples

## Purpose

This document turns the command-routing rules into concrete request examples.
Use it when implementing or operating Academic Coach across different surfaces:
- chat / pseudo-command
- natural language
- document-first notes
- cron-generated reminders

The goal is simple:
Every trigger should normalize into one canonical request shape before execution logic begins.

## Canonical Request Schema

Recommended logical fields:

```yaml
request_id: 2026-06-13-continue-logic-functions
status: open
mode: continue
course: Digital Electronics
topic_hint: Logic function representation
goal: continue the next dependency-safe knowledge point
source: user-chat
source_note: null
created_at: 2026-06-13 20:10
updated_at: 2026-06-13 20:10
blocking_questions: []
session_note: null
```

## Field Rules

- `request_id`
  - stable per request
  - use timestamp + mode + short slug when no external ID exists
- `status`
  - one of: `open`, `needs_clarification`, `ready`, `awaiting_user_answer`, `completed`, `cancelled`
- `mode`
  - one of: `help`, `init`, `status`, `continue`, `review`, `weak`, `plan`, `exam`, `sync`, `mistakes`, `schedule`, `audit`
- `course`
  - required except in the earliest ambiguous bootstrap moment
- `topic_hint`
  - optional, but preserve it if the user gave one
- `goal`
  - optional distilled intent in operator language
- `source`
  - examples: `user-chat`, `user-note`, `pseudo-command`, `cron-reminder`, `cron-doc-update`
- `source_note`
  - path to the originating note if the request came from markdown
- `blocking_questions`
  - empty only when enough information exists to proceed honestly
- `session_note`
  - filled once a real teaching/review/exam/audit transaction starts

## Normalization Pipeline

1. detect the surface
2. detect intent
3. map to one canonical `mode`
4. identify course context if possible
5. check whether initialized state exists
6. decide whether the request is `ready`, `needs_clarification`, or should route into full init / lightweight bootstrap
7. only then execute the mode-specific protocol

## Surface-to-Mode Examples

### 1. Explicit pseudo-command in chat

Input:
```text
/academic-coach continue
```

Normalize to:
```yaml
mode: continue
source: pseudo-command
status: open
```

If no study-system exists:
- do not execute `continue` directly
- move into bootstrap gating

### 2. Natural-language continuation request

Input:
```text
继续学习数电
```

Normalize to:
```yaml
mode: continue
course: Digital Electronics
source: user-chat
goal: continue the course teaching loop
```

If multiple course candidates exist:
- status becomes `needs_clarification`
- add a blocking question asking which course is meant

### 3. Natural-language review request

Input:
```text
帮我复习今天该复习的内容
```

Normalize to:
```yaml
mode: review
source: user-chat
goal: review due items first
```

If state exists:
- use actual due items only

If no state exists:
- do not invent a due queue
- bootstrap first

### 4. Exam-mode request

Input:
```text
进入考试模式
```

Normalize to:
```yaml
mode: exam
source: user-chat
goal: run exam-focused workflow
```

If the course is ambiguous:
- `needs_clarification`

If no state exists but the user wants immediate mock testing:
- allow ad-hoc mock only after minimum bootstrap
- explicitly mark evidence limits

### 5. Document request in INBOX.md

Input:
```md
## Request: 2026-06-13-review-gray-code
status: open
mode: review
course: Digital Electronics
topic_hint: Gray code
source: user

请优先复习 Gray code，并检查我是不是已经忘了转换规则。
```

Normalize to:
```yaml
request_id: 2026-06-13-review-gray-code
mode: review
course: Digital Electronics
topic_hint: Gray code
source: user-note
source_note: INBOX.md
status: open
```

### 6. Topic-note frontmatter request

Input:
```yaml
---
type: academic-coach-request
status: open
mode: weak
course: Signals and Systems
topic_hint: convolution
created: 2026-06-13
source_note: TOPICS/Convolution.md
---
```

Normalize to:
```yaml
mode: weak
course: Signals and Systems
topic_hint: convolution
source: user-note
source_note: TOPICS/Convolution.md
```

### 7. Cron reminder message

Input:
```text
Daily review reminder for Machine Learning. Check due items and continue only if nothing is due.
```

Normalize to:
```yaml
mode: review
course: Machine Learning
source: cron-reminder
goal: review due items first, otherwise continue
```

Rule:
- the cron reminder itself does not mutate academic state
- state changes happen only when a real review/continue transaction is executed

### 8. Cron-created INBOX request

Input written to `INBOX.md`:
```md
## Request: 2026-06-13-daily-review
status: open
mode: review
course: Machine Learning
source: cron

Today has 3 due items. Review them before starting anything new.
```

Normalize to:
```yaml
mode: review
course: Machine Learning
source: cron-doc-update
status: open
```

## Clarification Routing Examples

### Missing course identity

Input:
```text
帮我继续学习
```

If there is exactly one active course context:
- infer that course

If there are multiple plausible courses:
```yaml
status: needs_clarification
blocking_questions:
  - Which course do you want to continue?
```

### No initialized state

Input:
```text
/acadmic-coach review
```

Normalized mode is still `review` even if the typo had to be interpreted.
But execution must become:
```yaml
status: needs_clarification
mode: review
blocking_questions:
  - I don't detect an initialized study-system yet. Do you want full init or a lightweight bootstrap first?
```

## Request State Transitions

Typical flow:

```text
open -> needs_clarification -> ready -> awaiting_user_answer -> completed
```

Possible alternates:
- `open -> ready -> completed`
- `open -> cancelled`
- `awaiting_user_answer -> completed`
- `awaiting_user_answer -> ready` when a follow-up execution turn is needed after the user replies

## Conflict Rules

### Multiple open requests in one course
- prioritize explicit user urgency
- otherwise prioritize: review due today > awaiting clarification blockers > continue > audit/plan housekeeping
- keep only one request in `awaiting_user_answer` for a course when possible

### Competing surfaces
If the same course has both:
- a fresh chat request
- an old lingering note request

Use this order:
1. explicit fresh user request
2. unresolved active teaching thread
3. queued note request
4. cron-generated reminder

### Freeform vs structured note disagreement
- immediate execution intent follows the request entry
- durable context remains in the topic/session notes

## Hard Rules

Do not:
- skip normalization and branch directly by surface
- create different mastery logic for chat vs notes
- fabricate request fields that imply evidence you do not have
- mark a request `completed` if the teaching loop is still waiting on the user's answer
- let cron reminders silently mutate mastery state on their own

## Bottom Line

Different surfaces may look different to the user.
But underneath, Academic Coach should behave like one request router feeding one tutoring protocol.
