---
title: "How learning works: loss, objective, and ERM"
description: Every model that "learns" is minimizing a loss function over data. Understand that loop and most of ML stops being magic.
tags: [foundations, loss, optimization, training]
order: 1
updated: 2026-06-07
---
# How learning works: loss, objective, and ERM

A model that "learns" is doing something mechanical: it has **parameters**, a way
to turn parameters + input into a prediction, and a **loss function** that scores
how wrong each prediction is. Training is the search for parameters that make the
average loss small.

## The three pieces

1. **A model family** — a parameterized function `f(x; θ)`. The parameters `θ` are
   what training changes (weights of a network, coefficients of a regression).
2. **A loss function** — `L(prediction, target)` returns a number that is large
   when the prediction is bad. Examples: squared error for regression,
   cross-entropy for classification.
3. **An optimizer** — a procedure that nudges `θ` to reduce loss, almost always a
   variant of [[ai/foundations/gradient-descent-intuition|gradient descent]].

## Empirical risk minimization (ERM)

We actually want low loss on the *true distribution* of data ("risk"), but we only
have a finite sample. So we minimize the **average loss on the training set** —
the *empirical* risk — and hope it tracks the true risk:

> minimize over θ:  (1/N) Σ L( f(xᵢ; θ), yᵢ )

This "hope" is the entire game. When empirical risk is low but true risk is high,
you have [[ai/foundations/generalization-and-overfitting|overfitting]]. The gap
between them is what [[ai/foundations/data-splits-and-leakage|held-out evaluation]]
exists to estimate.

## The loss encodes what you actually want

The loss is a **value statement**, not a technicality. If false negatives are
worse than false positives, the loss must say so (class weights, custom costs). A
model optimizes exactly what you measure — not what you meant.

- Squared error punishes large errors disproportionately → sensitive to outliers.
- Cross-entropy punishes confident wrong answers harshly → drives calibration.
- A proxy loss (what's differentiable) often differs from the real goal (what the
  business cares about). Mind that gap.

## Pitfall

Optimizing the wrong objective is the most expensive bug in ML, and it is silent:
the loss curve looks great while the model gets better at the wrong thing.

**Connects to:** [[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/foundations/evaluation-metrics|metrics vs loss]] ·
[[ai/foundations/information-theory-basics|why cross-entropy]]
