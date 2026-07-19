---
title: Interpretability
description: Methods for investigating model decisions and internal representations without confusing plausible explanations for faithful mechanisms.
tags: [interpretability, explainability, representations, causality]
order: 0
updated: 2026-07-19
status: planned
level: intermediate
---
# Interpretability

Interpretability asks what evidence supports a claim about a model's behavior or internal computation. An explanation that sounds plausible is not automatically faithful to the mechanism that produced the output.

## Mental model

Start with the question and unit of analysis: input feature, example, neuron, activation direction, representation, circuit, or causal pathway. Choose an observational or intervention method whose limitations match the claim. Validate with counterfactuals, controls, and behavioral effects.

## Candidate note roadmap

- `feature-importance-permutation-and-partial-dependence` — global and local behavior for classical models.
- `lime-and-shap` — surrogate explanations, Shapley framing, assumptions, and instability.
- `saliency-integrated-gradients-and-attribution` — gradient-based signals and saturation problems.
- `probes-and-representation-analysis` — decodability, controls, and the gap between presence and use.
- `activation-analysis-and-steering` — directions, interventions, and behavioral validation.
- `mechanistic-interpretability-and-circuits` — components, pathways, causal tracing, and scope.
- `sparse-autoencoders-and-features` — superposition, dictionary learning, feature quality, and scaling.
- `causal-interventions-and-ablation` — patching, ablation, mediation, and confounding.
- `faithfulness-and-explanation-theater` — when an explanation is useful, misleading, or unvalidated.
- `interpretability-evaluation` — ground truth, synthetic tasks, human utility, and falsification.

## Boundary

Interpretability does not by itself prove safety, fairness, truthfulness, or causality in the world. It can generate and test hypotheses about a particular model under particular interventions.

**Connects to:** [[ai/evaluation/systematic-error-analysis|Systematic Error Analysis]] · [[ai/ai-ethics-and-governance/transparency-and-explainability|Transparency and Explainability]] · [[ai/ai-safety-and-security/red-teaming-ai-systems|Red Teaming AI Systems]]

## Core sources

- [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874) — SHAP's formal framing.
- [Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365) — Integrated Gradients and attribution axioms.
- [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) — foundational mechanistic-interpretability decomposition.
- [Scaling Monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/) — sparse autoencoders at model scale, with explicit limitations.
