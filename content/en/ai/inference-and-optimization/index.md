---
title: Inference & Optimization
description: Serving LLMs fast and cheap - quantization, the KV cache, batching, speculative decoding, serving engines, and the cost/latency knobs that decide unit economics.
tags: [inference, optimization, serving, latency, cost]
order: 0
updated: 2026-06-07
---
# Inference & Optimization

You train a model once but **serve it forever**, so inference is where most of the cost
and latency of an AI product live. This branch is the systems side of running models:
how to make them fast, cheap, and scalable without retraining.

## Mental model

Inference is a scheduled flow of tensor kernels and memory movement under a latency objective. Prompt processing and token-by-token decoding have different bottlenecks; batching, cache policy, precision, model shape, and hardware determine the feasible quality-cost envelope.

## Roadmap: measure the workload

- [[ai/inference-and-optimization/why-inference-is-the-real-cost|Why inference is the real cost]] explains train-once, serve-forever economics.
- [[ai/inference-and-optimization/latency-vs-throughput|Latency vs throughput]] separates TTFT, prefill, decode, tokens/sec, and p95.
- [[ai/inference-and-optimization/cost-modeling-for-llm-serving|Cost modeling for LLM serving]] turns model, traffic, tokens, hardware, and cache behavior into unit economics.

## Make serving faster

- [[ai/inference-and-optimization/kv-cache-and-memory|The KV cache and memory]] covers why memory capacity and bandwidth dominate LLM serving.
- [[ai/inference-and-optimization/batching-for-llm-serving|Batching for LLM serving]] compares static, dynamic, and continuous batching.
- [[ai/inference-and-optimization/speculative-decoding|Speculative decoding]] uses a small draft model to accelerate larger-model decoding.
- [[ai/inference-and-optimization/flashattention-and-efficient-attention|FlashAttention and efficient attention]] reduces memory movement in attention kernels.

## Make serving cheaper

- [[ai/inference-and-optimization/quantization-for-inference|Quantization for inference]] covers int8, 4-bit, GPTQ, AWQ, and what can degrade.
- [[ai/inference-and-optimization/prefix-and-semantic-caching|Prefix and semantic caching]] avoids repeated work at the prompt and product layers.
- [[ai/inference-and-optimization/right-sizing-models|Right-sizing models]] compares smaller models, distillation, routing, and task decomposition.

## Run it in production

- [[ai/inference-and-optimization/serving-engines|Serving engines]] maps vLLM, TGI, TensorRT-LLM, and framework-level tradeoffs.
- [[ai/inference-and-optimization/gpu-and-hardware-basics|GPU and hardware basics]] explains VRAM, bandwidth, compute, interconnects, and utilization.

**Connects to:** [[ai/llms/from-prompt-to-generated-token|From Prompt to Generated Token]] · [[ai/mlops/index|MLOps]] · [[ai/ai-product-engineering/latency-cost-quality-triangle|Latency, Cost, and Quality]]

## Core sources

- [vLLM paper](https://arxiv.org/abs/2309.06180) — PagedAttention and serving-throughput evaluation.
- [FlashAttention](https://arxiv.org/abs/2205.14135) — IO-aware exact attention.
- [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) — exact speculative decoding and speed analysis.
- [GPTQ](https://arxiv.org/abs/2210.17323) — post-training quantization for generative transformers.
- [Hugging Face KV cache strategies](https://huggingface.co/docs/transformers/kv_cache) — current cache implementations and trade-offs.
