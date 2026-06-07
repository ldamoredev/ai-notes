---
title: "Long context & lost in the middle"
description: A 200K-token window doesn't mean the model uses all of it well. Why models attend best to the start and end, and what to do about it.
tags: [llms, long-context, retrieval, context-engineering]
order: 10
updated: 2026-06-07
---
# Long context & lost in the middle

Context windows exploded — hundreds of thousands of tokens, sometimes millions. But
**a big window is not the same as good use of it.** Models reliably under-attend to the
middle of long inputs, so "just stuff everything in" is a trap.

## Lost in the middle

Across many models, accuracy on a fact placed in a long context is **U-shaped**:
high when the relevant information is near the **beginning** or **end**, and notably
lower when it's buried in the **middle**. A model can have a 200K window and still
"miss" a sentence at position 100K. The window is the *capacity*, not a guarantee of
attention.

A related, newer concern is **context rot**: as inputs get very long, overall
reliability drifts down even when the answer is technically present.

## Why it happens

Training data has far fewer genuinely long, uniformly-important documents than short
ones, and [[ai/llms/positional-encodings|positional]] effects + attention dilution
mean salience concentrates at the edges. The model learned that beginnings and ends
carry the most signal.

## What to do about it

- **Retrieve, then place well** — use [[ai/rag-and-retrieval/index|RAG]] to fetch only
  what's relevant instead of dumping everything; put the most important context at the
  **start or end**, not the middle.
- **Compress** — summarize history and stale material; keep the window dense with
  signal ([[ai/prompt-engineering/index|context engineering]]).
- **[[ai/rag-and-retrieval/index#reranking|Rerank]]** so the top, best chunks land in
  the high-attention positions.
- **Don't pay for context you don't need** — more tokens = more
  [[ai/llms/context-window-and-kv-cache|cost and latency]] for often *worse* results.

> Treat the context window as expensive, attention-biased real estate, not a bucket.
> Curation beats capacity.

**Connects to:** [[ai/llms/context-window-and-kv-cache|context window]] ·
[[ai/rag-and-retrieval/index|retrieval & reranking]] ·
[[ai/prompt-engineering/index|context engineering]]
