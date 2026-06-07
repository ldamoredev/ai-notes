---
title: "Stand up LLM observability"
description: A startup procedure for logging traces, prompts, outputs, retrieval, tools, costs, latency, feedback, and eval replay in an LLM application.
tags: [playbook, observability, mlops]
order: 8
updated: 2026-06-07
---
# Stand up LLM observability

Use this playbook before the first serious release of an LLM feature. If you cannot
see prompts, context, outputs, tool calls, cost, latency, and feedback, you cannot
debug or evaluate the system reliably.

## Inputs

- Product workflows and model call sites.
- Privacy and retention policy.
- Eval and incident-review needs.
- Cost and latency budget.

## Procedure

1. Assign a trace ID to every user request and downstream model call.
2. Log model, prompt version, input metadata, retrieved context IDs, output, tool calls, errors, latency, token counts, and cost.
3. Redact or mask sensitive fields before storage where required.
4. Capture user feedback, human review labels, and support escalations against the trace ID.
5. Add dashboards for volume, error rate, cost, latency, guardrail decisions, and quality signals.
6. Make traces replayable in staging for prompt, retrieval, and model changes.
7. Define retention windows and access rules for traces.
8. Add alerting for cost spikes, tool errors, safety failures, and quality drops.

## Minimum dashboard

| Panel | Why |
|---|---|
| Cost by workflow | finds expensive paths |
| Latency p50/p95 | protects UX |
| Error and retry rate | catches brittle integrations |
| Guardrail outcomes | exposes safety/product tension |
| Feedback and review labels | feeds evals and backlog |

## Pitfall

Observability that stores everything forever creates a privacy problem. Trace what you
need, protect it, and set retention deliberately.

**Connects to:** [[ai/mlops/llm-observability-and-tracing|LLM observability and tracing]] ·
[[ai/mlops/feedback-loops|feedback loops]] ·
[[ai/ai-safety-and-security/privacy-and-data-governance|privacy governance]]
