---
title: "Feature engineering"
description: For classical ML on tabular data, features beat algorithms. Encoding, scaling, interactions, and the leakage traps that lurk in each.
tags: [machine-learning, feature-engineering, preprocessing]
order: 6
updated: 2026-06-07
---
# Feature engineering

In classical ML, **the features decide the ceiling** and the algorithm just
approaches it. Deep learning automates this for text and images, but for tabular
data, thoughtful features still beat a fancier model. It's where domain knowledge
enters the model.

## The everyday toolkit

- **Scaling** — standardize/normalize numeric features so distance- and
  gradient-based models behave (kNN, SVM, linear, neural nets). Trees don't care.
- **Encoding categoricals** — one-hot for low cardinality; target/ordinal/hashing or
  embeddings for high cardinality.
- **Handling missing values** — impute (mean/median/model) *and* often add a
  "was-missing" flag, since missingness itself can be signal.
- **Transforms** — log/Box-Cox for skewed values; binning; date → (dayofweek, month,
  is_holiday).
- **Interactions & ratios** — `price_per_sqft`, `clicks/impressions`. Linear models
  can't invent these; you must add them (a way to inject
  [[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] by hand).

## Good features share traits

- **Relevant** to the target (carry signal), not just available.
- **Available at prediction time** — if a feature is only known *after* the outcome,
  it's [[ai/foundations/data-splits-and-leakage|target leakage]].
- **Stable** — not prone to [[ai/foundations/distribution-shift|drift]] that breaks
  the model later.

## The leakage trap

Any feature learned from data (scaler stats, target encoding, TF-IDF) must be fit on
the **training fold only**, inside a [[ai/machine-learning/ml-pipelines-and-leakage|pipeline]].
Target encoding is especially dangerous: computing category means over all rows leaks
the label.

> More features is not better. Relevant, leak-free, available-at-serving features are.
> Prune aggressively; each weak feature adds variance.

**Connects to:** [[ai/machine-learning/ml-pipelines-and-leakage|pipelines & leakage]] ·
[[ai/foundations/features-and-dimensionality|representations]] ·
[[ai/machine-learning/regularization-l1-l2|regularization for selection]]
