---
title: "Vector databases & ANN indexes"
description: Exact nearest-neighbor search doesn't scale, so vector DBs use approximate indexes like HNSW. What they trade, plus metadata filtering.
tags: [rag, vector-database, hnsw, ann]
order: 4
updated: 2026-06-10
---
# Vector databases & ANN indexes

**Mental model:** exact nearest-neighbor search is a linear scan — fine at 100K
vectors, hopeless at 100M. ANN (Approximate Nearest Neighbor) indexes trade a few
points of **recall** for orders of magnitude of **speed**, and expose knobs that let
you buy the recall back with latency. Your job is to know where that dial sits,
because a too-aggressive setting silently drops the right chunk before the LLM ever
sees it.

## HNSW, the default index

**HNSW** (Hierarchical Navigable Small World — Malkov & Yashunin 2016,
[arXiv:1603.09320](https://arxiv.org/abs/1603.09320)) builds a multi-layer proximity
graph: sparse upper layers for long hops, dense bottom layer for precision. A query
greedily descends toward its neighborhood in O(log N) hops.

The knobs (pgvector names; defaults in parentheses):

| Knob | Phase | Effect |
|---|---|---|
| `m` (16) | build | edges per node — graph density vs index size |
| `ef_construction` (64) | build | candidate list during build — quality vs build time |
| `ef_search` (40) | query | candidates explored — **your recall/latency dial** |

Practical tuning: leave build params at defaults unless recall plateaus; tune
`ef_search` per-query-class against a measured
[[ai/rag-and-retrieval/evaluating-rag|recall@k]] target (e.g. raise until recall@10 ≥
0.95, then stop). Other families: **IVF** (cluster-then-scan; cheaper build, needs
training, recall degrades as data drifts) and **DiskANN** (Subramanya et al., NeurIPS
2019) for billion-scale on NVMe. HNSW in RAM is the right default until ~50–100M
vectors.

## pgvector specifics (the likely v1 store)

pgvector ≥ 0.8 covers most production needs in Postgres you already operate:

```sql
CREATE EXTENSION vector;

CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

SET hnsw.ef_search = 80;          -- per-session/query recall dial
SET hnsw.iterative_scan = relaxed_order;  -- 0.8.0+: fixes filtered-search recall
```

Worth knowing:

- **Iterative index scans (0.8.0, 2024)** — pre-0.8, `WHERE tenant_id = ...` +
  ANN could return *too few rows* (the index found k neighbors, the filter discarded
  most). Iterative scans keep walking the graph until enough filtered results exist
  (`hnsw.max_scan_tuples`, default 20,000, bounds the walk).
- **`halfvec`** — half-precision storage, ~50% smaller index, minimal recall loss;
  also the only way to index >2,000-dim vectors.
- **The planner can betray you** — verify with `EXPLAIN ANALYZE` that queries actually
  use the HNSW index; an unexpected seq scan turns 5 ms into 5 s at scale.

Drizzle query with tenant filtering:

```typescript
import { cosineDistance, desc, eq, sql, and, gt } from "drizzle-orm";

const similarity = sql<number>`1 - (${cosineDistance(chunks.embedding, qVec)})`;
const hits = await db
  .select({ id: chunks.id, text: chunks.text, similarity })
  .from(chunks)
  .innerJoin(documents, eq(chunks.documentId, documents.id))
  .where(and(eq(documents.tenantId, tenantId), gt(similarity, 0.3)))
  .orderBy((t) => desc(t.similarity))
  .limit(20);
```

(The `similarity > 0.3` floor discards garbage matches on out-of-corpus queries —
calibrate the threshold on your own score distribution; absolute cosine values are not
comparable across embedding models.)

## Metadata filtering matters as much as vectors

Real queries are "similar chunks **from this tenant's docs, in English, since 2024**."
Filtering is also where [[ai/ai-safety-and-security/privacy-and-data-governance|access
control]] lives — enforce it in the retrieval query (DB-side, ideally with Postgres
RLS), never by post-filtering chunks in application code where a bug leaks another
tenant's data into a prompt. Filtered ANN is *the* classic correctness trap: know
whether your store filters during traversal (pgvector 0.8 iterative scans, Qdrant
filtered HNSW) or after (recall collapse on selective filters).

## Choosing a store (decision rule, 2026)

| Scale / need | Choice |
|---|---|
| <5–10M vectors, already on Postgres | **pgvector** — no new infra, joins + RLS for free |
| Heavy filtered search, hybrid built-in | Qdrant / Weaviate (open-source) |
| Zero-ops, elastic scale | managed (Pinecone, Turbopuffer) |
| Library inside one process, static corpus | FAISS / hnswlib |
| Billion-scale | Milvus, DiskANN-based engines |

Bias: stay on pgvector until a *measured* limit (index RAM, p95 latency, write
throughput) forces a move. A second datastore is a permanent operational tax —
consistency, backups, ACL duplication.

## Cost & latency lens

ANN query latency is single-digit milliseconds — never your bottleneck (embedding the
query, [[ai/rag-and-retrieval/reranking|reranking]], and generation are). The real
costs are **RAM** (HNSW must fit in memory: ~`N × dims × 4` bytes + graph overhead —
10M × 1024-dim float32 ≈ 40 GB + edges; `halfvec` halves it) and **write churn**
(HNSW inserts are expensive; bulk-load then index, not the reverse). Log retrieval
latency and result scores per query in your
[[ai/mlops/llm-observability-and-tracing|traces]].

## Failure modes

- **Silent recall loss** — low `ef_search`, post-filtering, or an IVF index trained on
  old data distribution. Symptom: answers miss facts that are in the corpus. Check
  index recall against exact scan on a sample before blaming the model.
- **Score thresholds ported across models** — a 0.7 cosine in model A ≠ 0.7 in model
  B. Recalibrate on every embedding change.
- **Index/table drift** — deleted docs whose vectors linger serve
  [[ai/rag-and-retrieval/rag-failure-modes|stale chunks]]. Make delete/update paths
  first-class, not afterthoughts.

**Connects to:** [[ai/machine-learning/knn-and-svm|nearest neighbors]] ·
[[ai/rag-and-retrieval/hybrid-search|hybrid search]] ·
[[ai/rag-and-retrieval/evaluating-rag|recall measurement]] ·
[[ai/rag-and-retrieval/rag-first-pass-design|first-pass schema]]

## Sources

- [Malkov & Yashunin 2016 — HNSW (arXiv:1603.09320)](https://arxiv.org/abs/1603.09320) — the index you're almost certainly running; §4 explains what `ef` actually does.
- [pgvector README](https://github.com/pgvector/pgvector) — authoritative for operators, index options, iterative scans, `halfvec`; short and current.
- [Supabase — HNSW indexes guide](https://supabase.com/docs/guides/ai/vector-indexes/hnsw-indexes) — pragmatic pgvector tuning walkthrough with benchmarks.
- [Subramanya et al. 2019 — DiskANN (NeurIPS)](https://proceedings.neurips.cc/paper/2019/hash/09853c7fb1d3f8ee67a61b6bf4a7f8e6-Abstract.html) — what billion-scale on SSD looks like, for when RAM-resident HNSW stops scaling.
- [Qdrant docs — Filtrable HNSW](https://qdrant.tech/articles/filtrable-hnsw/) — the clearest write-up of why filtered ANN breaks naive indexes and how in-traversal filtering fixes it.
