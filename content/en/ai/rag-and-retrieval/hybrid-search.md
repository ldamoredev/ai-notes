---
title: "Hybrid search: dense + keyword"
description: Dense embeddings capture meaning; keyword (BM25) nails exact terms. Combining them with fusion beats either alone — the reliable RAG default.
tags: [rag, hybrid-search, bm25, retrieval]
order: 5
updated: 2026-06-07
---
# Hybrid search: dense + keyword

The single most reliable retrieval upgrade is to **stop choosing** between semantic and
keyword search and run **both**. They fail in opposite ways, so together they cover each
other.

## Two complementary methods

- **Dense (vector)** — [[ai/rag-and-retrieval/embeddings-for-retrieval|embedding]]
  similarity. Captures *meaning* and paraphrase ("car" ≈ "automobile") but can miss
  exact strings.
- **Sparse (keyword, BM25)** — classic term-frequency matching. Nails **exact** terms:
  product codes, error messages, names, rare jargon, acronyms — precisely what
  embeddings blur.

## Fusing the results

Run both retrievers and merge their ranked lists. The common, robust method is
**Reciprocal Rank Fusion (RRF)**: score each result by its *rank* in each list and sum,
so an item ranked highly by either method floats up — no need to calibrate
incompatible score scales. Then optionally [[ai/rag-and-retrieval/reranking|rerank]] the
fused top-k.

## Why it wins

| Query type | Dense | Keyword | Hybrid |
|---|---|---|---|
| "how do I reset my password" | strong | ok | strong |
| "error E1042" / "SKU 9F-22" | weak | strong | strong |
| paraphrased concept | strong | weak | strong |

Hybrid is rarely worse than the better of the two and often better than both — which
is why it's the sensible default for production RAG.

## Pitfall

Keyword search needs its own index (e.g. BM25/Elasticsearch/OpenSearch or a vector DB
with built-in sparse support), so hybrid adds infra. But reaching for a fancier
embedding model when the real miss is an **exact-term** query is a common misdiagnosis
— add keyword first.

**Connects to:** [[ai/rag-and-retrieval/embeddings-for-retrieval|dense embeddings]] ·
[[ai/rag-and-retrieval/reranking|reranking the fused list]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|indexes]]
