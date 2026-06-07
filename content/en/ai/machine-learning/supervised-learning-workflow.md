---
title: "The supervised learning workflow, end to end"
description: The repeatable loop from problem framing to a shipped model — and why a dumb baseline is the most valuable first model you build.
tags: [machine-learning, workflow, baseline]
order: 1
updated: 2026-06-07
---
# The supervised learning workflow, end to end

Most ML projects fail in **framing and data**, not modeling. The algorithm is the
easy part. This is the loop that keeps you honest.

## The loop

1. **Frame the problem.** What decision does this output drive? Classification or
   regression? What does a wrong answer cost (this picks your
   [[ai/foundations/evaluation-metrics|metric]])?
2. **Get and split the data** *before* you touch it — train/validation/test, by
   time or group if needed (see [[ai/foundations/data-splits-and-leakage|leakage]]).
3. **Build a baseline.** A constant, a heuristic, or a logistic regression. This is
   the bar every fancier model must beat.
4. **Train a real model** on the training split.
5. **Evaluate** on validation and do [[ai/machine-learning/error-analysis|error
   analysis]] — not just a score, but *which* cases fail.
6. **Iterate** on features, data, and model. Most gains come from data, not
   algorithms.
7. **Final check** on the untouched test set, once. Then ship and monitor.

## Why a baseline first

A baseline is the cheapest insurance in ML:

- It tells you if the problem is even learnable from your data.
- It exposes leakage early (a "too good" baseline is a red flag).
- It sets the reference: a 92%-accurate model is worthless if predicting the
  majority class gives 91%.
- It's a working end-to-end pipeline you can improve incrementally.

> Ship the dumbest model that runs end to end on day one. Optimize from there.

## Where time actually goes

| Phase | Reality |
|---|---|
| Framing & data | most of the project; most of the risk |
| Modeling | often a few well-chosen defaults |
| Evaluation & error analysis | underrated; where real gains hide |
| Productionization | [[ai/mlops/index|its own discipline]] |

## Pitfall

Jumping to a complex model before a baseline means you can't tell whether your
gains come from the model, a leak, or noise.

**Connects to:** [[ai/machine-learning/error-analysis|error analysis]] ·
[[ai/foundations/how-learning-works|how learning works]] ·
[[ai/machine-learning/ml-pipelines-and-leakage|pipelines]]
