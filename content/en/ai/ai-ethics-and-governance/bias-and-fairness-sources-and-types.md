---
title: "Bias and fairness: sources and types"
description: Unfair outcomes emerge from framing, data, labels, objectives, interfaces, and feedback loops; locate the mechanism before choosing a mitigation.
tags: [fairness, bias, responsible-ai]
order: 2
updated: 2026-07-20
kind: concept
level: foundational
status: current
prerequisites: [ai/data-for-ai/dataset-design-and-sampling, ai/evaluation/systematic-error-analysis]
last_verified: 2026-07-20
---
# Bias and fairness: sources and types

**Mental model:** bias is a mismatch between a system's measurement and decision
process and the legitimate interests of people affected by it. It is not a property
that lives only in model weights. Trace an outcome backwards through the product:
decision rule → score or generation → labels and features → collection process →
institutional context → feedback from deployment.

## Where unfairness enters

| Mechanism | Example | Diagnostic evidence |
|---|---|---|
| Framing | “fraud risk” substitutes for a support need | stakeholder and harm analysis |
| Representation | rural speakers are absent from speech data | coverage by relevant group/context |
| Measurement | arrests proxy crime differently across places | measurement process and missingness |
| Labeling | historical approvals encode prior discretion | label audit and annotator agreement |
| Aggregation | one threshold serves unequal populations | slice error and calibration results |
| Deployment | score used for denial although trained for triage | observed workflow and user research |
| Feedback | recommendations determine what becomes future data | longitudinal exposure and outcome data |

Sensitive attributes may be unavailable for valid reasons, but simply removing them
does not remove correlated proxies such as geography, language, device, or history.
Conversely, collecting group data introduces privacy and governance duties. Decide
with affected communities and applicable law; do not infer protected traits casually.

## A minimal slice audit

Run with `python3`; expected output shows different false-negative rates, which is a
signal to investigate—not proof of unlawful discrimination.

```python
def fnr(rows):
    positives = [r for r in rows if r[0] == 1]
    return sum(r[1] == 0 for r in positives) / len(positives)

group_a = [(1, 1), (1, 0), (0, 0), (0, 0)]  # (truth, prediction)
group_b = [(1, 0), (1, 0), (0, 0), (0, 1)]
print("FNR A", fnr(group_a), "FNR B", fnr(group_b))
```

The denominator, confidence interval, missing-group rate, and decision consequence
belong beside every slice metric. Small samples should trigger collection or review,
not confident optimization.

## Mitigate at the mechanism

Improve collection or labeling for representation and measurement problems; change a
threshold or provide a review path for decision-rule harms; redesign the product where
automation creates a harmful feedback loop. Reweighting or debiasing a model cannot
repair an invalid label or a use case that should not be automated. Preserve baseline
metrics and test a mitigation for benefit, regressions, and new harms.

## Failure modes and decision rule

- Treating demographic gaps as the only fairness question misses accessibility and
  individual recourse.
- Optimizing a proxy metric can move harm to an unmeasured group.
- Declaring “fair” from historical labels launders historical decisions.
- Publishing group metrics without privacy controls can itself expose people.

Before changing a model, state the harm, affected groups or contexts, causal story,
metric limits, owner, and recourse. If none can be stated, do discovery rather than
selecting a fairness algorithm.

## Exercises

1. Add sample sizes and Wilson intervals to the artifact; decide when to withhold a slice result.
2. Map one product feature to each row of the table and choose a non-model mitigation.

**Connects to:** [[ai/ai-ethics-and-governance/fairness-metrics-and-impossibility-tradeoffs|fairness metrics]] · [[ai/data-for-ai/dataset-design-and-sampling|dataset design]] · [[ai/evaluation/systematic-error-analysis|error analysis]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|recourse]]

## Sources

- [NIST SP 1270: Towards a Standard for Identifying and Managing Bias in AI](https://doi.org/10.6028/NIST.SP.1270) — lifecycle sources of bias and risk-management framing.
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — collection, composition, and maintenance questions that expose data assumptions.
- [Fairness and Machine Learning](https://fairmlbook.org/) — formal concepts and the limits of purely technical interventions.
- [Model Cards for Model Reporting](https://arxiv.org/abs/1810.03993) — reporting intended use, subgroup evaluation, and limitations.
