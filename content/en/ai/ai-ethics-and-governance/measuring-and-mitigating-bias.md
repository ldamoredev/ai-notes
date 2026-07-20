---
title: "Measuring and mitigating bias"
description: Turn a suspected unfair outcome into a scoped harm, slice audit, intervention experiment, release decision, and monitored control.
tags: [fairness, bias, mitigation, evaluation]
order: 4
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/ai-ethics-and-governance/bias-and-fairness-sources-and-types, ai/ai-ethics-and-governance/fairness-metrics-and-impossibility-tradeoffs]
last_verified: 2026-07-20
---
# Measuring and mitigating bias

**Mental model:** mitigation is an experiment on a harm, not a knob that makes a
dashboard green. Name the affected decision, people, error consequence, and baseline;
then change the earliest mechanism that plausibly creates the harm and test both the
intended benefit and what the change breaks.

## Mechanism: audit → hypothesis → intervention → release gate

Start with a versioned dataset and decision policy. Slice outcomes by relevant group
or context, inspect examples and denominators, trace the gap to data, labels,
threshold, workflow, or interface, and choose a control at that layer. Re-run the
same slice suite against a holdout before a release decision.

```python
def fnr(rows):
    positives = [r for r in rows if r[0]]
    return sum(not r[1] for r in positives) / len(positives)
before = [(1,1), (1,0), (1,0), (0,0)]
after  = [(1,1), (1,1), (1,0), (0,1)]
print("before", fnr(before), "after", fnr(after))
assert fnr(after) < fnr(before)
```

Run with `python3`; expected output shows the false-negative rate improves from about
`0.67` to `0.33`. It also introduces a false positive, so this is evidence to weigh,
not an automatic approval.

## Intervention map

| Observed mechanism | Prefer first | Guardrail |
|---|---|---|
| missing coverage | collection, sampling, label review | privacy and representativeness |
| proxy measurement | replace or qualify the measure | subgroup validity |
| threshold mismatch | calibrated thresholds or abstention | error tradeoff and appeal |
| workflow overreliance | review UX and authority limits | reviewer workload |
| feedback loop | exposure logging and policy change | longitudinal outcomes |

Track sample size, intervals, missing-group rate, decision threshold, and the exact
model/prompt/data version. Mitigations can improve a selected metric while worsening
calibration, privacy, utility, or an unmeasured subgroup; report the comparison rather
than optimizing in secret.

## Production lens, failures, and decision rule

Monitor slice metrics, complaints, appeals, overrides, and data drift after launch.
Roll back or route to review when a predeclared disparity or harm threshold is crossed.
Do not collect sensitive attributes without a justified governance and privacy basis;
do not call a group gap proof of cause without investigating the data-generating
process. Release only when an accountable owner accepts the documented residual risk
and recourse path.

## Exercises

1. Add false-positive rate and a minimum sample-size guard to the artifact.
2. Design a non-model intervention for a biased support-routing workflow.

**Connects to:** [[ai/ai-ethics-and-governance/fairness-metrics-and-impossibility-tradeoffs|metric tradeoffs]] · [[ai/evaluation/task-specific-evals|task evals]] · [[ai/mlops/monitoring-and-drift|monitoring]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|accountability]]

## Sources

- [NIST SP 1270](https://doi.org/10.6028/NIST.SP.1270) — bias identification and management across the lifecycle.
- [Fairness and Machine Learning](https://fairmlbook.org/) — metrics, interventions, and technical limits.
- [NIST AI RMF Playbook: Measure](https://airc.nist.gov/airmf-resources/playbook/measure/) — evaluation and governance actions.
