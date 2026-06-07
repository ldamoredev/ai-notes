---
title: "Decoding & sampling"
description: A model outputs a probability distribution; decoding turns it into text. Temperature, top-p/top-k, greedy vs sampling — the knobs that control creativity vs reliability.
tags: [llms, decoding, sampling, temperature]
order: 6
updated: 2026-06-07
---
# Decoding & sampling

At each step the [[ai/llms/the-decoder-transformer|model]] outputs a probability over
the whole vocabulary. **Decoding** is the strategy for picking the next token from
that distribution — and it controls how creative, repetitive, or reliable the output
feels, *without changing the model at all*.

## Greedy vs sampling

- **Greedy** — always take the highest-probability token. Deterministic, but bland and
  prone to loops.
- **Sampling** — draw from the distribution, so output varies. Needs shaping, or it
  occasionally picks something incoherent.

## The knobs

| Knob | Effect | Lower → / Higher → |
|---|---|---|
| **Temperature** | scales the distribution's sharpness | low = focused/deterministic; high = creative/random |
| **Top-k** | sample only from the k most likely tokens | smaller = safer; larger = more diverse |
| **Top-p (nucleus)** | sample from the smallest set covering probability p | adapts the candidate pool to confidence |
| **Repetition / frequency penalty** | discourage repeating tokens | reduces loops and verbatim repeats |

**Temperature** is the headline dial: ~0 for extraction, classification, code, and
anything needing reproducibility; higher (~0.7–1.0) for brainstorming and prose.

## Practical guidance

- Need **structure or facts** (JSON, classification, tool calls)? Use temperature ≈ 0.
- Need **variety** (ideation, creative writing)? Raise temperature and/or top-p.
- "The model is inconsistent run-to-run" is usually temperature > 0, not a bug.
- Decoding does not add knowledge or fix [[ai/llms/why-llms-hallucinate|hallucination]];
  temperature 0 makes a wrong answer *consistent*, not *correct*.

> Same weights, different decoding = different product behavior. Set it deliberately
> per task; don't leave defaults to chance.

**Connects to:** [[ai/llms/the-decoder-transformer|logits → tokens]] ·
[[ai/prompt-engineering/index|structured output]] ·
[[ai/llms/why-llms-hallucinate|hallucination]]
