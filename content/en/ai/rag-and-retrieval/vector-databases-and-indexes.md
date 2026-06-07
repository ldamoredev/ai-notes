---
title: "Vector databases & ANN indexes"
description: Exact nearest-neighbor search doesn't scale, so vector DBs use approximate indexes like HNSW. What they trade, plus metadata filtering.
tags: [rag, vector-database, hnsw, ann]
order: 4
updated: 2026-06-07
---
# Vector databases & ANN indexes

Once chunks are [[ai/rag-and-retrieval/embeddings-for-retrieval|embedded]], you need to
find the nearest vectors to a query *fast*, across millions of them. Comparing the
query to every vector (exact kNN) is accurate but too slow at scale, so vector
databases use **Approximate Nearest Neighbor (ANN)** indexes.

## The core tradeoff

ANN trades a little **recall** for a lot of **speed**: it usually returns the true top
results, occasionally missing one, in milliseconds instead of seconds. For RAG that's
a great deal — and you can tune how approximate it is.

## HNSW, the common index

**HNSW** (Hierarchical Navigable Small World) builds a multi-layer graph you traverse
to hop quickly toward a query's neighborhood. Knobs:

- Build-time (`M`, `ef_construction`) — graph density vs index size/build time.
- Query-time (`ef_search`) — higher = better recall, slower. This is your
  speed/accuracy dial.

Other families exist (IVF, ScaNN, DiskANN for billion-scale on disk), but HNSW is the
default in most vector DBs.

## Metadata filtering matters as much as vectors

Real queries are "similar chunks **from this user's docs, in English, since 2024**."
Vector DBs combine ANN search with **metadata filters**. Store useful fields
(source, date, tenant, section) at index time — filtering is often what makes results
correct *and* enforces [[ai/ai-safety-and-security/index|access control]].

## Choosing one (briefly)

Managed (Pinecone), open-source (Weaviate, Qdrant, Milvus), or just a library
(FAISS) or a Postgres extension (pgvector). For small corpora, pgvector or FAISS is
plenty — don't over-engineer.

## Pitfall

Low [[ai/rag-and-retrieval/evaluating-rag|recall]] from a too-aggressive `ef_search`
silently drops the right chunk before the LLM ever sees it. If answers miss facts that
*are* in the corpus, check index recall and filters before blaming the model.

**Connects to:** [[ai/machine-learning/knn-and-svm|nearest neighbors]] ·
[[ai/rag-and-retrieval/hybrid-search|hybrid search]] ·
[[ai/rag-and-retrieval/evaluating-rag|recall]]
