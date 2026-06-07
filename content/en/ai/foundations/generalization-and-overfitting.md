---
title: "Generalization, overfitting & the bias–variance tradeoff"
description: A model is only useful if it works on data it never saw. Overfitting, underfitting, and the tradeoff that governs both.
tags: [foundations, generalization, overfitting, bias-variance]
order: 2
updated: 2026-06-07
---
# Generalization, overfitting & the bias–variance tradeoff

**Generalization** is the only thing that matters: performance on data the model
did not train on. A model that memorizes its training set perfectly and fails on
new inputs has learned nothing useful.

## Underfitting vs overfitting

- **Underfitting** — the model is too simple (or under-trained) to capture the
  pattern. High error on *both* training and test data.
- **Overfitting** — the model fit the training data *too* well, including its
  noise and quirks. Low training error, high test error.

The signature is the **gap** between training and validation error. A small gap
with high error → underfit. A large gap → overfit.

## The bias–variance tradeoff

Total error decomposes (informally) into:

| Term | Meaning | Driven by |
|---|---|---|
| **Bias** | error from wrong assumptions / too-simple model | underfitting |
| **Variance** | error from sensitivity to the particular training sample | overfitting |
| **Irreducible** | noise no model can remove | the data itself |

More capacity (bigger model, more features) lowers bias but raises variance. The
classic goal is the sweet spot in between. (Very large models complicate this neat
story — see *double descent* — but the intuition still guides daily work.)

## Levers that improve generalization

- **More/cleaner data** — the most reliable fix; shrinks variance.
- **Regularization** — L2/L1 penalties, dropout, early stopping; trade a little
  bias for less variance.
- **Simpler model or fewer features** when data is scarce.
- **Cross-validation** to estimate the gap honestly rather than trusting one split.

## Pitfall

The validation set is a budget you spend by looking at it. Tune against it enough
times and you start overfitting *to the validation set* — which is why a final,
untouched [[ai/foundations/data-splits-and-leakage|test set]] exists.

**Connects to:** [[ai/foundations/data-splits-and-leakage|splits & leakage]] ·
[[ai/foundations/inductive-bias-and-no-free-lunch|inductive bias]] ·
[[ai/foundations/distribution-shift|distribution shift]]
