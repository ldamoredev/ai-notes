---
title: "Linear & logistic regression"
description: The two workhorses worth truly understanding — a strong baseline, an interpretable model, and the building block inside every neural network.
tags: [machine-learning, regression, classification, baseline]
order: 2
updated: 2026-06-07
---
# Linear & logistic regression

These are the first models to reach for and the last to fully retire. They're fast,
interpretable, hard to overfit, and — crucially — a single neuron in a neural
network *is* one of them. Understand these and deep learning is less mysterious.

## Linear regression — predict a number

Fit a weighted sum of features to predict a continuous value: `ŷ = w·x + b`. Train
by minimizing squared error via [[ai/foundations/gradient-descent-intuition|gradient
descent]] (or a closed-form solution). Each weight is readable: "holding others
fixed, +1 here moves the prediction by wᵢ."

Assumptions worth knowing: roughly linear relationship, errors not wildly
heteroscedastic, features not perfectly collinear. Break them badly and the
coefficients become unstable or misleading.

## Logistic regression — predict a probability

For classification, wrap the same linear score in a **sigmoid** to squash it into
[0, 1]: a calibrated-ish probability. Train with
[[ai/foundations/information-theory-basics|cross-entropy]] loss. Despite the name,
it's a *classifier*. A threshold (default 0.5, but tune it — see
[[ai/foundations/evaluation-metrics|metrics]]) turns the probability into a decision.

> A logistic regression is exactly the output layer of a classification neural
> network. The "deep" part just learns better features to feed it.

## Why they remain the default baseline

- **Fast** to train and predict, even on large data.
- **Interpretable** — coefficients are inspectable, which matters for trust and
  debugging.
- **Hard to overfit** with [[ai/machine-learning/regularization-l1-l2|regularization]],
  great when data is limited.
- A strong score here means a complex model must *earn* its added risk.

## Pitfall

Linear models need sensible [[ai/machine-learning/feature-engineering|features]]:
scale them, encode categoricals, and add interaction/nonlinear terms by hand, since
the model can't discover them on its own (that's the [[ai/foundations/inductive-bias-and-no-free-lunch|linear inductive bias]]).

**Connects to:** [[ai/machine-learning/regularization-l1-l2|regularization]] ·
[[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/deep-learning/index|the neuron inside a net]]
