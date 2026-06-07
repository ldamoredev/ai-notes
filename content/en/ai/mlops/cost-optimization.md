---
title: "Cost optimization"
description: AI cost is controlled by model choice, token budget, caching, routing, batching, retrieval design, and evaluation-driven pruning.
tags: [mlops, cost, optimization, llmops]
order: 10
updated: 2026-06-07
---
# Cost optimization

AI cost is a product architecture problem. The biggest savings usually come from using
the right model and context for the task, not from shaving tiny percentages off a
single model call.

## Cost drivers

- Input tokens: system prompt, history, retrieved context, tool results.
- Output tokens: verbosity, reasoning traces, structured output.
- Model choice: larger models cost more and may be unnecessary.
- Retrieval and reranking calls.
- Tool calls and external services.
- Retries from invalid output or failures.

## Cost levers

| Lever | Tradeoff |
|---|---|
| Smaller model | Lower cost, weaker capability |
| Model routing | Complexity, but better cost-quality fit |
| Prompt/context trimming | Risk of missing useful evidence |
| Semantic cache | Staleness and cache invalidation |
| Batch processing | Higher throughput, possible latency |
| Fine-tune/distill | Upfront cost, cheaper repeated inference |

## Measure unit economics

Track cost per successful task, not only cost per call. A cheap call that fails and
retries may be more expensive than one stronger model call that succeeds.

## Pitfall

Blindly reducing context can increase hallucination and support load. Cost cuts must be
validated with [[ai/evaluation/index|evals]], not only billing charts.

**Connects to:** [[ai/prompt-engineering/managing-the-context-window|context window management]] ·
[[ai/fine-tuning-and-alignment/distillation|distillation]] ·
[[ai/mlops/serving-and-inference|serving]]
