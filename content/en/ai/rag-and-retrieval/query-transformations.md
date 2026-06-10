---
title: "Query transformations (rewriting, HyDE, multi-query)"
description: The user's raw question is often a poor search query. Rewriting, expansion, multi-query, and HyDE reshape it to retrieve better.
tags: [rag, query-rewriting, hyde, multi-query]
order: 7
updated: 2026-06-10
---
# Query transformations (rewriting, HyDE, multi-query)

**Mental model:** there is a register mismatch between how users *ask* (terse,
pronoun-laden, multi-part, typo'd) and how answers are *written* (complete, declarative
prose). Query transformation spends an LLM call before retrieval to close that gap —
often a bigger recall win than any index tuning, and the *only* fix for conversational
follow-ups.

## The techniques, with their papers

- **Rewriting / contextualization** — resolve references and produce a standalone
  search query. In chat, "what about the second one?" is unsearchable until history is
  folded in. Rewrite-Retrieve-Read (Ma et al. 2023,
  [arXiv:2305.14283](https://arxiv.org/abs/2305.14283)) formalized the gain from
  rewriting before retrieval.
- **Multi-query** — generate 3–5 paraphrases, retrieve for each, fuse with
  [[ai/rag-and-retrieval/hybrid-search|RRF]]. Reduces sensitivity to wording; cheap
  insurance for recall.
- **Decomposition** — split compound questions ("compare our 2024 and 2025 refund
  policies") into sub-queries, retrieve per sub-query, answer over the union
  ([[ai/prompt-engineering/task-decomposition|task decomposition]] applied to
  retrieval).
- **HyDE** (Gao et al. 2022, [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)) —
  have the LLM draft a *hypothetical answer*, embed **that** instead of the question.
  The fake answer lives in the same linguistic register as real documents, so dense
  similarity improves. Shines zero-shot with weak/no domain tuning; loses value once
  embeddings are strong and hybrid+rerank are in place — and it injects the model's
  parametric guesses into retrieval (a hallucinated draft can *steer* retrieval
  wrong).
- **Expansion** — add synonyms/related terms; mostly a BM25-side trick now, largely
  subsumed by multi-query.

## Conversational rewriting (the one you'll definitely need)

```typescript
import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();

export async function rewriteQuery(
  history: { role: "user" | "assistant"; content: string }[],
  question: string,
): Promise<string> {
  const msg = await anthropic.messages.create({
    model: "claude-haiku-4-5", // fast+cheap; rewriting doesn't need a frontier model
    max_tokens: 200,
    system:
      "Rewrite the user's last message as ONE standalone search query. " +
      "Resolve pronouns and references using the conversation. " +
      "Preserve exact identifiers (error codes, SKUs, names) verbatim. " +
      "If it is already standalone, return it unchanged. Return ONLY the query.",
    messages: [
      ...history.slice(-6), // recent turns suffice; full history adds cost, not signal
      { role: "user" as const, content: `Rewrite this as a standalone query: ${question}` },
    ],
  });
  const text = msg.content.filter((b) => b.type === "text").map((b) => b.text).join("").trim();
  return text || question; // empty/failed rewrite → fall back to the original
}
```

Two details that matter in production: **preserve identifiers verbatim** (a rewrite
that "fixes" `E1042` to "error 1042" breaks the
[[ai/rag-and-retrieval/hybrid-search|BM25 branch]]), and **always retrieve with the
original query too** — union both result sets so an over-eager rewrite can't lose what
the raw query would have found.

## Decision rules

| Symptom (from [[ai/rag-and-retrieval/evaluating-rag|evals]]) | Transform |
|---|---|
| Follow-up questions retrieve nonsense | rewriting — mandatory for chat UIs |
| Recall varies wildly with phrasing | multi-query (3–5 paraphrases + RRF) |
| Compound questions answered partially | decomposition |
| Zero-shot domain, weak embeddings, no reranker yet | HyDE |
| Exact-term queries miss | not a transform problem — [[ai/rag-and-retrieval/hybrid-search|hybrid]] |

Ordering heuristic: **hybrid + rerank before transforms.** They fix more failure
modes per millisecond, cost no tokens per query, and transforms stack cleanly on top
later. Exception: conversational rewriting, which nothing else replaces — build it
into any chat-style RAG from day one.

## Cost & latency lens

Every transform is an extra serial LLM call *before* retrieval starts: ~200–600 ms
with a small fast model (Haiku-class), plus tokens. Multi-query also multiplies
retrieval fan-out (cheap) and candidate volume for
[[ai/rag-and-retrieval/reranking|reranking]] (not cheap). Mitigations: small model,
`max_tokens` ≤ 200, tight output format, run multi-query paraphrase retrievals in
parallel, and cache rewrites for repeated questions
([[ai/inference-and-optimization/prefix-and-semantic-caching|semantic caching]]).
Trace the rewrite as its own span — when retrieval misbehaves you must see *what was
actually searched*, which is no longer what the user typed.

## Failure modes

- **Intent drift** — the rewrite answers a slightly different question; user notices,
  metrics don't. Mitigate: original-query union (above) + eval set with
  conversational cases.
- **HyDE hallucination steering** — the hypothetical answer asserts a wrong entity and
  retrieval dutifully follows it. Keep HyDE off factual-lookup paths where wrong-doc
  retrieval is costly.
- **Transform-by-default** — adding all techniques "for robustness" buys latency and
  cost with no measured gain. Add each transform against a named, measured recall
  failure; delete it if the eval delta disappears after other upgrades.
- **Rewriter sees stale history** — truncated/summarized history makes the rewriter
  resolve "it" to the wrong referent. Keep the last few raw turns, not a summary.

**Connects to:** [[ai/rag-and-retrieval/hybrid-search|recall]] ·
[[ai/prompt-engineering/task-decomposition|decomposition]] ·
[[ai/rag-and-retrieval/evaluating-rag|measuring retrieval]] ·
[[ai/prompt-engineering/memory-and-history|conversation history]]

## Sources

- [Gao et al. 2022 — HyDE: Precise Zero-Shot Dense Retrieval (arXiv:2212.10496)](https://arxiv.org/abs/2212.10496) — the hypothetical-document trick and, importantly, the zero-shot framing that bounds when it helps.
- [Ma et al. 2023 — Query Rewriting for Retrieval-Augmented LLMs (arXiv:2305.14283)](https://arxiv.org/abs/2305.14283) — rewrite-retrieve-read; the case for treating the query as the trainable/promptable component.
- [LangChain blog — Query Transformations (2023)](https://blog.langchain.dev/query-transformations/) — concise practitioner taxonomy (multi-query, decomposition, step-back) with implementation patterns.
- [LlamaIndex docs — Query Transformations](https://docs.llamaindex.ai/en/stable/optimizing/advanced_retrieval/query_transformations/) — reference implementations to borrow shapes from.
- [Anthropic docs — Prompt engineering overview](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) — for tightening the rewriter system prompt (instruction placement, output constraints).
