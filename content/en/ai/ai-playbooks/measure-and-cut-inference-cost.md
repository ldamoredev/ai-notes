---
title: "Measure and cut inference cost"
description: A practical procedure for finding cost drivers in LLM systems and reducing spend without blindly degrading quality.
tags: [playbook, cost, inference, mlops]
order: 6
updated: 2026-06-07
---
# Measure and cut inference cost

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
