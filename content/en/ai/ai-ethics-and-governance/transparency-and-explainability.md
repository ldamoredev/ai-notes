---
title: "Transparency and explainability"
description: Transparency tells people how AI is used; explainability tries to make model behavior understandable, but explanations have limits.
tags: [transparency, explainability, interpretability]
order: 5
updated: 2026-06-07
---
# Transparency and explainability

Transparency and explainability are related but different. Transparency tells people
when and how AI is involved; explainability tries to make a model's behavior
understandable enough for debugging, contesting, or oversight.

## Types of transparency

| Type | Example |
|---|---|
| User transparency | disclose chatbot or AI-generated content |
| System transparency | document model, data, metrics, and limits |
| Decision transparency | explain important factors in an output |
| Process transparency | record review, approval, and appeal paths |
| Provenance transparency | label generated media and source data |

## Explainability tools

- Feature attribution methods such as SHAP or LIME.
- Example-based explanations and nearest neighbors.
- Counterfactual explanations.
- Attention or saliency visualizations.
- Model cards, data cards, and evaluation reports.

## Limits

Post-hoc explanations can be unstable, incomplete, or misleading. For LLMs and
generative models, fluent rationales can be plausible stories rather than faithful
accounts of the internal process.

## Pitfall

An explanation is not accountability. Users need meaningful recourse, human review, and
clear ownership when an AI-assisted decision affects them.

**Connects to:** [[ai/evaluation/human-evaluation|human evaluation]] ·
[[ai/multimodal-and-generative/deepfakes-provenance-and-watermarking|provenance]] ·
[[ai/ai-ethics-and-governance/accountability-and-human-oversight|accountability]]
