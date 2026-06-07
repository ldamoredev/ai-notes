---
title: "Handling errors and hallucinations in UI"
description: AI UI should make errors recoverable: cite evidence, invite correction, separate draft from final, and route unsupported claims safely.
tags: [ai-product, hallucination, error-handling, ux]
order: 7
updated: 2026-06-07
---
# Handling errors and hallucinations in UI

LLMs can produce plausible unsupported claims. Product design cannot eliminate that
alone, but it can make errors visible, recoverable, and less damaging.

## UI defenses

| Risk | UI pattern |
|---|---|
| Unsupported claim | Citation, evidence panel, source highlight |
| Wrong answer | Report/correct control and visible revision path |
| Overconfident draft | Label as draft until reviewed |
| Ambiguous request | Ask clarification before answering |
| High-stakes advice | Refuse, escalate, or require expert review |
| Tool/action error | Show action status separately from generated prose |

Design the interface so users can check the answer without starting from scratch.

## Separate answer from evidence

When grounding matters, show the answer and the evidence path. If evidence is missing,
the product should say so, not invent confidence.

## Recovery controls

Useful recovery controls include regenerate with instruction, edit, mark wrong,
request sources, ask follow-up, undo action, and escalate to human.

## Pitfall

"AI may be wrong" disclaimers do not make errors safe. They shift responsibility to
the user without improving inspectability.

**Connects to:** [[ai/llms/why-llms-hallucinate|why LLMs hallucinate]] ·
[[ai/rag-and-retrieval/grounding-and-citations|grounding and citations]] ·
[[ai/ai-product-engineering/fallbacks-and-graceful-degradation|fallbacks]]
