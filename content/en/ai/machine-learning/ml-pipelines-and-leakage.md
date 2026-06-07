---
title: "Pipelines & preventing preprocessing leakage"
description: Why preprocessing must be fit on training data only, and how a pipeline makes that the default instead of a thing you remember to do.
tags: [machine-learning, pipelines, data-leakage, scikit-learn]
order: 12
updated: 2026-06-07
---
# Pipelines & preventing preprocessing leakage

The most common silent bug in ML is **fitting preprocessing on the whole dataset**.
Scaling, imputation, encoding, and feature selection all *learn* statistics — and if
they learn from the test rows, your evaluation is contaminated. A pipeline makes the
correct behavior automatic.

## The leak, concretely

Say you standardize features using the mean and standard deviation. If you compute
those over the entire dataset *before* splitting, the test set's distribution has
leaked into training. Your validation score looks better than production ever will.
This is a form of [[ai/foundations/data-splits-and-leakage|data leakage]].

Other leak-prone steps: imputing missing values, target/mean encoding, TF-IDF
vectorizers, feature selection, oversampling for [[ai/machine-learning/class-imbalance|imbalance]]
(resample **inside** cross-validation folds, never before).

## The fix: fit on train, transform on the rest

> Every step that *learns* from data must see **only the training fold**, then apply
> what it learned to validation/test.

A **pipeline** chains preprocessing + model into one object so that:

- `fit()` learns every step's parameters from training data only.
- `transform/predict()` reuses them on new data.
- Cross-validation refits the *entire* pipeline per fold, so no statistic crosses
  the fold boundary.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([
    ("scale", StandardScaler()),
    ("clf", LogisticRegression()),
])
pipe.fit(X_train, y_train)      # scaler learns from train only
pipe.predict(X_test)            # reuses train statistics
```

## Bonus: train/serve parity

A pipeline is also the artifact you deploy, so the exact preprocessing used in
training runs in production — eliminating "training/serving skew", a top cause of
models that test well and fail live.

## Pitfall

Calling `scaler.fit_transform(X)` on the full dataset in a notebook is the canonical
leak. If preprocessing happens outside the cross-validation loop, assume leakage.

**Connects to:** [[ai/foundations/data-splits-and-leakage|leakage]] ·
[[ai/machine-learning/cross-validation|cross-validation]] ·
[[ai/mlops/index|train/serve parity]]
