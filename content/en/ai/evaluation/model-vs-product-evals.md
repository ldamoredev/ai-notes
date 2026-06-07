---
title: "Model vs product evals"
description: Model evals test capability in isolation; product evals test whether the whole user-facing workflow succeeds under real constraints.
tags: [evaluation, product, model-quality]
order: 1
updated: 2026-06-07
---
# Model vs product evals

Model evals and product evals answer different questions. A strong model can still
fail in a product because the prompt, retrieval, tools, latency, cost, or UX contract
breaks the actual workflow.

## Two different units of analysis

| Eval type | Unit | Answers |
|---|---|---|
| Model eval | one model call or benchmark task | "Can this model perform the capability?" |
| Component eval | retriever, prompt, classifier, tool call | "Which part of the system is weak?" |
| Product eval | end-to-end user workflow | "Does the product reliably solve the user's job?" |
| Operational eval | production traces over time | "Is quality stable after launch?" |

Model evals help choose a base model. Product evals decide whether a change should
ship.

## What product evals include

- Task success against a user-visible goal.
- Groundedness and citation quality for knowledge workflows.
- Format correctness for APIs, JSON, and downstream automation.
- Latency, cost, and reliability under realistic traffic.
- Safety behavior, refusals, escalation, and human review.
- UX handling of uncertainty, errors, and partial answers.

## When each matters

- Use model evals when selecting models, checking capability ceilings, or estimating cost and speed.
- Use component evals when diagnosing whether failure comes from retrieval, prompting, fine-tuning, tools, or UI.
- Use product evals before release because they match the user promise.
- Use operational evals after release because distributions drift.

## Pitfall

Do not ship because a public benchmark improved. Benchmarks are proxies; the product
contract is the target. A cheaper model with better retrieval and UX can beat a
stronger model with poor context assembly.

**Connects to:** [[ai/evaluation/public-benchmarks-and-limits|public benchmarks]] ·
[[ai/ai-product-engineering/evals-inside-the-product|evals inside the product]] ·
[[ai/rag-and-retrieval/evaluating-rag|RAG eval]]
