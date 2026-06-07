---
title: "Serving engines"
description: Serving engines such as vLLM, TGI, and TensorRT-LLM package scheduling, batching, KV-cache management, kernels, APIs, and deployment concerns.
tags: [inference, serving, vllm, tgi, tensorrt-llm]
order: 8
updated: 2026-06-07
---
# Serving engines

A serving engine is the runtime that turns a model checkpoint into a production API.
It handles batching, scheduling, KV cache, kernels, streaming, quantization support,
metrics, and operational integration.

## Common engines

| Engine | Strength |
|---|---|
| vLLM | high-throughput serving, PagedAttention, OpenAI-compatible APIs |
| TGI | Hugging Face ecosystem integration and production serving features |
| TensorRT-LLM | NVIDIA-optimized inference and deployment stack |
| llama.cpp-style runtimes | local and CPU/GPU edge deployment |
| Managed APIs | operational simplicity, less hardware control |

## Selection criteria

- Model architecture and weight format support.
- Quantization support.
- Continuous batching and KV-cache strategy.
- Streaming API and structured-output compatibility.
- Metrics, tracing, and autoscaling integration.
- Hardware support and deployment environment.
- Team ability to operate and debug it.

## Production concerns

Serving engines still need capacity planning, safety checks, rate limits, model
versioning, rollback, observability, and data governance. The runtime does not replace
the product's release process.

## Pitfall

Do not choose an engine from a benchmark headline alone. Match it to your model,
traffic shape, latency target, hardware, and operational maturity.

**Connects to:** [[ai/mlops/serving-and-inference|serving and inference]] ·
[[ai/inference-and-optimization/kv-cache-and-memory|KV cache]] ·
[[ai/inference-and-optimization/batching-for-llm-serving|batching]]
