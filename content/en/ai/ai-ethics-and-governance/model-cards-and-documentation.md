---
title: "Model cards and documentation"
description: Model cards document intended use, data, evaluation, limitations, ethical considerations, and operational guidance for model consumers.
tags: [model-cards, documentation, governance]
order: 6
updated: 2026-06-07
---
# Model cards and documentation

Model cards make model assumptions and limitations explicit. They help downstream
builders decide whether a model is appropriate for a use case and what checks are
needed before deployment.

## What a model card should cover

- Model name, version, provider, and release date.
- Intended use and out-of-scope use.
- Training data summary and known gaps.
- Evaluation results by task and slice.
- Safety, fairness, privacy, and security limitations.
- Required input/output constraints.
- Operational guidance: latency, cost, monitoring, fallback, and update cadence.
- Contact, owner, and incident reporting path.

## Documentation stack

| Artifact | Describes |
|---|---|
| Datasheet or data card | dataset provenance, composition, collection, limits |
| Model card | model behavior, evals, risks, intended use |
| System card | product-level architecture, controls, deployment context |
| Eval report | release-specific evidence and failure analysis |
| Incident report | post-deployment failures and mitigations |

## How to use documentation

Documentation should feed release gates. If a model card says the model was not
evaluated for a domain, language, or safety risk, the product team must either test it
or avoid that use.

## Pitfall

Documentation that is not updated after fine-tuning, prompt changes, retrieval changes,
or model upgrades becomes misleading.

**Connects to:** [[ai/data-for-ai/datasheets-and-data-documentation|datasheets]] ·
[[ai/evaluation/model-vs-product-evals|product evals]] ·
[[ai/mlops/model-and-prompt-registry|model registry]]
