# Review History Schema

Use this reference when appending entries to `review_history` inside `KNOWLEDGE_REGISTRY.json`.

## Goal
Keep review-history entries consistent across different agents and sessions.

## Recommended Entry Shape

```json
{
  "date": "2026-06-13",
  "mode": "continue",
  "score": 82,
  "status_before": "unseen",
  "status_after": "learning",
  "question_types": ["concept", "understanding", "application"],
  "mistake_tags": ["concept confusion"],
  "notes": "Could explain intuition but failed the transfer question.",
  "next_review": "2026-06-16"
}
```

## Field Notes
- `date`: ISO date string.
- `mode`: usually `continue`, `review`, `weak`, or `exam`.
- `score`: 0-100.
- `status_before` / `status_after`: one of `unseen`, `learning`, `mastered`, `weak`, `forgotten`.
- `question_types`: what was actually tested.
- `mistake_tags`: normalized labels like `concept confusion`, `formula misuse`, `missing prerequisite`.
- `notes`: concise but informative.
- `next_review`: ISO date string or null if not scheduled yet.

## Rules
- Append entries; do not rewrite history unless correcting a factual error.
- Keep one entry per evaluated session per knowledge point.
- If no questions were asked and no score was assigned, do not append a fake review-history record.
