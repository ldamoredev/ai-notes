---
title: "Measure and cut inference cost"
description: A practical procedure for finding cost drivers in LLM systems and reducing spend without blindly degrading quality.
tags: [playbook, cost, inference, mlops]
order: 6
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/inference-and-optimization/index]
last_verified: 2026-07-20
---
# Measure and cut inference cost

**Mental model:** inference cost is a property of successful workflows, not requests. Context, output, retries, loops, routing, and cache misses are the numerator; verified success is the denominator.

## Mechanism: trace → attribution → constrained optimization

Use this playbook when an AI feature works but spend is too high, unpredictable, or
hard to attribute to users, workflows, prompts, models, or agents.

## Inputs

- Per-request traces with model, tokens, latency, retries, tool calls, cache hits, and outcome.
- Cost by provider, model, endpoint, customer, task, and environment.
- Eval suite that can catch quality regressions.

## Procedure

1. Break cost down by task type, model, prompt version, customer, and success/failure.
2. Separate fixed prompt tokens, retrieved-context tokens, output tokens, retries, and agent loops.
3. Identify the top cost contributors with p50, p95, and worst-case requests.
4. Remove unnecessary context before changing models.
5. Add caching for repeated semantic requests or stable intermediate results.
6. Route easy tasks to smaller or cheaper models.
7. Cap retries, agent steps, output length, and retrieval fanout.
8. Re-run evals after every cost change and compare quality, latency, and safety.

## Cost levers

| Lever | Watch for |
|---|---|
| Shorter context | lost evidence or worse grounding |
| Smaller model | format or reasoning regressions |
| Semantic cache | stale or cross-user responses |
| Fewer retries | lower recovery rate |
| Agent step cap | incomplete tasks |

## Pitfall

Cutting cost without evals often just hides quality loss. Measure cost per successful
task, not only cost per request.

**Connects to:** [[ai/mlops/cost-optimization|cost optimization]] ·
[[ai/ai-product-engineering/pricing-vs-compute-cost|pricing vs compute cost]] ·
[[ai/ai-product-engineering/semantic-caching|semantic caching]]

## Executable cost model

```python
requests, successes, cost = 120, 90, 18.0
print("cost/request", cost/requests, "cost/success", cost/successes)
```

Run with `python3`; expected output makes retries visible. Re-run holdout quality, safety, and latency gates after every optimization.

## Sources

- [vLLM](https://arxiv.org/abs/2309.06180) — serving throughput and memory management.
- [FlashAttention](https://arxiv.org/abs/2205.14135) — IO-aware attention efficiency.
- [Greenhouse Gas Protocol Scope 2 Guidance](https://ghgprotocol.org/scope_2_guidance) — electricity-accounting context.
