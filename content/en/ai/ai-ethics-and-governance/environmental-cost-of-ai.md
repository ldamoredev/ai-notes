---
title: "Environmental cost of AI"
description: AI environmental cost includes training and inference energy, water, hardware manufacturing, utilization, and the carbon intensity of compute.
tags: [environment, sustainability, compute, governance]
order: 12
updated: 2026-06-07
---
# Environmental cost of AI

AI systems consume energy, water, hardware, and data-center capacity. The environmental
question is not only how expensive a model is to train, but how much compute the product
uses over its lifetime.

## Cost sources

| Source | What to track |
|---|---|
| Training | GPU hours, energy, hardware, experiment count |
| Inference | tokens served, model size, utilization, retries |
| Evaluation | judge calls, benchmark runs, human review tooling |
| Storage | datasets, vector indexes, traces, generated media |
| Hardware | manufacturing, replacement, e-waste |
| Data center | energy source, cooling, water, regional carbon intensity |

## Reduction levers

- Use smaller or routed models where quality allows.
- Cache repeated work.
- Reduce unnecessary context and output length.
- Batch and right-size serving capacity.
- Reuse models and eval results instead of rerunning by habit.
- Choose lower-carbon regions or schedules where available.

## Governance questions

- Is the capability worth the compute?
- What is cost per successful task, not just total tokens?
- Are environmental costs visible in product and procurement decisions?
- Can model upgrades be justified by measured value?

## Pitfall

Training headlines can distract from inference. A popular product may spend far more
energy serving users every day than it spent on one training run.

**Connects to:** [[ai/inference-and-optimization/why-inference-is-the-real-cost|inference cost]] ·
[[ai/inference-and-optimization/right-sizing-models|right-sizing models]] ·
[[ai/mlops/cost-optimization|cost optimization]]
