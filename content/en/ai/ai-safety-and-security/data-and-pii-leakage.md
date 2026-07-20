---
title: "Data and PII leakage"
description: Data leakage happens when sensitive information enters prompts, logs, retrieval, training, traces, or outputs without the right access and retention controls.
tags: [ai-safety, privacy, pii, data-governance]
order: 5
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/privacy-and-pii-in-datasets]
last_verified: 2026-07-20
---
# Data and PII leakage

## Mechanism: data class → scoped access → minimized context → retention/deletion proof

```python
request = {"tenant":"a", "doc_tenant":"b", "contains_pii":True}
print("block" if request["tenant"] != request["doc_tenant"] else "consider_redaction")
```

Run with `python3`; expected output is `block`. Enforce authorization before retrieval, minimize before model calls, and verify deletion across indexes, caches, traces, exports, and vendors.

## Sources

- [EDPB: Artificial Intelligence](https://www.edpb.europa.eu/topics/ai-and-technology/artificial-intelligence_en) — data-protection guidance for AI.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — privacy-enhanced system controls.
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — sensitive-information disclosure risks.

AI systems move data through prompts, retrieval contexts, traces, logs, caches, tools,
fine-tuning datasets, and outputs. Leakage happens when sensitive data crosses one of
those paths without the right access control, minimization, retention, or redaction.

## Leakage paths

| Path | Failure mode |
|---|---|
| Prompt | unnecessary customer or employee data sent to a model |
| Retrieval | user receives chunks they are not authorized to see |
| Logs and traces | prompts, tool results, or PII stored in plain text |
| Cache | one user's response reused for another user |
| Fine-tuning data | private examples become part of training material |
| Output | model reveals secrets, credentials, or hidden context |

## Controls

- Minimize data before sending it to the model.
- Enforce document-level and row-level authorization before retrieval.
- Redact secrets, credentials, and PII from prompts and logs where possible.
- Separate tenants in indexes, caches, traces, and analytics.
- Define retention windows for prompts, outputs, and traces.
- Review fine-tuning datasets for privacy and licensing constraints.

## Access is not context

A user being allowed to ask a question does not mean the model should receive every
document the organization can access. Retrieval must enforce the user's permissions
before context enters the prompt.

## Pitfall

The model provider is only one leakage surface. Internal logs, observability tools,
debug screenshots, embeddings stores, and exported eval datasets often carry the same
data risk.

**Connects to:** [[ai/rag-and-retrieval/vector-databases-and-indexes|vector databases]] ·
[[ai/mlops/llm-observability-and-tracing|tracing]] ·
[[ai/fine-tuning-and-alignment/building-the-finetuning-dataset|fine-tuning datasets]]
