---
title: "Latency vs throughput"
description: LLM serving separates user-facing latency from system throughput, with different bottlenecks in prefill, decode, TTFT, and tokens per second.
tags: [inference, latency, throughput, serving]
order: 2
updated: 2026-06-07
---
# Latency vs throughput

Latency is what one user feels. Throughput is how much work the system finishes per
unit time. LLM serving optimizes both, but the knobs often trade against each other.

## Key latency terms

| Term | Meaning |
|---|---|
| TTFT | time to first token, dominated by queueing and prefill |
| Prefill | processing input tokens and building the KV cache |
| Decode | generating output tokens one step at a time |
| Tokens/sec | generation rate after the first token |
| p95 latency | slow-tail user experience |
| Queueing delay | time waiting for capacity or batch formation |

Long prompts make prefill expensive. Long answers make decode expensive.

## Throughput knobs

- Larger batches improve GPU utilization.
- Continuous batching keeps the GPU busy as requests start and finish.
- Quantization can fit more requests or larger models in memory.
- Prefix caching avoids repeated prefill for shared prompt prefixes.
- Routing easy tasks to smaller models frees larger-model capacity.

## UX implications

Streaming improves perceived latency because users see progress after TTFT. It does not
reduce total compute by itself. A product can feel fast with a good TTFT and streaming
even if total completion time is unchanged.

## Pitfall

Optimizing aggregate tokens/sec can hurt users if queueing delay grows. Track TTFT,
p95, and task completion time, not just hardware throughput.

**Connects to:** [[ai/ai-product-engineering/streaming-and-perceived-latency|streaming latency]] ·
[[ai/inference-and-optimization/batching-for-llm-serving|batching]] ·
[[ai/mlops/serving-and-inference|serving and inference]]
