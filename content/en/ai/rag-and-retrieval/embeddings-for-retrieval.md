---
title: "Embeddings & embedding models"
description: Embeddings turn text into vectors where nearby means similar. Choosing a model, the symmetry trap, and why you must re-embed when you switch.
tags: [rag, embeddings, semantic-search]
order: 3
updated: 2026-06-10
---
# Embeddings & embedding models

**Mental model:** an embedding model maps text into a vector space where semantic
similarity becomes [[ai/foundations/linear-algebra-for-ml|geometric closeness]];
retrieval is "find the chunk vectors nearest the query vector." The space is defined
by one specific model — vectors from different models are mutually meaningless, which
drives every operational rule below.

## How retrieval embeddings actually work

Modern retrieval embedders are **bi-encoders** descended from Sentence-BERT (Reimers &
Gurevych 2019, [arXiv:1908.10084](https://arxiv.org/abs/1908.10084)) and DPR
(Karpukhin et al. 2020, [arXiv:2004.04906](https://arxiv.org/abs/2004.04906)): a
transformer encodes query and document *independently* into single vectors, trained
with contrastive objectives so relevant query–passage pairs land close together.
Independence is what makes them fast (document vectors are precomputed); it is also
their accuracy ceiling — the query never "sees" the document, which is why
[[ai/rag-and-retrieval/reranking|cross-encoder reranking]] exists.

Two consequences worth internalizing:

- **Asymmetry is trained in.** Retrieval models are trained on (short query → long
  passage) pairs, and most expose this: Voyage has `input_type: "query" | "document"`;
  open models like E5 (Wang et al. 2022,
  [arXiv:2212.03533](https://arxiv.org/abs/2212.03533)) require `query:` / `passage:`
  prefixes. Omitting these silently costs recall — the #1 silent embedding bug.
- **Similarity is topical, not factual.** "What is our refund window?" embeds close to
  a chunk *discussing* refund windows whether or not that chunk states the answer —
  and close to a chunk stating the *wrong* (outdated) answer. Similarity ranks
  candidates; [[ai/rag-and-retrieval/grounding-and-citations|grounding]] and
  [[ai/rag-and-retrieval/evaluating-rag|evals]] handle truth.

## Choosing a model (2026 state)

Benchmarks: **MTEB** (Muennighoff et al. 2022,
[arXiv:2210.07316](https://arxiv.org/abs/2210.07316)) is the standard leaderboard;
**BEIR** (Thakur et al. 2021, [arXiv:2104.08663](https://arxiv.org/abs/2104.08663))
tests zero-shot retrieval transfer. Both are widely targeted by training data, so use
them as a shortlist filter, never as the decision.

| Model (2026) | Type | Notes |
|---|---|---|
| Voyage `voyage-3-large` | hosted (MongoDB-owned since Feb 2025) | top-tier retrieval quality; Anthropic's recommended partner (Anthropic has no embeddings API) |
| Google `gemini-embedding` | hosted | leads MTEB v2 English (~68.3) |
| Cohere `embed-v4` | hosted | strong multilingual + multimodal |
| OpenAI `text-embedding-3-large` | hosted | ubiquitous baseline; Matryoshka-truncatable |
| Qwen3-Embedding ([arXiv:2506.05176](https://arxiv.org/abs/2506.05176)) | open (Apache 2.0) | 100+ languages; rivals hosted APIs |
| BGE-M3 ([arXiv:2402.03216](https://arxiv.org/abs/2402.03216)) | open | dense + sparse + multi-vector from one model |

Decision rule: shortlist 2–3 from the leaderboard, then **run your own 50-question
recall@k eval on your corpus** — domain fit (legal, medical, code, your product's
jargon) reorders leaderboards routinely. Prefer hosted if you don't want to operate
GPU inference; prefer open if data cannot leave your infra.

**Dimensions:** bigger ≠ better past a point; it costs storage, RAM, and index build
time ([[ai/rag-and-retrieval/vector-databases-and-indexes|HNSW]] memory scales with
dims). Matryoshka-trained models (Kusupati et al. 2022,
[arXiv:2205.13147](https://arxiv.org/abs/2205.13147)) let you truncate vectors (e.g.
2048 → 512) with modest recall loss — re-rank the truncated top-100 with full vectors
if you need the quality back. 1024 dims is a sane 2026 default.

## The hard operational rules

- **Never mix models.** Query and documents must be embedded by the same model *and
  version*. There is no cross-model compatibility, ever.
- **Model change = full re-embed + reindex.** Budget for it (rate limits make this
  days, not minutes, on large corpora) and version the embedding model in your schema:

```typescript
// store model + version with every embedding — migrations become queryable
export const chunks = pgTable("chunks", {
  // ...
  embedding: vector("embedding", { dimensions: 1024 }).notNull(),
  embeddingModel: text("embedding_model").notNull().default("voyage-3-large"),
});
```

- **Match the distance metric to the model.** Most retrieval models are trained for
  cosine; many hosted APIs return already-normalized vectors, making cosine and dot
  product equivalent. Check the model card; in pgvector use `vector_cosine_ops` unless
  documented otherwise.
- **Batch document embedding.** APIs take 100+ inputs per call; embedding one chunk
  per request makes indexing 50× slower and rate-limit-bound.

## Cost & latency lens

Embedding is the cheap part of RAG: on the order of $0.02–$0.18 per million tokens
(2026 hosted pricing) — one-time per document version, plus ~50–100 ms per query at
answer time. The real recurring cost lives downstream in
[[ai/inference-and-optimization/cost-modeling-for-llm-serving|generation tokens]].
Implication: don't pick an embedding model to save money; pick it for recall, and
spend savings-attention on how many chunks you stuff into the prompt.

## Failure modes

- **Query/document prefix omitted** → uniform, mediocre recall. Check first.
- **Domain vocabulary gap** — generic embedders blur product codes, error strings, and
  rare jargon; exact-term queries fail. The fix is usually
  [[ai/rag-and-retrieval/hybrid-search|hybrid search]], not a bigger embedder.
- **Stale-truth similarity** — outdated chunks embed just as well as current ones;
  deduplicate and version the corpus.
- **Silent model upgrades** — a hosted provider deprecating your model version forces
  a re-embed on their schedule; pin versions and keep raw chunk text so re-embedding
  is mechanical.

**Connects to:** [[ai/deep-learning/embeddings-and-latent-spaces|embedding spaces]] ·
[[ai/rag-and-retrieval/vector-databases-and-indexes|vector indexes]] ·
[[ai/rag-and-retrieval/hybrid-search|hybrid search]] ·
[[ai/rag-and-retrieval/reranking|cross-encoders]]

## Sources

- [Reimers & Gurevych 2019 — Sentence-BERT (arXiv:1908.10084)](https://arxiv.org/abs/1908.10084) — the bi-encoder blueprint; explains why independent encoding is fast and limited.
- [Karpukhin et al. 2020 — Dense Passage Retrieval (arXiv:2004.04906)](https://arxiv.org/abs/2004.04906) — contrastive training for asymmetric query→passage retrieval.
- [Muennighoff et al. 2022 — MTEB (arXiv:2210.07316)](https://arxiv.org/abs/2210.07316) + [leaderboard](https://huggingface.co/spaces/mteb/leaderboard) — the shortlisting tool; read the paper to know what the scores do and don't measure.
- [Kusupati et al. 2022 — Matryoshka Representation Learning (arXiv:2205.13147)](https://arxiv.org/abs/2205.13147) — why modern vectors can be truncated, and the storage/recall trade.
- [Voyage AI docs (MongoDB)](https://docs.voyageai.com/docs/embeddings) — `input_type` semantics and current model lineup; Anthropic's recommended embeddings partner.
- [Wang et al. 2022 — E5 (arXiv:2212.03533)](https://arxiv.org/abs/2212.03533) — the canonical open model with mandatory query/passage prefixes; the bug you'll actually hit.
