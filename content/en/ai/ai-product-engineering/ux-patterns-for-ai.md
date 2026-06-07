---
title: "UX patterns for AI"
description: AI UX is about exposing capability while making uncertainty, control, review, and recovery visible to the user.
tags: [ai-product, ux, interface-patterns]
order: 1
updated: 2026-06-07
---
# UX patterns for AI

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
