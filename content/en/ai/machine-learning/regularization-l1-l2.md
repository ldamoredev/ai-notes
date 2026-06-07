---
title: "Regularization: L1, L2 & how they differ"
description: The main lever against overfitting — penalize complexity. Why L1 zeroes features out, L2 shrinks them, and what dropout and early stopping share with both.
tags: [machine-learning, regularization, overfitting, l1, l2]
order: 3
updated: 2026-06-07
---
# Regularization: L1, L2 & how they differ

Regularization is the main dial for the [[ai/foundations/generalization-and-overfitting|bias–variance
tradeoff]]: add a penalty for complexity so the model can't fit noise. You trade a
little training accuracy for better generalization.

## The idea

Instead of minimizing just the [[ai/foundations/how-learning-works|loss]], minimize
`loss + λ × penalty(weights)`. Large weights mean a more flexible, wigglier function;
penalizing them keeps the model simpler. **λ (lambda)** controls the strength — a key
[[ai/machine-learning/hyperparameter-tuning|hyperparameter]] you tune by
[[ai/machine-learning/cross-validation|cross-validation]].

## L1 vs L2

| | Penalty | Effect on weights | Use when |
|---|---|---|---|
| **L2** (Ridge) | sum of squares | shrinks all weights toward zero, smoothly | default; correlated features |
| **L1** (Lasso) | sum of absolute values | drives some weights to **exactly zero** | you want automatic feature selection / sparsity |
| **Elastic Net** | mix of both | shrinks *and* selects | many correlated features |

The key intuition: **L1 produces sparse models** (built-in feature selection),
because its penalty geometry has corners that push weights to zero. **L2 keeps all
features but small**, which is more stable when features are correlated.

## Same idea, other names

Regularization is everywhere; the form changes:

- **Early stopping** — stop training when validation loss rises (limits effective
  capacity).
- **Dropout** — randomly zero activations during training (a [[ai/deep-learning/index|deep
  learning]] regularizer).
- **Weight decay** — L2 by another name, baked into optimizers like AdamW.
- **More data / augmentation** — the strongest "regularizer" of all.

## Pitfall

Scale your features before L1/L2 — the penalty treats all weights equally, so an
unscaled large-range feature gets unfairly penalized (or spared). And too-strong λ
underfits: the symptom is high error on *both* train and validation.

**Connects to:** [[ai/foundations/generalization-and-overfitting|bias–variance]] ·
[[ai/machine-learning/hyperparameter-tuning|tuning λ]] ·
[[ai/machine-learning/feature-engineering|feature selection]]
