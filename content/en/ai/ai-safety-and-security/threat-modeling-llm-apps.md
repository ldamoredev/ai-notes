---
title: "Threat modeling LLM apps"
description: Model threats across identities, untrusted content, data, models, retrieval, tools, networks, and users; convert attacker paths into testable controls.
tags: [security, threat-modeling, llm-apps, agents]
order: 2
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/defense-in-depth-and-least-privilege]
last_verified: 2026-07-20
---
# Threat modeling LLM apps

**Mental model:** threat modeling asks what can cross a trust boundary, who can influence it, what authority it reaches, and how harm is prevented or recovered. An LLM app is not just a prompt: it includes identities, retrieval, tools, secrets, logs, UI, vendors, and human approvals.

## Mechanism: asset → boundary → attacker path → control → regression

Inventory assets (personal data, credentials, money, reputation), actors, entry points, and side effects. Draw the path from untrusted input through model/context/tool execution to the asset. For each path, add a preventive control, detection signal, owner, recovery action, and a reproducible attack fixture.

```python
path = {"source":"web page", "asset":"customer data", "action":"send_email", "gate":False}
print("block release" if not path["gate"] else "test control")
```

Run with `python3`; expected output is `block release`. The artifact expresses a rule: an untrusted-content-to-external-action path needs an independent authorization boundary.

| Boundary | Typical threat | Control |
|---|---|---|
| User → model | direct injection, data exposure | input policy, minimization |
| Retrieval → context | indirect injection, cross-tenant data | ACL before retrieval, source labels |
| Model → tool | excessive agency, malformed action | narrow schema, semantic validation, approval |
| Output → UI | XSS, misleading action | context-aware encoding, confirmation |
| Trace → operator | PII leakage | redaction, retention, access audit |

## Failure modes and decision rule

Do not model only model behavior while ignoring credentials, logs, or side effects. A prompt refusal is not a control against a compromised tool path. Release only when each high-impact path has a testable preventive control, detection, owner, and rollback or incident path.

## Exercises

1. Model a retrieved support ticket that asks an agent to export data.
2. Add a tenant boundary and prove that the execution layer rejects a cross-tenant request.

**Connects to:** [[ai/ai-safety-and-security/indirect-prompt-injection|indirect injection]] · [[ai/ai-safety-and-security/defense-in-depth-and-least-privilege|least privilege]] · [[ai/ai-playbooks/run-ai-red-team-lite|red-team playbook]] · [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gates]]

## Sources

- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle risk-management framework.
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial ML tactics and techniques.
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — application-security threat taxonomy.
