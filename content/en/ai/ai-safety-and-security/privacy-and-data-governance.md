---
title: "Privacy and data governance"
description: AI data governance defines what data can enter prompts, retrieval, training, logs, caches, traces, and human review workflows.
tags: [ai-safety, privacy, governance, data]
order: 12
updated: 2026-06-07
---
# Privacy and data governance

Privacy and data governance decide what data an AI system may collect, process, store,
retrieve, expose, and learn from. Without those rules, every prompt, trace, embedding,
cache, and eval export becomes a possible privacy boundary failure.

## Governance questions

- What data classes can be sent to each model provider or runtime?
- Which users and agents can retrieve each document or record?
- How long are prompts, outputs, traces, and tool results retained?
- Are embeddings, caches, and eval datasets tenant-isolated?
- Can production data be used for fine-tuning, evaluation, or human review?
- How are deletion, access requests, and audit requirements handled?

## Data lifecycle controls

| Stage | Control |
|---|---|
| Collection | minimize fields and document purpose |
| Prompting | redact or mask unnecessary sensitive data |
| Retrieval | enforce permissions before context assembly |
| Logging | scrub secrets and set retention windows |
| Evaluation | de-identify cases where possible |
| Fine-tuning | review consent, licensing, privacy, and leakage risk |
| Deletion | propagate deletes to indexes, caches, and derived datasets |

## Governance artifacts

- Data classification policy for AI features.
- Approved model/provider list by data class.
- Retrieval authorization design.
- Logging and retention policy.
- Human review and labeling rules.
- Incident response plan for data exposure.

## Pitfall

Embeddings are not a privacy bypass. They can encode sensitive information, support
membership inference, and retrieve protected records if access controls are weak.

**Connects to:** [[ai/ai-safety-and-security/data-and-pii-leakage|data leakage]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector databases]] ·
[[ai/mlops/llm-observability-and-tracing|observability traces]]
