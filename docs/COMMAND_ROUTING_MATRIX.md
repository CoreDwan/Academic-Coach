# Command Routing Matrix

This document defines how Academic Coach should route pseudo-commands and natural-language requests into the correct protocol path.

## Core Principle

Do not route only by surface wording. Route by:
1. detected intent
2. whether a `study-system/` already exists
3. whether the course identity is already known
4. whether enough evidence exists for full execution

If state is missing, do not fabricate progress, review queues, or weak-point history.

## Routing States

### State A — Initialized course exists
Conditions:
- a target course folder is known
- `study-system/` exists or clearly established course state is available

Expected behavior:
- execute the requested command normally
- update persistent files and registry as needed

### State B — No initialized course exists yet
Conditions:
- no known `study-system/`
- no usable course state
- fresh directory or ambiguous new-course request

Expected behavior:
- enter the implicit bootstrap gate
- decide between full `init` and lightweight bootstrap
- ask only the minimum clarification needed for the selected path

### State C — Partial / lightweight state exists
Conditions:
- workspace is marked partially initialized
- minimal files may exist but archive-quality init is incomplete

Expected behavior:
- allow immediate learning/review actions within known limits
- recommend `academic-coach init` or `academic-coach sync` when more materials arrive
- do not overstate coverage

## Command Routing

| User input pattern | If initialized state exists | If no state exists | Notes |
|---|---|---|---|
| `academic-coach help` | explain protocol and next actions | same | always safe |
| `academic-coach init` | initialize or re-initialize after confirmation | full init clarification flow | explicit init always wins |
| `academic-coach status` | report real progress | explain no state yet, then offer bootstrap | never fabricate progress |
| `academic-coach continue` | continue next best knowledge point | bootstrap first | respect dependencies + exam weight |
| `academic-coach review` | run due review flow | bootstrap first | no fake due queue |
| `academic-coach weak` | inspect weak points and teach/review | bootstrap first | no fake weak history |
| `academic-coach plan` | produce study plan using real state | bootstrap or lightweight planning | can use partial materials |
| `academic-coach exam` | run exam mode using known materials/state | allow ad-hoc mock only after minimum bootstrap | must state evidence limits |
| `academic-coach sync` | reconcile new materials into existing system | usually convert no-state into init flow | sync assumes something to sync into |
| `academic-coach mistakes` | inspect/update mistake log | bootstrap first | no fake logs |
| `academic-coach schedule` | inspect or change review schedule | bootstrap first | cron changes still need confirmation |
| `academic-coach audit` | verify real study-system consistency | explain nothing to audit yet, then bootstrap | do not audit empty air |

## Natural-Language Routing

Natural language should be normalized into the same command paths.

### Examples

Input:
- `/academic-coach 帮我复习概率论`
- `use academic-coach to study operating systems`
- `帮我继续这个课程`
- `进入考试模式`

Routing logic:
1. detect command-equivalent intent
2. detect whether the request refers to an existing course or a new one
3. check state availability
4. route into:
   - initialized execution
   - full init
   - lightweight bootstrap
   - clarification for ambiguous course identity

## Intent Normalization Examples

| Natural-language request | Normalized intent |
|---|---|
| `帮我继续学习` | `academic-coach continue` |
| `帮我复习今天该复习的` | `academic-coach review` |
| `看看我现在学到哪了` | `academic-coach status` |
| `找出我的薄弱点` | `academic-coach weak` |
| `进入考试模式` | `academic-coach exam` |
| `把新 PPT 同步进去` | `academic-coach sync` |
| `检查一下这个 study-system` | `academic-coach audit` |

## Full Init vs Lightweight Bootstrap

### Choose full `academic-coach init` when:
- the user explicitly says `init`
- the user wants the long-term system set up now
- sufficient materials are available
- the user expects persistent files immediately

### Choose lightweight bootstrap when:
- there is no state yet
- the user wants immediate help now
- available evidence is incomplete
- a full archive-quality knowledge tree would be premature

## Required Clarification by Path

### For full init
Ask for:
- subject / course name
- preferred teaching/output language
- workspace mode and target folder
- available materials
- current goal and deadline context
- whether review scheduling should be prepared later

### For lightweight bootstrap
Ask only for:
- subject / course name
- preferred teaching/output language
- immediate goal for this session
- target folder now or permission to defer file creation
- what evidence/material is currently available

## Hard Failure Cases

Do not do the following:
- output a fake progress header when no course state exists
- claim there are due reviews when no schedule exists
- generate weak-point rankings without mistake/review evidence
- pretend `audit` succeeded when there is no real study-system
- silently upgrade lightweight bootstrap into full init

## Interaction Priority Rules

1. Explicit user intent beats defaults.
2. Real state beats guessed state.
3. Initialization truth beats convenience.
4. Immediate help is allowed, but only within declared evidence limits.
5. Persistent records must reflect actual observed evidence only.
