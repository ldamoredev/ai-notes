---
title: "Activation functions & why nonlinearity matters"
description: Without a nonlinearity, a deep net is just a linear model. Why ReLU won, what dead neurons are, and where GELU fits in modern transformers.
tags: [deep-learning, activations, relu, gelu]
order: 2
updated: 2026-06-07
---
# Activation functions & why nonlinearity matters

The activation is the **nonlinear** step between linear layers. Remove it and a
hundred stacked layers collapse algebraically into one linear layer — no extra
power. The nonlinearity is what lets a network bend, fold, and carve complex
decision boundaries.

## Why nonlinearity is non-negotiable

A composition of linear functions is still linear. Nonlinear activations let each
layer reshape space so the next layer's [[ai/machine-learning/linear-and-logistic-regression|linear
boundary]] can separate things that weren't linearly separable before. Depth only
buys you anything *because* of activations.

## The usual suspects

| Activation | Shape | Notes |
|---|---|---|
| **Sigmoid / tanh** | squashing | classic; saturate and kill gradients in deep nets |
| **ReLU** | `max(0, x)` | the default workhorse — cheap, sparse, avoids saturation for positive inputs |
| **Leaky ReLU / ELU** | ReLU with a small negative slope | fixes dead neurons |
| **GELU / SiLU** | smooth, ReLU-like | standard inside transformers and modern nets |

## Why ReLU changed deep learning

Sigmoids saturate: their gradient goes to ~0 for large-magnitude inputs, so deep
stacks suffer [[ai/deep-learning/neural-networks-and-backprop|vanishing gradients]]
and barely train. ReLU keeps a gradient of 1 for positive inputs, so signal flows
through deep networks — a big reason training deep nets became practical.

## The dead-ReLU pitfall

A ReLU neuron that only ever sees negative inputs outputs 0 forever and its gradient
is 0 — it's **dead** and never recovers. Causes: too-high
[[ai/deep-learning/optimizers|learning rate]] or bad
[[ai/deep-learning/initialization-and-normalization|initialization]]. Leaky variants
or careful init prevent it.

> Default to ReLU; reach for GELU/SiLU in transformers. The output layer is separate
> — it uses softmax (classification) or none (regression), matched to the
> [[ai/deep-learning/loss-functions-in-dl|loss]].

**Connects to:** [[ai/deep-learning/neural-networks-and-backprop|backprop]] ·
[[ai/deep-learning/initialization-and-normalization|init & norm]] ·
[[ai/llms/index|GELU in transformers]]
