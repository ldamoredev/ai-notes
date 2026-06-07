---
title: "Latency vs cost vs quality"
description: AI product work is a three-way tradeoff: better models and richer context improve quality but usually increase latency and cost.
tags: [ai-product, latency, cost, quality]
order: 3
updated: 2026-06-07
---
# Latency vs cost vs quality

AI product decisions usually move along a triangle: latency, cost, and quality. Larger
models, longer context, tool calls, and reranking can improve quality, but they often
increase latency and spend.

## The tradeoff table

| Choice | Quality | Latency | Cost |
|---|---|---|---|
| Larger model | Often higher | Slower | Higher |
| More retrieved context | Better grounding if relevant | Slower | Higher tokens |
| Reranking | Better retrieval precision | Extra step | Extra call/compute |
| Tool call | Fresh/actionable data | Network wait | External cost |
| Smaller model | Lower ceiling | Faster | Lower |

The right point depends on the user moment. Drafting a legal clause has a different
budget than autocomplete.

## Segment the task

Use the strongest path only where it matters:

- Route easy tasks to cheaper models.
- Use retrieval only when the answer needs external context.
- Use reranking only for ambiguous or high-stakes queries.
- Use structured outputs for deterministic downstream logic.
- Escalate uncertain cases to humans or stronger models.

## Measure successful task cost

Cost per call is incomplete. Measure cost per accepted answer, completed workflow, or
resolved case. A cheap answer that users reject is expensive.

## Pitfall

Optimizing one vertex blindly damages the others. A "fast" feature users cannot trust
is not fast; it just moves work to review and correction.

**Connects to:** [[ai/mlops/cost-optimization|cost optimization]] ·
[[ai/mlops/serving-and-inference|serving]] ·
[[ai/ai-product-engineering/product-metrics-for-ai|product metrics]]
