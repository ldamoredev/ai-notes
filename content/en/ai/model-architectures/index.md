---
title: Model Architectures
description: Architectural mechanisms that route information and computation across space, time, tokens, experts, and denoising trajectories.
tags: [architectures, attention, transformers, diffusion]
order: 0
updated: 2026-07-19
status: current
level: intermediate
---
# Model Architectures

An architecture specifies a parameterized computation and its inductive biases: which interactions are cheap, which information paths exist, which symmetries are encoded, and how cost scales with input size.

## Mental model

CNNs reuse local filters across space. RNNs compress history into recurrent state. Attention creates content-dependent interactions. Transformers compose attention and per-token transformations with residual pathways. State-space models propagate structured latent state. Diffusion models learn iterative denoising. No architecture is universally best; each moves cost and bias.

## Current foundation note

- [[ai/model-architectures/self-attention-from-first-principles|Self-Attention from First Principles]]

## Candidate note roadmap

- `convolutions-cnns-and-spatial-bias` — kernels, receptive fields, equivariance, and hierarchy.
- `rnns-lstms-and-sequence-state` — recurrence, gating, gradient paths, and serial cost.
- `transformer-block-from-first-principles` — attention, MLP, residual streams, normalization, and shapes.
- `encoder-decoder-and-cross-attention` — representation, conditioning, and sequence transduction.
- `mixture-of-experts` — sparse routing, load balancing, capacity, and distributed cost.
- `state-space-models` — recurrence, convolution views, selective state, and tradeoffs.
- `autoregressive-and-energy-based-perspectives` — factorization, scoring, normalization, and sampling.
- `diffusion-architecture-and-denoising-objectives` — U-Nets/DiTs, schedules, conditioning, and sampling.
- `foundation-models-as-platforms` — pretraining breadth, adaptation surfaces, and operational implications.

## Comparison rule

Compare architectures by information path, inductive bias, asymptotic and measured cost, memory traffic, trainability, data regime, and the task's evaluation—not by release recency.

**Connects to:** [[ai/deep-learning/index|Deep Learning]] · [[ai/llms/the-decoder-transformer|The Decoder Transformer]] · [[ai/multimodal-and-generative/index|Vision, Audio and Multimodal AI]]

## Core sources

- [Deep Learning](https://www.deeplearningbook.org/) — canonical foundations for neural architectures and optimization.
- [Dive into Deep Learning](https://d2l.ai/) — executable architecture implementations with shape-level explanations.
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — original Transformer architecture.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — Vision Transformer and its data/scale result.
