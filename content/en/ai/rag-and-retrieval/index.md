---
title: RAG and Retrieval
description: Retrieval-augmented generation as an information system — chunking, embeddings, hybrid search, reranking, grounding, and how to evaluate every stage.
tags: [rag, retrieval]
order: 0
updated: 2026-06-07
---
# RAG and Retrieval

**Retrieval-augmented generation** gives an [[ai/llms/index|LLM]] the facts it needs at
answer time by fetching relevant text and putting it in the
[[ai/llms/context-window-and-kv-cache|context window]]. It is how most teams ship
knowledge-grounded AI, because it fixes the model's two biggest weaknesses —
[[ai/llms/why-llms-hallucinate|hallucination]] and stale
[[ai/foundations/distribution-shift|knowledge]] — without retraining.

> RAG is a **search problem wearing an LLM hat.** Most "RAG quality" issues are
> retrieval issues. Fix retrieval first.

## Foundations

- [[ai/rag-and-retrieval/why-rag|Why RAG (and when not to)]]
- [[ai/rag-and-retrieval/rag-first-pass-design|RAG first-pass design]]
- [[ai/rag-and-retrieval/chunking|Chunking that respects structure]]
- [[ai/rag-and-retrieval/embeddings-for-retrieval|Embeddings & embedding models]]

## Retrieval quality

- [[ai/rag-and-retrieval/vector-databases-and-indexes|Vector databases & ANN indexes]]
- [[ai/rag-and-retrieval/hybrid-search|Hybrid search: dense + keyword]]
- [[ai/rag-and-retrieval/reranking|Reranking]]
- [[ai/rag-and-retrieval/query-transformations|Query transformations (rewriting, HyDE, multi-query)]]

## Generation & assessment

- [[ai/rag-and-retrieval/grounding-and-citations|Grounding & citations]]
- [[ai/rag-and-retrieval/evaluating-rag|Evaluating RAG: retriever vs generator]]
- [[ai/rag-and-retrieval/rag-failure-modes|RAG failure modes]]

## Beyond basic RAG

- [[ai/rag-and-retrieval/advanced-rag-patterns|Advanced patterns: contextual, graph & agentic RAG]]
- [[ai/rag-and-retrieval/rag-vs-long-context|RAG vs long context]]

## Core sources

- Anthropic — *Contextual Retrieval*.
- Pinecone / Weaviate — learning guides (chunking, hybrid, reranking).
- LlamaIndex & LangChain — advanced RAG docs.
- RAGAS — retrieval/generation evaluation; Jason Liu & Eugene Yan — RAG patterns.
