---
title: "Add a human approval gate"
description: A procedure for adding meaningful human approval to high-impact AI actions without turning oversight into rubber-stamping.
tags: [playbook, human-in-the-loop, agents, safety]
order: 10
updated: 2026-06-07
---
# Add a human approval gate

Use this playbook when an AI system can take an action with external, irreversible,
costly, sensitive, or regulated consequences.

## Inputs

- List of actions the AI can propose or execute.
- Risk tier for each action.
- Required evidence, policy, and audit requirements.
- UX surface where the human will review.

## Procedure

1. Classify actions by blast radius: draft, reversible, external, irreversible, financial, regulated.
2. Decide which tiers require approval and which can auto-execute.
3. Show the human the proposed action, target, evidence, confidence, and risk reason.
4. Let the human approve, edit, reject, or escalate.
5. Log the proposal, reviewer, decision, timestamp, evidence, and final action.
6. Prevent the model from bypassing approval by calling lower-level tools directly.
7. Sample approved actions for quality review and reviewer drift.
8. Add failed or confusing approvals to evals and UX backlog.

## Review screen checklist

| Element | Purpose |
|---|---|
| Proposed action | what will happen |
| Target | who or what is affected |
| Evidence | why the model proposed it |
| Risk label | why approval is required |
| Diff or preview | what changes if approved |
| Undo path | how recovery works |

## Pitfall

Human-in-the-loop is not a checkbox. If the reviewer lacks context or the UI makes
approval easier than understanding, the gate becomes rubber-stamping.

**Connects to:** [[ai/agents-and-tools/guardrails-and-human-in-the-loop|guardrails and HITL]] ·
[[ai/ai-safety-and-security/excessive-agency|excessive agency]] ·
[[ai/ai-product-engineering/human-in-the-loop-and-trust|HITL and trust]]
