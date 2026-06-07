---
title: "Monitoring and drift"
description: Production models fail when data, users, or the world changes. Monitor inputs, outputs, quality, latency, cost, and drift signals.
tags: [mlops, monitoring, drift, production]
order: 5
updated: 2026-06-07
---
# Monitoring and drift

Models are trained on yesterday's distribution and used on tomorrow's traffic.
Monitoring is how you notice when the gap becomes large enough to hurt quality,
safety, latency, or cost.

## What to monitor

| Layer | Signals |
|---|---|
| Input | schema breaks, missing fields, topic mix, prompt length |
| Model output | score, refusal rate, invalid format, toxicity, groundedness |
| System | latency, errors, retries, cost, cache hit rate |
| Product | conversion, escalation, user correction, retention |
| Data drift | feature distribution, embedding distribution, query mix |

For LLMs, drift often appears as new user intents, longer prompts, novel documents, or
tool errors rather than classic numeric feature drift.

## Drift types

- **Covariate drift** — inputs change.
- **Label drift** — the relationship between input and target changes.
- **Concept drift** — what "good" means changes.
- **Policy drift** — product or safety expectations change.

## Alert on actionability

Alerts should map to an operational response: rollback, disable a tool, rebuild an
index, update a prompt, collect labels, or trigger human review. Noisy dashboards are
not monitoring.

## Pitfall

Aggregate averages hide localized failure. Segment by customer, language, topic,
model version, prompt version, retrieval source, and tool path.

**Connects to:** [[ai/foundations/distribution-shift|distribution shift]] ·
[[ai/rag-and-retrieval/rag-failure-modes|RAG failure modes]] ·
[[ai/mlops/feedback-loops|feedback loops]]
