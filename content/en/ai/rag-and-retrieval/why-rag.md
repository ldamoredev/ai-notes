---
title: "Why RAG (and when not to)"
description: RAG injects fresh, private, citable facts into a frozen model. Why it beats fine-tuning for knowledge — and the cases where it's the wrong tool.
tags: [rag, retrieval, grounding]
order: 1
updated: 2026-06-07
---
# Why RAG (and when not to)

An [[ai/llms/index|LLM]]'s knowledge is frozen at its [[ai/llms/pretraining-next-token|training
cutoff]] and contains nothing private to you. **RAG** fixes that at answer time: search
a corpus for relevant passages, put them in the
[[ai/llms/context-window-and-kv-cache|context window]], and instruct the model to
answer from them.

## What RAG buys you

- **Fresh knowledge** — update the index, not the model; no retraining for new facts.
- **Private/proprietary data** — your docs, never in pretraining.
- **Grounding & [[ai/rag-and-retrieval/grounding-and-citations|citations]]** — answers
  trace to sources, which curbs [[ai/llms/why-llms-hallucinate|hallucination]] and
  builds trust.
- **Access control** — filter what's retrievable per user.

## RAG vs fine-tuning (the key distinction)

> **RAG is for knowledge (facts); [[ai/fine-tuning-and-alignment/index|fine-tuning]]
> is for behavior (form, style, format).** They're complementary, not competitors.

Fine-tuning to "teach facts" is expensive, goes stale, and still
[[ai/llms/why-llms-hallucinate|hallucinates]]. RAG is the default for knowledge-grounded
apps; fine-tune on top when you also need a specific tone or output shape.

## When NOT to reach for RAG

- The task needs **no external knowledge** (summarize the text I pasted; classify this).
- The needed facts already **fit in the prompt** — just include them
  ([[ai/rag-and-retrieval/rag-vs-long-context|RAG vs long context]]).
- You need a **behavior** change, not facts → fine-tune.
- The corpus is tiny and static → a long prompt or simple lookup may beat a vector DB.

## Pitfall

RAG adds real complexity (chunking, indexing, retrieval quality, eval). Don't build a
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector pipeline]] for a problem a
paragraph of context solves. Earn the complexity.

**Connects to:** [[ai/fine-tuning-and-alignment/index|RAG vs fine-tune]] ·
[[ai/llms/why-llms-hallucinate|grounding vs hallucination]] ·
[[ai/rag-and-retrieval/rag-vs-long-context|RAG vs long context]]
