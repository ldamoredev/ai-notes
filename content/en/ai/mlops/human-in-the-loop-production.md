---
title: "Human-in-the-loop in production"
description: HITL production systems route uncertain, risky, or high-impact model outputs to humans with enough context to decide.
tags: [mlops, hitl, production, review]
order: 11
updated: 2026-06-07
---
# Human-in-the-loop in production

Human-in-the-loop (HITL) is not a checkbox. It is a production design pattern for
routing uncertain, risky, or high-impact model behavior to people who can decide,
correct, approve, or escalate.

## When to insert humans

- High-impact actions: money movement, legal advice, account changes, deletion.
- Low confidence or conflicting evidence.
- Safety/policy uncertainty.
- New intent clusters not covered by evals.
- User disputes, corrections, or appeals.

The review threshold should match blast radius. Low-stakes outputs can be logged;
irreversible actions need approval.

## Design the review packet

Show the human:

- User request and relevant context.
- Model answer or proposed action.
- Evidence, retrieved chunks, or tool results.
- Confidence/eval signals and policy flags.
- Clear approve/edit/reject/escalate controls.

Bad HITL UX creates rubber-stamping. The human needs enough signal to decide quickly.

## Feedback capture

Every review decision should become data: label, correction, reason, segment, and
version. That feeds [[ai/mlops/feedback-loops|feedback loops]] and future evals.

## Pitfall

Putting a human at the end does not make the system safe if the human lacks context,
time, authority, or a usable interface.

**Connects to:** [[ai/agents-and-tools/guardrails-and-human-in-the-loop|agent HITL]] ·
[[ai/ai-product-engineering/index|AI product UX]] ·
[[ai/mlops/feedback-loops|feedback loops]]
