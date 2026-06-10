---
title: "Why RAG (and when not to)"
description: RAG injects fresh, private, citable facts into a frozen model. Why it beats fine-tuning for knowledge — and the cases where it's the wrong tool.
tags: [rag, retrieval, grounding]
order: 1
updated: 2026-06-10
---
# Why RAG (and when not to)

**Mental model:** an LLM's weights are a lossy, frozen snapshot of its training data.
RAG (Retrieval-Augmented Generation) sidesteps both problems at answer time — search an
external corpus for relevant passages, place them in the
[[ai/llms/context-window-and-kv-cache|context window]], and instruct the model to answer
from them. The knowledge lives in an index you control, not in weights you don't.

The term comes from **Lewis et al. 2020** ("Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks", [arXiv:2005.11401](https://arxiv.org/abs/2005.11401)),
which jointly trained a dense retriever (DPR, Karpukhin et al. 2020,
[arXiv:2004.04906](https://arxiv.org/abs/2004.04906)) with a seq2seq generator.
Production RAG in 2026 keeps the *architecture idea* (retriever feeds generator) but
drops the joint training: a frozen embedding model + a frozen LLM, glued by an index.

## What RAG buys you

- **Fresh knowledge** — update the index, not the model. New doc → re-embed → queryable
  in seconds. No retraining cycle, no model deployment.
- **Private/proprietary data** — your contracts, tickets, and runbooks were never in
  pretraining and never will be.
- **Grounding & [[ai/rag-and-retrieval/grounding-and-citations|citations]]** — answers
  trace to retrievable sources, which both curbs
  [[ai/llms/why-llms-hallucinate|hallucination]] and gives users a verification path.
- **Access control** — retrieval is a query you control, so per-user/per-tenant
  filtering happens *before* the model ever sees the text. You cannot do this with
  knowledge baked into weights.
- **Auditability** — "why did it say that?" becomes "look at the retrieved chunks", a
  loggable, traceable artifact (wire it into
  [[ai/mlops/llm-observability-and-tracing|tracing]]).

## RAG vs fine-tuning (the key distinction)

> **RAG is for knowledge (facts); [[ai/fine-tuning-and-alignment/when-to-fine-tune|fine-tuning]]
> is for behavior (form, style, format, tool protocols).** They are complementary, not
> competitors.

Fine-tuning to "teach facts" is the classic mistake: it is expensive, goes stale the day
your docs change, gives no citations, and the model still
[[ai/llms/why-llms-hallucinate|hallucinates]] plausible variants of what it half-learned.
Empirically, supervised fine-tuning moves *behavior* reliably and *knowledge* poorly —
new facts that conflict with pretraining tend to increase hallucination (Gekhman et al.
2024, [arXiv:2405.05904](https://arxiv.org/abs/2405.05904)). Default: RAG for facts;
fine-tune on top only if you also need a tone, schema, or skill the base model won't
produce via prompting.

## Decision rule

| Situation | Reach for |
|---|---|
| Answers depend on docs the model never saw | RAG |
| Facts change weekly/daily | RAG (re-index) |
| Corpus fits comfortably in one prompt and is static | long context / prompt stuffing |
| You need a style, format, or protocol change | fine-tuning or prompting |
| Per-user data isolation required | RAG with filtered retrieval |
| Task needs no external knowledge (classify, summarize given text) | plain prompting |

## The minimum viable pipeline (your stack)

The smallest honest RAG loop — Postgres + pgvector for storage, an embedding API,
Claude for generation. This is the skeleton every later note refines:

```typescript
import Anthropic from "@anthropic-ai/sdk";
import { db } from "./db"; // drizzle + pgvector, see vector-databases note
import { chunks } from "./schema";
import { cosineDistance, desc, sql } from "drizzle-orm";

const anthropic = new Anthropic();

async function embed(text: string): Promise<number[]> {
  const res = await fetch("https://api.voyageai.com/v1/embeddings", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.VOYAGE_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ model: "voyage-3-large", input: [text], input_type: "query" }),
  });
  const json = await res.json();
  return json.data[0].embedding;
}

export async function answer(question: string): Promise<string> {
  const qVec = await embed(question);
  const similarity = sql<number>`1 - (${cosineDistance(chunks.embedding, qVec)})`;
  const hits = await db
    .select({ id: chunks.id, text: chunks.text, source: chunks.source, similarity })
    .from(chunks)
    .orderBy((t) => desc(t.similarity))
    .limit(8);

  const context = hits
    .map((h, i) => `<chunk id="${i}" source="${h.source}">\n${h.text}\n</chunk>`)
    .join("\n");

  const msg = await anthropic.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    system:
      "Answer ONLY from the provided chunks. Cite chunk ids like [0]. " +
      "If the answer is not in the chunks, say you don't know.",
    messages: [{ role: "user", content: `${context}\n\nQuestion: ${question}` }],
  });
  return msg.content.filter((b) => b.type === "text").map((b) => b.text).join("");
}
```

What this skeleton deliberately lacks — and what each gap costs — is the syllabus of
this branch: [[ai/rag-and-retrieval/chunking|chunking]] discipline,
[[ai/rag-and-retrieval/hybrid-search|hybrid search]] for exact terms,
[[ai/rag-and-retrieval/reranking|reranking]] for precision,
[[ai/rag-and-retrieval/evaluating-rag|evals]] so you know which of those to add.

## When NOT to reach for RAG

- **The facts fit in the prompt.** A single contract, one API doc, a pasted log file —
  just include them ([[ai/rag-and-retrieval/rag-vs-long-context|RAG vs long context]]).
  With 1M-token windows (Claude Opus 4.8 / Sonnet 4.6, 2026) plus prompt caching, the
  "fits in the prompt" threshold is far higher than 2023 intuitions suggest.
- **You need behavior, not facts** → fine-tune or prompt-engineer.
- **The corpus is tiny and static** → a long cached prompt or a SQL lookup beats a
  vector pipeline on cost, latency, and moving parts.
- **Answers require computation, not lookup** ("sum Q3 revenue across these CSVs") →
  give an [[ai/agents-and-tools/tool-calling|agent a SQL/code tool]]; retrieval of
  prose won't compute anything.

## Failure modes & cost

- RAG converts a hallucination problem into a **search relevance problem** — which is
  better (it's measurable) but not free. Most "the LLM is wrong" reports in RAG apps
  are [[ai/rag-and-retrieval/rag-failure-modes|retrieval failures]].
- **Pipeline tax**: chunking decisions, index operations, embedding model migrations,
  eval sets. Budget engineering time for retrieval quality, not just the happy path.
- **Latency**: embed query (~50–100 ms hosted) + ANN search (ms) + optional rerank
  (~100–600 ms) + generation. Retrieval is rarely the bottleneck; reranking and extra
  LLM calls ([[ai/rag-and-retrieval/query-transformations|query transforms]]) are.
- **Cost asymmetry**: embedding + storage is cheap (one-time per doc); the recurring
  cost is *context tokens per query*. Retrieving 8 tight chunks instead of 50 sloppy
  ones is a direct, permanent cost cut — see
  [[ai/inference-and-optimization/cost-modeling-for-llm-serving|cost modeling]].

## In practice

Earn the complexity incrementally: start with prompt stuffing; add vector retrieval
when the corpus outgrows the window; add hybrid + rerank when
[[ai/rag-and-retrieval/evaluating-rag|measured recall/precision]] demands it; consider
[[ai/rag-and-retrieval/advanced-rag-patterns|advanced patterns]] last. Teams that start
from "we need a vector database" usually built the wrong thing — start from "which
questions must we answer, from which documents?"
([[ai/rag-and-retrieval/rag-first-pass-design|first-pass design]]).

**Connects to:** [[ai/fine-tuning-and-alignment/when-to-fine-tune|RAG vs fine-tune]] ·
[[ai/llms/why-llms-hallucinate|grounding vs hallucination]] ·
[[ai/rag-and-retrieval/rag-vs-long-context|RAG vs long context]] ·
[[ai/ai-playbooks/decide-prompt-vs-rag-vs-finetune|decision playbook]]

## Sources

- [Lewis et al. 2020 — Retrieval-Augmented Generation (arXiv:2005.11401)](https://arxiv.org/abs/2005.11401) — the original RAG paper; read §2 for the retriever-generator factorization that still defines the architecture.
- [Karpukhin et al. 2020 — Dense Passage Retrieval (arXiv:2004.04906)](https://arxiv.org/abs/2004.04906) — why learned dense retrieval beat BM25 on open-domain QA, the result that made RAG viable.
- [Gekhman et al. 2024 — Does Fine-Tuning LLMs on New Knowledge Encourage Hallucinations? (arXiv:2405.05904)](https://arxiv.org/abs/2405.05904) — empirical backing for "fine-tuning teaches facts poorly".
- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — also the best concise statement of when to skip RAG entirely (small corpora → prompt + caching).
- [Eugene Yan — Patterns for Building LLM-based Systems (2023)](https://eugeneyan.com/writing/llm-patterns/) — practitioner survey placing RAG among the other reliability patterns.
