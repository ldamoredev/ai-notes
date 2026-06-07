---
title: "Serving and inference"
description: Serving turns model behavior into a production API with latency, throughput, batching, fallback, and reliability constraints.
tags: [mlops, serving, inference, latency]
order: 9
updated: 2026-06-07
---
# Serving and inference

Serving is where model quality meets product constraints. A model that is excellent
offline may be unusable if it is too slow, too expensive, hard to batch, or unreliable
under traffic.

## Serving constraints

| Constraint | Question |
|---|---|
| Latency | How long can the user wait? |
| Throughput | How many requests per second must the system handle? |
| Cost | What does each request spend? |
| Availability | What happens when the model/API fails? |
| Variability | How stable are outputs and timings? |

For LLMs, latency includes prompt assembly, retrieval, model generation, tool calls,
post-processing, and streaming behavior.

## Inference levers

- Batch requests when latency budget allows.
- Cache deterministic or repeated work.
- Use smaller models for simple tasks.
- Stream tokens when perceived latency matters.
- Use quantization or optimized runtimes for local models.
- Add fallbacks for model/API failure.

## Product contracts

Define timeouts, retries, fallback copy, escalation paths, and partial-response behavior.
The user experience should not depend on the model always being fast and correct.

## Pitfall

Optimizing model latency alone misses system latency. Retrieval, reranking, tools, and
post-processing can dominate the request path.

**Connects to:** [[ai/llms/quantization-and-inference|quantization and inference]] ·
[[ai/rag-and-retrieval/reranking|reranking]] ·
[[ai/ai-product-engineering/index|product constraints]]
