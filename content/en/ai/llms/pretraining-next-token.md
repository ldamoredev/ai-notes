---
title: "Pretraining: next-token prediction"
description: One objective — predict the next token — over trillions of tokens produces a model that has implicitly learned grammar, facts, and reasoning. How and why it works.
tags: [llms, pretraining, self-supervised, base-model]
order: 3
updated: 2026-06-07
---
# Pretraining: next-token prediction

The entire base capability of an LLM comes from one self-supervised task repeated at
unimaginable scale: **given the text so far, predict the next token.** No human labels
— the "answer" is just the token that actually came next ([[ai/foundations/types-of-learning|self-supervision]]).

## Why such a dumb objective works

To predict the next token *well* across the whole internet, a model is forced to
learn an enormous amount as a side effect:

- Grammar and syntax (to predict function words).
- Facts and associations (to finish "The capital of France is …").
- Style, format, code structure, and rudimentary reasoning (to continue an argument
  or a proof).

The objective is simple; the *only* way to get good at it is to build a rich internal
model of language and the world. Training minimizes
[[ai/mathematics-for-ai/information-theory-entropy-and-divergence|cross-entropy]] (equivalently, perplexity)
over the corpus.

## The result is a "base model"

Pretraining yields a **base model**: a powerful text *completer*, not an assistant. Ask
it a question and it might continue with *more questions* — because that's what
documents do. It has knowledge but no instinct to be helpful, honest, or safe. Turning
it into a usable assistant is the job of [[ai/llms/base-vs-instruct|post-training]].

## Consequences worth remembering

- **Knowledge cutoff** — the model only knows what was in its training data up to a
  date; the world keeps moving ([[ai/foundations/distribution-shift|distribution
  shift]]) → an argument for [[ai/rag-and-retrieval/index|retrieval]].
- **It models *plausibility*, not truth** — the seed of
  [[ai/llms/why-llms-hallucinate|hallucination]].
- **Data quality is everything** — garbage and duplication in, garbage out;
  curation and dedup are now central ([[ai/deep-learning/scaling-laws|Chinchilla]]).

**Connects to:** [[ai/foundations/types-of-learning|self-supervised learning]] ·
[[ai/llms/base-vs-instruct|post-training]] ·
[[ai/llms/why-llms-hallucinate|hallucination]]
