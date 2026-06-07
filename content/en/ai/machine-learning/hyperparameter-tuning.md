---
title: "Hyperparameter tuning"
description: Parameters are learned; hyperparameters are chosen. How to search them without burning compute or overfitting your validation set.
tags: [machine-learning, hyperparameters, tuning, model-selection]
order: 9
updated: 2026-06-07
---
# Hyperparameter tuning

**Parameters** are learned from data (weights). **Hyperparameters** are the knobs you
set *before* training: learning rate, tree depth, number of estimators,
[[ai/machine-learning/regularization-l1-l2|regularization λ]], `k` in kNN. The right
settings can move a model from mediocre to strong — but the search can waste compute
and quietly overfit if done carelessly.

## Search strategies

| Method | How | When |
|---|---|---|
| **Grid search** | try every combination on a grid | few hyperparameters, cheap models |
| **Random search** | sample combinations randomly | more efficient; better with many params (most don't matter) |
| **Bayesian / Optuna / Hyperband** | model which settings look promising, focus there | expensive models, larger budgets |

Random search usually beats grid for the same budget: only a couple of
hyperparameters tend to matter, and random sampling explores those dimensions more
thoroughly than a rigid grid.

## Do it without fooling yourself

- Tune against a **validation set or [[ai/machine-learning/cross-validation|cross-validation]]**,
  never the test set.
- Every tuning trial that peeks at the validation data spends some of its
  trustworthiness — the more trials, the more you risk overfitting *to the validation
  set*. Use **nested CV** or a held-out test set for the final, honest number.
- Spend effort where it pays: for gradient boosting, learning rate + number of trees
  + depth dominate; for neural nets, the [[ai/foundations/gradient-descent-intuition|learning
  rate]] is king.

## Practical order of operations

1. Get a baseline with sane defaults.
2. Tune the 2–3 hyperparameters that matter most (random search).
3. Refine around the best region.
4. Lock it and report on the untouched test set.

## Pitfall

Chasing a 0.2% CV gain through hundreds of trials is usually noise-mining, not
improvement — and it inflates your estimate. Better features or more data beat
hyperparameter obsession almost every time.

**Connects to:** [[ai/machine-learning/cross-validation|cross-validation]] ·
[[ai/machine-learning/regularization-l1-l2|regularization]] ·
[[ai/machine-learning/decision-trees-and-ensembles|tuning boosting]]
