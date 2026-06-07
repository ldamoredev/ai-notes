---
title: "Batching for LLM serving"
description: Batching improves GPU utilization, but LLM serving needs dynamic and continuous batching because requests have different prompt and output lengths.
tags: [inference, batching, serving, throughput]
order: 5
updated: 2026-06-07
---
# Batching for LLM serving

Batching lets the GPU process multiple requests together. For LLMs, batching is tricky
because each request has different prompt length, output length, arrival time, and
stopping condition.

## Batching types

| Type | How it works | Tradeoff |
|---|---|---|
| Static batching | fixed batch formed before processing | simple but wastes capacity |
| Dynamic batching | briefly waits to group arrivals | higher throughput, possible TTFT delay |
| Continuous batching | adds and removes requests during generation | high utilization, complex scheduler |

Continuous batching is valuable because decode steps are sequential and requests finish
at different times.

## What batching optimizes

- GPU utilization.
- Tokens/sec across all users.
- Cost per generated token.
- Serving capacity under bursty traffic.

It can also increase queueing delay if the scheduler waits too long to form efficient
batches.

## Scheduler considerations

- Separate prefill and decode workloads where useful.
- Avoid one long request blocking many short requests.
- Track per-tenant fairness and priority.
- Combine batching with KV-cache management.
- Monitor TTFT and p95, not only throughput.

## Pitfall

Batching is not a free win for interactive products. A system can be efficient and feel
slow if users spend too long waiting for their first token.

**Connects to:** [[ai/inference-and-optimization/latency-vs-throughput|latency vs throughput]] ·
[[ai/inference-and-optimization/kv-cache-and-memory|KV cache]] ·
[[ai/mlops/serving-and-inference|serving]]
