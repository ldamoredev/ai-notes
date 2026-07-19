---
title: Phase 03 — Training and Inference
description: The systems that fit, adapt, load, schedule, optimize, and serve models under hardware and reliability constraints.
tags: [phase, training, inference, systems]
order: 6
updated: 2026-07-19
---
# Phase 03 — Training and Inference

Training and inference execute related graphs under different constraints. Training stores activations and gradients to update parameters; inference optimizes loading, memory traffic, batching, caching, and response latency.

## Mental model

Training is a repeated measure-and-update system; inference is a scheduled read-only execution system. Both are bounded by tensor shapes, memory movement, precision, parallelism, and reliability requirements.

## Roadmap through the branches

- [[ai/fine-tuning-and-alignment/index|Training and Adaptation]]
- [[ai/inference-and-optimization/index|Inference Systems]]

## Exit criteria

You can describe data/model/pipeline parallelism, mixed precision, checkpointing, adaptation methods, prefill versus decode, KV-cache pressure, continuous batching, quantization, and latency-throughput-cost tradeoffs.

**Connects to:** [[ai/phase-02-learning-and-models|Phase 02 — Learning and Models]] · [[ai/phase-04-context-and-agency|Phase 04 — Context and Agency]]

## Core sources

- [PyTorch Distributed Overview](https://pytorch.org/tutorials/beginner/dist_overview.html) — training parallelism primitives.
- [QLoRA](https://arxiv.org/abs/2305.14314) — memory-efficient adaptation.
- [vLLM](https://arxiv.org/abs/2309.06180) — memory-aware high-throughput serving.
