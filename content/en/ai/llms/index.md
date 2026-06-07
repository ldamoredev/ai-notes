---
title: LLMs
description: How large language models actually work — the decoder transformer, tokenization, pretraining, decoding, context, and the behaviors (and failure modes) that follow.
tags: [llms, transformers]
order: 0
updated: 2026-06-07
---
# LLMs

A large language model is a [[ai/deep-learning/attention-mechanism|transformer]]
trained on one deceptively simple objective — **predict the next token** — at
enormous scale. Everything people find magical or maddening about LLMs (in-context
learning, hallucination, sensitivity to phrasing) falls out of that objective and
the architecture around it. This branch builds the mental model from the inside out.

> An LLM is a next-token predictor. It is astonishingly capable *and* it has no
> built-in notion of truth — both facts come from the same training objective.

## The architecture

- [[ai/llms/the-decoder-transformer|The decoder transformer]]
- [[ai/llms/transformer-attention-map|Transformer attention map]]
- [[ai/llms/tokenization|Tokenization: why models see tokens, not words]]
- [[ai/llms/positional-encodings|Positional encodings & RoPE]]

## Training & adaptation

- [[ai/llms/pretraining-next-token|Pretraining: next-token prediction]]
- [[ai/llms/base-vs-instruct|Base vs instruct vs chat models]]
- [[ai/llms/emergent-abilities-and-scale|Emergent abilities & in-context learning]]

## Generation & context

- [[ai/llms/decoding-and-sampling|Decoding & sampling]]
- [[ai/llms/context-window-and-kv-cache|Context window & the KV cache]]
- [[ai/llms/long-context-and-lost-in-the-middle|Long context & lost in the middle]]
- [[ai/llms/reasoning-and-test-time-compute|Reasoning & test-time compute]]

## Behavior & deployment

- [[ai/llms/why-llms-hallucinate|Why LLMs hallucinate]]
- [[ai/llms/quantization-and-inference|Quantization & inference]]

## Core sources

- Andrej Karpathy — *Let's build GPT*, *Intro to LLMs*, *Deep Dive into LLMs*.
- Sebastian Raschka — *Build a Large Language Model (From Scratch)*.
- Jay Alammar — *The Illustrated Transformer* / *Illustrated GPT-2*.
- Hugging Face — *LLM Course*; Jurafsky & Martin — *Speech and Language Processing* (SLP3).
- Lilian Weng — blog (attention, hallucination, agents).
