---
title: "Guardrails & human-in-the-loop"
description: An agent that can act can act wrongly. Input/output guardrails, approval gates for high-impact actions, and designing the human checkpoint.
tags: [agents, guardrails, human-in-the-loop, safety]
order: 9
updated: 2026-06-07
---
# Guardrails & human-in-the-loop

The moment an agent can take **real actions** (send email, move money, delete data),
mistakes have consequences. Guardrails and human checkpoints are what make autonomy
deployable rather than reckless.

## Guardrails: automated checks around the agent

- **Input guardrails** — validate/sanitize what enters the agent; detect
  [[ai/ai-safety-and-security/index|prompt injection]] and off-policy requests before
  they reach the loop.
- **Output guardrails** — check the agent's proposed action/response before it executes
  or ships: format/schema validation, policy filters, PII redaction.
- **Action constraints** — the agent can only call **allowlisted tools** with validated
  arguments; risky operations are blocked or require escalation
  ([[ai/agents-and-tools/autonomy-and-control|least privilege]]).

## Human-in-the-loop (HITL)

For high-impact or low-confidence actions, insert a human:

- **Approval gates** — the agent proposes; a human confirms before execution. Standard
  for irreversible or costly actions (payments, deletes, external sends).
- **Confidence-based escalation** — auto-handle routine cases; route uncertain ones to a
  human.
- **Show the plan** — let the agent surface what it intends to do *before* doing it, so
  oversight is meaningful.

> Match the checkpoint to the **blast radius**: reversible/low-stakes → let it run and
> log; irreversible/high-stakes → require explicit human approval.

## Design the human moment well

HITL only works if the human has the context to decide quickly: show the proposed
action, why, and the evidence — not a wall of trace. Bad HITL UX gets rubber-stamped,
which is no guardrail at all.

## Pitfall

Guardrails in the prompt ("please don't delete anything") are not security — a
[[ai/ai-safety-and-security/index|determined injection]] or a confused agent ignores
them. Enforce hard limits in **code and permissions**, outside the model.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|least privilege]] ·
[[ai/ai-safety-and-security/index|injection & excessive agency]] ·
[[ai/ai-product-engineering/index|HITL UX]]
