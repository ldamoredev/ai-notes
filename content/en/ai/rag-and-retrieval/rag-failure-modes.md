---
title: "RAG failure modes"
description: A field guide to why RAG answers go wrong — and which stage to fix for each symptom. Most "the LLM is dumb" complaints are retrieval bugs.
tags: [rag, debugging, failure-modes]
order: 10
updated: 2026-06-07
---
# RAG failure modes

RAG has many moving parts, so failures need diagnosis, not guesswork. The useful habit:
map each **symptom** to the **stage** that owns it, because the fixes are different and
non-overlapping.

## The failure map

| Symptom | Likely stage | Fix |
|---|---|---|
| Answer misses a fact that **is** in the corpus | retrieval recall | [[ai/rag-and-retrieval/chunking|chunking]], [[ai/rag-and-retrieval/hybrid-search|hybrid search]], index recall |
| Right doc retrieved but ranked low / crowded out | ranking | [[ai/rag-and-retrieval/reranking|reranking]], smaller top-k |
| Exact term/code not found | lexical gap | add [[ai/rag-and-retrieval/hybrid-search|keyword search]] |
| Chunk retrieved but answer ignores it | generation | [[ai/rag-and-retrieval/grounding-and-citations|grounding]] prompt, ordering, fewer chunks |
| Confident but unsupported claims | grounding | "answer only from context", low temp, [[ai/rag-and-retrieval/evaluating-rag|faithfulness eval]] |
| Follow-up questions retrieve nonsense | query | [[ai/rag-and-retrieval/query-transformations|rewrite follow-ups to standalone]] |
| Answer buried / partial on long context | context | [[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]] — rerank + trim |

## Two structural traps

- **The answer isn't in the corpus** — no retrieval trick invents it. RAG can only
  surface what exists; coverage gaps need *content*, not tuning.
- **Stale or duplicated index** — outdated chunks or near-duplicates poison results;
  keep the index fresh and deduplicated.

## The debugging order

1. **Inspect what was retrieved** for failing queries — this answers "retrieval or
   generation?" in seconds and is the step people skip.
2. Fix the **earliest** broken stage first (recall before ranking before generation).
3. Re-[[ai/rag-and-retrieval/evaluating-rag|measure]]; don't change two things at once.

> "The LLM gave a bad answer" is usually "retrieval gave it bad context." Look at the
> retrieved chunks before touching the prompt or the model.

**Connects to:** [[ai/rag-and-retrieval/evaluating-rag|evaluating RAG]] ·
[[ai/rag-and-retrieval/chunking|chunking]] ·
[[ai/llms/why-llms-hallucinate|hallucination]]
