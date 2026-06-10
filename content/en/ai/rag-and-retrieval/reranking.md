---
title: "Reranking"
description: First-stage retrieval favors recall; a cross-encoder reranker restores precision by carefully re-scoring the top candidates. The cheap, high-impact RAG upgrade.
tags: [rag, reranking, cross-encoder, precision]
order: 6
updated: 2026-06-10
---
# Reranking

**Mental model:** retrieval is two stages with opposite objectives. Stage one
([[ai/rag-and-retrieval/vector-databases-and-indexes|ANN]] /
[[ai/rag-and-retrieval/hybrid-search|hybrid]]) is tuned to *not miss* the right chunk
across millions (recall); its ordering is rough. Stage two — the **reranker** —
re-scores only the top ~50–100 candidates with a much more accurate model and keeps
the best 3–8 for the [[ai/llms/context-window-and-kv-cache|context window]]
(precision). You need both: the right chunk must first be *retrieved*, then *ranked to
the top*.

## Bi-encoder vs cross-encoder — why the accuracy gap exists

- **Bi-encoder** (stage one) embeds query and document *separately*; relevance is a
  dot product between two precomputed points. Fast, indexable — but the query never
  attends to the document's tokens.
- **Cross-encoder** (reranker) feeds **query + document together** through one
  transformer; every query token attends to every document token, capturing exact
  matches, negation, and conditionals that bi-encoders structurally cannot. The
  lineage runs from BERT passage re-ranking (Nogueira & Cho 2019,
  [arXiv:1901.04085](https://arxiv.org/abs/1901.04085)) to today's hosted rerankers.
  Accurate, but O(candidates) full forward passes per query — usable only on a
  shortlist.

Middle ground: **ColBERT** late interaction (Khattab & Zaharia 2020,
[arXiv:2004.12832](https://arxiv.org/abs/2004.12832); ColBERTv2
[arXiv:2112.01488](https://arxiv.org/abs/2112.01488)) stores per-token vectors and
computes MaxSim at query time — near-cross-encoder quality, indexable, at ~10×
storage. Worth knowing; rarely worth operating yourself when hosted rerankers exist.

## What it's worth (numbers)

Anthropic's [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval)
stack: contextual embeddings + contextual BM25 cut top-20 retrieval failures 49%;
**adding a reranker took it to 67%** (5.7% → 1.9% failure rate). Reranking also
*shrinks* prompts: passing a reranked top-5 instead of a raw top-20 routinely improves
answers (less [[ai/llms/long-context-and-lost-in-the-middle|middle-of-context dilution]])
while cutting generation tokens — one of the few upgrades that improves quality and
cost in the same move.

## Model options (2026)

| Model | Type | Notes |
|---|---|---|
| Cohere Rerank 3.5 / 4.0 | hosted | multilingual, ~600 ms typical on 100 docs; the common default |
| Voyage `rerank-2.5` | hosted (MongoDB) | comparable quality/latency tier |
| ZeroEntropy `zerank` | hosted | tops 2026 reranker leaderboards (ELO-style evals) |
| Qwen3-Reranker ([arXiv:2506.05176](https://arxiv.org/abs/2506.05176)) | open, Apache 2.0 | 0.6B–8B; 100+ languages; self-host |
| BGE `reranker-v2-m3` | open | lightweight self-host baseline |
| RankGPT-style LLM ranking (Sun et al. 2023, [arXiv:2304.09542](https://arxiv.org/abs/2304.09542)) | any LLM | listwise prompting; flexible, slow, pricey — fine for offline eval, rarely for serving |

Model size ≠ quality here — small dedicated rerankers regularly match models 10×
larger. Pick hosted unless data residency forbids it; benchmark 2 candidates on your
own [[ai/rag-and-retrieval/evaluating-rag|eval set]].

## Wiring it in (TypeScript)

```typescript
type Candidate = { id: string; text: string };

export async function rerank(
  query: string,
  candidates: Candidate[],
  topN = 6,
): Promise<Candidate[]> {
  const res = await fetch("https://api.cohere.com/v2/rerank", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.COHERE_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "rerank-v3.5",
      query,
      documents: candidates.map((c) => c.text),
      top_n: topN,
    }),
  });
  if (!res.ok) return candidates.slice(0, topN); // degrade gracefully: keep stage-1 order
  const { results } = await res.json() as {
    results: { index: number; relevance_score: number }[];
  };
  return results.map((r) => candidates[r.index]);
}

// pipeline: hybrid top-50 → rerank → top-6 → prompt
const fused = await hybridSearch(query, 50);
const context = await rerank(query, fused, 6);
```

The fallback branch matters: a reranker outage should degrade ranking quality, not
take down answering. Log `relevance_score`s in your
[[ai/mlops/llm-observability-and-tracing|traces]] — their distribution over time is an
early-warning signal for retrieval drift.

## Decision rule: when to add it

- Add a reranker when evals show **recall@50 high but precision@5 low** — the right
  chunk is being retrieved but ranked 12th. That's precisely the gap rerankers close.
- Skip it when stage-1 already ranks well (small/clean corpora), when your corpus is
  tiny enough to pass everything, or when the p95 latency budget can't absorb
  ~100–600 ms.
- Don't use it to paper over [[ai/rag-and-retrieval/chunking|bad chunks]] or recall
  misses — a reranker **only reorders what stage one returned**. If the answer isn't
  in the candidate set, fix chunking/recall first.

## Cost & latency lens

Hosted reranking adds ~100–600 ms p50 and a per-search fee (Cohere bills per 1K
searches of ≤100 docs). It sits on the critical path before generation, so it's
usually the second-largest latency contributor after the LLM itself. Offsets: smaller
prompts (fewer input tokens per answer) and fewer retries on wrong answers. For
latency-critical paths, rerank 30 candidates instead of 100 — quality loss is usually
negligible.

## Failure modes

- **Candidate set too small** — reranking a top-5 is a no-op with extra latency; feed
  it 30–100.
- **Truncation** — rerankers have input limits; oversized chunks get tail-truncated
  and the evidence may live in the tail. Another reason for
  [[ai/rag-and-retrieval/chunking|disciplined chunk sizes]].
- **Stage-1 confidence in the prompt** — after reranking, stage-1 scores are obsolete;
  don't surface them to users or the model.
- **Cross-encoder ≠ truth** — it ranks topical relevance better, but a relevant-looking
  wrong chunk still ranks high; [[ai/rag-and-retrieval/grounding-and-citations|grounding]]
  is still on the generator.

**Connects to:** [[ai/rag-and-retrieval/hybrid-search|hybrid first stage]] ·
[[ai/rag-and-retrieval/evaluating-rag|precision vs recall]] ·
[[ai/llms/long-context-and-lost-in-the-middle|ordering context]] ·
[[ai/rag-and-retrieval/advanced-rag-patterns|contextual retrieval stack]]

## Sources

- [Nogueira & Cho 2019 — Passage Re-ranking with BERT (arXiv:1901.04085)](https://arxiv.org/abs/1901.04085) — where modern reranking starts; the cross-encoder recipe in 4 pages.
- [Khattab & Zaharia 2020 — ColBERT (arXiv:2004.12832)](https://arxiv.org/abs/2004.12832) — late interaction, the principled middle point between bi- and cross-encoders.
- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — the 49% → 67% reranking delta on a production-shaped benchmark.
- [Cohere docs — Rerank](https://docs.cohere.com/docs/rerank) — API semantics, limits, and model versions for the most-used hosted reranker.
- [Sun et al. 2023 — RankGPT (arXiv:2304.09542)](https://arxiv.org/abs/2304.09542) — LLMs as listwise rerankers; useful for offline judgment, instructive about cost at serving time.
- [ZeroEntropy — Ultimate guide to choosing a reranker (2025)](https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/) — current vendor landscape with latency/quality trade-offs (vendor-written; read critically).
