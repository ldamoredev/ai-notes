---
title: "Initialization & normalization"
description: How you start the weights and keep activations well-scaled decides whether a deep net trains at all. Xavier/He init, BatchNorm vs LayerNorm.
tags: [deep-learning, initialization, batchnorm, layernorm]
order: 3
updated: 2026-06-07
---
# Initialization & normalization

Deep networks are finicky about the **scale of numbers** flowing through them. Start
the weights wrong or let activations drift, and gradients vanish or explode and
training stalls. Two families of tricks keep the signal in a healthy range.

## Initialization: where you start matters

If initial weights are too large, activations and gradients blow up; too small and
they shrink to nothing over many layers. Principled schemes set the initial scale so
variance is preserved layer to layer:

- **Xavier/Glorot** — for tanh/sigmoid-style activations.
- **He/Kaiming** — for [[ai/deep-learning/activation-functions|ReLU]]-family
  activations (the common default today).

Never initialize all weights to the same constant — neurons would stay identical
forever (symmetry). Randomness breaks the symmetry so neurons specialize.

## Normalization: keep activations well-behaved

Normalization layers rescale activations during training so each layer sees a stable
distribution, which lets you use higher [[ai/deep-learning/optimizers|learning
rates]] and train deeper.

| Norm | Normalizes over | Used in |
|---|---|---|
| **BatchNorm** | the batch dimension (per feature) | CNNs / vision |
| **LayerNorm** | the feature dimension (per example) | transformers / [[ai/llms/index|LLMs]], RNNs |

LayerNorm won in transformers because it doesn't depend on batch statistics — it
behaves the same for batch size 1 or 1000 and for variable-length sequences, which
matters for language.

## Why it works (the short version)

Normalization smooths the loss landscape, reducing the chance that a layer's update
wildly shifts the inputs of the next layer ("internal covariate shift" is the
classic, if debated, explanation). Residual connections + LayerNorm are what make
100+ layer transformers trainable.

## Pitfall

A network that won't learn (flat or NaN loss) is very often init/normalization or
[[ai/deep-learning/optimizers|learning rate]] — check those before architecture.

**Connects to:** [[ai/computation-and-autodiff/backpropagation-from-first-principles|vanishing gradients]] ·
[[ai/deep-learning/optimizers|optimizers]] ·
[[ai/llms/index|LayerNorm in transformers]]
