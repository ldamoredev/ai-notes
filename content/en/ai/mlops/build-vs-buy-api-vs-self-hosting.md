---
title: "Build vs buy: provider API vs self-hosting"
description: Call a hosted API or run the model yourself? The cost-crossover, privacy, control, and operational tradeoffs that decide one of the biggest architecture choices.
tags: [mlops, deployment, self-hosting, build-vs-buy]
order: 13
updated: 2026-06-07
---
# Build vs buy: provider API vs self-hosting

One of the highest-stakes infra decisions: consume a **hosted API** (OpenAI,
Anthropic, …) or **self-host** an open-weights model on your own GPUs. There's no
universal answer — it's a function of volume, privacy, control, and the engineering you
can sustain.

## What you're really trading

| | Hosted API (buy) | Self-host (build) |
|---|---|---|
| Time-to-first-value | minutes | days–weeks (set up [[ai/inference-and-optimization/serving-engines|serving]]) |
| Capability | frontier models | strong open models, slightly behind |
| Cost shape | per-token (opex, scales with use) | fixed GPU cost (capex-ish), cheaper at high volume |
| Privacy | data leaves your boundary | data stays in-house / on-prem |
| Control | provider's roadmap & [[ai/mlops/model-deprecation-and-migration|deprecations]] | you own the model & version |
| Ops burden | provider handles it | you own uptime, scaling, GPUs |

## The cost crossover

APIs win at **low and spiky** volume — you pay only for what you use and skip GPU ops.
Self-hosting wins at **high, steady** volume, where a saturated GPU is cheaper per token
than API pricing. The crossover depends on utilization: an idle GPU is pure waste, so
self-hosting only pays if you keep it busy. Model it with real traffic
([[ai/inference-and-optimization/cost-modeling-for-llm-serving|cost modeling]]), not a
napkin.

## When each clearly wins

- **Buy (API)**: early stage, unpredictable load, need frontier capability, small team,
  no strict data-residency rule.
- **Build (self-host)**: strict privacy/compliance, very high steady volume, need
  [[ai/fine-tuning-and-alignment/index|deep customization]], or want insulation from
  provider changes.
- **Hybrid** is common: API for hard/rare calls, a cheap self-hosted model for the
  high-volume easy ones (a [[ai/ai-product-engineering/choosing-a-model|routing]]
  strategy).

## Pitfall

Underestimating the **operational** cost of self-hosting — GPU supply, autoscaling,
batching, KV-cache memory, upgrades, on-call. The model is the easy part; running it
reliably at scale is a real platform. And don't self-host for "privacy" if a hosted
provider's zero-retention enterprise tier already meets your requirement.

**Connects to:** [[ai/ai-product-engineering/choosing-a-model|choosing a model]] ·
[[ai/inference-and-optimization/cost-modeling-for-llm-serving|cost modeling]] ·
[[ai/mlops/serving-and-inference|serving]]
