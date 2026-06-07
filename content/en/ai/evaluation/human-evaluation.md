---
title: "Human evaluation"
description: Human eval is strongest when reviewers share clear rubrics, calibrated examples, sampling rules, and disagreement handling.
tags: [evaluation, human-review, labeling]
order: 8
updated: 2026-06-07
---
# Human evaluation

Human evaluation is still the reference point for subjective, high-stakes, or ambiguous
AI behavior. But "ask people what they think" is not an eval; it is a survey unless
the review process is designed.

## What humans are best for

- Calibrating LLM judges against trusted labels.
- Reviewing high-impact decisions and safety failures.
- Judging tone, usefulness, nuance, and domain appropriateness.
- Discovering new failure modes that the rubric did not include.
- Resolving cases where the evidence is ambiguous.

## Review design

| Element | Good practice |
|---|---|
| Rubric | small number of criteria with examples |
| Instructions | define pass, fail, partial, and abstain |
| Sampling | mix random production samples with targeted edge cases |
| Calibration | reviewers grade the same seed set and discuss disagreements |
| Quality control | measure inter-rater agreement and audit outliers |

## Avoiding noisy labels

- Hide model identity when comparing models.
- Randomize answer order in pairwise comparisons.
- Keep the reviewer focused on one criterion at a time.
- Capture rationale for failures, not only a score.
- Track reviewer drift over time.

## Pitfall

Human eval is expensive, so teams often under-specify it. That wastes the expense.
Ten carefully calibrated reviews are more useful than a hundred inconsistent opinions.

**Connects to:** [[ai/evaluation/llm-as-judge|LLM-as-judge]] ·
[[ai/mlops/human-in-the-loop-production|human-in-the-loop production]] ·
[[ai/evaluation/task-specific-evals|task-specific evals]]
