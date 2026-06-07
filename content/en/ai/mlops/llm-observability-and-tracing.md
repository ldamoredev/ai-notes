---
title: "LLM observability and tracing"
description: LLM observability captures the full request trace: prompt, context, tools, model calls, costs, latency, and eval signals.
tags: [mlops, observability, tracing, llmops]
order: 6
updated: 2026-06-07
---
# LLM observability and tracing

LLM applications are multi-step systems. A bad answer may come from the prompt, model,
retrieval, reranker, tool result, parser, or product policy. Tracing makes that path
visible.

## The trace

A useful trace records:

- User input and request metadata.
- System prompt and assembled context.
- Retrieved chunks and scores.
- Model calls, parameters, tokens, latency, and cost.
- Tool calls, arguments, results, and errors.
- Final response and post-processing.
- Eval/judge scores and human feedback.

That trace is the debugging unit. Without it, you are guessing from the final answer.

## The five pillars for LLM apps

| Pillar | Question |
|---|---|
| Quality | Did the system answer correctly? |
| Latency | Where did time go? |
| Cost | Which step spent tokens or compute? |
| Safety | Did policy or guardrails trigger? |
| Reliability | Which component failed or retried? |

## Trace replay

Good observability lets you replay production traces against a new prompt, model, or
retrieval config before release. That turns real traffic into regression tests.

## Pitfall

Logging only final prompts can leak sensitive data and still miss the failure. Log
structured traces with redaction, retention policy, and access control.

**Connects to:** [[ai/prompt-engineering/assembling-context|assembling context]] ·
[[ai/agents-and-tools/tool-calling|tool calls]] ·
[[ai/evaluation/index|evals]]
