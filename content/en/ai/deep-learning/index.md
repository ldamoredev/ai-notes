---
title: Deep Learning
description: How neural networks actually learn representations — backprop, architectures, the training tricks that make them work, and why scale matters.
tags: [deep-learning, neural-networks]
order: 0
updated: 2026-06-07
---
# Deep Learning

Deep learning is what happens when you stack many simple, differentiable layers and
let [[ai/foundations/gradient-descent-intuition|gradient descent]] discover the
features instead of hand-engineering them. That single shift — **learned
representations over crafted features** — is why it took over vision, speech, and
language, and it's the substrate every [[ai/llms/index|LLM]] is built on.

> A neural network is a stack of [[ai/machine-learning/linear-and-logistic-regression|linear
> models]] separated by nonlinearities, trained end to end by backprop. Everything
> else is making that train stably at scale.

## How a network learns

- [[ai/deep-learning/neural-networks-and-backprop|Neural networks & backpropagation]]
- [[ai/deep-learning/activation-functions|Activation functions & why nonlinearity matters]]
- [[ai/deep-learning/loss-functions-in-dl|Loss functions in deep learning]]

## Making training work

- [[ai/deep-learning/initialization-and-normalization|Initialization & normalization]]
- [[ai/deep-learning/optimizers|Optimizers: from SGD to AdamW]]
- [[ai/deep-learning/regularization-in-deep-nets|Regularization: dropout, weight decay & augmentation]]
- [[ai/deep-learning/training-dynamics|Training dynamics: schedules, warmup & debugging]]

## Architectures

- [[ai/deep-learning/cnns|CNNs: convolution & spatial structure]]
- [[ai/deep-learning/rnns-and-their-limits|RNNs & their limits]]
- [[ai/deep-learning/attention-mechanism|The attention mechanism]]

## Representations & scale

- [[ai/deep-learning/embeddings-and-latent-spaces|Embeddings & latent spaces]]
- [[ai/deep-learning/scaling-laws|Scaling laws: why bigger keeps working]]

## Core sources

- Andrej Karpathy — *Neural Networks: Zero to Hero* (micrograd → makemore → GPT).
- 3Blue1Brown — *Neural Networks* series (visual intuition for backprop).
- *Dive into Deep Learning* (d2l.ai) — runnable, comprehensive.
- Goodfellow, Bengio, Courville — *Deep Learning* (the reference text).
- Stanford CS231n; Distill.pub for visual explanations.
