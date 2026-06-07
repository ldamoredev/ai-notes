---
title: "Decide prompt vs RAG vs fine-tune"
description: A decision procedure for choosing whether to improve an AI system with prompting, retrieval, fine-tuning, tools, or product constraints.
tags: [playbook, architecture, rag, fine-tuning]
order: 5
updated: 2026-06-07
---
# Decide prompt vs RAG vs fine-tune

Use this playbook when a model is underperforming and the team is debating whether to
change the prompt, add RAG, fine-tune, add tools, or redesign the product boundary.

## Inputs

- Failure examples with traces.
- Desired behavior and current behavior.
- Evidence requirements, freshness requirements, latency target, and cost target.
- Data availability for retrieval or training.

## Procedure

1. Classify the failure: missing knowledge, bad instruction following, weak format, stale facts, domain style, reasoning gap, or unsafe behavior.
2. Check whether the needed information exists in the prompt or context.
3. Use prompting when the model has the capability but needs clearer task framing, examples, or output constraints.
4. Use RAG when the answer depends on external, private, changing, or citable knowledge.
5. Use fine-tuning when you need consistent behavior, format, style, domain adaptation, or preference alignment across many examples.
6. Use tools when the task requires computation, lookup, transaction, or state change.
7. Use product constraints when the safe answer is to narrow the feature, ask clarification, or add human review.
8. Run a small eval before committing to the most expensive option.

## Decision table

| Need | First move |
|---|---|
| Better instructions | prompt and examples |
| Fresh or private knowledge | RAG |
| Consistent style or schema | fine-tune or structured output |
| Deterministic computation | tool |
| High-risk action | approval gate |

## Pitfall

Fine-tuning is not a database. If the system needs current facts, permissions, or
citations, retrieval usually belongs in the architecture.

**Connects to:** [[ai/fine-tuning-and-alignment/when-to-fine-tune|when to fine-tune]] ·
[[ai/rag-and-retrieval/why-rag|why RAG]] ·
[[ai/prompt-engineering/prompt-to-context-engineering|context engineering]]
