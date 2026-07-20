---
title: "Choosing a model: open vs closed, capability vs cost"
description: There is no "best model" — only the best fit for a task's quality bar, latency, cost, privacy, and control needs. A framework for picking and not over-paying.
tags: [model-selection, open-source, cost, product]
order: 14
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/evaluation/designing-eval-sets]
last_verified: 2026-07-20
---
# Choosing a model: open vs closed, capability vs cost

## Mechanism: held-out workload → admissible models → lowest-cost route

Model choice is a recurring product decision, not a one-time pick. The frontier moves
monthly and your tasks differ, so the question is never "what's the best model?" but
"what's the **cheapest model that clears this task's quality bar**?"

## The axes that matter

- **Capability** — does it pass your [[ai/evaluation/designing-eval-sets|eval set]] on
  *this* task? (Benchmarks are a weak proxy; test on your data.)
- **Cost** — price per [[ai/llms/tokenization|token]], and how it scales with volume.
- **Latency** — [[ai/inference-and-optimization/latency-vs-throughput|time-to-first-token
  and tokens/sec]]; reasoning models are slower.
- **Context window** — does your [[ai/prompt-engineering/managing-the-context-window|context]]
  fit?
- **Privacy / control** — can data leave your boundary? Do you need on-prem?
- **Reliability** — rate limits, uptime, and the provider's deprecation cadence
  ([[ai/mlops/model-deprecation-and-migration|migration risk]]).

## Open vs closed (hosted)

| | Closed API (frontier) | Open weights (self-host or hosted) |
|---|---|---|
| Best capability | usually | catching up fast |
| Setup | trivial | you run [[ai/inference-and-optimization/serving-engines|serving]] |
| Cost at scale | per-token; can balloon | fixed GPU cost; cheaper at high volume |
| Privacy/control | data leaves your boundary | full control, on-prem possible |
| Customization | limited | full [[ai/fine-tuning-and-alignment/index|fine-tuning]] |

This is the [[ai/mlops/build-vs-buy-api-vs-self-hosting|build-vs-buy]] decision in
practice.

## A practical strategy

- **Start with a strong hosted model** to validate the product, then optimize cost.
- **Right-size** ([[ai/inference-and-optimization/right-sizing-models|down]]) once it
  works: many tasks run fine on a smaller/cheaper model.
- **Route** — send easy requests to a cheap model, hard ones to a strong one
  (model routing / cascades).
- **Decouple** your code from any single model behind a thin interface, because you
  *will* switch.

## Pitfall

Defaulting to the biggest model "to be safe" burns money and latency on tasks a small
model handles — and chasing the newest model without re-running your
[[ai/evaluation/prompt-regression-testing|evals]] ships silent regressions. Decide with
evals, not vibes or leaderboards.

**Connects to:** [[ai/mlops/build-vs-buy-api-vs-self-hosting|build vs buy]] ·
[[ai/inference-and-optimization/right-sizing-models|right-sizing]] ·
[[ai/evaluation/designing-eval-sets|eval on your task]]

```python
models = [{"name":"small", "quality":.86, "cost":.01}, {"name":"large", "quality":.91, "cost":.04}]
print(min((m for m in models if m["quality"] >= .90), key=lambda m: m["cost"])["name"])
```

Run with `python3`; expected output is `large`. Add safety, latency, region, availability, and fallback gates before release.

## Sources

- [HELM](https://crfm.stanford.edu/helm/) — scenario-based model evaluation.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk-aware selection.
