---
title: "Chunking that respects structure"
description: How you split documents decides what can be retrieved. Chunk size, overlap, structure-aware splitting, and why bad chunking caps RAG quality.
tags: [rag, chunking, preprocessing]
order: 2
updated: 2026-06-07
---
# Chunking that respects structure

Before anything can be retrieved, documents are split into **chunks** that get
[[ai/rag-and-retrieval/embeddings-for-retrieval|embedded]] and indexed. The chunk is the
unit of retrieval, so chunking quietly sets the ceiling on RAG quality — a great
retriever can't fix badly cut text.

## The size tradeoff

- **Too small** — a chunk lacks the surrounding context to be understood or to answer
  fully; facts get severed from their referents.
- **Too large** — chunks dilute relevance (one query term in a wall of text scores
  poorly), waste [[ai/llms/context-window-and-kv-cache|context budget]], and bury the
  answer ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]).

There's no universal size; common starting points are a few hundred tokens with some
**overlap** so a fact spanning a boundary isn't cut in half.

## Respect structure

Splitting blindly every N characters cuts mid-sentence and mid-table. Better:

- Split on **natural boundaries** — headings, paragraphs, sections, code blocks, list
  items.
- Keep **semantically coherent** units together (a Q&A pair, a function, a table row +
  its header).
- Attach **metadata** (title, section, source, date) for filtering and
  [[ai/rag-and-retrieval/grounding-and-citations|citation]].

## Add context to chunks

A standalone chunk often loses what it refers to ("it improves performance" — *what*
does?). **Contextual retrieval** (prepend a short summary of the document/section to
each chunk before embedding) and adding titles/headers measurably boost retrieval —
see [[ai/rag-and-retrieval/advanced-rag-patterns|advanced patterns]].

## Pitfall

Chunking is the most under-invested, highest-leverage RAG step. If retrieval is poor,
inspect your chunks **before** swapping embedding models or
[[ai/rag-and-retrieval/reranking|rerankers]] — the problem is often a chunk that never
contained the answer cleanly.

**Connects to:** [[ai/rag-and-retrieval/embeddings-for-retrieval|embeddings]] ·
[[ai/rag-and-retrieval/advanced-rag-patterns|contextual retrieval]] ·
[[ai/rag-and-retrieval/rag-failure-modes|failure modes]]
