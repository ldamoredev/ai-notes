---
title: "Product metrics for AI"
description: Measure AI products as a causal chain from user outcome to model behavior, reliability, cost, latency, safety, and recourse—not a single engagement number.
tags: [product-metrics, evaluation, ai-product]
order: 3
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/evaluation/model-vs-product-evals, ai/ai-product-engineering/latency-cost-quality-triangle]
last_verified: 2026-07-20
---
# Product metrics for AI

**Mental model:** a model metric becomes a product metric only when it predicts a user outcome under the real workflow. Instrument the chain: eligible user → request → model/tool trajectory → user action → verified outcome → harm, correction, or support cost. Optimize the narrowest metric that safely moves that outcome.

## Mechanism: outcome hypothesis → leading indicators → release decision

State one outcome hypothesis, such as “grounded answer reduces support reopens.” Pair it with leading indicators—evidence coverage, successful completion, abstention correctness, p95 latency, cost per successful task—and guardrails: unsafe action, appeal, over-reliance, and disparate error rates. A change ships only when outcome and guardrails clear their thresholds.

```python
completed, eligible, unsafe, cost = 82, 100, 1, 18.0
print("success", completed/eligible, "unsafe_rate", unsafe/eligible, "cost_per_success", cost/completed)
```

Run with `python3`; expected output separates success, harm, and unit economics. An engagement increase alone may mean users are confused, entertained, or trapped in retries.

| Layer | Example metric | Decision it supports |
|---|---|---|
| User outcome | task completed or correction avoided | does the feature help? |
| Behavior | evidence cited, tool success, abstention | why did it help or fail? |
| Experience | p95 time-to-useful-result, edit rate | can people use it? |
| Operations | cost/success, retry rate, incident rate | can it scale safely? |
| Trust | appeal, override, complaint, opt-out | should authority widen? |

## Failure modes and decision rule

Do not optimize clicks, tokens, or thumbs-up without a task-level counterfactual. Segment metrics by workflow and affected group, retain traces needed to investigate, and treat a safety or trust regression as a release blocker even when the aggregate outcome improves. Revisit metrics when the product boundary, model, or user behavior changes.

## Exercises

1. Define one outcome metric and two guardrails for a drafting assistant.
2. Add a retry rate to the artifact and compare request cost with successful-task cost.

**Connects to:** [[ai/evaluation/model-vs-product-evals|product evals]] · [[ai/ai-product-engineering/latency-cost-quality-triangle|tradeoffs]] · [[ai/mlops/feedback-loops|feedback loops]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|recourse]]

## Sources

- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — product and system measurement sequencing.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — production-readiness evidence.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — outcome, risk, and monitoring framing.
