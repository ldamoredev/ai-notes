---
title: "Gradient descent: how models actually learn"
description: The optimization loop behind nearly every model — walking downhill on a loss surface, and why learning rate is the knob that matters most.
tags: [foundations, optimization, gradient-descent, training]
order: 10
updated: 2026-06-07
---
# Gradient descent: how models actually learn

Training reduces to one loop: measure how wrong you are, figure out which way to
nudge each parameter to be *less* wrong, take a small step, repeat. That's gradient
descent, and it powers everything from linear regression to frontier LLMs.

## The mental picture

Imagine the [[ai/foundations/how-learning-works|loss]] as a hilly landscape where
height = error and your position = the current parameters. The **gradient** is the
direction of steepest *uphill*; you step in the **opposite** direction to go down.

> new_params = old_params − learning_rate × gradient

Repeat until the loss stops improving. You're walking downhill in a space with
millions or billions of dimensions.

## Learning rate: the make-or-break knob

- **Too large** → you overshoot the valley, loss bounces or diverges (NaNs).
- **Too small** → training crawls and may stall in a poor spot.
- In practice you use a **schedule**: warm up, then decay. This single
  hyperparameter often matters more than model tweaks.

## Why "stochastic" (SGD)

Computing the gradient over the *entire* dataset each step is too expensive, so we
estimate it on a **mini-batch**. The estimate is noisy — but the noise is a feature:
it helps escape bad spots and generalizes better. Batch size trades gradient
quality against speed and memory.

## What you actually use

Plain SGD is rarely used raw. **Adam / AdamW** adapt the step size per parameter
using running averages of past gradients — robust defaults for deep nets.

| Term | One-line meaning |
|---|---|
| Gradient | direction of steepest increase in loss |
| Backpropagation | the chain rule computing gradients layer by layer |
| Learning rate | step size — the most important hyperparameter |
| Mini-batch | a sample used to estimate the gradient cheaply |
| Adam/AdamW | adaptive optimizer; the common default |

## Pitfall

A loss that explodes to NaN is almost always learning rate (or unscaled inputs, or
a missing normalization). Lower the LR before blaming the model.

**Connects to:** [[ai/foundations/how-learning-works|loss & objective]] ·
[[ai/deep-learning/index|backprop & optimizers]] ·
[[ai/foundations/linear-algebra-for-ml|the math underneath]]
