---
title: "Choose a model for production"
description: Choose the least-cost model configuration that clears held-out product-quality, safety, reliability, latency, privacy, and operational thresholds.
tags: [playbook, model-selection, production]
order: 9
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/evaluation/model-vs-product-evals, ai/inference-and-optimization/index]
last_verified: 2026-07-20
---
# Choose a model for production

**Mental model:** model selection is constrained optimization over a real workload, not a leaderboard lookup. A model is admissible only after it passes product tasks, safety and schema rules, latency/cost budgets, provider/data constraints, and a rollback plan. Optimize cost only among admissible options.

## Mechanism: evaluate → constrain → route

Fix the task distribution, run equivalent versioned evals across candidates, reject any that miss a non-negotiable gate, then choose the lowest-cost remaining configuration. Deploy it behind a monitored fallback. Re-run the selection whenever the model snapshot, prompt, routing, tools, provider, or traffic changes.

```python
candidates = [{"name":"A", "quality":.91, "p95":1.8, "cost":.03}, {"name":"B", "quality":.89, "p95":1.1, "cost":.01}]
eligible = [m for m in candidates if m["quality"] >= .90 and m["p95"] <= 2]
print(min(eligible, key=lambda m: m["cost"])["name"])
```

Run with `python3`; expected output is `A`: B is cheaper but fails quality. A production chooser adds safety, availability, region, and data-policy gates.

## Procedure

1. Define acceptance thresholds, critical slices, prohibited outcomes, and p95 budgets.
2. Shortlist by data policy, region, context, tool/schema support, rate limit, and fallback compatibility.
3. Measure holdout success, refusal quality, schema validity, retries, tokens, latency, and cost per successful task.
4. Inspect slice and adversarial failures; reject a model that only improves the aggregate.
5. Record the decision and deploy with alerts and a tested fallback.

| Dimension | Gate |
|---|---|
| Quality | holdout success by critical slice |
| Reliability | schema/tool validity and retry rate |
| Safety | forbidden-action and escalation tests |
| Operations | p95 latency, capacity, observability, fallback |
| Governance | data policy, region, retention, vendor terms |

Public benchmarks are priors, not product evidence. Roll back when a critical slice or safety gate fails even if average quality improves.

## Exercises

1. Add a 99.5% schema-validity constraint to the artifact.
2. Write a fallback test for a forced provider outage.

**Connects to:** [[ai/evaluation/model-vs-product-evals|product evals]] · [[ai/evaluation/public-benchmarks-and-limits|benchmarks]] · [[ai/mlops/serving-and-inference|serving]] · [[ai/agents-and-tools/evaluating-agents|agent evals]]

## Sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk-based selection context.
- [HELM](https://crfm.stanford.edu/helm/) — transparent multi-scenario evaluation.
- [OpenAI model-selection guide](https://platform.openai.com/docs/guides/model-selection) — provider model tradeoffs.
