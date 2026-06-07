---
title: "Product guardrails"
description: Product guardrails define what the AI feature may do, when it must refuse, when it must ask, and when it must escalate.
tags: [ai-product, guardrails, safety, policy]
order: 9
updated: 2026-06-07
---
# Product guardrails

Product guardrails are the product-level rules around model behavior: what the feature
can do, what it must not do, when it asks clarification, and when it escalates to a
human or safer workflow.

## Guardrail layers

| Layer | Example |
|---|---|
| Input | Block unsupported task types or unsafe requests |
| Context | Do not pass data the user lacks permission to see |
| Output | Validate schema, citations, policy, PII |
| Action | Require approval before irreversible operations |
| UI | Explain limits and expose recovery controls |

The strongest guardrails live in code and permissions, not in a system prompt alone.

## Product policy map

For each task, define:

- Allowed scope.
- Disallowed scope.
- Required evidence.
- Human review threshold.
- Refusal or fallback copy.
- Logging and audit requirements.

## Guardrails as UX

A guardrail should feel like a clear product boundary, not a random model refusal.
Offer the next safe step when possible.

## Pitfall

If the model can choose its own permissions, the guardrail is fictional. Enforce
limits outside the model.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|least privilege]] ·
[[ai/ai-safety-and-security/index|AI safety and security]] ·
[[ai/prompt-engineering/system-prompts-and-roles|system prompts]]
