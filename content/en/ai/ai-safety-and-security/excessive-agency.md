---
title: "Excessive agency"
description: Excessive agency happens when an AI system has more autonomy, tool access, permissions, or budget than the task requires.
tags: [ai-safety, agents, autonomy, least-privilege]
order: 6
updated: 2026-06-07
---
# Excessive agency

Excessive agency is the risk of giving an AI system too much power. The model might be
tricked, confused, or wrong, but the damage comes from the permissions and actions the
system allowed it to take.

## Agency dimensions

| Dimension | Risky default |
|---|---|
| Tool access | every tool exposed to every agent |
| Credentials | agent acts with a human admin token |
| Autonomy | high-impact actions execute without approval |
| Budget | unlimited loops, tokens, API calls, or spend |
| Scope | agent can operate across tenants, files, or accounts |
| Memory | past instructions influence future tasks without review |

## Controls

- Give each agent a narrow role and allowlist only required tools.
- Use service identities with scoped credentials, not broad human accounts.
- Validate tool arguments against policy and the user's original request.
- Gate irreversible, external, costly, or regulated actions with human approval.
- Cap iterations, spend, retries, and runtime.
- Make every action auditable and reversible where possible.

## Autonomy tiers

| Tier | Example |
|---|---|
| Suggest | draft a plan, no side effects |
| Prepare | produce an action for human review |
| Execute reversible | update a draft, stage a change, create a ticket |
| Execute high impact | send, delete, purchase, deploy, transfer funds |

Each tier needs a different permission and approval model.

## Pitfall

Do not rely on the model to decide whether it deserves more permissions. Permission
boundaries belong outside the model.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|autonomy and least privilege]] ·
[[ai/agents-and-tools/guardrails-and-human-in-the-loop|guardrails and HITL]] ·
[[ai/evaluation/evaluating-agent-systems|agent evals]]
