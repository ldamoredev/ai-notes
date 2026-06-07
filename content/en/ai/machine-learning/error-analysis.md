---
title: "Error analysis: reading your model's mistakes"
description: A single aggregate score hides where a model fails. Slicing, learning curves, and confusion patterns turn errors into a roadmap.
tags: [machine-learning, error-analysis, debugging, evaluation]
order: 11
updated: 2026-06-07
---
# Error analysis: reading your model's mistakes

The fastest way to improve a model is to **look at what it gets wrong**, not to
swap algorithms. A 0.87 F1 tells you nothing about *how* to get to 0.90. Error
analysis does.

## Read the errors by hand first

Pull a sample of wrong predictions and categorize them. Patterns appear fast:

- "Half the errors are one mislabeled category" → fix the labels.
- "It fails on short inputs" → a feature or data-coverage gap.
- "Confident and wrong on a sub-group" → bias or [[ai/foundations/distribution-shift|shift]].

Counting error types tells you the *expected value* of each fix — fix the bucket
that's both large and cheap first.

## Slice, don't average

An aggregate metric can be fine while a critical slice is broken. Always evaluate
per segment (region, device, class, input length, customer tier). The model that's
95% accurate overall but 60% on your highest-value users is a failure dressed as a
success.

## Learning curves diagnose the bottleneck

Plot training vs validation error as data/size grows:

| Pattern | Diagnosis | Fix |
|---|---|---|
| Both high, close together | underfitting (high bias) | bigger model, better features |
| Train low, val high (big gap) | overfitting (high variance) | more data, [[ai/machine-learning/regularization-l1-l2|regularization]] |
| Val still falling at the end | not enough data yet | get more data |

This maps directly onto the [[ai/foundations/generalization-and-overfitting|bias–variance tradeoff]].

## Pitfall

Tuning against a single number invites [[ai/foundations/evaluation-metrics|Goodhart's
law]]. Pair the score with slices and a confusion matrix, or you'll optimize the
metric while the product gets worse.

**Connects to:** [[ai/machine-learning/supervised-learning-workflow|the workflow]] ·
[[ai/foundations/evaluation-metrics|metrics]] ·
[[ai/evaluation/index|evaluating systems]]
