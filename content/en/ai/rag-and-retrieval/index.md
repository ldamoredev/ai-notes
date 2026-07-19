---
title: RAG and Retrieval
description: Retrieval-augmented generation as an information system — chunking, embeddings, hybrid search, reranking, grounding, and how to evaluate every stage.
tags: [rag, retrieval]
order: 0
updated: 2026-06-10
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

## Mental model

RAG is an information-retrieval system whose selected evidence becomes model input. Query construction, indexing, candidate generation, reranking, context assembly, and answer attribution are separate stages with separate recall, precision, latency, and failure budgets.

## Roadmap: foundations to advanced retrieval

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

**Connects to:** [[ai/data-for-ai/index|Data for AI]] · [[ai/prompt-engineering/index|Context Engineering]] · [[ai/evaluation/evaluating-rag-systems|Evaluating RAG Systems]]

## Core sources

- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — the single most useful applied-RAG write-up: technique, measured failure-rate reductions, costs, and the runnable cookbook.
- [Lewis et al. 2020 — Retrieval-Augmented Generation (arXiv:2005.11401)](https://arxiv.org/abs/2005.11401) — the original paper; the retriever-generator factorization that still defines the field.
- [RAGAS docs](https://docs.ragas.io/) — the standard vocabulary and tooling for RAG evaluation (faithfulness, context precision/recall).
- [pgvector](https://github.com/pgvector/pgvector) — the reference Postgres vector store; the README doubles as an ANN-tuning crash course.
- [Pinecone Learning Center](https://www.pinecone.io/learn/) — consistently solid explainers on chunking, hybrid search, and reranking (vendor-hosted, technique-focused).
