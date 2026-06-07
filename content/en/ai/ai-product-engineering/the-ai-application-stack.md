---
title: "The AI application stack"
description: How the pieces fit — model, prompt/context, retrieval, tools, guardrails, evaluation, and observability — into a production LLM application. A map of the whole atlas.
tags: [architecture, llm-app, system-design, stack]
order: 13
updated: 2026-06-07
---
# The AI application stack

Most of this atlas describes one layer at a time. This note assembles them. A
production LLM app is not "call the API" — it's a **stack of layers**, each with its
own failure modes and [[ai/evaluation/index|evals]]. Knowing the stack tells you where
a problem lives and where to add the next improvement.

## The layers (request flow, top to bottom)

| Layer | Job | Atlas branch |
|---|---|---|
| **Interface / UX** | streaming, trust, error handling, human review | [[ai/ai-product-engineering/ux-patterns-for-ai|product]] |
| **Orchestration** | workflow vs [[ai/agents-and-tools/workflows-vs-agents|agent]], routing, retries | agents |
| **Context assembly** | [[ai/prompt-engineering/assembling-context|prompt + retrieved docs + tools + memory]] | prompting |
| **Retrieval** | [[ai/rag-and-retrieval/why-rag|fetch relevant knowledge]] | RAG |
| **Tools** | [[ai/agents-and-tools/tool-calling|act on the world]] | agents |
| **Model** | the LLM (base / [[ai/llms/base-vs-instruct|instruct]] / [[ai/llms/reasoning-and-test-time-compute|reasoning]]) | LLMs |
| **Guardrails** | [[ai/ai-safety-and-security/index|input/output checks, policy]] | safety |
| **Serving** | [[ai/inference-and-optimization/serving-engines|latency, throughput, cost]] | inference |
| **Eval & observability** | [[ai/mlops/llm-observability-and-tracing|tracing]], offline + online quality | eval / MLOps |

The model is one box among many. Most product quality comes from the layers *around*
it — context, retrieval, guardrails, and evaluation.

## Two cross-cutting planes

- **Evaluation** runs through every layer: you [[ai/evaluation/model-vs-product-evals|eval
  the product]], not just the model, and you eval each component
  ([[ai/rag-and-retrieval/evaluating-rag|retriever]], [[ai/agents-and-tools/evaluating-agents|agent]]).
- **Observability** ([[ai/mlops/llm-observability-and-tracing|tracing]]) makes the whole
  stack inspectable — without it, you can't tell which layer failed.

## How to use the map

- **Debugging**: trace a bad output down the stack — wrong answer → retrieval? prompt?
  model? guardrail? Fix the *earliest* broken layer.
- **Building**: start with the smallest stack that works (prompt + model), add layers
  only when evals show you need them. Don't build RAG + agents on day one.
- **Cost/latency**: each layer adds both; the [[ai/ai-product-engineering/latency-cost-quality-triangle|triangle]]
  is a stack-wide budget.

## Pitfall

Treating the LLM as the whole system. The model is a probabilistic component; the
**engineering around it** — grounding, validation, fallbacks, evals — is what makes a
product reliable. Design the system, not the prompt.

**Connects to:** [[ai/foundations/mental-models-for-ai|mental models for AI systems]] ·
[[ai/ai-product-engineering/index|product engineering]] ·
[[ai/evaluation/model-vs-product-evals|product evals]]
