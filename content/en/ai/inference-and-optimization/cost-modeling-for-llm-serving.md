---
title: "Cost modeling for LLM serving"
description: LLM serving cost models connect traffic, token counts, model size, hardware, utilization, cache rate, retries, and quality gates.
tags: [inference, cost-modeling, unit-economics]
order: 11
updated: 2026-06-07
---
# Cost modeling for LLM serving

Cost modeling turns inference from a surprise bill into an engineering variable. The
goal is to understand cost per successful task under realistic traffic, not only cost
per token in isolation.

## Cost drivers

| Driver | What to measure |
|---|---|
| Traffic | requests per minute, burstiness, concurrency |
| Input tokens | system prompt, history, RAG context, tool output |
| Output tokens | answer length, retries, multi-step workflows |
| Model mix | model size, provider, quantization, routing |
| Hardware | GPU type, hourly cost, utilization |
| Caching | prefix, semantic, retrieval, and result cache hit rates |
| Reliability | retry rate, timeouts, failed tasks |

## Simple model

```text
cost_per_successful_task =
  total_inference_cost
  / successful_completed_tasks
```

Then split total cost by workflow, model, customer, prompt version, and error class.
The split matters more than the average.

## Scenario analysis

- What happens if traffic doubles?
- What happens if average context grows by 4x?
- What if p95 latency target requires more spare capacity?
- What if cache hit rate falls after a product change?
- What if a smaller model passes 80% of tasks and routes the rest upward?

## Pitfall

Do not calculate only provider list-price tokens. Include retries, tool loops,
observability, evals, idle capacity, human review, and failed tasks.

**Connects to:** [[ai/ai-product-engineering/pricing-vs-compute-cost|pricing vs compute cost]] ·
[[ai/ai-playbooks/measure-and-cut-inference-cost|measure and cut inference cost]] ·
[[ai/mlops/cost-optimization|MLOps cost optimization]]
