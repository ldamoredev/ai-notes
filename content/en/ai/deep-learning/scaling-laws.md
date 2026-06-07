---
title: "Scaling laws: why bigger keeps working"
description: Performance improves predictably with compute, data, and parameters. Scaling laws — and Chinchilla's data lesson — explain the whole frontier-model strategy.
tags: [deep-learning, scaling-laws, chinchilla, compute]
order: 12
updated: 2026-06-07
---
# Scaling laws: why bigger keeps working

The defining empirical fact of modern AI: as you increase **compute, data, and
parameters together**, loss falls in a smooth, predictable way — often a power law
across many orders of magnitude. This predictability is *why* labs bet billions on
bigger models: the payoff can be forecast before training.

## The three knobs

Test loss is driven jointly by:

- **Parameters** (N) — model size.
- **Data** (D) — number of training tokens.
- **Compute** (C) — roughly `C ≈ 6 · N · D` for transformers.

Scale one alone and you hit diminishing returns; the gains come from scaling them
**together** in the right ratio.

## The Chinchilla correction

Early large models were **undertrained** — too many parameters for too little data.
The *Chinchilla* result showed that for a fixed compute budget, parameters and tokens
should scale **roughly equally**, and that a smaller model trained on more data beats
a bigger model trained on less. This reframed the field from "biggest model" toward
"right model, more (and better) data," and is why data quality and quantity became
the bottleneck.

## Emergence (read with care)

Some capabilities appear to "switch on" past a scale threshold — *emergent
abilities*. The effect is real but partly an artifact of harsh pass/fail metrics;
under smoother metrics, progress is more continuous. Treat dramatic "emergence"
claims with healthy skepticism. (More in [[ai/llms/index|LLMs]].)

## Why it matters in practice

- **Forecasting** — you can predict large-model loss from small-scale runs and pick
  the compute-optimal size before committing.
- **The ceiling** — high-quality data is finite, so scaling is bumping into a data
  wall, pushing interest toward data quality, synthetic data, and
  [[ai/foundations/types-of-learning|better training signals]].
- **Inference cost** — a bigger model is also more expensive to *serve*, which loops
  back to [[ai/mlops/index|serving]] and [[ai/ai-product-engineering/index|product
  cost]] tradeoffs.

> Scaling laws explain the strategy; they don't promise it's free or forever. Data
> and serving cost are the real-world ceilings.

**Connects to:** [[ai/llms/index|LLM pretraining]] ·
[[ai/deep-learning/training-dynamics|training at scale]] ·
[[ai/foundations/how-learning-works|loss as the objective]]
