---
title: "Why inference is the real cost"
description: Training is a large upfront expense, but inference repeats for every user request and often dominates product unit economics.
tags: [inference, cost, serving]
order: 1
updated: 2026-06-07
---
# Why inference is the real cost

Training can be spectacularly expensive, but production inference is the recurring bill.
Every prompt, completion, retry, agent step, embedding lookup, and background eval turns
model capability into ongoing cost.

## Train once, serve forever

| Cost type | Shape | Example driver |
|---|---|---|
| Training | large upfront batch | data, GPUs, experiments |
| Fine-tuning | smaller repeated batch | adapters, evals, reruns |
| Inference | per request forever | traffic, tokens, latency target |
| Observability | per trace | logs, storage, replay |
| Evaluation | per release and monitor | judges, test suites, human review |

For many products, inference cost scales with adoption. That makes it a product and
business constraint, not only an infrastructure detail.

## What drives inference spend

- Input tokens: system prompt, history, retrieved context, tool results.
- Output tokens: generated answer length and retries.
- Model size: parameters, memory footprint, and hardware tier.
- Latency target: lower p95 often requires more capacity.
- Utilization: idle GPUs are expensive even when no tokens are generated.
- Agent loops: multiple model calls and tool calls per user task.

## Design implication

Inference-aware systems avoid doing unnecessary work: shorter context, smaller models
for easy tasks, caching, batching, streaming UX, and routing. The goal is cost per
successful task, not the cheapest single model call.

## Pitfall

Do not optimize cost only after launch. Prompt shape, RAG design, model choice, and UX
all lock in the token and latency profile before infrastructure gets involved.

**Connects to:** [[ai/ai-product-engineering/pricing-vs-compute-cost|pricing vs compute cost]] ·
[[ai/mlops/cost-optimization|cost optimization]] ·
[[ai/inference-and-optimization/cost-modeling-for-llm-serving|cost modeling]]
