---
title: Sistemas de Inferencia
description: Carga, memoria, kernels, KV cache, batching, quantization, routing, latencia, throughput y costo de servir modelos.
tags: [inference, serving, optimization, hardware]
order: 0
updated: 2026-07-19
---
# Sistemas de Inferencia

Inferencia es un sistema de memoria, cómputo y scheduling. El mismo modelo puede tener comportamiento operativo radicalmente distinto según hardware, precisión, tamaño de batch, patrón de prompts, caching y motor de serving.

## Modelo mental

Prefill y decode tienen cuellos distintos. Batching, KV cache, precisión, forma del modelo y hardware determinan juntos el sobre viable de latencia, throughput, memoria y costo.

## Hoja de ruta

- [[ai/inference-and-optimization/why-inference-is-the-real-cost|Por qué inferencia concentra el costo]]
- [[ai/inference-and-optimization/latency-vs-throughput|Latencia vs throughput]]
- [[ai/inference-and-optimization/gpu-and-hardware-basics|Fundamentos de GPU y hardware]]
- [[ai/inference-and-optimization/kv-cache-and-memory|KV cache y memoria]]
- [[ai/inference-and-optimization/batching-for-llm-serving|Batching]]
- [[ai/inference-and-optimization/quantization-for-inference|Quantization]]
- [[ai/inference-and-optimization/flashattention-and-efficient-attention|FlashAttention]]
- [[ai/inference-and-optimization/speculative-decoding|Speculative decoding]]
- [[ai/inference-and-optimization/prefix-and-semantic-caching|Prefix y semantic caching]]
- [[ai/inference-and-optimization/serving-engines|Motores de serving]]
- [[ai/inference-and-optimization/right-sizing-models|Right-sizing]]
- [[ai/inference-and-optimization/cost-modeling-for-llm-serving|Modelado de costo]]

**Conecta con:** [[ai/computation-and-autodiff/index|Computación y Autodiff]] · [[ai/llms/from-prompt-to-generated-token|Del prompt al token generado]] · [[ai/mlops/serving-and-inference|Serving e inferencia]]

## Fuentes principales

- [vLLM](https://docs.vllm.ai/) — serving y continuous batching.
- [PagedAttention](https://arxiv.org/abs/2309.06180) · [FlashAttention](https://arxiv.org/abs/2205.14135) · [Speculative Decoding](https://arxiv.org/abs/2211.17192) — mecanismos primarios.
