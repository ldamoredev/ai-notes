---
title: "Reranking"
description: First-stage retrieval favors recall; a cross-encoder reranker restores precision by carefully re-scoring the top candidates. The cheap, high-impact RAG upgrade.
tags: [rag, reranking, cross-encoder, precision]
order: 6
updated: 2026-06-07
---
# Reranking

Retrieval is usually **two stages**: a fast first pass casts a wide net (high recall),
then a slower, smarter **reranker** re-orders those candidates for precision before
they hit the [[ai/llms/context-window-and-kv-cache|context window]]. It's one of the
highest-ROI additions to a RAG pipeline.

## Why two stages

[[ai/rag-and-retrieval/vector-databases-and-indexes|ANN]] and
[[ai/rag-and-retrieval/hybrid-search|hybrid]] search are tuned to *not miss* the right
chunk (recall) across millions of docs, but their ordering is rough. You only want to
spend [[ai/llms/tokenization|tokens]] on the few **best** chunks — so re-score the top
~50–100 and keep the top ~3–8.

## Bi-encoder vs cross-encoder

- **Bi-encoder** (first stage) — embeds query and doc *separately*, compares vectors.
  Fast and precomputable, but never lets the query and document "see" each other.
- **Cross-encoder** (reranker) — feeds **query + chunk together** through a model that
  scores their relevance directly. Far more accurate, far too slow to run over the whole
  corpus — perfect for re-scoring a shortlist.

> First-stage retrieval optimizes recall; the reranker optimizes precision. You need
> both because the right chunk must first be *retrieved*, then *ranked to the top*.

## Practical notes

- Use a hosted reranker (Cohere Rerank, etc.) or an open cross-encoder; it's a small
  add to latency for a big relevance gain.
- Rerank the **fused** hybrid results, then pass only the top few to the model — this
  also fights [[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]] by
  keeping context short and ordered.

## Pitfall

A reranker can't surface a chunk that first-stage retrieval never returned — it only
reorders what it's given. If the answer isn't in the candidate set, fix
[[ai/rag-and-retrieval/chunking|chunking]]/[[ai/rag-and-retrieval/hybrid-search|recall]]
first.

**Connects to:** [[ai/rag-and-retrieval/hybrid-search|hybrid search]] ·
[[ai/rag-and-retrieval/evaluating-rag|precision vs recall]] ·
[[ai/llms/long-context-and-lost-in-the-middle|ordering context]]
