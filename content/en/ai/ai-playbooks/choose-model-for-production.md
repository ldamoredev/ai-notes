---
title: "Choose a model for production"
description: A decision procedure for selecting a production model using product evals, cost, latency, safety, reliability, context needs, and operational constraints.
tags: [playbook, model-selection, production]
order: 9
updated: 2026-06-07
---
# Choose a model for production

Use this playbook when deciding which model should power a real product workflow. The
best benchmark model is not automatically the best production model.

## Inputs

- Product eval suite and target slices.
- Latency, cost, context-window, privacy, and reliability constraints.
- Candidate models with pricing, rate limits, tool support, structured-output support, and deployment options.

## Procedure

1. Define the product task and non-negotiable constraints.
2. Shortlist models using broad capability, context window, provider fit, and data policy.
3. Run the same product eval suite across candidates.
4. Compare quality by slice, not only aggregate score.
5. Measure latency, cost, output length, retry rate, and format reliability.
6. Test safety behavior and refusal quality on risk cases.
7. Check operational concerns: rate limits, uptime, observability, regional availability, and fallback options.
8. Choose the cheapest model that clears quality, safety, and operational gates.
9. Define fallback and re-evaluation cadence before launch.

## Comparison matrix

| Dimension | Question |
|---|---|
| Quality | does it pass the product eval suite? |
| Cost | what is cost per successful task? |
| Latency | does p95 fit the workflow? |
| Reliability | does it follow schema and tool contracts? |
| Safety | does it refuse and escalate correctly? |
| Operations | can the team monitor, route, and fall back? |

## Pitfall

Do not compare models on a few demos. Demos reward fluency; production rewards
reliable behavior across the distribution.

**Connects to:** [[ai/evaluation/model-vs-product-evals|model vs product evals]] ·
[[ai/evaluation/public-benchmarks-and-limits|public benchmarks]] ·
[[ai/mlops/serving-and-inference|serving and inference]]
