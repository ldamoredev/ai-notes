---
title: "Defense in depth and least privilege"
description: AI security depends on layered controls and narrow permissions because no single model, prompt, classifier, or guardrail is reliable enough alone.
tags: [ai-safety, defense-in-depth, least-privilege]
order: 11
updated: 2026-06-07
---
# Defense in depth and least privilege

Defense in depth assumes one control will fail. Least privilege assumes the model will
eventually make a bad decision. Together, they make failures contained instead of
catastrophic.

## Layered controls

| Layer | Example control |
|---|---|
| Identity | per-user and per-agent authorization |
| Data | permission-filtered retrieval and tenant isolation |
| Prompt | role separation and clear task boundaries |
| Model | safer model choice for riskier tasks |
| Guardrail | input and output classifiers, schema checks |
| Tool | allowlists, scoped credentials, argument validation |
| Human | approval for irreversible or high-impact actions |
| Operations | monitoring, rate limits, alerts, incident response |

## Least privilege for AI

- Expose fewer tools than the model could theoretically use.
- Give read-only access unless writes are essential.
- Scope credentials to the task, tenant, and time window.
- Bound amounts, destinations, file paths, recipients, and APIs.
- Require approval when an action has irreversible or external side effects.

## Failure containment

Design for the moment when prompt injection succeeds, retrieval returns poisoned
content, a judge misses a violation, or an agent chooses the wrong tool. The question
is whether that failure can reach data, money, production, or users.

## Pitfall

Security by model behavior is fragile. A model refusal is helpful, but it is not an
access-control system, a transaction limit, or an audit trail.

**Connects to:** [[ai/agents-and-tools/autonomy-and-control|autonomy and least privilege]] ·
[[ai/ai-safety-and-security/excessive-agency|excessive agency]] ·
[[ai/mlops/monitoring-and-drift|monitoring]]
