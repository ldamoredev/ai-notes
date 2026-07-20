---
title: "Input and output guardrails"
description: Guardrails are layered checks around the model that classify inputs, constrain context, validate outputs, and route risky cases to safer workflows.
tags: [ai-safety, guardrails, policy]
order: 9
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/defense-in-depth-and-least-privilege]
last_verified: 2026-07-20
---
# Input and output guardrails

## Mechanism: classify → validate → allow, transform, escalate, or block

```python
decision = "escalate" if "payment" in "refund payment" else "allow"
print(decision)
```

Run with `python3`; expected output is `escalate`. Guardrails need a policy owner, false-positive monitoring, adversarial tests, and action-layer enforcement; filters alone cannot authorize a tool call.

## Sources

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — guardrail failure classes.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — measurement and control context.

Guardrails are controls around the model, not magic words inside the prompt. They help
detect unsafe requests, constrain what context enters the model, validate output, and
route risky cases to refusal, fallback, or human review.

## Guardrail layers

| Layer | Examples |
|---|---|
| Input | abuse detection, prompt-injection classifier, task allowlist |
| Context | permission-filtered retrieval, PII redaction, source allowlist |
| Model | system prompt, safe model choice, constrained decoding |
| Output | schema validation, groundedness check, PII scan, policy classifier |
| Action | approval gates, scoped credentials, tool argument validation |
| UX | clarification, refusal, escalation, undo, evidence display |

## Design principles

- Match guardrails to the task's risk level.
- Prefer deterministic checks for format, permissions, and policy boundaries.
- Use model-based classifiers where semantic judgment is needed.
- Log guardrail decisions for debugging and audits.
- Build safe fallbacks instead of only blocking.

## False positives and false negatives

Guardrails change product behavior, so evaluate them like product features. Measure
blocked useful requests, missed unsafe requests, latency, cost, and escalation volume.

## Pitfall

A guardrail that only lives in the same prompt as the task can be overridden by the
same failure modes it is supposed to prevent. Enforce critical controls in code.

**Connects to:** [[ai/ai-product-engineering/product-guardrails|product guardrails]] ·
[[ai/evaluation/task-specific-evals|task-specific evals]] ·
[[ai/agents-and-tools/guardrails-and-human-in-the-loop|agent guardrails]]
