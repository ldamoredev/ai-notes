---
title: "Training dynamics: schedules, warmup & debugging"
description: The practical knobs that decide whether a big model trains smoothly — learning-rate schedules, warmup, gradient clipping, batch size, and reading the loss curve.
tags: [deep-learning, training, learning-rate, debugging]
order: 11
updated: 2026-06-07
---
# Training dynamics: schedules, warmup & debugging

Two networks with identical architecture can succeed or fail purely on **how** they
were trained. These are the practical levers — and the skill of reading a loss curve.

## Learning-rate schedules

A fixed [[ai/deep-learning/optimizers|learning rate]] is rarely best. Standard recipe:

- **Warmup** — start tiny and ramp up over the first few hundred/thousand steps.
  Early on, weights are random and a big step can blow up; warmup avoids the early
  divergence that plagues transformers.
- **Decay** — gradually lower the rate (cosine or linear) so the model takes big
  steps early and fine, careful steps later as it nears a good minimum.

## The other key knobs

- **Gradient clipping** — cap the gradient norm so a rare huge gradient can't throw
  the weights off a cliff. Near-mandatory for RNNs and transformers.
- **Batch size** — larger batches give smoother gradients and faster hardware
  throughput but use more memory and can generalize slightly worse; often scaled
  together with the learning rate.
- **Mixed precision (fp16/bf16)** — train in lower precision for speed and memory,
  keeping a few things in fp32 for stability. Standard for large models.

## Reading the loss curve

| Symptom | Likely cause |
|---|---|
| Loss → NaN / explodes | LR too high, no warmup, no grad clipping, unscaled inputs |
| Loss flat from step 0 | LR too low, bad [[ai/deep-learning/initialization-and-normalization|init]], broken data pipeline |
| Train ↓ but val ↑ | [[ai/foundations/generalization-and-overfitting|overfitting]] → regularize / more data |
| Loss spikes then recovers | usually fine; persistent spikes → lower LR or clip harder |

## Debugging order of operations

1. **Overfit a single batch** to ~zero loss — proves the model + loss + backprop wiring works.
2. Then scale up data and tune the LR (the highest-leverage hyperparameter).
3. Only then touch architecture.

> If a model won't learn, suspect the data pipeline and learning rate long before
> the architecture.

**Connects to:** [[ai/deep-learning/optimizers|optimizers]] ·
[[ai/deep-learning/initialization-and-normalization|init & norm]] ·
[[ai/machine-learning/error-analysis|learning curves]]
