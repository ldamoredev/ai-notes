---
title: "Tokenization: why models see tokens, not words"
description: LLMs read subword tokens, not characters or words. How BPE works, why it explains odd failures (spelling, math, non-English cost), and token economics.
tags: [llms, tokenization, bpe, tokens]
order: 2
updated: 2026-06-07
---
# Tokenization: why models see tokens, not words

An LLM never sees text — it sees a sequence of integer **token IDs**. Tokenization is
the translation layer, and a surprising number of "weird" LLM behaviors trace
directly back to it.

## Why subwords (BPE)

Characters make sequences too long; whole words make the vocabulary huge and choke on
rare/new words. **Byte-Pair Encoding (BPE)** splits the difference: start from
characters and greedily merge the most frequent pairs until you have a vocabulary of
subword pieces. Common words become one token; rare words split into parts ("tokeniz",
"ation"). This handles any input, including words never seen in training.

## What tokenization explains

- **Spelling/character tasks fail** ("how many r's in strawberry?") — the model sees
  a token, not letters, so character-level reasoning is unnatural to it.
- **Arithmetic is shaky** — numbers tokenize inconsistently ("1234" may be one token,
  "1235" several), so digits don't line up cleanly.
- **Non-English costs more** — tokenizers are trained mostly on English, so other
  languages fragment into more tokens → more cost and less effective context.
- **Trailing spaces / odd formatting** can change tokenization and shift outputs.

## Token economics

You pay (in money, latency, and [[ai/llms/context-window-and-kv-cache|context budget]])
**per token**, not per word. Rough rule of thumb: ~1 token ≈ 4 characters ≈ ¾ of a
word in English. Estimating token counts is essential for cost and for fitting inside
the [[ai/llms/context-window-and-kv-cache|context window]].

## Pitfall

Token boundaries are invisible but consequential. When a prompt behaves strangely
around numbers, code, or non-English text, suspect tokenization before the model's
"intelligence."

**Connects to:** [[ai/llms/the-decoder-transformer|the architecture]] ·
[[ai/llms/context-window-and-kv-cache|context budget]] ·
[[ai/ai-product-engineering/index|cost per token]]
