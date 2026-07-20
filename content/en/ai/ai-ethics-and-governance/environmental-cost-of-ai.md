---
title: "Environmental cost of AI"
description: Measure an AI product's energy, emissions, water, and hardware impact across training and its operating lifetime; optimize successful work, not model prestige.
tags: [environment, sustainability, compute, governance]
order: 12
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/inference-and-optimization/why-inference-is-the-real-cost, ai/mlops/cost-optimization]
last_verified: 2026-07-20
---
# Environmental cost of AI

**Mental model:** environmental impact is a lifecycle accounting problem. Training is
one capital-like event; serving, retries, evaluation, storage, cooling, hardware
manufacture, and disposal are operating effects. Compare alternatives by useful
outcome—such as a verified task—not by parameter count or one headline training run.

## Mechanism: workload → energy → impact

Measure the workload that a service actually executes, convert measured or estimated
energy with an explicit boundary, then divide the resulting impact by verified useful
outcomes. That chain exposes retries and idle capacity that a training-only estimate
cannot see.

## A measurable boundary

For operational electricity, estimate `energy_kWh = average_power_kW × hours` and
location-based emissions `kgCO2e = energy_kWh × grid_intensity_kgCO2e_per_kWh`.
State the boundary: accelerator only or full server; model calls only or storage and
network; location-based or market-based emissions; measured power or estimate. Water
and embodied hardware impact need separate methods and should not be silently folded
into carbon.

```python
power_kw, hours, intensity = 1.2, 75, 0.42
energy = power_kw * hours
print(f"energy_kWh={energy:.1f} kgCO2e={energy * intensity:.1f}")
print(f"per_success_kg={energy * intensity / 900:.3f}")
```

Run with `python3`; expected output includes `energy_kWh=90.0` and `kgCO2e=37.8`.
The denominator of 900 is successful tasks, not requests: failed retries are part of
the burden and must remain visible.

## Inventory the system

| Stage | Record | Common hidden driver |
|---|---|---|
| Training/tuning | accelerator-hours, utilization, experiments, region | discarded runs and checkpoints |
| Inference | input/output tokens, batching, cache hit rate, retries | long context and agent loops |
| Evaluation | model-judge calls, benchmark repetitions | unconstrained regression suites |
| Storage/egress | datasets, indexes, trace retention | duplicate corpora and verbose traces |
| Hardware | device lifetime, replacement, e-waste | low utilization and premature refresh |

## Decision levers

First remove useless work: cache stable results, cap context and output, stop looping
agents, and use deterministic checks before model judges. Then right-size model and
quality tier, batch compatible requests, increase utilization without breaking
latency/SLOs, and locate flexible workloads where cleaner energy is actually
available. A smaller model that increases retries or human corrections may increase
impact per successful task; measure the whole workflow.

## Failure modes and decision rule

- Quoting one carbon number without boundary, region, or measurement method.
- Optimizing training while unbounded inference dominates lifetime energy.
- Buying offsets as a substitute for efficiency and disclosure.
- Treating lower cost as proof of lower environmental impact without checking energy.

Choose the least-impact configuration that meets a predeclared quality, reliability,
safety, and latency target. Re-evaluate after model, traffic, region, or prompt
changes; report estimates as estimates.

## Exercises

1. Add a 30% retry rate to the artifact and compare per-request with per-success impact.
2. Define an emissions budget for an eval suite and decide which tests run on every commit.

**Connects to:** [[ai/inference-and-optimization/why-inference-is-the-real-cost|inference cost]] · [[ai/agents-and-tools/agent-failure-modes|runaway work]] · [[ai/mlops/cost-optimization|cost optimization]] · [[ai/ai-product-engineering/index|product economics]]

## Sources

- [IEA: Energy and AI](https://www.iea.org/reports/energy-and-ai) — energy-system context and data-centre demand analysis.
- [Greenhouse Gas Protocol Scope 2 Guidance](https://ghgprotocol.org/scope_2_guidance) — boundary and reporting concepts for purchased electricity.
- [Carbon Intensity API methodology](https://carbonintensity.org.uk/) — an example of time- and region-dependent grid-intensity data.
- [Energy and Policy Considerations for Deep Learning in NLP](https://aclanthology.org/P19-1355/) — measurement and reporting challenges for ML experimentation.
