---
title: "Fallbacks and graceful degradation"
description: AI products need fallback paths for model failures, low confidence, missing context, policy blocks, and slow dependencies.
tags: [ai-product, fallbacks, reliability]
order: 4
updated: 2026-06-07
---
# Fallbacks and graceful degradation

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
