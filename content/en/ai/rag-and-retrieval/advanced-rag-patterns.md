---
title: "Advanced patterns: contextual, graph & agentic RAG"
description: When basic retrieve-then-read isn't enough — contextual retrieval, graph RAG for connected facts, and agentic RAG that decides what to fetch.
tags: [rag, contextual-retrieval, graph-rag, agentic-rag]
order: 11
updated: 2026-06-07
---
# Advanced patterns: contextual, graph & agentic RAG

Basic RAG — embed query, fetch top-k, stuff into prompt — covers a lot. When it
plateaus, these patterns target specific weaknesses. Reach for them only after the
[[ai/rag-and-retrieval/chunking|fundamentals]] and
[[ai/rag-and-retrieval/evaluating-rag|eval]] are solid.

## Contextual retrieval

[[ai/rag-and-retrieval/chunking|Chunks]] lose the context they came from. **Contextual
retrieval** (Anthropic) prepends a short, LLM-generated description of the
document/section to each chunk *before* embedding, so an isolated chunk still "knows"
what it's about. Pair it with [[ai/rag-and-retrieval/hybrid-search|hybrid search]] +
[[ai/rag-and-retrieval/reranking|reranking]] for a strong, simple stack — it
meaningfully cuts retrieval misses for modest cost.

## Graph RAG

Vector search retrieves *similar* chunks but struggles with questions that require
**connecting facts across documents** ("how is X related to Y across these reports?").
**Graph RAG** builds a knowledge graph of entities and relations, so retrieval can
traverse connections and answer multi-hop / global questions. More powerful for
relational and summarization-over-corpus queries — but heavier to build and maintain.

## Agentic RAG

Instead of one fixed retrieval step, an [[ai/agents-and-tools/index|agent]] *decides*:
whether to retrieve at all, which source/tool to query, whether the results suffice, and
whether to search again. Retrieval becomes a **tool** in a loop, enabling multi-step
research over several sources. The cost is latency, complexity, and new
[[ai/agents-and-tools/index|failure modes]] — use it when queries genuinely need
iterative, decision-driven lookup.

## Choosing

| Need | Pattern |
|---|---|
| Chunks lack context, recall misses | contextual retrieval |
| Multi-hop / relational / global questions | graph RAG |
| Dynamic, multi-source, iterative lookup | agentic RAG |

> Don't start here. Most RAG quality comes from [[ai/rag-and-retrieval/chunking|chunking]]
> + [[ai/rag-and-retrieval/hybrid-search|hybrid]] + [[ai/rag-and-retrieval/reranking|rerank]]
> + grounding. Add an advanced pattern to fix a *measured* gap.

**Connects to:** [[ai/rag-and-retrieval/chunking|contextual chunks]] ·
[[ai/agents-and-tools/index|agentic retrieval]] ·
[[ai/rag-and-retrieval/evaluating-rag|measure first]]
