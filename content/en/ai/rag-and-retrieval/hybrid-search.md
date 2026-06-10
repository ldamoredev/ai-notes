---
title: "Hybrid search: dense + keyword"
description: Dense embeddings capture meaning; keyword (BM25) nails exact terms. Combining them with fusion beats either alone — the reliable RAG default.
tags: [rag, hybrid-search, bm25, retrieval]
order: 5
updated: 2026-06-10
---
# Hybrid search: dense + keyword

**Mental model:** dense and sparse retrieval fail in *opposite* directions — embeddings
blur exact strings; keyword matching is blind to paraphrase. Running both and fusing
the ranked lists covers each method's blind spot, which is why hybrid is the most
reliable single retrieval upgrade and the production default.

## The two retrievers

- **Dense** — [[ai/rag-and-retrieval/embeddings-for-retrieval|embedding]] similarity.
  Captures meaning ("car" ≈ "automobile", question ≈ answer phrasing) but smears
  product codes, error strings, names, and rare jargon into fuzzy semantic soup.
- **Sparse (BM25)** — the term-weighting function from Robertson & Zaragoza 2009
  ([The Probabilistic Relevance Framework](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf)),
  still the lexical baseline 30+ years after its Okapi roots. Score ≈ sum over query
  terms of `IDF(term) × saturated term frequency`, normalized by document length
  (knobs `k1` ≈ 1.2–2.0 controls TF saturation, `b` ≈ 0.75 controls length
  normalization). It nails exact tokens: `E1042`, `SKU 9F-22`, `useEffect`.

BEIR (Thakur et al. 2021, [arXiv:2104.08663](https://arxiv.org/abs/2104.08663)) made
the case quantitatively: zero-shot, BM25 beats many dense retrievers out of domain.
Dense wins in-domain on paraphrase; neither dominates — hence fusion.

## Reciprocal Rank Fusion

The standard merge is **RRF** (Cormack, Clarke & Büttcher, SIGIR 2009): score each doc
by the sum of `1 / (k + rank)` across lists (`k = 60` in the paper; it damps the
influence of top ranks). Rank-based fusion sidesteps the impossible problem of
calibrating cosine scores against BM25 scores.

```typescript
type Ranked = { id: string }[];

export function rrf(lists: Ranked[], k = 60, weights?: number[]): string[] {
  const scores = new Map<string, number>();
  lists.forEach((list, li) => {
    const w = weights?.[li] ?? 1;
    list.forEach(({ id }, rank) => {
      scores.set(id, (scores.get(id) ?? 0) + w / (k + rank + 1));
    });
  });
  return [...scores.entries()].sort((a, b) => b[1] - a[1]).map(([id]) => id);
}
```

`weights` lets you bias dense vs sparse (e.g. 0.7/0.3 for a prose-heavy corpus,
inverted for log search) — tune against your
[[ai/rag-and-retrieval/evaluating-rag|eval set]], don't guess.

## Hybrid in Postgres (no new infra)

Postgres gives you both halves: pgvector for dense, full-text search for sparse. One
round trip with two CTEs:

```typescript
const hits = await db.execute(sql`
  WITH dense AS (
    SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> ${qVec}::vector) AS r
    FROM chunks WHERE tenant_id = ${tenantId}
    ORDER BY embedding <=> ${qVec}::vector LIMIT 40
  ),
  sparse AS (
    SELECT id, ROW_NUMBER() OVER (
      ORDER BY ts_rank_cd(tsv, websearch_to_tsquery('english', ${query})) DESC) AS r
    FROM chunks
    WHERE tenant_id = ${tenantId}
      AND tsv @@ websearch_to_tsquery('english', ${query})
    LIMIT 40
  )
  SELECT c.id, c.text,
         COALESCE(1.0/(60+dense.r), 0) + COALESCE(1.0/(60+sparse.r), 0) AS rrf
  FROM chunks c
  LEFT JOIN dense  ON dense.id  = c.id
  LEFT JOIN sparse ON sparse.id = c.id
  WHERE dense.id IS NOT NULL OR sparse.id IS NOT NULL
  ORDER BY rrf DESC LIMIT 20
`);
```

(Requires a `tsv tsvector` generated column + GIN index. Postgres FTS is not full
BM25 — `ts_rank_cd` lacks IDF — but it captures most of the exact-match win; if evals
demand true BM25, the `pg_search`/ParadeDB extension or OpenSearch provide it.)

Anthropic's [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
numbers quantify the stack: contextual embeddings alone cut top-20 retrieval failures
35%; **adding contextual BM25 took it to 49%** — the BM25 half of hybrid carried a
third of the total improvement.

## Why it wins (and when it doesn't)

| Query type | Dense | BM25 | Hybrid |
|---|---|---|---|
| "how do I reset my password" | strong | ok | strong |
| "error E1042" / "SKU 9F-22" | weak | strong | strong |
| paraphrased concept, cross-lingual | strong | weak | strong |
| misspelled exact term | weak | weak | weak (needs fuzzy/trigram) |

Hybrid is rarely worse than the better single method and usually better than both. It
does **not** fix: misspellings (add `pg_trgm` fuzzy matching), answers missing from
the corpus, or [[ai/rag-and-retrieval/chunking|bad chunking]].

## Cost & latency lens

Both branches run in parallel against the same Postgres in one query — the latency
add is effectively zero next to embedding the query (~50–100 ms) and generation.
Sparse needs its own index (GIN on `tsvector`: storage + write amplification) but no
new service. This is the rare quality upgrade that costs no per-query tokens —
compare [[ai/rag-and-retrieval/query-transformations|query transforms]] (extra LLM
call) or [[ai/rag-and-retrieval/reranking|reranking]] (extra model call). Order of
adoption follows: **hybrid first, then rerank, then transforms.**

## Failure modes

- **Fusing too-short lists** — RRF over two top-5 lists has nothing to work with;
  fuse top-40/top-50 from each branch, then cut to 20 (or
  [[ai/rag-and-retrieval/reranking|rerank]] the fused list down to 5–8).
- **Language/analyzer mismatch** — `websearch_to_tsquery('english', ...)` stems
  English; code identifiers and other languages need different analyzers or they
  silently tokenize wrong.
- **Misdiagnosis in reverse** — teams swap embedding models for months chasing
  exact-term misses that BM25 fixes in a day. If failing queries contain identifiers,
  codes, or names: it's lexical. Add the sparse branch first.

**Connects to:** [[ai/rag-and-retrieval/embeddings-for-retrieval|dense embeddings]] ·
[[ai/rag-and-retrieval/reranking|reranking the fused list]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|indexes]] ·
[[ai/rag-and-retrieval/rag-failure-modes|lexical-gap failures]]

## Sources

- [Robertson & Zaragoza 2009 — The Probabilistic Relevance Framework: BM25 and Beyond](https://www.staff.city.ac.uk/~sbrp622/papers/foundations_bm25_review.pdf) — the definitive BM25 reference; §3 demystifies k1 and b.
- [Cormack, Clarke & Büttcher 2009 — Reciprocal Rank Fusion (SIGIR)](https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf) — two pages; RRF beating learned fusion methods is the whole point.
- [Thakur et al. 2021 — BEIR (arXiv:2104.08663)](https://arxiv.org/abs/2104.08663) — the zero-shot benchmark showing BM25's stubborn strength out of domain.
- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — production numbers for embeddings+BM25 fusion (and contextualizing both).
- [Weaviate — Hybrid search explained](https://weaviate.io/blog/hybrid-search-explained) — clear walkthrough of fusion math and weighting in a production engine.
