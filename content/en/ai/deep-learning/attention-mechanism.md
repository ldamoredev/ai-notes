---
title: "The attention mechanism"
description: Attention is a learned, content-based lookup — each position pulls information from the positions most relevant to it. The core idea behind every transformer.
tags: [deep-learning, attention, transformers, qkv]
order: 8
updated: 2026-06-07
---
# The attention mechanism

Attention is the single most important idea in modern deep learning. The intuition:
instead of forcing information through a fixed-size [[ai/deep-learning/rnns-and-their-limits|recurrent
state]], let each position **look at and pull from every other position**, weighting
them by relevance. It's a soft, learnable lookup table.

## Query, Key, Value

Each token produces three vectors (via learned [[ai/foundations/linear-algebra-for-ml|matrix
projections]]):

- **Query** — what this token is looking for.
- **Key** — what each token offers / can be matched against.
- **Value** — the information a token contributes if attended to.

The mechanism: compare a token's query against **every** key (a
[[ai/foundations/linear-algebra-for-ml|dot product]] = relevance score), softmax the
scores into weights, then take the weighted sum of the values. Each token's output is
a blend of the values it found most relevant.

> Attention = "for each token, softly retrieve a weighted mix of information from the
> tokens that matter to it." A differentiable, content-addressed lookup.

## Why it's powerful

- **Direct long-range links** — token 500 can attend to token 1 in one hop; no
  vanishing chain.
- **Parallel** — all positions computed at once (great for GPUs).
- **Dynamic** — the "wiring" depends on the content, not a fixed structure.

## Multi-head attention

Run several attention operations in parallel ("heads"), each with its own
projections. Different heads specialize — one tracks syntax, another coreference,
another position — and their outputs are concatenated. More heads = more kinds of
relationships captured at once.

## The catch

Comparing every token to every token is **quadratic** in sequence length (n²), which
is why long context is expensive and why the [[ai/llms/index|KV cache]] and
efficient-attention research matter. This cost is the central scaling constraint of
transformers.

This mechanism, stacked with feed-forward layers and
[[ai/deep-learning/initialization-and-normalization|LayerNorm]], **is** the
transformer — see [[ai/llms/index|LLMs]].

**Connects to:** [[ai/deep-learning/rnns-and-their-limits|why it beat RNNs]] ·
[[ai/foundations/linear-algebra-for-ml|dot-product similarity]] ·
[[ai/llms/index|the transformer]]
