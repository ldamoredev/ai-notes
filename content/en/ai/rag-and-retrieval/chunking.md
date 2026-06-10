---
title: "Chunking that respects structure"
description: How you split documents decides what can be retrieved. Chunk size, overlap, structure-aware splitting, and why bad chunking caps RAG quality.
tags: [rag, chunking, preprocessing]
order: 2
updated: 2026-06-10
---
# Chunking that respects structure

**Mental model:** the chunk is the unit of retrieval, so chunking sets a hard ceiling
on RAG quality — a retriever can only return what chunking produced, and a great
[[ai/rag-and-retrieval/reranking|reranker]] cannot resurrect an answer that was split
across two chunks. It is the most under-invested, highest-leverage stage of the
pipeline.

## The size trade-off, concretely

- **Too small (≲150 tokens)** — facts get severed from their referents ("it improves
  throughput by 40%" — *what* does?); you need more chunks per answer, so recall must
  be higher everywhere.
- **Too large (≳1,500 tokens)** — one matching sentence is diluted by a wall of
  off-topic text, so [[ai/rag-and-retrieval/embeddings-for-retrieval|embedding]]
  similarity drops; retrieved chunks waste
  [[ai/llms/context-window-and-kv-cache|context budget]] and bury the answer
  ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]).

There is no universal optimum. Defensible 2026 starting points: **400–800 tokens** for
prose, with **10–20% overlap**; whole functions/classes for code; row-groups with
repeated headers for tables. Anthropic's
[Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) experiments
used "a few hundred tokens" per chunk. Treat size as a tunable hyperparameter and
[[ai/rag-and-retrieval/evaluating-rag|measure recall@k]] across 2–3 candidate sizes —
an afternoon of work that outperforms any blog's recommendation.

## The strategy ladder

| Strategy | What it does | When |
|---|---|---|
| Fixed-size + overlap | split every N tokens | never as final choice; only as baseline |
| Recursive | split on `\n\n` → `\n` → sentence → token, biggest unit that fits | good default for plain prose |
| **Structure-aware** | split on headings/sections/code blocks; never cut mid-table or mid-function | the production default |
| Semantic | embed sentences, cut where adjacent similarity drops | rarely worth it (below) |
| Late chunking | embed full doc with a long-context embedder, then pool per chunk | long-context embedding models only |

On semantic chunking: Qu et al. 2024
([arXiv:2410.13070](https://arxiv.org/abs/2410.13070)) found its gains over simple
splitting are inconsistent and often fail to justify the compute — fix structure-aware
splitting and chunk context first. **Late chunking** (Günther et al., Jina 2024,
[arXiv:2409.04701](https://arxiv.org/abs/2409.04701)) attacks the same problem
(chunks losing document context) at embedding time instead of text time.

## Structure-aware splitting in TypeScript

Markdown-aware splitter that keeps heading context attached to every chunk — the part
that matters more than the exact token count:

```typescript
type Chunk = { heading: string; text: string; ordinal: number };

export function chunkMarkdown(doc: string, maxTokens = 700): Chunk[] {
  // crude but adequate token estimate for splitting purposes (~4 chars/token)
  const tokens = (s: string) => Math.ceil(s.length / 4);
  const sections = doc.split(/^(?=#{1,3} )/m); // split BEFORE each heading, keep it
  const chunks: Chunk[] = [];
  let ordinal = 0;

  for (const section of sections) {
    const heading = section.match(/^#{1,3} (.*)$/m)?.[1] ?? "";
    if (tokens(section) <= maxTokens) {
      if (section.trim()) chunks.push({ heading, text: section.trim(), ordinal: ordinal++ });
      continue;
    }
    // section too big: split on blank lines between blocks
    const blocks = section.split(/\n\n+/);
    let buf = "";
    for (const block of blocks) {
      if (tokens(buf + block) > maxTokens && buf) {
        chunks.push({ heading, text: buf.trim(), ordinal: ordinal++ });
        buf = "";
      }
      buf += block + "\n\n";
    }
    if (buf.trim()) chunks.push({ heading, text: buf.trim(), ordinal: ordinal++ });
  }
  return chunks;
}
```

(Production caveat: a regex splitter like this will cut inside fenced code blocks —
use a Markdown AST parser such as `remark` to treat fences as atomic blocks.)

Store `heading` and `ordinal` with each chunk
([[ai/rag-and-retrieval/rag-first-pass-design|schema]]): the heading gives the chunk
cheap context and a citation label; the ordinal lets you fetch neighboring chunks at
answer time ("small-to-big" retrieval: match on small chunks, hand the LLM the
surrounding window).

## Add context to chunks

A standalone chunk often loses what it refers to. Two proven fixes:

- **Cheap and always-on**: prepend `Document: <title> > <section heading>` to the text
  you embed (not necessarily to the text you display).
- **Contextual retrieval** (Anthropic 2024): generate a 50–100-token,
  chunk-specific context with a small model and prepend it before embedding *and*
  before BM25 indexing. Cuts top-20 retrieval failures **35%** alone, **49%** combined
  with contextual BM25 (one-time cost ≈ **$1.02 per million document tokens** with
  prompt caching). Implementation in
  [[ai/rag-and-retrieval/advanced-rag-patterns|advanced patterns]].

## Failure modes

- **Mid-structure cuts** — half a table, half a code block, a step list split at step
  3. These chunks are unretrievable garbage. Structure-aware splitting exists to
  prevent exactly this.
- **Boundary-straddling facts** — overlap mitigates but doesn't cure; if evals show
  misses on multi-paragraph answers, retrieve neighbors via `ordinal` instead of
  growing chunk size.
- **One config for heterogeneous corpora** — FAQs, API references, and long-form
  policies need different chunkers. Route by document type.
- **Re-chunking churn** — changing chunking invalidates the whole index and your eval
  baselines. Version the chunker config alongside the index; re-run the eval set
  before/after.

## In practice

When retrieval quality disappoints, **read 20 retrieved chunks before touching
anything else**. Mid-sentence cuts, missing referents, and headerless table fragments
are visible to the naked eye — and no embedding model upgrade fixes them. Chunk
inspection is the highest-ROI debugging step in all of RAG
([[ai/rag-and-retrieval/rag-failure-modes|failure modes]]).

**Connects to:** [[ai/rag-and-retrieval/embeddings-for-retrieval|embeddings]] ·
[[ai/rag-and-retrieval/advanced-rag-patterns|contextual retrieval]] ·
[[ai/rag-and-retrieval/rag-failure-modes|failure modes]] ·
[[ai/rag-and-retrieval/rag-first-pass-design|first-pass schema]]

## Sources

- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — the measured case that chunk *context*, not chunk *size*, is the big lever; includes costs and the contextualizer prompt.
- [Qu et al. 2024 — Is Semantic Chunking Worth the Computational Cost? (arXiv:2410.13070)](https://arxiv.org/abs/2410.13070) — evidence that fancy chunking often doesn't pay; calibrates where to spend effort.
- [Günther et al. 2024 — Late Chunking (arXiv:2409.04701)](https://arxiv.org/abs/2409.04701) — the long-context-embedder alternative to prepending context.
- [Pinecone — Chunking Strategies for LLM Applications](https://www.pinecone.io/learn/chunking-strategies/) — practical taxonomy of splitters with trade-offs.
- [LlamaIndex docs — Node parsers & text splitters](https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/) — reference implementations (sentence window, hierarchical) worth borrowing even outside LlamaIndex.
