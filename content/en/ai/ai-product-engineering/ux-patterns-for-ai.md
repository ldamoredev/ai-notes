---
title: "UX patterns for AI"
description: AI UX is about exposing capability while making uncertainty, control, review, and recovery visible to the user.
tags: [ai-product, ux, interface-patterns]
order: 1
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-product-engineering/onboarding-and-expectations]
last_verified: 2026-07-20
---
# UX patterns for AI

## Mechanism: task stakes → interaction pattern → correction and recourse

```python
risk, reversible = "high", False
print("review_queue" if risk == "high" or not reversible else "copilot")
```

Run with `python3`; expected output is `review_queue`. Test comprehension, user control, correction success, escalation, and overreliance—not visual polish alone.

## Sources

- [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — AI interaction patterns.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — transparency and accountability context.

AI features need interfaces that admit uncertainty. The product should make it clear
what the system can do, what evidence it used, how the user can steer it, and how to
recover when it is wrong.

## Common patterns

| Pattern | Use when |
|---|---|
| Copilot | User remains in control and AI suggests drafts or actions |
| Autocomplete | The next step is short, low-risk, and reversible |
| Chat assistant | The task is exploratory or conversational |
| Batch generator | User wants many candidates or transformations |
| Review queue | Outputs require human approval before action |
| Agent workspace | Multi-step work needs tools, plan, trace, and checkpoints |

Pick the pattern based on task risk and user control, not because chat is fashionable.

## Make uncertainty operable

- Show sources or evidence when claims depend on context.
- Offer regenerate, edit, accept, reject, and explain actions.
- Keep user edits first-class; the AI should not overwrite them silently.
- Preserve a trace for high-impact actions.
- Surface confidence through concrete signals, not vague magic words.

## Match automation to stakes

Low-stakes and reversible tasks can be fast and fluid. High-stakes or irreversible
tasks need review, confirmation, and audit trail.

## Pitfall

The most common AI UX mistake is hiding the model behind a confident interface. If the
system can be wrong, design the wrongness path.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|autonomy and control]] ·
[[ai/ai-product-engineering/human-in-the-loop-and-trust|HITL and trust]] ·
[[ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui|error UX]]
