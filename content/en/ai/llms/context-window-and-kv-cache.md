---
title: "Context window & the KV cache"
description: The context window is the model's working memory; the KV cache is what makes generation fast. Both explain why long prompts cost more and why latency behaves as it does.
tags: [llms, context-window, kv-cache, inference]
order: 5
updated: 2026-06-07
---
# Context window & the KV cache

The **context window** is everything the model can "see" at once — system prompt,
history, retrieved docs, the user's message, and the tokens it has generated so far.
It is the model's entire working memory; nothing outside it exists to the model.

## The window is a hard budget

Measured in [[ai/llms/tokenization|tokens]], the window is finite (a few K to ~1M
depending on model). Everything competes for it: instructions, few-shot examples,
[[ai/rag-and-retrieval/index|retrieved context]], and the running conversation. When
it fills, something must be dropped or summarized — which is the whole job of
[[ai/prompt-engineering/index|context engineering]]. The model has **no memory across
calls**; persistence is something *you* engineer by putting the right things back in
the window.

## The KV cache: why generation is fast

Generation is autoregressive — one token at a time, each conditioned on all previous
ones. Naively, every new token would re-process the entire sequence. The **KV cache**
stores the attention Keys and Values already computed for prior tokens, so each new
step only computes attention for the *new* token against the cached past. Without it,
long generations would be unbearably slow.

The cost: the cache **grows with sequence length** and consumes GPU memory — often the
real limit on how long a context you can serve and how many requests fit on a GPU.
This is why long contexts are expensive in both latency and money.

## Practical implications

- **Prompt caching** — providers can cache the KV for a stable prefix (a long system
  prompt or document), so repeated calls skip recomputing it: cheaper and faster. Put
  the stable stuff first.
- **More context ≠ better** — beyond cost, quality degrades
  ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]). Curate, don't
  dump.
- The quadratic cost of [[ai/deep-learning/attention-mechanism|attention]] is the
  reason all of this matters.

**Connects to:** [[ai/llms/tokenization|token budget]] ·
[[ai/llms/long-context-and-lost-in-the-middle|long context limits]] ·
[[ai/prompt-engineering/index|context engineering]]
