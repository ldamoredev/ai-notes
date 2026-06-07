---
title: "Fairness metrics and impossibility tradeoffs"
description: Fairness metrics encode different ideas of fairness, and several desirable metrics cannot all be satisfied at once when base rates differ.
tags: [fairness, metrics, tradeoffs]
order: 3
updated: 2026-06-07
---
# Fairness metrics and impossibility tradeoffs

Fairness metrics are not interchangeable. Each one encodes a different normative
choice about what equal treatment means, and some cannot be satisfied simultaneously
unless the world has special statistical properties.

## Common metrics

| Metric | Question |
|---|---|
| Demographic parity | are positive decisions equally common across groups? |
| Equal opportunity | are true positives equally likely across groups? |
| Equalized odds | are true positive and false positive rates equal across groups? |
| Predictive parity | are positive predictions equally reliable across groups? |
| Calibration | does a score mean the same risk across groups? |
| Individual fairness | are similar individuals treated similarly? |

## Why tradeoffs appear

When groups have different base rates, calibration, equalized error rates, and equal
positive predictive value can conflict. Choosing a metric is therefore a product,
legal, and ethical decision, not just a mathematical one.

## Practical framing

- Start from the harm: false positive, false negative, exclusion, surveillance, stigma, or loss of opportunity.
- Pick metrics that match that harm.
- Report multiple metrics instead of hiding tradeoffs.
- Use slice-level confidence intervals where sample sizes are small.
- Document the decision and who approved it.

## Pitfall

A fairness dashboard does not decide what is fair. It makes tradeoffs visible so the
organization can make an accountable decision.

**Connects to:** [[ai/foundations/evaluation-metrics|evaluation metrics]] ·
[[ai/machine-learning/class-imbalance|class imbalance]] ·
[[ai/ai-ethics-and-governance/measuring-and-mitigating-bias|measuring bias]]
