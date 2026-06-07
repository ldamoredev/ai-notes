---
title: "Cross-validation done right"
description: How to estimate performance without wasting data or fooling yourself — k-fold, stratified, grouped, time-series, and the nested CV that tuning requires.
tags: [machine-learning, cross-validation, evaluation, model-selection]
order: 7
updated: 2026-06-07
---
# Cross-validation done right

A single train/validation [[ai/foundations/data-splits-and-leakage|split]] gives a
noisy estimate — get unlucky and you draw the wrong conclusion. Cross-validation
(CV) rotates the validation role across the data for a more stable estimate, and it
uses scarce data efficiently.

## k-fold CV

Split the data into `k` folds. Train on `k−1`, validate on the held-out fold,
rotate so every fold is validated once, then average. You get `k` scores — their
**mean** estimates performance and their **spread** estimates how reliable that
number is. `k = 5` or `10` are standard.

## Pick the variant that matches your data

| Variant | Use when |
|---|---|
| **Stratified k-fold** | classification — preserves class balance in each fold (essential for [[ai/machine-learning/class-imbalance|imbalanced]] data) |
| **Grouped k-fold** | repeated entities (user, patient) — keep a group entirely in one fold to avoid [[ai/foundations/data-splits-and-leakage|group leakage]] |
| **Time-series split** | temporal data — always train on the past, validate on the future; never shuffle |
| **Leave-one-out** | very small datasets (expensive, high variance) |

## Nested CV: the part people skip

If you tune [[ai/machine-learning/hyperparameter-tuning|hyperparameters]] using your
CV score and then *report* that same score, it's optimistic — you've fit to the
validation folds. **Nested CV** uses an inner loop to tune and an outer loop to
estimate honestly. At minimum, keep a final [[ai/foundations/data-splits-and-leakage|test
set]] you never touch during tuning.

## Pitfall

All preprocessing must happen **inside** the CV loop (via a
[[ai/machine-learning/ml-pipelines-and-leakage|pipeline]]). Fit a scaler or do
resampling before splitting and every fold is contaminated — the most common way CV
lies to you.

**Connects to:** [[ai/foundations/data-splits-and-leakage|splits & leakage]] ·
[[ai/machine-learning/hyperparameter-tuning|tuning]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|pipelines]]
