---
title: Deep Learning
description: How neural networks actually learn representations — backprop, architectures, the training tricks that make them work, and why scale matters.
tags: [deep-learning, neural-networks]
order: 0
updated: 2026-06-07
---
# Deep Learning

Deep learning is what happens when you stack many simple, differentiable layers and
let [[ai/mathematics-for-ai/gradient-descent-and-optimization|gradient descent]] discover the
features instead of hand-engineering them. That single shift — **learned
representations over crafted features** — is why it took over vision, speech, and
language, and it's the substrate every [[ai/llms/index|LLM]] is built on.

> A neural network is a stack of [[ai/machine-learning/linear-and-logistic-regression|linear
> models]] separated by nonlinearities, trained end to end by backprop. Everything
> else is making that train stably at scale.

## Mental model

Deep learning composes differentiable transformations so useful representations can be learned with the task. Architecture determines information paths; the objective supplies pressure; backpropagation assigns local credit; optimization and numerical systems make the process viable at scale.

## Roadmap: how a network learns

- [[ai/computation-and-autodiff/backpropagation-from-first-principles|Neural networks & backpropagation]]
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
- [[ai/model-architectures/self-attention-from-first-principles|The attention mechanism]]

## Representations & scale

- [[ai/deep-learning/embeddings-and-latent-spaces|Embeddings & latent spaces]]
- [[ai/deep-learning/scaling-laws|Scaling laws: why bigger keeps working]]

## Paradigms & strategy

- [[ai/reinforcement-learning/reinforcement-learning-essentials|Reinforcement learning, the essentials]] covers reward, policy, and the paradigm behind RLHF and reasoning models.
- [[ai/deep-learning/the-bitter-lesson|The bitter lesson]] explains why general, compute-hungry methods keep beating hand-crafted structure.

**Connects to:** [[ai/computation-and-autodiff/index|Computation and Autodiff]] · [[ai/model-architectures/index|Model Architectures]] · [[ai/llms/index|Language and Foundation Models]]

## Core sources

- [Deep Learning](https://www.deeplearningbook.org/) — canonical reference for feed-forward networks, optimization, and regularization.
- [Dive into Deep Learning](https://d2l.ai/) — executable implementations with equations and tensor shapes.
- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — mechanism-first implementations from scalar autodiff to GPT.
- [Stanford CS231n](https://cs231n.github.io/) — convolutional networks, optimization, and practical training diagnostics.
