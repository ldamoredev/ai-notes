---
title: RAG First-Pass Design
description: A small checklist for designing a first useful RAG system.
tags: [rag, retrieval, engineering]
order: 1
updated: 2026-06-10
---
# RAG First-Pass Design

**Mental model:** a first-pass RAG system should optimize for **inspectability before
cleverness**. Every component you add before you can see what retrieval returned is a
component you'll debug blind. The v1 goal is not maximum quality — it's a pipeline
where every stage's output is loggable, so v2 improvements are
[[ai/rag-and-retrieval/evaluating-rag|measured]], not guessed.

## Design questions before any code

1. **What is the answerable question set?** Write 20–50 real questions users will ask.
   If you can't, you're not ready to build — you're guessing at requirements.
2. **Which documents own those answers?** Map each question to the doc(s) that should
   answer it. Questions with no owning doc are *content gaps*; no retrieval tuning
   will fix them ([[ai/rag-and-retrieval/rag-failure-modes|structural trap #1]]).
3. **Who may see what?** Tenancy and ACLs are retrieval *filters*, designed into the
   schema on day one — retrofitting them is painful and a
   [[ai/ai-safety-and-security/data-and-pii-leakage|leak risk]].
4. **How fresh must answers be?** Determines whether indexing is a batch job or an
   event-driven pipeline.
5. **What does a wrong answer cost?** Calibrates how much you invest in
   [[ai/rag-and-retrieval/grounding-and-citations|grounding/citations]] and refusal
   behavior before launch.

## The v1 architecture (and what to defer)

| Component | v1 choice | Defer until measured need |
|---|---|---|
| Store | Postgres + pgvector (you already run Postgres) | dedicated vector DB at ~10M+ vectors |
| Chunking | structure-aware, ~500–800 tokens, store doc/section metadata | semantic chunking, contextual retrieval |
| Retrieval | dense top-k (k≈20) → take top 5–8 | [[ai/rag-and-retrieval/hybrid-search|hybrid]], [[ai/rag-and-retrieval/reranking|rerank]] |
| Generation | one model, "answer only from context, cite chunk ids" | structured citations API, streaming |
| Eval | log every query/chunks/answer; 20-question manual eval | RAGAS-style automated eval |

The deliberate omissions matter: hybrid search, reranking, and query rewriting each fix
a *specific, diagnosable* failure. Adding them before you've seen those failures means
you can't attribute quality (or regressions) to anything.

## Schema that makes v2 possible

The single highest-leverage v1 decision is storing enough metadata to debug and filter.
With Drizzle:

```typescript
import { pgTable, text, uuid, timestamp, integer, vector, index } from "drizzle-orm/pg-core";

export const documents = pgTable("documents", {
  id: uuid("id").primaryKey().defaultRandom(),
  source: text("source").notNull(),        // canonical URL / path
  tenantId: text("tenant_id").notNull(),   // ACL filter — day one, not later
  title: text("title").notNull(),
  updatedAt: timestamp("updated_at").notNull(),
});

export const chunks = pgTable(
  "chunks",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    documentId: uuid("document_id").references(() => documents.id).notNull(),
    ordinal: integer("ordinal").notNull(), // position in doc → enables neighbor expansion
    heading: text("heading"),              // section context → citation display
    text: text("text").notNull(),
    embedding: vector("embedding", { dimensions: 1024 }).notNull(),
  },
  (t) => [index("chunks_embedding_idx").using("hnsw", t.embedding.op("vector_cosine_ops"))],
);
```

`ordinal` (fetch neighboring chunks later), `heading` (cheap context), and `tenantId`
(filtering) cost nothing now and unlock the most common v2 upgrades without re-indexing.

## Log everything per query

Inspectability is a logging schema, not an aspiration. Per request, persist: the raw
query, the embedded query text (if transformed), retrieved chunk ids + scores, the
final prompt, the answer, token counts, and latency per stage — ideally as spans in
[[ai/mlops/llm-observability-and-tracing|Langfuse/OTel-style tracing]]. This single
artifact answers "retrieval or generation?" for every complaint in seconds, which is
the whole [[ai/rag-and-retrieval/rag-failure-modes|debugging method]].

## Failure signals to watch in week one

- Correct-looking answers with **missing or vague citations** → grounding prompt too
  weak, or chunks too large to cite precisely.
- Retrieval hits that are **semantically close but task-irrelevant** (similar topic,
  wrong document) → chunking or metadata filtering problem, not an embedding problem.
- Users asking **follow-ups that retrieve nonsense** → you need query rewriting for
  conversational context ([[ai/rag-and-retrieval/query-transformations|transforms]]),
  the most common v1→v2 upgrade.
- **"I don't know" on answerable questions** → check recall@20 before touching the
  prompt; the chunk probably wasn't retrieved.

## Decision rule for v2

Run the 20–50 question set weekly. Compute two numbers:
**retrieval recall@k** (was the needed chunk in the top k?) and **answer pass rate**
(human or [[ai/evaluation/llm-as-judge|LLM judge]]). Then:

- Recall low → fix [[ai/rag-and-retrieval/chunking|chunking]], add
  [[ai/rag-and-retrieval/hybrid-search|hybrid]].
- Recall fine, ranking poor (needed chunk at position 15) → add
  [[ai/rag-and-retrieval/reranking|reranking]].
- Recall and ranking fine, answers bad → fix
  [[ai/rag-and-retrieval/grounding-and-citations|grounding]] / prompt.

**Connects to:** [[ai/rag-and-retrieval/why-rag|why RAG]] ·
[[ai/rag-and-retrieval/evaluating-rag|evaluating RAG]] ·
[[ai/rag-and-retrieval/rag-failure-modes|failure modes]] ·
[[ai/ai-playbooks/evaluate-rag-answer-quality|eval playbook]]

## Sources

- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — includes the pragmatic baseline guidance (when prompt+caching beats building RAG at all).
- [Barnett et al. 2024 — Seven Failure Points When Engineering a RAG System (arXiv:2401.05856)](https://arxiv.org/abs/2401.05856) — case-study catalog of where first-pass RAG systems actually break.
- [Jason Liu — RAG is more than embedding search (2023)](https://jxnl.co/writing/2023/09/17/rag-is-more-than-embeddings/) — argues for the query-set-first, inspectability-first design stance this note takes.
- [pgvector README](https://github.com/pgvector/pgvector) — the reference for the v1 store; indexing and filtering semantics you'll rely on.
- [Hamel Husain — Your AI Product Needs Evals (2024)](https://hamel.dev/blog/posts/evals/) — why the 20-question logged eval set is non-negotiable from day one.
