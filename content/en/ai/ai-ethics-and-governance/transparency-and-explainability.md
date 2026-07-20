---
title: "Transparency and explainability"
description: Disclose an AI system's role and limits, then test whether explanations are faithful, useful, and connected to a decision or recourse path.
tags: [transparency, explainability, interpretability]
order: 5
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/interpretability/index, ai/ai-ethics-and-governance/accountability-and-human-oversight]
last_verified: 2026-07-20
---
# Transparency and explainability

**Mental model:** transparency answers what system is involved, for what purpose, and with what limits. Explainability answers how an output was produced or what it means in context. Neither proves correctness, fairness, or accountability; their value is enabling calibration, debugging, review, and recourse.

## Mechanism: audience → question → evidence → action

Choose the audience—user, operator, auditor, or affected person—their decision, and the evidence needed to act. Link an explanation to attribution, example, counterfactual, retrieval citation, model card, or audit log. Test its fidelity and usefulness rather than judging fluent prose.

```python
explanation = {"audience":"reviewer", "claim":"income changed score", "evidence":"attribution:v7", "action":"request review"}
assert all(explanation.values())
print("explanation has a recourse path")
```

Run with `python3`; expected output is `explanation has a recourse path`.

| Surface | Example | Test |
|---|---|---|
| User | AI interaction or generated-media disclosure | comprehension and opt-out |
| Operator | retrieval sources and tool state | correct intervention |
| Auditor | versions, evals, approvals | reproducible trace |
| Affected person | decision factors and appeal | meaningful correction |

Post-hoc attribution, attention, saliency, and model-generated rationales can be unstable or non-faithful. Prefer inherently interpretable methods where appropriate; otherwise state limits and test whether an explanation changes when its claimed cause changes.

## Failure modes and decision rule

Do not expose confidential prompts as “transparency,” or give a plausible story that cannot be checked. Provide the least information that lets the audience make its legitimate decision, with human escalation for high-impact outcomes.

## Exercises

1. Add a fidelity test that fails when the cited feature changes but the score does not.
2. Write separate transparency text for a user and an on-call operator.

**Connects to:** [[ai/interpretability/index|interpretability]] · [[ai/ai-ethics-and-governance/model-cards-and-documentation|documentation]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|recourse]]

## Sources

- [NISTIR 8312](https://doi.org/10.6028/NIST.IR.8312) — principles for explainable AI.
- [NIST AI RMF Measure guidance](https://airc.nist.gov/airmf-resources/playbook/measure/) — explanation evaluation with relevant actors.
- [Model Cards](https://arxiv.org/abs/1810.03993) — system and model transparency evidence.
