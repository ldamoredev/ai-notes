---
title: "Embeddings & embedding models"
description: Embeddings turn text into vectors where nearby means similar. Choosing a model, the symmetry trap, and why you must re-embed when you switch.
tags: [rag, embeddings, semantic-search]
order: 3
updated: 2026-06-07
---
# Embeddings & embedding models

Semantic search rests on [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]]:
a model maps each chunk and each query into a vector so that semantic similarity
becomes [[ai/foundations/linear-algebra-for-ml|geometric closeness]]. Retrieval is then
"find the chunk vectors nearest the query vector."

## What makes a good retrieval embedding

- **Trained for retrieval** — query↔document matching (often with instructions/prefixes
  like "query:" / "passage:"), not just generic similarity.
- **Right dimension** — bigger isn't always better; it costs storage and
  [[ai/rag-and-retrieval/vector-databases-and-indexes|index]] memory.
- **Domain fit** — a model that understands your jargon (legal, medical, code) beats a
  generic one. Check a benchmark like MTEB, then test on *your* data.
- **Multilingual**, if your corpus or queries are.

## The hard rules

- **Never mix models** — query and documents must be embedded by the **same** model;
  vectors from different models are incomparable.
- **Re-embed everything when you change models** — the whole index must be rebuilt; you
  can't compare old and new vectors.
- **Normalize** if you compare with cosine similarity (most do).

## Embeddings vs keywords

Embeddings capture *meaning* ("car" ≈ "automobile") but can miss **exact** terms —
product codes, names, rare jargon — that keyword search nails. That gap is exactly why
[[ai/rag-and-retrieval/hybrid-search|hybrid search]] exists.

## Pitfall

Embedding similarity is **topical**, not factual: a chunk can be highly similar to the
query and still not contain the answer (or contain a *wrong* one). Similarity ranks
candidates; it doesn't verify truth — that's the job of the model +
[[ai/rag-and-retrieval/grounding-and-citations|grounding]] and
[[ai/rag-and-retrieval/evaluating-rag|eval]].

**Connects to:** [[ai/deep-learning/embeddings-and-latent-spaces|embeddings]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]] ·
[[ai/rag-and-retrieval/hybrid-search|hybrid search]]
