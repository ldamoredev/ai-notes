---
title: "Privacy and PII in datasets"
description: Dataset privacy requires minimization, consent, access control, retention rules, de-identification, and careful handling of derived artifacts.
tags: [data-for-ai, privacy, pii, governance]
order: 10
updated: 2026-06-07
---
# Privacy and PII in datasets

Datasets can contain direct identifiers, quasi-identifiers, secrets, sensitive
attributes, private documents, and inferred information. Privacy work starts before the
data enters training, evaluation, retrieval, or logging.

## Data minimization

- Collect only fields needed for the task.
- Remove secrets, credentials, and unnecessary identifiers.
- Prefer aggregation, masking, or redaction where full detail is not required.
- Keep retention periods explicit.
- Limit who can inspect raw examples.

## De-identification is not magic

| Technique | Helps with | Watch for |
|---|---|---|
| Redaction | obvious PII | missed entities and context clues |
| Pseudonymization | direct identifiers | re-identification via joins |
| Aggregation | individual exposure | loss of minority slices |
| Synthetic data | sharing constraints | leakage from seed data |
| Access control | operational safety | broad admin access |

## Derived artifacts matter

Embeddings, caches, traces, eval exports, fine-tuning files, and model outputs can
carry sensitive information even when the original dataset is controlled. Governance
must cover the whole lifecycle.

## Pitfall

Do not assume "we only store embeddings" removes privacy risk. Embeddings can retrieve
sensitive records and may leak information through similarity, membership inference, or
weak authorization.

**Connects to:** [[ai/ai-safety-and-security/privacy-and-data-governance|privacy governance]] ·
[[ai/ai-safety-and-security/data-and-pii-leakage|data and PII leakage]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]]
