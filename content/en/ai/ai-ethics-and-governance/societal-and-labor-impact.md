---
title: "Societal and labor impact"
description: Evaluate how AI redistributes tasks, discretion, error burden, access, and power across workers and affected people—not just productivity.
tags: [societal-impact, labor, responsible-ai]
order: 11
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-product-engineering/product-metrics-for-ai, ai/ai-ethics-and-governance/accountability-and-human-oversight]
last_verified: 2026-07-20
---
# Societal and labor impact

**Mental model:** automation reallocates work and authority. Measure who saves time, who does hidden review, who bears wrong-output cost, and who can challenge a decision. A throughput gain can transfer risk to workers, customers, or contractors.

## Mechanism: task change → stakeholder harm → control

Decompose the workflow, identify affected stakeholders and changed decision rights, then compare outcomes before and after deployment. Include users, workers, decision subjects, support teams, and data contributors. Consultation and appeal data belong in the evaluation fixture.

```python
before = {"agent_minutes": 12, "review_minutes": 0, "appeals": 3}
after = {"agent_minutes": 4, "review_minutes": 10, "appeals": 9}
print("changed review burden", after["review_minutes"] - before["review_minutes"])
```

Run with `python3`; expected output is `changed review burden 10`. Keep time, errors, and appeals separate rather than claiming one productivity number explains all effects.

| Question | Evidence |
|---|---|
| Is work augmented or intensified? | task study and worker feedback |
| Who bears error cost? | incidents and appeal slices |
| Can people contest decisions? | accessible recourse and overturn rate |
| Does surveillance or power change? | data and access-policy review |

The ILO's 2025 update treats occupational exposure as distinct from job loss; task and context matter. Require stakeholder review and an appeal path when deployment changes work allocation or access to material services. Pause when measured harm exceeds its accepted benefit.

## Exercises

1. Add an error-burden metric for one workflow.
2. Design feedback collection independent of the AI system being judged.

**Connects to:** [[ai/ai-product-engineering/product-metrics-for-ai|product metrics]] · [[ai/evaluation/human-evaluation|human evaluation]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|accountability]]

## Sources

- [ILO: Generative AI and jobs, 2025 update](https://www.ilo.org/publications/generative-ai-and-jobs-2025-update) — task-level exposure evidence and limits.
- [OECD AI Principles](https://oecd.ai/en/ai-principles) — inclusive growth and human-centered values.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — socio-technical risk framing.
