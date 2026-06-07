---
title: "Measuring and mitigating bias"
description: Bias mitigation starts with scoped harms, slice metrics, data audits, model interventions, UX controls, and ongoing monitoring.
tags: [fairness, bias, mitigation, evaluation]
order: 4
updated: 2026-06-07
---
# Measuring and mitigating bias

Bias work becomes useful when it is tied to a concrete use case, affected groups,
measured harms, and interventions that can be evaluated before and after deployment.

## Measurement workflow

1. Define the decision or output being audited.
2. Identify affected groups and legally or contextually relevant attributes.
3. Define harms and choose fairness metrics that match them.
4. Measure performance and error rates by slice.
5. Inspect examples from the worst slices.
6. Check data coverage, labels, features, thresholds, and product flow.
7. Test mitigations and monitor for regressions.

## Mitigation levers

| Layer | Interventions |
|---|---|
| Data | collect missing slices, relabel, rebalance, remove leakage |
| Features | remove risky proxies, improve measurement quality |
| Model | reweight, constrain, calibrate, tune thresholds |
| Evaluation | add slice-specific release gates |
| UX | disclose limits, support appeals, route uncertain cases to humans |
| Governance | require review for high-impact use cases |

## Monitoring

Bias can change after launch as users, data, and workflows shift. Track slice metrics,
complaints, overrides, appeals, and feedback loops over time.

## Pitfall

Mitigation can improve one metric while worsening another. Always compare quality,
fairness, safety, and utility together.

**Connects to:** [[ai/data-for-ai/feedback-data-and-active-learning|feedback data]] ·
[[ai/evaluation/task-specific-evals|task-specific evals]] ·
[[ai/mlops/monitoring-and-drift|monitoring and drift]]
