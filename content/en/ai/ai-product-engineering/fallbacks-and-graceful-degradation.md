---
title: "Fallbacks and graceful degradation"
description: AI products need fallback paths for model failures, low confidence, missing context, policy blocks, and slow dependencies.
tags: [ai-product, fallbacks, reliability]
order: 4
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/mlops/serving-and-inference]
last_verified: 2026-07-20
---
# Fallbacks and graceful degradation

**Mental model:** a fallback preserves the user’s safe next action when a dependency, model, policy, or budget fails. It must be designed and tested as a product path, not improvised in an outage.

## Mechanism: failure signal → bounded alternative → observable recovery

```python
def route(model_ok, retrieval_ok):
    return "grounded_answer" if model_ok and retrieval_ok else "show_sources_or_escalate"
print(route(True, False))
```

Run with `python3`; expected output is `show_sources_or_escalate`. Fallbacks need a user explanation, preserved authority limits, metrics, and a rollback path.

## Sources

- [Google SRE Book](https://sre.google/sre-book/handling-overload/) — overload and graceful-degradation patterns.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — resilience and risk-management context.

AI systems fail in more ways than ordinary deterministic software: bad retrieval,
invalid output, safety block, timeout, tool failure, low confidence, or model outage.
Graceful degradation keeps the product useful when the ideal path fails.

## Fallback ladder

| Failure | Fallback |
|---|---|
| Model timeout | Retry once, then smaller model or async completion |
| Invalid structured output | Repair/validate, then ask for correction |
| Missing evidence | Say what is missing and offer search/retrieval |
| Safety uncertainty | Escalate to human or safe refusal |
| Tool failure | Show partial answer and retry action later |
| Low confidence | Ask clarification or route to review |

Fallbacks should be explicit product states, not generic "something went wrong."

## Make partial value useful

When full automation fails, the system can still provide:

- A draft instead of a final answer.
- Evidence without synthesis.
- A checklist instead of action.
- A safe summary instead of a risky recommendation.
- A handoff packet for human review.

## Design for reversibility

If the AI action is reversible, allow undo. If it is irreversible, require confirmation
or human approval before execution.

## Pitfall

Pretending the model always works creates brittle UX. The fallback path is part of the
main product, not an error afterthought.

**Connects to:** [[ai/mlops/serving-and-inference|serving reliability]] ·
[[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gates]] ·
[[ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui|error handling]]
