---
title: "Privacy, consent, and data rights"
description: AI governance must cover consent, data minimization, access rights, retention, deletion, secondary use, and derived artifacts.
tags: [privacy, consent, data-rights, governance]
order: 7
updated: 2026-06-07
---
# Privacy, consent, and data rights

AI systems create privacy questions at every stage: collection, labeling, prompting,
retrieval, training, evaluation, logging, human review, and deletion. Governance has to
cover original data and derived artifacts.

## Governance questions

- Was the data collected with a valid purpose and basis?
- Can it be used for training, evaluation, retrieval, or human review?
- Can users access, correct, delete, or opt out where applicable?
- Are prompts, traces, embeddings, caches, and eval exports covered by retention rules?
- Are sensitive attributes needed, protected, and justified?
- Are model outputs revealing personal or confidential information?

## Controls

| Control | Purpose |
|---|---|
| Data minimization | reduce unnecessary exposure |
| Consent and purpose tracking | prevent unauthorized secondary use |
| Access control | restrict who and what can see data |
| Retention policy | define when prompts, traces, and datasets expire |
| Redaction and masking | reduce sensitive fields before processing |
| Deletion propagation | remove data from indexes, caches, and derived datasets |

## LLM-specific concerns

RAG indexes, embeddings, long prompts, traces, and fine-tuning files can all carry
sensitive data. A privacy review that covers only the database misses the AI surface.

## Pitfall

Anonymization is often fragile. Quasi-identifiers, context, embeddings, and joins can
re-identify people even when names are removed.

**Connects to:** [[ai/data-for-ai/privacy-and-pii-in-datasets|PII in datasets]] ·
[[ai/ai-safety-and-security/privacy-and-data-governance|privacy governance]] ·
[[ai/ai-safety-and-security/data-and-pii-leakage|data leakage]]
