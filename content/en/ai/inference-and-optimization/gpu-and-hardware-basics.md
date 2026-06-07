---
title: "GPU and hardware basics"
description: LLM inference is often limited by VRAM capacity, memory bandwidth, interconnects, utilization, and the shape of prefill versus decode workloads.
tags: [inference, gpu, hardware, memory-bandwidth]
order: 9
updated: 2026-06-07
---
# GPU and hardware basics

Inference optimization only makes sense when you understand the hardware bottleneck.
For LLMs, the limiting factor is often memory capacity and memory bandwidth, especially
during token-by-token decoding.

## Hardware terms

| Term | Why it matters |
|---|---|
| VRAM capacity | determines which model, batch, and KV cache fit |
| Memory bandwidth | determines how fast weights and cache can be read |
| FLOPs | matters more in compute-heavy prefill than decode |
| Interconnect | affects multi-GPU model parallel serving |
| Utilization | idle GPU time becomes wasted cost |
| Host memory and CPU | can bottleneck tokenization, routing, or data movement |

## Prefill vs decode hardware profile

- Prefill processes many input tokens and can use parallel compute efficiently.
- Decode generates one token at a time and repeatedly reads model weights and KV cache.
- Long contexts increase memory pressure.
- High concurrency increases cache and scheduling pressure.

## Deployment choices

- Single GPU for smaller or quantized models.
- Tensor parallelism when one model does not fit or needs more throughput.
- CPU or edge inference for small models and privacy-sensitive workloads.
- Managed inference when operational simplicity matters more than low-level control.

## Pitfall

GPU utilization alone can mislead. A server can show high utilization while users still
experience bad TTFT, poor p95 latency, or excessive queueing.

**Connects to:** [[ai/inference-and-optimization/latency-vs-throughput|latency vs throughput]] ·
[[ai/inference-and-optimization/quantization-for-inference|quantization]] ·
[[ai/mlops/cost-optimization|cost optimization]]
