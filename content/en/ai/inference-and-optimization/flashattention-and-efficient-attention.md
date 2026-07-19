---
title: "FlashAttention and efficient attention"
description: FlashAttention speeds transformer attention by reducing memory reads and writes, making attention more IO-aware.
tags: [inference, attention, flashattention, kernels]
order: 7
updated: 2026-06-07
---
# FlashAttention and efficient attention

Attention is mathematically simple but expensive to run naively. FlashAttention improves
attention performance by organizing computation to reduce memory movement between GPU
high-bandwidth memory and faster on-chip memory.

## The bottleneck

Transformer attention computes interactions between tokens. Naive implementations can
materialize large intermediate matrices, which costs memory and bandwidth. On modern
GPUs, moving bytes is often the bottleneck, not the arithmetic itself.

## What FlashAttention changes

| Idea | Effect |
|---|---|
| Tiling | process attention in blocks that fit on-chip |
| IO awareness | minimize high-bandwidth-memory reads and writes |
| Fused operations | avoid materializing unnecessary intermediates |
| Exact attention | preserve the same mathematical result, not an approximation |

## Where efficient attention matters

- Long-context prefill.
- High-throughput serving.
- Training and fine-tuning large transformers.
- Multimodal models with many visual or audio tokens.
- Serving stacks that rely on optimized kernels.

## Pitfall

Efficient kernels are workload- and hardware-dependent. Benchmark the actual sequence
lengths, batch sizes, model architecture, and serving engine you plan to run.

**Connects to:** [[ai/model-architectures/self-attention-from-first-principles|attention]] ·
[[ai/llms/transformer-attention-map|attention maps]] ·
[[ai/inference-and-optimization/gpu-and-hardware-basics|hardware basics]]
