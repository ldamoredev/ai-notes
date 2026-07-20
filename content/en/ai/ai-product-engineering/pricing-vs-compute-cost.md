---
title: "Pricing vs compute cost"
description: AI pricing must account for variable inference cost, retries, review, margins, abuse, and product value rather than tokens alone.
tags: [ai-product, pricing, cost, unit-economics]
order: 11
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-playbooks/measure-and-cut-inference-cost]
last_verified: 2026-07-20
---
# Pricing vs compute cost

## Mechanism: unit economics → margin → routing decision

```python
price, compute, support = .20, .06, .03
print("margin", price - compute - support)
```

Run with `python3`; expected output is `margin 0.11000000000000001`. Measure successful-task cost, retries, support, and quality loss before lowering price or model quality.

## Production lens and exercises

Track gross margin by workflow, customer segment, model route, cache hit, and successful outcome. A low token price can still lose money through retries, reviewer time, support, storage, or abuse; rate limits and budgets are product controls.

1. Add a 20% retry rate and a human-review cost to the artifact.
2. Compare a flat price with usage pricing under a stated quality floor.

## Sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle risk/cost context.
- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — compute demand context.

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
