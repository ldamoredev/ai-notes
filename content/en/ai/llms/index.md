---
title: LLMs
description: How large language models actually work — the decoder transformer, tokenization, pretraining, decoding, context, and the behaviors (and failure modes) that follow.
tags: [llms, transformers]
order: 0
updated: 2026-06-07
---
# LLMs

A large language model is a [[ai/model-architectures/self-attention-from-first-principles|transformer]]
trained on one deceptively simple objective — **predict the next token** — at
enormous scale. Everything people find magical or maddening about LLMs (in-context
learning, hallucination, sensitivity to phrasing) falls out of that objective and
the architecture around it. This branch builds the mental model from the inside out.

> An LLM is a next-token predictor. It is astonishingly capable *and* it has no
> built-in notion of truth — both facts come from the same training objective.

## Mental model

A language model factorizes sequence probability into repeated next-token predictions. A decoder transformer converts the current prefix into logits; decoding commits one token; the new prefix becomes the next input. Training, post-training, context construction, and serving each change a different part of that system.

## Roadmap: architecture to behavior

- [[ai/llms/from-prompt-to-generated-token|From prompt to generated token]]
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

**Connects to:** [[ai/model-architectures/index|Model Architectures]] · [[ai/fine-tuning-and-alignment/index|Training and Adaptation]] · [[ai/inference-and-optimization/index|Inference Systems]]

## Core sources

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — the original transformer architecture.
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — autoregressive scaling and in-context learning evidence.
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) — current reference for tokenization, language modeling, and transformers.
- [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/) — executable tokenizer, transformer, fine-tuning, and inference material.
