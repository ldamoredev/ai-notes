---
title: "Threat modeling LLM apps"
description: Threat modeling LLM apps maps assets, actors, trust boundaries, data flows, model behaviors, tools, and abuse cases before controls are chosen.
tags: [ai-safety, threat-modeling, architecture]
order: 8
updated: 2026-06-07
---
# Threat modeling LLM apps

Threat modeling is how AI risk becomes concrete. Instead of asking "is this model
safe?", ask what assets exist, who can influence the model, what the model can access,
and what happens if it behaves incorrectly.

## Map the system

- Users, admins, internal services, external attackers, and third-party tools.
- Assets: PII, credentials, proprietary documents, money movement, production systems.
- Data flows: prompts, retrieved context, tool output, logs, traces, caches, training data.
- Trust boundaries: user input, retrieved documents, tool results, model output, approvals.
- Actions: read, write, send, delete, purchase, deploy, search, execute code.

## AI-specific questions

| Question | Why it matters |
|---|---|
| Can untrusted text influence instructions? | prompt injection |
| Can the model see data the user cannot? | authorization failure |
| Can output trigger side effects? | insecure output handling |
| Can tools return malicious content? | indirect injection |
| Can memory persist attacker instructions? | long-lived compromise |
| Can loops consume resources? | unbounded consumption |

## Choose controls by boundary

- Before the model: authentication, authorization, input classification, retrieval filtering.
- Around the model: instruction hierarchy, context separation, model choice, rate limits.
- After the model: schema validation, policy checks, citation checks, output encoding.
- Around tools: allowlists, scoped credentials, argument validation, approvals, audit logs.

## Pitfall

Threat models that stop at the prompt miss the system. Most serious AI failures happen
at the boundaries between model, data, tools, permissions, and users.

**Connects to:** [[ai/agents-and-tools/agent-computer-interface|agent-computer interface]] ·
[[ai/rag-and-retrieval/why-rag|RAG]] ·
[[ai/mlops/llm-observability-and-tracing|tracing]]
