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

## Measure the workload

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

## Core sources

- Lilian Weng, **Large Transformer Model Inference Optimization**.
- vLLM documentation, especially PagedAttention; Hugging Face **Text Generation Inference** docs.
- Dao et al., **FlashAttention**; Leviathan et al., **Speculative Decoding**; **GPTQ** and **AWQ** papers.
- NVIDIA technical material on **TensorRT-LLM** and inference quantization.
- Chip Huyen, **AI Engineering**, especially inference, latency, and cost chapters.
