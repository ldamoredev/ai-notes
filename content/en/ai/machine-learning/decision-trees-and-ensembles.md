---
title: "Decision trees & ensembles (RF, gradient boosting)"
description: Why gradient-boosted trees are still the default winner on tabular data, and how bagging and boosting tame a single tree's instability.
tags: [machine-learning, trees, random-forest, gradient-boosting, xgboost]
order: 4
updated: 2026-06-07
---
# Decision trees & ensembles (RF, gradient boosting)

For tabular data, an ensemble of trees is usually the model to beat — often
out-performing neural networks while training in seconds and needing little feature
scaling. Knowing how they work tells you when to trust them.

## A single decision tree

A tree splits the data with a series of yes/no questions ("is age > 30?"), choosing
each split to make the resulting groups more pure. It captures nonlinearities and
interactions automatically and is easy to read — but a single deep tree **overfits
badly**: it's high [[ai/foundations/generalization-and-overfitting|variance]],
memorizing noise. The fix is to combine many trees.

## Two ways to combine trees

| Method | Idea | Trees are | Effect |
|---|---|---|---|
| **Bagging / Random Forest** | train many trees on bootstrap samples + random feature subsets, average them | independent, parallel | mainly cuts **variance** |
| **Boosting** (GBM, XGBoost, LightGBM) | each new tree fixes the previous ensemble's errors | sequential, dependent | cuts **bias** *and* variance |

- **Random Forest**: robust, hard to misconfigure, a great strong baseline.
- **Gradient boosting**: usually the top scorer on tabular data, but more sensitive
  to hyperparameters (learning rate, tree depth, number of trees, regularization)
  and can overfit if pushed — [[ai/machine-learning/cross-validation|validate]] and
  use early stopping.

## Why trees love tabular data

- No need to scale features; handle mixed numeric/categorical naturally.
- Capture interactions and nonlinearities without manual
  [[ai/machine-learning/feature-engineering|feature crosses]].
- Give **feature importances** for interpretability (with caveats).

## Pitfall

Default boosting settings can overfit silently. Watch the validation curve, cap
tree depth, and use early stopping. And remember feature importances can be
misleading with correlated features — corroborate with permutation importance or
SHAP.

**Connects to:** [[ai/machine-learning/hyperparameter-tuning|tuning]] ·
[[ai/foundations/generalization-and-overfitting|variance & overfitting]] ·
[[ai/machine-learning/feature-engineering|features]]
