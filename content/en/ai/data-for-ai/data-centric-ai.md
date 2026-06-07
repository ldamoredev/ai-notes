---
title: "Data-centric AI"
description: Data-centric AI holds the model mostly fixed and improves the data, because data quality, coverage, and labels often dominate model choice.
tags: [data-for-ai, data-centric-ai, datasets]
order: 1
updated: 2026-06-07
---
# Data-centric AI

Data-centric AI treats the dataset as the main product of iteration. Instead of
immediately swapping architectures or prompts, you improve labels, coverage, examples,
documentation, and feedback loops.

## The shift in focus

| Model-centric question | Data-centric question |
|---|---|
| Which model should we try next? | Which examples are wrong, missing, stale, or mislabeled? |
| How do we tune hyperparameters? | Which slices fail and why? |
| Can a bigger model fix this? | Is the input distribution represented? |
| How do we improve the score? | Which data change would reduce the largest error cluster? |

The model still matters. Data-centric work just prevents model iteration from hiding
dataset problems.

## Where it pays off

- Small or medium datasets where label quality dominates.
- Domain tasks where examples need expert judgment.
- Evaluation suites where one bad label can mislead release decisions.
- RAG systems where document quality and chunk boundaries decide answer quality.
- Fine-tuning where consistent examples matter more than raw volume.

## Data iteration loop

1. Measure performance by slice.
2. Inspect errors by hand.
3. Label the root cause: missing coverage, bad label, noisy input, ambiguous task, stale data, or leakage.
4. Fix the data or rubric.
5. Re-run the same eval.
6. Version the dataset change.

## Pitfall

Data-centric does not mean "collect more data". More of the same noisy distribution can
make the system harder to debug. Improve the examples that change decisions.

**Connects to:** [[ai/machine-learning/error-analysis|error analysis]] ·
[[ai/evaluation/designing-eval-sets|designing eval sets]] ·
[[ai/fine-tuning-and-alignment/data-quality-for-finetuning|data quality for fine-tuning]]
