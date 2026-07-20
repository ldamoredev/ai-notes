---
title: "Privacy, consent, and data rights"
description: Map personal data through prompts, retrieval, evaluation, logs, models, and deletion workflows; retain only a lawful, necessary, protected purpose.
tags: [privacy, consent, data-rights, governance]
order: 7
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/privacy-and-pii-in-datasets, ai/ai-ethics-and-governance/ai-governance-frameworks]
last_verified: 2026-07-20
---
# Privacy, consent, and data rights

**Mental model:** personal data does not stop being personal after tokenization,
embedding, caching, or inclusion in a trace. Privacy engineering maps each data class
through the system, attaches a purpose and retention rule, and makes access, correction,
deletion, and incident paths executable. Requirements vary by jurisdiction; involve
qualified privacy counsel for a real deployment.

## Mechanism: data inventory → permitted purpose → propagation controls

For every input and derived artifact, record source, data class, purpose/legal basis,
processor, storage location, access policy, retention, and deletion propagation. A
retrieval index, eval export, support trace, and vendor request are separate stores,
not one “database.” A rights request must locate all applicable copies and explain
limits where removal from a trained model is not technically or legally equivalent to
deleting a record.

```python
stores = {"prompt_log": 30, "vector_index": 30, "eval_export": 7}
request = {"id": "u_8", "purpose": "support", "authorized": True}
assert request["authorized"] and all(days > 0 for days in stores.values())
print("deletion plan covers", sorted(stores))
```

Run with `python3`; expected output lists all three stores. The artifact proves only
inventory coverage; production deletion needs durable IDs, vendor contracts, and
verification receipts.

## Controls and tradeoffs

Minimize fields before model calls; use scoped identities and encryption; redact where
appropriate; segregate tenants; restrict review access; and expire prompts, caches,
indexes, and exports. Pseudonymization lowers exposure but is not automatically
anonymization. Fairness measurement can require sensitive data, while expanding its
collection creates privacy risk: document necessity, safeguards, access, and deletion.

## Failure modes and decision rule

“Consent” does not automatically authorize every secondary use. A removal from the
primary database that leaves embeddings and traces is incomplete. Anonymization claims
need contextual re-identification analysis. Do not send personal data to a model or
provider until the purpose, access, retention, and rights workflow are recorded and
approved; stop processing on a missing lawful route.

## Exercises

1. Extend the artifact with a cache and fail it when its retention exceeds the source policy.
2. Trace one user document through ingestion, chunking, embedding, retrieval, logging, and deletion.

**Connects to:** [[ai/data-for-ai/privacy-and-pii-in-datasets|PII in datasets]] · [[ai/ai-safety-and-security/data-and-pii-leakage|data leakage]] · [[ai/ai-ethics-and-governance/accountability-and-human-oversight|oversight]] · [[ai/mlops/model-and-prompt-registry|artifact registry]]

## Sources

- [European Data Protection Board: AI](https://www.edpb.europa.eu/topics/ai-and-technology/artificial-intelligence_en) — current AI/data-protection guidance hub.
- [EDPB opinion on AI models](https://www.edpb.europa.eu/news/edpb-opinion-ai-models-gdpr-principles-support-responsible-ai_en) — model anonymity, legitimate interests, and unlawful processing context.
- [NIST AI RMF privacy guidance](https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/) — privacy-enhanced AI as a lifecycle characteristic.
