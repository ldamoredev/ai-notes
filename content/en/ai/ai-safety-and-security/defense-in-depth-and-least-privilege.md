---
title: "Defense in depth and least privilege"
description: Limit AI-system blast radius with independent controls across identity, data, tools, networks, approvals, observability, and recovery.
tags: [security, least-privilege, defense-in-depth, agents]
order: 3
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/agents-and-tools/autonomy-and-control, ai/ai-safety-and-security/indirect-prompt-injection]
last_verified: 2026-07-20
---
# Defense in depth and least privilege

**Mental model:** an AI model is an untrusted proposal generator. Defense in depth assumes a prompt, classifier, provider, or reviewer will eventually fail; independent controls must prevent one failure from becoming unauthorized disclosure or action. Least privilege gives every identity, tool, and workflow only the authority required for its current task.

## Mechanism: identity → scoped capability → verified side effect

Resolve the user and tenant before retrieval, issue a service identity with a narrow allowlist, validate arguments and current state at execution, and require approval for consequential actions. Log the decision and keep a kill switch. A model cannot upgrade its authority because retrieved text says so.

```python
policy = {"support-agent": {"search_orders", "draft_reply"}}
def authorize(role, tool): return tool in policy.get(role, set())
print(authorize("support-agent", "issue_refund"))
assert not authorize("support-agent", "issue_refund")
```

Run with `python3`; expected output is `False`. The executor must also enforce tenant scope, amount limits, idempotency, and approval policy; an allowlist alone is not a full control.

## Layers that should fail independently

| Layer | Control | Failure it contains |
|---|---|---|
| Identity | separate service principals, tenant scoping | cross-user access |
| Data | authorization before retrieval, minimization | private context exposure |
| Tools | narrow schemas and semantic checks | malformed or excessive action |
| Network | egress allowlists and secret isolation | exfiltration |
| Workflow | budgets, approvals, idempotency | runaway or irreversible action |
| Operations | traces, alerts, kill switch, rollback | delayed incident response |

## Failure modes and decision rule

Prompt rules and post-hoc output filters are not authorization. A broad database token, shell access, or shared admin credential defeats the whole design. Remove unnecessary capabilities first; then add compensating controls for the remaining high-impact paths. Release only when each external action has a named identity, policy, audit record, and recovery route.

## Exercises

1. Add a tenant identifier to the artifact and test a cross-tenant denial.
2. Classify five tools by reversibility and decide which requires human approval.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|autonomy control]] · [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gates]] · [[ai/ai-safety-and-security/indirect-prompt-injection|indirect injection]] · [[ai/mlops/llm-observability-and-tracing|tracing]]

## Sources

- [OWASP LLM06: Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — excessive functionality, permissions, and autonomy risks.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — secure, resilient lifecycle controls.
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial ML tactics and mitigations.
