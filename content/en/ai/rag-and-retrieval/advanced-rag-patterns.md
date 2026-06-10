---
title: "Advanced patterns: contextual, graph & agentic RAG"
description: When basic retrieve-then-read isn't enough — contextual retrieval, graph RAG for connected facts, and agentic RAG that decides what to fetch.
tags: [rag, contextual-retrieval, graph-rag, agentic-rag]
order: 11
updated: 2026-06-10
---
# Advanced patterns: contextual, graph & agentic RAG

**Mental model:** basic retrieve-then-read fails in three distinct ways — chunks lose
their document context, single-hop similarity can't connect facts across documents,
and one fixed retrieval step can't serve queries that need iteration. Each advanced
pattern targets exactly one of these. Adopt them against a *measured* gap, in this
order of cost: contextual retrieval (cheap, always reasonable) → agentic retrieval
(moderate) → graph RAG (expensive, niche).

## Contextual retrieval (Anthropic, 2024)

Fixes: **chunks losing their context**. For each chunk, a small model writes 50–100
tokens situating it in its document; the context is prepended before embedding *and*
before BM25 indexing. Measured on Anthropic's benchmark: top-20 retrieval failures
drop **35%** (embeddings only), **49%** (+ contextual BM25), **67%** (+
[[ai/rag-and-retrieval/reranking|reranking]]). One-time cost ≈ **$1.02 per million
document tokens** using prompt caching — cache the full document, vary only the chunk.

```typescript
import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();

export async function contextualize(doc: string, chunk: string): Promise<string> {
  const msg = await anthropic.messages.create({
    model: "claude-haiku-4-5", // small model: this is a bulk indexing job
    max_tokens: 150,
    system: [{
      type: "text",
      text: `<document>\n${doc}\n</document>`,
      cache_control: { type: "ephemeral" }, // doc cached across all its chunks
    }],
    messages: [{
      role: "user",
      content:
        `Here is a chunk from the document above:\n<chunk>\n${chunk}\n</chunk>\n` +
        `Give a short succinct context to situate this chunk within the overall ` +
        `document for the purposes of improving search retrieval of the chunk. ` +
        `Answer only with the succinct context and nothing else.`,
    }],
  });
  const ctx = msg.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  return `${ctx}\n\n${chunk}`; // embed + BM25-index this; display the raw chunk
}
```

The prompt is Anthropic's verbatim. The cache-the-document trick is what makes the
economics work — without it, contextualizing costs ~10× more. This pattern is the
first thing to add after [[ai/rag-and-retrieval/hybrid-search|hybrid]] + rerank.

## Graph RAG (Microsoft, 2024)

Fixes: **multi-hop and corpus-global questions** — "how do the risks in these 40
reports relate?", "what themes recur across customer interviews?" — where the answer
is a *synthesis across documents* no single chunk contains. GraphRAG (Edge et al.
2024, [arXiv:2404.16130](https://arxiv.org/abs/2404.16130),
[microsoft/graphrag](https://github.com/microsoft/graphrag)) has an LLM extract an
entity-relation graph from the corpus, clusters it into communities, and pre-writes
community summaries; "global" queries are answered over summaries, "local" ones by
graph traversal.

The catch is cost: indexing makes LLM calls over the *entire corpus* (orders of
magnitude above embedding), and re-indexing on updates is painful.
**LazyGraphRAG** (Microsoft, Nov 2024) defers all extraction to query time — indexing
cost equal to vector RAG (~0.1% of full GraphRAG) with ~4% of the global-search query
cost; as of mid-2026 it ships in Microsoft platforms with open-source integration into
the `graphrag` library still pending. Decision rule: graph RAG only when evals show
genuine multi-hop/global failures *and* the corpus is stable enough to amortize
indexing; if tempted, start with LazyGraphRAG-style query-time synthesis or
[[ai/rag-and-retrieval/query-transformations|decomposition]], which fixes many
"multi-hop" cases for far less.

## Agentic RAG

Fixes: **the fixed retrieve-once pipeline**. Retrieval becomes a
[[ai/agents-and-tools/tool-calling|tool]] the model calls in a loop: it decides
*whether* to search, reformulates after weak results, queries multiple sources, and
stops when it has enough. The research lineage — Self-RAG's retrieve-on-demand +
self-critique (Asai et al. 2023, [arXiv:2310.11511](https://arxiv.org/abs/2310.11511)),
CRAG's corrective re-retrieval (Yan et al. 2024,
[arXiv:2401.15884](https://arxiv.org/abs/2401.15884)), FLARE's anticipatory retrieval
(Jiang et al. 2023, [arXiv:2305.06983](https://arxiv.org/abs/2305.06983)) — has
converged in practice on plain tool use with a capable model:

```typescript
const tools: Anthropic.Tool[] = [{
  name: "search_docs",
  description:
    "Search the internal documentation. Call with a specific, standalone query. " +
    "Call again with a reformulated query if results don't answer the question.",
  input_schema: {
    type: "object",
    properties: { query: { type: "string" } },
    required: ["query"],
  },
}];
// loop: messages.create(...tools) → execute search_docs via hybrid+rerank →
// return results as search_result content blocks (citations flow through) →
// repeat until the model answers. Cap iterations (e.g. 4) — see failure modes.
```

Costs: each loop iteration is a full LLM call — latency multiplies by 2–5×, and
budget caps are mandatory (an agent that "wants" one more search is a runaway-cost
bug, [[ai/agents-and-tools/agent-failure-modes|agent failure modes]]). Use when
queries genuinely require iteration/multiple sources; for single-hop QA it's pure
overhead.

## Choosing

| Measured gap | Pattern | Cost profile |
|---|---|---|
| Chunks lack context; recall misses on ambiguous chunks | contextual retrieval | one-time ~$1/M doc tokens |
| Genuine multi-hop / corpus-global synthesis | graph RAG (prefer lazy variants) | high indexing OR high query cost |
| Queries need iteration, source choice, reformulation | agentic RAG | 2–5× latency + tokens per query |

> Don't start here. Most RAG quality lives in
> [[ai/rag-and-retrieval/chunking|chunking]] +
> [[ai/rag-and-retrieval/hybrid-search|hybrid]] +
> [[ai/rag-and-retrieval/reranking|rerank]] +
> [[ai/rag-and-retrieval/grounding-and-citations|grounding]]. Every pattern on this
> page exists to close a gap your [[ai/rag-and-retrieval/evaluating-rag|evals]] must
> first demonstrate.

**Connects to:** [[ai/rag-and-retrieval/chunking|contextual chunks]] ·
[[ai/agents-and-tools/tool-calling|retrieval as a tool]] ·
[[ai/rag-and-retrieval/evaluating-rag|measure first]] ·
[[ai/inference-and-optimization/prefix-and-semantic-caching|prompt caching economics]]

## Sources

- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — full technique, numbers, prompt, and cost math; the cookbook notebook linked there is runnable.
- [Edge et al. 2024 — GraphRAG (arXiv:2404.16130)](https://arxiv.org/abs/2404.16130) — local vs global queries, community summaries; read §3 before deciding you need it.
- [Microsoft Research — LazyGraphRAG (Nov 2024)](https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/) — the cost-structure fix that makes graph-style RAG defensible.
- [Asai et al. 2023 — Self-RAG (arXiv:2310.11511)](https://arxiv.org/abs/2310.11511) — retrieve-on-demand + self-critique; the conceptual basis of agentic retrieval.
- [Yan et al. 2024 — Corrective RAG (arXiv:2401.15884)](https://arxiv.org/abs/2401.15884) — evaluate-then-re-retrieve; the recovery loop pattern.
- [Anthropic docs — Search results content blocks](https://platform.claude.com/docs/en/build-with-claude/search-results) — how tool-returned results carry API-level citations in agentic RAG.
