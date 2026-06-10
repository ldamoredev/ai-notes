---
title: "RAG vs long context"
description: If a model has a million-token window, why retrieve at all? The cost, latency, attention, and freshness reasons RAG still wins for most knowledge apps.
tags: [rag, long-context, architecture, cost]
order: 12
updated: 2026-06-10
---
# RAG vs long context

**Mental model:** a context window is working memory, not a knowledge base. 1M-token
windows (Claude Opus 4.8 / Sonnet 4.6, Gemini — standard by 2026) changed *where the
line sits*, not whether there is one: you still pay per token per call, attention
still degrades with length, and corpora still outgrow any window. The decision is
economic and empirical, not ideological.

## When window-stuffing wins

If the corpus is **small, stable, and shared across queries**, skipping RAG is
genuinely better — no chunking bugs, no recall misses, the model sees everything.
Anthropic's own guidance in
[Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval): for
knowledge bases under ~200K tokens, just include the whole thing and skip RAG.

**Prompt caching changes the math decisively.** With Anthropic's caching, cache reads
cost ~10% of base input price: a 200K-token corpus in a cached system prompt costs
full price once, then ~0.1× per query within the TTL. For a single contract, one
codebase's docs, or a product manual, *cached long context beats RAG on both quality
and engineering cost*. The 2023-era "RAG because tokens are expensive" reflex
under-weights this.

```typescript
// corpus-in-prompt with caching: right answer for small stable corpora
const msg = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: [
    { type: "text", text: "Answer from the documentation below. Cite sections." },
    { type: "text", text: FULL_DOCS, cache_control: { type: "ephemeral" } },
  ],
  messages: [{ role: "user", content: question }],
});
```

## Why RAG still wins at scale

- **Cost & latency.** Cache reads are ~0.1×, not 0×: 500K cached tokens per query is
  still ~50K tokens-equivalent of input spend *every call*, plus time-to-first-token
  grows with prompt length. RAG sends 2–8K curated tokens. At volume the gap is the
  [[ai/inference-and-optimization/cost-modeling-for-llm-serving|whole margin]].
- **Attention degrades with length.** "Lost in the middle" (Liu et al. 2023,
  [arXiv:2307.03172](https://arxiv.org/abs/2307.03172)) showed U-shaped attention —
  models use the start and end of context well, the middle poorly. Chroma's
  **Context Rot** study (2025, 18 frontier models) extended this: performance
  degrades as input grows *at every length tested*, far below window limits, and
  semantically-similar distractors actively mislead. A model that *accepts* 1M tokens
  does not *use* 1M tokens uniformly. Curated context beats dumped context.
- **Freshness & cost-of-update.** RAG re-indexes one doc; window-stuffing re-sends
  (and re-caches) the corpus. Caching also pins you to byte-identical prefixes — any
  doc edit invalidates the cache.
- **Scale.** Corpora are GBs; windows are MBs. No contest above the threshold.
- **Access control.** Per-user filtering must happen *before* the model sees text.
  A shared stuffed prompt is one prompt-injection away from leaking everything to
  everyone ([[ai/ai-safety-and-security/data-and-pii-leakage|PII leakage]]); RAG
  filters at the retrieval query.
- **Debuggability.** "Which 6 chunks did it see?" beats "which of 500K tokens did it
  attend to?" for every production incident.

## Decision rule

| Corpus | Per-user filtering? | Update rate | Choice |
|---|---|---|---|
| <200K tokens | no | rarely | **stuff + cache** |
| <200K tokens | yes | any | RAG (filtering forces it) |
| 200K–1M tokens | no | rarely | hybrid: cache the hot core, retrieve the rest |
| >1M tokens or fast-changing | any | any | **RAG** |

And a practical tie-breaker: if you're unsure, prototype with window-stuffing (one
afternoon), and switch to RAG when cost, latency, or quality measurably hurts. The
stuffed prototype doubles as your quality baseline — **if RAG can't beat full-context
quality on your [[ai/rag-and-retrieval/evaluating-rag|eval set]], your retrieval is
broken**, which is itself worth knowing.

## The synthesis (not a competition)

Long context made RAG *better*, not obsolete: you can afford a reranked top-10 instead
of a starved top-3, include whole sections instead of fragments
([[ai/rag-and-retrieval/chunking|small-to-big retrieval]]), and keep multi-turn
[[ai/prompt-engineering/managing-the-context-window|conversation history]] alongside
retrieved context. Meanwhile caching made the *non-RAG* baseline competitive for small
corpora. The honest 2026 default: **cached long context below ~200K tokens, RAG
above, and retrieval feeding a generous window in between.** The same logic as
[[ai/rag-and-retrieval/why-rag|RAG vs fine-tune]]: pick the cheapest mechanism that
reliably gets the right facts in front of the model.

## Failure modes

- **Cargo-cult RAG** — building a vector pipeline for a 50-page manual. The complexity
  buys recall bugs, not quality.
- **Cargo-cult stuffing** — "the window fits it" ignores context rot: quality on
  needle-ish tasks degrades well before the limit, silently.
- **Cache-invalidation churn** — frequently-edited corpora make cached stuffing pay
  write-price constantly; check your cache hit rate before declaring victory.
- **Mid-window evidence** — whether stuffed or retrieved, evidence placed mid-prompt
  underperforms evidence at the edges; order retrieved chunks best-first or
  best-last.

**Connects to:** [[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]] ·
[[ai/rag-and-retrieval/why-rag|when to use RAG]] ·
[[ai/inference-and-optimization/prefix-and-semantic-caching|prompt caching]] ·
[[ai/ai-product-engineering/latency-cost-quality-triangle|latency/cost/quality]]

## Sources

- [Liu et al. 2023 — Lost in the Middle (arXiv:2307.03172)](https://arxiv.org/abs/2307.03172) — the U-shaped attention result; the original evidence that capacity ≠ effective use.
- [Chroma — Context Rot (2025)](https://research.trychroma.com/context-rot) — 18 models, degradation at every input length, distractor effects; the strongest current case against naive stuffing.
- [Anthropic — Contextual Retrieval (2024)](https://www.anthropic.com/news/contextual-retrieval) — source of the ~200K-token "just use the prompt" threshold.
- [Anthropic docs — Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — the pricing mechanics (write 1.25×, read 0.1×, TTLs) that decide the small-corpus case.
- [Anthropic docs — Context windows](https://platform.claude.com/docs/en/build-with-claude/context-windows) — current window sizes and long-context behavior for Claude models.
