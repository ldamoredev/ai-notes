---
title: "Optimizers: from SGD to AdamW"
description: SGD walks downhill; momentum and Adam make the walk faster and more stable. What each adds, and why AdamW is the transformer default.
tags: [deep-learning, optimizers, adam, sgd, momentum]
order: 4
updated: 2026-06-07
---
# Optimizers: from SGD to AdamW

The optimizer turns gradients into weight updates. They all build on
[[ai/foundations/gradient-descent-intuition|gradient descent]] — the differences are
in how they use the *history* of gradients to take smarter steps.

## The progression

- **SGD** — step opposite the mini-batch gradient. Simple, well-understood, often
  generalizes best in vision, but slow and sensitive to the learning rate.
- **Momentum** — accumulate a velocity that averages recent gradients, so the
  optimizer powers through noise and small bumps instead of zig-zagging. Think of a
  ball rolling downhill.
- **RMSProp / Adagrad** — scale each parameter's step by its own recent gradient
  magnitude, so rarely-updated parameters still move.
- **Adam** — momentum **+** per-parameter scaling combined. Robust, fast to
  converge, forgiving about learning rate — the default for most deep nets.
- **AdamW** — Adam with **decoupled weight decay**, which makes the
  [[ai/deep-learning/regularization-in-deep-nets|L2 regularization]] behave
  correctly. The standard for training transformers.

## What "adaptive" buys you

Adam adapts the effective step size per parameter using running averages of the
gradient (first moment) and its square (second moment). Practically: it just works
with less tuning, which is why it dominates. SGD with momentum + a good schedule can
generalize slightly better but needs more babysitting.

## The knob that still matters most

No optimizer saves you from a bad [[ai/foundations/gradient-descent-intuition|learning
rate]]. Adam reduces sensitivity but doesn't remove it — pair it with a
[[ai/deep-learning/training-dynamics|warmup + decay schedule]]. Too high → loss
diverges (NaNs); too low → it crawls.

> Sensible default: **AdamW + warmup + cosine decay.** Reach for plain SGD+momentum
> when squeezing the last bit of generalization out of a vision model.

**Connects to:** [[ai/foundations/gradient-descent-intuition|gradient descent]] ·
[[ai/deep-learning/training-dynamics|LR schedules]] ·
[[ai/deep-learning/regularization-in-deep-nets|weight decay]]
