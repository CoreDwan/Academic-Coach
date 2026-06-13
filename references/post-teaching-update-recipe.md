# Post-Teaching File Update Recipe

After each `academic-coach continue` teaching round (Step 7), update all relevant files in one `execute_code` block using `patch()`. Do NOT use individual `write_file` calls — they're slow and create unnecessary tool-call overhead.

## Update Order (all in one execute_code block)

### 1. KNOWLEDGE_REGISTRY.json (authoritative source)
- Read the full JSON, modify the target KP, write back
- Fields to update:
  - `status`: classify as `mastered` (90-100), `learning` (70-89), or `weak` (<70)
  - `mastery_score`: the numeric score (0-100)
  - `last_studied`: ISO date string (e.g., "2026-06-13")
  - `next_review`: ISO datetime. In intensive mode, use +4h from now; in normal mode, use +1d
  - `review_history`: append entry with `{date, type: "first_learning"|"review", score, status_from, status_to}`
  - `notes`: brief summary of strengths/weaknesses observed
- Recompute status counts for use in other file updates

### 2. PROGRESS.md (patch specific fields)
- `Overall progress`: recalc as `round(studied/total * 100)%`
- `Mastered/Learning/Weak/Forgotten/Unseen`: update counts from registry
- `Latest studied`: KP name + score + status
- `Next recommended`: next KP from study plan (or same if score < 70)
- `Latest score`: numeric score
- `RECENT UPDATES`: append new row to the table

### 3. STATUS.md (patch header fields)
- `当前知识点`: current KP + result summary
- `总体进度`: match PROGRESS.md
- `已掌握/学习中/薄弱项`: match PROGRESS.md counts
- `Last action`: teaching round summary
- `Next action`: suggested next command

### 4. MISTAKES.md (append rows, never overwrite)
- Only add rows if the user made substantive errors
- Use the MISTAKES.md log table format
- **Question format**: write the question as the user heard it during assessment, not a paraphrase — this makes later review rounds more effective
- Normalize error reasons to the canonical set: concept confusion, formula misuse, missing prerequisite, careless arithmetic, incomplete reasoning, memorized but not understood
- If the same error pattern already exists, increment the occurrence count rather than adding a duplicate row

### 5. WEAK_POINTS.md (update ranking)
- Only change if the new KP scored < 70 (add to weak list) or a previously weak KP improved
- Update the RANKING table with current scores

### 6. TEACHING_LOG.md (append row)
- Columns: Date | Knowledge Point | Score | Status Before | Status After | Notes

### 7. REVIEW_SCHEDULE.md (update due items)
- If the KP was just learned, add it to "DUE SOON" with the computed next_review date
- If a previously due item was reviewed, move it from "DUE TODAY" to "DUE SOON" with new date

### 8. KNOWLEDGE_TREE.md (optional, only on status change)
- Update the status icon (□ → ◐ → ✓ → ⚠ → ✗) next to the KP in the tree view

## Consistency Contract

All files MUST agree on:
- Status counts (Mastered/Learning/Weak/Forgotten/Unseen)
- Latest studied KP name and score
- Overall progress percentage

If any file drifts, run `academic-coach audit` to detect and repair.

## Example Patch Sequence (ch1-1 scored 70, learning)

```python
from hermes_tools import patch
import json

SS = "/path/to/study-system"

# 1. Registry: read-modify-write
with open(f"{SS}/KNOWLEDGE_REGISTRY.json") as f:
    reg = json.load(f)
for kp in reg["knowledge_points"]:
    if kp["id"] == "ch1-1":
        kp["status"] = "learning"
        kp["mastery_score"] = 70
        kp["last_studied"] = "2026-06-13"
        kp["next_review"] = "2026-06-13T17:00:00"
        kp["review_history"].append({"date":"2026-06-13","type":"first_learning","score":70,"status_from":"unseen","status_to":"learning"})
        break
with open(f"{SS}/KNOWLEDGE_REGISTRY.json","w") as f:
    json.dump(reg, f, ensure_ascii=False, indent=2)

# Count statuses for other updates
counts = {}
for kp in reg["knowledge_points"]:
    counts[kp["status"]] = counts.get(kp["status"], 0) + 1

# 2-7. Patch markdown files
patch(f"{SS}/PROGRESS.md", "- Overall progress: 0%", f"- Overall progress: {round((counts.get('learning',0)+counts.get('mastered',0))/42*100)}%")
# ... (continue for each field in PROGRESS, STATUS, MISTAKES, TEACHING_LOG)
```

## Pitfalls

- Never overwrite MISTAKES.md rows — always append
- Don't update WEAK_POINTS.md if the score is ≥ 70 and there are no existing weak entries for this KP
- Don't auto-start the next KP after updating — stop and wait for user input
- If the user scored < 70, the "next recommended" should stay on the SAME KP (not advance)
