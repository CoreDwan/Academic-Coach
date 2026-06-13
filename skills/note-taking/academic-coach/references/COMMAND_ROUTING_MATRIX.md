# Command Routing Matrix

Use this reference when the user invokes Academic Coach through pseudo-commands or natural language.

## Core routing rule
Route by intent + state, not surface wording.

Check:
1. whether a `study-system/` already exists
2. whether the course identity is already known
3. whether evidence is sufficient for full execution

If state is missing, do not fabricate progress, due reviews, weak-point history, or audit results.

## Routing states

### A. Initialized state exists
Use the requested command normally and update persistent records.

### B. No initialized state exists
Enter the implicit bootstrap gate:
- acknowledge the requested intent
- state that no initialized course state is present yet
- ask only the minimum clarification needed
- choose between full `academic-coach init` and lightweight bootstrap

### C. Partial/lightweight state exists
Allow immediate work within known limits, mark coverage limits explicitly, and recommend later full `init` or `sync` when more materials arrive.

## Command normalization

- `academic-coach help` -> always safe
- `academic-coach init` -> full init flow
- `academic-coach status` -> real status if state exists; otherwise explain no state yet and bootstrap
- `academic-coach continue` -> next best knowledge point if state exists; otherwise bootstrap
- `academic-coach review` -> due review flow if state exists; otherwise bootstrap
- `academic-coach weak` -> weak-point flow if state exists; otherwise bootstrap
- `academic-coach plan` -> plan from real state if available; otherwise bootstrap or lightweight planning
- `academic-coach exam` -> exam mode from known state; if no state, only allow an ad-hoc mock after minimum bootstrap and declare evidence limits
- `academic-coach sync` -> reconcile new materials into existing state; if no state, usually convert into init
- `academic-coach mistakes` -> real mistake log if state exists; otherwise bootstrap
- `academic-coach schedule` -> real review schedule if state exists; otherwise bootstrap
- `academic-coach audit` -> audit a real study-system only; never audit empty air

## Natural-language normalization examples

- `帮我继续学习` -> `academic-coach continue`
- `帮我复习今天该复习的` -> `academic-coach review`
- `看看我现在学到哪了` -> `academic-coach status`
- `找出我的薄弱点` -> `academic-coach weak`
- `进入考试模式` -> `academic-coach exam`
- `把新 PPT 同步进去` -> `academic-coach sync`
- `检查一下这个 study-system` -> `academic-coach audit`
- `/academic-coach 帮我复习概率论` -> detect course + no-state/has-state, then route accordingly

## Full init vs lightweight bootstrap

Choose full init when:
- the user explicitly says `init`
- the user wants the long-term system established now
- enough materials are available
- persistent files are expected immediately

Choose lightweight bootstrap when:
- no state exists yet
- the user wants immediate help now
- current evidence is incomplete
- a full archive-quality knowledge tree would be premature

## Hard failures to avoid

Never:
- output a fake progress header when no course state exists
- claim there are due reviews when no schedule exists
- generate weak-point rankings without evidence
- pretend `audit` succeeded when no study-system exists
- silently upgrade lightweight bootstrap into full init
