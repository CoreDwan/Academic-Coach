# Hybrid Chat↔Doc Persistence

Use this when Academic Coach runs in a hybrid workflow:
- terminal/chat remains an active interaction surface
- the course workspace also has doc-first artifacts such as `DASHBOARD.md`, `INBOX.md`, `OUTBOX.md`, `SESSIONS/`, or `TOPICS/`

## Rule

Terminal chat is an intake surface, not a persistence bypass.
If a real `continue`, `review`, `weak`, `exam`, or `audit` transaction is executed from chat/pseudo-command, it must leave the same durable paper trail as a note-originated run.

## Minimum write-back contract

After a chat-originated execution in a doc-first course workspace:
1. create or update one `SESSIONS/YYYY-MM-DD-HHMM-<mode>-<slug>.md` note
2. update `OUTBOX.md` with a short navigational summary
3. update `INBOX.md` when a normalized request record or clarification state needs to be preserved
4. patch `study-system/` state files exactly as the mode requires

## Session note contents

The session note should still contain:
- status header
- request context
- explanation / prompts
- user answer area
- evaluation block
- score / mastery decision
- state updates applied
- next recommended action

## Trigger rule

If the course already has doc-first artifacts, do not ask whether chat should be recorded too. Record it by default.

## Pitfall

Do not let terminal progress live only in transient chat history. That creates divergence between:
- what the user just did in chat
- what `SESSIONS/` says happened
- what `OUTBOX.md` points to
- what the study-system can explain later
