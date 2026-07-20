---
title: "OWASP LLM Top 10 overview"
description: OWASP's LLM Top 10 is a practical taxonomy for LLM application risks such as prompt injection, data leakage, excessive agency, and insecure output handling.
tags: [ai-safety, owasp, threat-modeling]
order: 1
updated: 2026-07-20
kind: overview
level: foundational
status: current
prerequisites: [ai/ai-safety-and-security/index]
last_verified: 2026-07-20
---
# OWASP LLM Top 10 overview

## Mechanism: threat scenario → system control → tested residual risk

```python
finding = {"risk":"prompt injection", "owner":"security", "test":"indirect fixture"}
assert all(finding.values())
print("risk is operationalized")
```

Run with `python3`; expected output is `risk is operationalized`. Use OWASP as a threat taxonomy, not a compliance stamp: map each applicable risk to owners, evidence, monitoring, and a remediation decision.

## Sources

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — authoritative risk taxonomy.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk-management process.

OWASP's LLM Top 10 is useful because it names LLM-specific application risks in a
language security engineers can act on. It is not a checklist to memorize; it is a map
for threat modeling.

## Risk families

| Risk family | Core idea |
|---|---|
| Prompt injection | attackers manipulate model instructions directly or through data |
| Sensitive information disclosure | private data leaks through prompts, retrieval, logs, or output |
| Supply chain | models, plugins, datasets, packages, and tools can be compromised |
| Data and model poisoning | training, fine-tuning, or retrieval data can be manipulated |
| Insecure output handling | model output is trusted by downstream systems |
| Excessive agency | the system gives the model too much action power |
| System prompt leakage | internal instructions or policy details are exposed |
| Vector and embedding weaknesses | retrieval stores leak or retrieve the wrong information |
| Misinformation | fluent incorrect output causes user or system harm |
| Unbounded consumption | runaway cost, latency, or resource use becomes an attack path |

## How to use it

- Start each AI feature with a threat model, not only a prompt review.
- Map each risk to a concrete asset, attacker, trust boundary, and mitigation.
- Prioritize by blast radius: data exposure and real-world actions outrank cosmetic bad output.
- Revisit the model when adding tools, RAG, memory, fine-tuning, or user uploads.

## LLM apps are still apps

Many controls are familiar: access control, input validation, output encoding, logging,
rate limiting, least privilege, secrets management, and audit trails. The difference is
that the model can transform untrusted text into instructions, code, tool calls, or
confident false claims.

## Pitfall

Do not treat OWASP as an after-the-fact security review. By then the architecture may
already put the model on the wrong side of trust boundaries.

**Connects to:** [[ai/ai-safety-and-security/threat-modeling-llm-apps|threat modeling]] ·
[[ai/ai-safety-and-security/direct-prompt-injection|direct injection]] ·
[[ai/agents-and-tools/autonomy-and-control|least privilege]]
