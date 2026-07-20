---
title: "Fairness metrics and impossibility tradeoffs"
description: Fairness metrics formalize different harms; when base rates differ, several desirable group criteria cannot generally hold together, so decisions need explicit values and evidence.
tags: [fairness, metrics, tradeoffs]
order: 3
updated: 2026-07-20
kind: derivation
level: intermediate
status: current
prerequisites: [ai/ai-ethics-and-governance/bias-and-fairness-sources-and-types, ai/foundations/evaluation-metrics]
last_verified: 2026-07-20
---
# Fairness metrics and impossibility tradeoffs

**Mental model:** a fairness metric is a compact statement of *which error or outcome
must be comparable for whom*. It does not discover justice from a confusion matrix.
Choose the harm first, calculate multiple criteria with uncertainty, then make the
tradeoff and accountability record explicit.

## Notation and metrics

For group `g`, let `Y` be the true outcome, `Ŷ` a binary decision, and `S` a score.
The base rate is `P(Y=1 | g)`. Common group criteria are:

| Criterion | Equation | Harm it foregrounds |
|---|---|---|
| Demographic parity | `P(Ŷ=1 | g=a) = P(Ŷ=1 | g=b)` | unequal access or selection |
| Equal opportunity | `TPR_a = TPR_b` | eligible people denied at different rates |
| Equalized odds | `TPR_a=TPR_b` and `FPR_a=FPR_b` | both missed benefits and wrongful positives |
| Predictive parity | `PPV_a = PPV_b` | positive decisions have unequal reliability |
| Calibration | `P(Y=1 | S=s,g=a)=P(Y=1 | S=s,g=b)` | the same score means different risk |

`TPR = TP/(TP+FN)`, `FPR = FP/(FP+TN)`, and `PPV = TP/(TP+FP)`. Metrics need
denominators, sample sizes, confidence intervals, missing-data policy, and the
threshold used to turn scores into actions.

## A numerical conflict

Suppose two groups use a calibrated score, but their prevalence differs. A shared
threshold can produce different positive predictive values or error rates; moving
thresholds can equalize one rate while changing another. The impossibility results
show that, except under special conditions (such as equal base rates or perfect
prediction), calibration and equalized error rates generally cannot both hold. This is
not a license to stop measuring; it prevents claiming that one dashboard solved every
normative question.

```python
def rates(tp, fp, tn, fn):
    return {"TPR": tp/(tp+fn), "FPR": fp/(fp+tn), "PPV": tp/(tp+fp)}
print("A", rates(80, 20, 80, 20))
print("B", rates(40, 30, 120, 10))
```

Run with `python3`. Both groups have `TPR=0.8` and `FPR=0.2`, yet PPV differs
(`0.8` versus about `0.57`) because prevalence differs. Change B's prevalence or
errors and observe which target moves. The exercise demonstrates bookkeeping, not a
conclusion about a real population.

## Decision procedure

1. Identify the affected people, decision, and asymmetric harms of false positives,
   false negatives, abstention, delay, and appeal.
2. Choose primary and guardrail metrics with stakeholders and applicable law; include
   accessibility and recourse, not only group rates.
3. Estimate uncertainty and inspect intersections and deployment slices.
4. Test mitigations against a baseline; document who accepted residual risk.
5. Monitor after release because prevalence, labels, and workflow can shift.

## Failure modes and decision rule

- Equal rates can conceal an invalid target label or an unacceptable use case.
- A group label can be missing, unsafe to collect, or too coarse to represent harm.
- Threshold tuning can merely reallocate errors to an unmeasured group.
- A metric without a contestation path leaves harmed users with no remedy.

Do not select a metric because it is easiest to optimize. Select it only when its
error tradeoff corresponds to a documented harm and an accountable owner can explain
the residual disparity.

## Exercises

1. Change the counts in the artifact until equal opportunity holds but predictive parity does not.
2. Add Wilson intervals and decide whether either group has enough data for a release decision.

**Connects to:** [[ai/ai-ethics-and-governance/bias-and-fairness-sources-and-types|bias mechanisms]] · [[ai/ai-ethics-and-governance/measuring-and-mitigating-bias|bias mitigation]] · [[ai/foundations/evaluation-metrics|evaluation metrics]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|accountability]]

## Sources

- [Fairness and Machine Learning](https://fairmlbook.org/) — definitions, limitations, and intervention taxonomy.
- [Inherent Trade-Offs in the Fair Determination of Risk Scores](https://arxiv.org/abs/1609.05807) — calibration and error-rate incompatibility conditions.
- [Equality of Opportunity in Supervised Learning](https://arxiv.org/abs/1610.02413) — equal opportunity and equalized-odds framing.
- [NIST SP 1270](https://doi.org/10.6028/NIST.SP.1270) — governance and bias-management considerations beyond a metric.
