---
title: "Feedback data and active learning"
description: Feedback data and active learning turn production uncertainty, corrections, and failures into targeted data improvements.
tags: [data-for-ai, feedback, active-learning]
order: 12
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/evaluation/systematic-error-analysis]
last_verified: 2026-07-20
---
# Feedback data and active learning

## Mechanism: uncertainty/error → selected example → label → evaluated update

```python
scores = [0.51, 0.92, 0.49]
print(min(scores, key=lambda s: abs(s-.5)))
```

Run with `python3`; expected output selects the most uncertain example. Feedback is not ground truth: log source, incentives, reviewer agreement, exposure bias, and label policy; assess whether sampling amplifies existing representation gaps.

## Sources

- [Active Learning Literature Survey](http://burrsettles.com/pub/settles.activelearning.pdf) — active-learning foundations.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — feedback-loop risks.

Production feedback is one of the best sources of new data, but only if it is captured,
triaged, labeled, and fed back deliberately. Otherwise it becomes noisy telemetry.

## Feedback sources

- User corrections, thumbs, edits, ratings, and comments.
- Human review decisions and escalation outcomes.
- Support tickets and incident reports.
- Low-confidence predictions and abstentions.
- Disagreement between model, judge, and human label.
- Drift or slice failures found in monitoring.

## Active learning loop

1. Identify examples where additional labels would most improve the system.
2. Prioritize by uncertainty, product impact, risk, and slice coverage.
3. Send selected examples to human review with clear guidelines.
4. Add labels to the dataset with provenance and reviewer metadata.
5. Update train or eval sets according to purpose.
6. Re-run the relevant evals and monitor for regressions.

## Feedback hygiene

| Risk | Control |
|---|---|
| Noisy user ratings | combine with trace review |
| Popularity bias | sample by slice, not only volume |
| Privacy leakage | redact and restrict review access |
| Feedback loops | keep holdout sets separate |
| Overfitting to complaints | compare against representative evals |

## Pitfall

Not all feedback should become training data. Some belongs in evals, product design,
documentation, or policy changes instead.

**Connects to:** [[ai/mlops/feedback-loops|feedback loops]] ·
[[ai/mlops/human-in-the-loop-production|human-in-the-loop production]] ·
[[ai/evaluation/systematic-error-analysis|systematic error analysis]]
