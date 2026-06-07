---
title: "Data quality > quantity"
description: Fine-tuning is dominated by dataset quality: consistency, coverage, and examples that actually demonstrate the desired behavior.
tags: [fine-tuning, data-quality, datasets]
order: 7
updated: 2026-06-07
---
# Data quality > quantity

Fine-tuning is unusually sensitive to data quality because every example is an
instruction about how the model should behave. More examples help only after the
examples are correct, consistent, and representative.

## What quality means

- **Correctness** — the target answer is actually right.
- **Consistency** — similar inputs receive similar formats and decisions.
- **Coverage** — common cases, edge cases, refusals, and hard negatives are present.
- **Specificity** — the example demonstrates the behavior you want, not vague style.
- **Clean metadata** — roles, system messages, tools, and citations are not corrupted.

Bad examples are not neutral. They train the model.

## Quantity has diminishing returns

Small, high-signal datasets often beat large scraped sets for behavior tuning. Once
the model sees the pattern, additional near-duplicates add little and can overweight
one style or failure mode.

| Dataset smell | Likely outcome |
|---|---|
| Duplicate templates | Model overfits phrasing |
| Mixed answer formats | Unstable output shape |
| Incorrect "gold" answers | Confident wrong behavior |
| Missing negative cases | Unsafe over-compliance |

## The review loop

Treat dataset work like product QA: sample examples, review failures, fix labels, and
rerun evaluation. Keep a held-out set that never gets used for training decisions.

## Pitfall

Fine-tuning does not average out bad labels; it amplifies them. The model learns the
distribution you give it, including contradictions and shortcuts.

**Connects to:** [[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|building the dataset]] ·
[[ai/foundations/data-splits-and-leakage|splits and leakage]] ·
[[ai/machine-learning/error-analysis|error analysis]]
