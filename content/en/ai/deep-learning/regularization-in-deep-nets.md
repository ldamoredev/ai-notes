---
title: "Regularization: dropout, weight decay & augmentation"
description: Big networks overfit easily. The deep-learning-specific tools that keep them honest — dropout, weight decay, early stopping, and data augmentation.
tags: [deep-learning, regularization, dropout, augmentation]
order: 5
updated: 2026-06-07
---
# Regularization: dropout, weight decay & augmentation

Deep nets have enough capacity to memorize their training set, so controlling
[[ai/foundations/generalization-and-overfitting|overfitting]] is central. These are
the same idea as classical [[ai/machine-learning/regularization-l1-l2|L1/L2
regularization]] — penalize complexity — wearing deep-learning clothes.

## The toolkit

- **Dropout** — during training, randomly zero a fraction of activations each step.
  No neuron can rely on a specific partner, so the network learns redundant, robust
  features (an implicit ensemble). Turned **off** at inference.
- **Weight decay** — shrink weights toward zero each step (L2 by another name; baked
  into [[ai/deep-learning/optimizers|AdamW]]). Keeps the function smoother.
- **Early stopping** — stop when validation loss starts rising. Free, effective,
  always worth wiring up.
- **Data augmentation** — expand the dataset with label-preserving transforms (flip/
  crop/rotate images; paraphrase/back-translate text). Often the **biggest** real-world
  win because it attacks the root cause: not enough data.
- **Batch/Layer norm** also regularize as a side effect.

## How much to use

Regularization trades a little training fit for better generalization. The
[[ai/machine-learning/error-analysis|learning curve]] tells you which way to push: a
big train-vs-validation gap → add regularization; high error on both → you're
*under*fitting, so back off.

> The strongest regularizer is almost always **more and better data**. Reach for
> data and augmentation before stacking dropout on dropout.

## Pitfall

Leaving dropout on at inference, or forgetting `model.eval()` in PyTorch, silently
degrades predictions. And too much dropout + weight decay together can underfit —
the symptom is training loss that won't go down.

**Connects to:** [[ai/foundations/generalization-and-overfitting|overfitting]] ·
[[ai/machine-learning/regularization-l1-l2|L1/L2]] ·
[[ai/deep-learning/training-dynamics|training dynamics]]
