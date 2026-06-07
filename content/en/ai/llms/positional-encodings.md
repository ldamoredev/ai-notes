---
title: "Positional encodings & RoPE"
description: Attention is order-blind by default, so position must be injected. Absolute vs rotary (RoPE) encodings, and why RoPE underpins long-context models.
tags: [llms, positional-encoding, rope, context]
order: 4
updated: 2026-06-07
---
# Positional encodings & RoPE

[[ai/deep-learning/attention-mechanism|Self-attention]] treats its inputs as a
**set** — it has no inherent notion of order. But "dog bites man" ≠ "man bites dog",
so position must be added explicitly. How that's done quietly determines how far a
model can extend its context.

## The problem

Attention computes relevance by comparing every token to every other, ignoring where
they sit. Without positional information, the model couldn't tell first from last.
So we inject position into the token representations.

## From absolute to rotary

- **Absolute positional encodings** (original transformer) — add a
  position-dependent vector to each token embedding. Simple, but ties the model to
  positions it saw in training, so extending beyond the trained length works poorly.
- **RoPE (Rotary Position Embedding)** — the modern default. Instead of *adding*
  position, it **rotates** the query/key vectors by an angle proportional to
  position. The elegant consequence: attention ends up depending on the **relative**
  distance between tokens, not absolute index.

## Why RoPE matters for long context

Because RoPE encodes *relative* position, it degrades more gracefully past the
training length and can be **interpolated/extended** (NTK/YaRN scaling) to stretch a
model's [[ai/llms/context-window-and-kv-cache|context window]] without full
retraining. That's a big part of how models jumped from 2K to 128K+ token contexts.
It doesn't make long context *free*, though — see
[[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]].

## The one-line takeaway

> Attention is order-blind; positional encodings restore order. RoPE encodes
> *relative* position by rotation, which is why today's long-context models lean on
> it.

**Connects to:** [[ai/deep-learning/attention-mechanism|attention is order-blind]] ·
[[ai/llms/context-window-and-kv-cache|context window]] ·
[[ai/llms/long-context-and-lost-in-the-middle|long context]]
