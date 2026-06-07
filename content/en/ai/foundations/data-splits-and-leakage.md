---
title: "Train/validation/test splits & data leakage"
description: How to estimate real-world performance honestly — and the subtle ways information leaks and inflates your scores.
tags: [foundations, evaluation, data-leakage, validation]
order: 5
updated: 2026-06-07
---
# Train/validation/test splits & data leakage

You cannot judge generalization on data the model trained on. So you partition
your data and keep some of it hidden — that held-out performance is your estimate
of how the model behaves in the wild.

## The three splits and their jobs

- **Training set** — the model fits its parameters here.
- **Validation set** — used to make *decisions*: hyperparameters, model selection,
  early stopping. You look at it many times.
- **Test set** — touched **once**, at the very end, to report an honest number. If
  you tune against it, it stops being a fair estimate.

Cross-validation rotates the validation role across folds to get a more stable
estimate when data is scarce.

## Data leakage: the silent score-inflator

**Leakage** is any time information from outside the training set sneaks into the
model, making validation scores look better than reality. It is the most common
cause of "great in the notebook, terrible in production."

Common leaks:

- **Preprocessing before splitting** — fitting a scaler/imputer/vectorizer on the
  *whole* dataset leaks test statistics into training. Fit on train only, then
  apply to validation/test (use a pipeline).
- **Target leakage** — a feature that encodes the answer (e.g., a field only filled
  in after the outcome is known).
- **Temporal leakage** — training on future data to predict the past. Time series
  must split by **time**, never randomly.
- **Group leakage** — the same entity (user, patient, document) appears in both
  train and test, so the model "recognizes" rather than generalizes. Split by
  group.
- **Duplicate / near-duplicate rows** straddling the split — rampant in scraped
  text corpora and a real concern for LLM benchmarks (contamination).

## Rule of thumb

> If a result looks too good, suspect leakage before you celebrate.

A realistic split that mirrors how the model will actually be used beats a clean
random split that quietly leaks.

**Connects to:** [[ai/foundations/generalization-and-overfitting|overfitting]] ·
[[ai/foundations/distribution-shift|distribution shift]] ·
[[ai/evaluation/index|evaluation]]
