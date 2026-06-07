---
title: "MLOps to LLMOps"
description: LLMOps extends MLOps from models and data pipelines to prompts, retrieval, tools, traces, evals, and human feedback.
tags: [mlops, llmops, production]
order: 1
updated: 2026-06-07
---
# MLOps to LLMOps

MLOps is about running learned systems reliably. LLMOps keeps that foundation but
adds new artifacts: prompts, context assembly, retrieval indexes, tools, traces, evals,
and human review.

## What stays the same

- You still need reproducible experiments.
- You still need versioned data, models, and evaluation sets.
- You still need CI/CD, rollout, monitoring, and rollback.
- You still need a feedback loop from production failures to training or design.

The old lesson survives: the model is not the system. The production system includes
data pipelines, serving, product logic, and operational controls.

## What changes with LLM systems

| MLOps artifact | LLMOps extension |
|---|---|
| Model version | Model + prompt + tool schema + retrieval index |
| Feature pipeline | Context assembly and retrieval pipeline |
| Prediction log | Full trace: prompt, context, tool calls, response |
| Model metric | Product eval, groundedness, cost, latency, safety |
| Label feedback | Human preference, correction, approval, escalation |

LLM changes often happen outside weights. A prompt or retrieval-index update can be as
behavior-changing as a model release.

## The release unit

Release the whole behavior bundle: model, prompt, retrieval configuration, tool
definitions, eval set, guardrails, and fallback policy. If you version only the model,
you cannot reproduce the behavior users saw.

## Pitfall

Calling an LLM API from production is not LLMOps. Operations begin when you can explain
which version produced an output, why it changed, and how you would roll it back.

**Connects to:** [[ai/mlops/model-and-prompt-registry|model and prompt registry]] ·
[[ai/prompt-engineering/prompt-to-context-engineering|context engineering]] ·
[[ai/rag-and-retrieval/index|retrieval systems]]
