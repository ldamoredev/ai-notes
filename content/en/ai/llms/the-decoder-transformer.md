---
title: "The decoder transformer"
description: How the GPT-style architecture assembles attention, feed-forward layers, residuals, and norms into a causal next-token predictor.
tags: [llms, transformers, architecture, gpt]
order: 1
updated: 2026-06-07
---
# The decoder transformer

Every GPT-style LLM is the same shape: turn tokens into vectors, push them through a
stack of identical blocks, and read off a probability distribution over the next
token. Understanding that pipeline demystifies the whole family.

## The pipeline, end to end

1. **Tokenize** the text into integer IDs ([[ai/llms/tokenization|tokenization]]).
2. **Embed** each token into a vector and add a
   [[ai/llms/positional-encodings|positional encoding]] so order is represented.
3. **N transformer blocks**, each doing two things:
   - **Masked self-attention** — every token mixes in information from earlier
     tokens (see [[ai/deep-learning/attention-mechanism|attention]]).
   - **Feed-forward network (FFN/MLP)** — a per-token nonlinear transform where much
     of the model's "knowledge" is stored.
   Both are wrapped in **residual connections** + **[[ai/deep-learning/initialization-and-normalization|LayerNorm]]**,
   which is what makes stacking dozens of blocks trainable.
4. **Unembed** the final vector into logits over the vocabulary; softmax →
   next-token probabilities ([[ai/llms/decoding-and-sampling|decoding]] picks one).

## "Decoder-only" and causal masking

The key property: a token may attend only to tokens **before** it (a causal mask).
This makes the model **autoregressive** — it predicts each next token from the
left context only, which is exactly what next-token
[[ai/llms/pretraining-next-token|pretraining]] and generation require. (The original
transformer had an encoder too; modern generative LLMs drop it and keep the decoder.)

## Where the parameters live

- **Attention** routes information between positions (relationships, syntax,
  coreference).
- **FFN layers** hold roughly two-thirds of the parameters and act like the model's
  associative memory of facts and patterns.
- Depth (more blocks) and width (bigger vectors) are the main
  [[ai/deep-learning/scaling-laws|scaling]] knobs.

## Pitfall

The architecture is small and repetitive — a few hundred lines of code. The
capability comes from **scale and data**, not architectural cleverness. Don't look
for the magic in the diagram; it's in the trillions of training tokens.

**Connects to:** [[ai/deep-learning/attention-mechanism|attention]] ·
[[ai/llms/pretraining-next-token|pretraining]] ·
[[ai/llms/tokenization|tokenization]]
