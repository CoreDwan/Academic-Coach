# Academic Coach User Journey

## Purpose

This document describes Academic Coach from the user's point of view rather than the protocol author's point of view.

The goal is to anchor future implementation work in the real learning journey:
- how a user discovers the skill
- how they start a course
- how they use it every day
- how their needs change over time
- how the workflow should evolve into a document-first academic operating system

## Core product promise

Academic Coach should feel like a long-term subject operating system, not a one-off explainer.

From the user's perspective, it should:
- help them start even when materials are incomplete
- turn a course into a maintained study system
- choose the next best thing to study
- teach exactly one knowledge point at a time
- remember progress across sessions
- track mistakes and weak points
- schedule review
- shift into exam mode when the course enters a sprint phase
- eventually run through a doc-first workspace that feels alive even outside terminal chat

## Timeline overview

The real user journey usually looks like this:

1. discover the skill
2. decide to start a course
3. inspect the initialized system
4. enter the daily learning loop
5. rely on weak-point and review support
6. switch into exam mode near the deadline
7. expect the system to become proactive and document-first

Each stage has different user expectations.

## Stage 0: discovery

### What the user is really asking

At first, the user is not asking for protocol details.
They are asking:
- what can this do for me?
- can I use it before my materials are perfectly organized?
- is it for one-off Q&A, or for long-term learning?
- do I have to use terminal chat forever, or can this live in Obsidian?

### What the skill must communicate clearly

Academic Coach is for:
- long-term course learning
- mixed-material course setup
- persistent progress tracking
- guided teaching and review
- exam preparation

It is not just a fancy prompt for answering one homework question.

### Requirement anchor

The user must be able to understand within one minute:
- this is a long-term tutoring system
- it can start from partial information
- it keeps state over time
- it is intended to grow into a markdown / Obsidian-centered workflow

## Stage 1: course bootstrap

This is the first real act of use.

### Common start patterns

Users usually arrive in one of three modes:

#### 1. Full-init user
"I have textbook, PPT, notes, homework, and past exams. Build the course system."

#### 2. Partial-material user
"I don't have everything organized yet, but I want to start learning now."

#### 3. Exam-pressure user
"The exam is coming soon. I need a focused learning system immediately."

### What the user needs at this stage

The skill must support:
- complete initialization
- lightweight bootstrap
- exam-first or deadline-driven startup

### Requirement anchor

The skill should never require an ideal textbook-perfect setup before becoming useful.
A user with incomplete materials should still be able to start.

## Stage 2: system visibility after init

Once the course is initialized, the user wants to see what the system actually built.

### User questions
- what is the scope of this course?
- what chapters / modules / knowledge points did you identify?
- what should I study first?
- what is already covered by my materials?
- what is still uncertain or missing?
- what does the system think my current state is?

### What the user should be able to inspect

#### 1. Course overview
- course identity
- exam / assessment context if known
- material coverage summary
- study strategy summary

#### 2. Knowledge map
- chapter -> module -> knowledge point
- fine granularity
- dependency-aware structure

#### 3. Current state snapshot
- total progress
- mastered / learning / weak / unseen counts
- due reviews
- next recommended knowledge point

#### 4. Confidence / evidence notes
- what materials were actually analyzed
- what exam focus is evidence-backed
- what parts are still provisional

### Requirement anchor

Initialization is not finished when files merely exist.
Initialization is finished when the user can look at the workspace and feel:
"My course has become a manageable system."

## Stage 3: daily learning loop

This is the highest-frequency usage stage.

### Typical user intents
- continue learning
- review due items
- repair weak points
- quickly inspect current status

### Expected user experience

The user should not need to restate context every day.
They should be able to say or trigger something equivalent to:
- continue
- review
- weak
- status

And the system should already know:
- current course
- current progress
- the best next knowledge point
- why that point was chosen

### Teaching expectations

For `continue`, `review`, and `weak`, the user expects:
- exactly one knowledge point at a time
- a real explanation, not a definition dump
- explicit waiting for the user's answer
- evaluation and score
- actual record updates afterward

### Requirement anchor

The core daily value is not just good teaching text.
It is reliable progression:
- the user learns one thing
- the system updates
- the next session starts from the new state

## Stage 4: diagnostic value

After a few sessions, the user's needs change.
They start asking not only:
- what should I study?

But also:
- what am I consistently bad at?
- what errors repeat?
- what do I forget fastest?
- what should I repair first?

### What becomes important
- weak-point ranking
- mistake type aggregation
- review urgency ranking
- forgotten-content detection
- explanation of why a point is considered fragile

### Requirement anchor

At this stage, Academic Coach must behave as a diagnostic system, not only a teaching system.
Mistake logging is not a side feature; it becomes a core value driver.

## Stage 5: exam phase

When the exam approaches, the user's priorities shift.

### The user no longer mainly wants
- broad exploration
- leisurely foundational study

### The user now wants
- high-yield focus
- probable重点 prediction
- triage of what to save vs what to postpone
- mock testing
- score estimation

### Expected exam-mode capabilities

#### 1. Focus prediction
Use:
- past papers
- homework patterns
- teacher emphasis
- high-frequency knowledge points

#### 2. Sprint planning
- what to review today
- what is must-know
- what is nice-to-have
- what gives the highest score gain per unit time

#### 3. Mock exam flow
- generate the paper
- optionally impose time pressure
- collect answers
- score them
- analyze score loss reasons

#### 4. Score outlook
- coverage estimate
- weak-point risk
- score-loss categories
- expected real exam range

### Requirement anchor

Exam mode is not just normal tutoring with a different label.
It is a distinct user phase with a different optimization target.

## Stage 6: proactive / autonomous workflow

Once the user trusts the system, they stop wanting a purely reactive assistant.
They begin wanting a system that helps maintain momentum on its own.

### User expectations at this stage
- remind me when review is due
- surface today's recommended work automatically
- queue a mock exam reminder weekly
- don't open multiple active teaching threads at once
- keep my dashboard current

### Why doc-first matters here

At this stage, the user no longer wants everything trapped in a linear terminal transcript.
They want a study workspace that stays visible and navigable between sessions.

That means the system should eventually center around:
- `DASHBOARD.md`
- `INBOX.md`
- `OUTBOX.md`
- `SESSIONS/`
- `TOPICS/`
- `study-system/`

### Requirement anchor

The mature form of Academic Coach should feel like an academic workspace that continues to exist even when the chat window is closed.

## User-facing command / trigger expectations by stage

### Early stage
- `academic-coach help`
- `academic-coach init`
- lightweight bootstrap through natural language

### Daily stage
- `academic-coach continue`
- `academic-coach review`
- `academic-coach weak`
- `academic-coach status`

### Mid-course diagnostic stage
- `academic-coach mistakes`
- `academic-coach weak`
- `academic-coach audit`
- `academic-coach sync`

### Exam stage
- `academic-coach plan`
- `academic-coach exam`
- intensified review / schedule workflows

### Mature doc-first stage
Equivalent requests should be triggerable from:
- chat
- pseudo-commands
- inbox requests
- note frontmatter
- dashboard actions
- cron-generated requests

## What absolutely must feel true to the user

No matter which stage they are in, the user should feel:
- the system remembers where we are
- the system teaches one thing at a time
- the system has evidence for its judgments
- the system is honest about uncertainty
- the system updates state after every real learning interaction
- the system adapts as the course moves from learning phase to exam phase

## Product requirement summary

If the timeline is compressed into product requirements, the most important ones are:

### Must-have
1. start a course even when materials are partial
2. build visible course structure and progress state
3. support a reliable daily single-knowledge-point teaching loop
4. maintain mistakes, weak points, and review schedule
5. switch into a meaningful exam mode

### High-priority next layer
6. support a document-first collaboration surface
7. support cron-assisted review flow
8. expose a dashboard / inbox / outbox / sessions / topics workflow

### Lower-priority later layer
9. helper automation around request scanning and linking
10. richer cross-note ergonomics and convenience tooling

## Bottom line

From the user's point of view, Academic Coach should evolve like this:

- first: a skill that can start a course and teach reliably
- then: a system that tracks progress, weakness, and review
- then: an exam coach that can prioritize under time pressure
- finally: a doc-first academic operating system living in markdown / Obsidian

Future implementation work should be judged against this journey, not only against protocol elegance.
