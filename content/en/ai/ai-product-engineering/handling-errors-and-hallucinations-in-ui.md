---
title: "Handling errors and hallucinations in UI"
description: AI UI should make errors recoverable: cite evidence, invite correction, separate draft from final, and route unsupported claims safely.
tags: [ai-product, hallucination, error-handling, ux]
order: 7
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-playbooks/debug-hallucination]
last_verified: 2026-07-20
---
# Handling errors and hallucinations in UI

**Mental model:** the UI is a safety boundary: it should expose uncertainty, preserve the user’s agency, and make correction cheaper than overreliance.

## Mechanism: confidence/evidence state → user affordance → feedback signal

```python
state = {"evidence": False, "action": "ask_clarifying_question"}
assert not state["evidence"]
print(state["action"])
```

Run with `python3`; expected output is `ask_clarifying_question`. Do not hide errors behind confident prose; offer sources, edit/undo, report, and escalation paths.

## Production lens and exercises

Track correction rate, report rate, unsupported-claim rate, time to recovery, and the outcome after escalation. Test the UI with absent evidence, contradictory sources, a tool failure, and an unsafe request; a fallback must preserve the user's next safe action.

1. Design a source card that exposes provenance and lets a user report a mismatch.
2. Add a regression fixture where the correct product behavior is an explicit “I don't know.”

## Sources

- [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — human-centered AI interaction patterns.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — transparency and accountability context.

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
