---
title: "Pricing vs compute cost"
description: AI pricing must account for variable inference cost, retries, review, margins, abuse, and product value rather than tokens alone.
tags: [ai-product, pricing, cost, unit-economics]
order: 11
updated: 2026-06-07
---
# Pricing vs compute cost

AI features often have variable marginal cost. Pricing has to cover model calls,
retrieval, tools, retries, human review, abuse controls, and support — while still
matching the value users perceive.

## Cost is not just tokens

| Cost | Example |
|---|---|
| Model inference | Input/output tokens or local GPU time |
| Retrieval | Embedding, vector search, reranking |
| Tool calls | External APIs, web fetches, code execution |
| Review | Human approval and correction time |
| Retries | Invalid output, timeout, user regeneration |
| Observability | Trace storage and eval pipelines |

Unit economics should be measured per successful task, not per model call.

## Pricing patterns

- Seat-based pricing when usage is predictable.
- Credits or metered usage when cost varies widely.
- Tiered limits for model quality, context length, and automation.
- Enterprise pricing when review, compliance, or data isolation dominates.

## Guard against abuse

Rate limits, quotas, model routing, and caching are pricing controls as much as
technical controls. Unbounded "AI included" can become margin leakage.

## Pitfall

Charging per token can expose cost but obscure value. Users buy completed work, not
inference units.

**Connects to:** [[ai/mlops/cost-optimization|cost optimization]] ·
[[ai/ai-product-engineering/product-metrics-for-ai|product metrics]] ·
[[ai/ai-product-engineering/latency-cost-quality-triangle|cost-quality tradeoff]]
