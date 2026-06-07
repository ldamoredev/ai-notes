---
title: "Why LLMs hallucinate"
description: Hallucination isn't a bug bolted on — it's the direct consequence of training a model to produce plausible text. Why it happens and how to reduce it.
tags: [llms, hallucination, grounding, reliability]
order: 9
updated: 2026-06-07
---
# Why LLMs hallucinate

A **hallucination** is a confident, fluent statement that is false or unsupported.
It's not a glitch — it's what you'd expect from a system trained to produce
*plausible* text, not *true* text. Understanding the cause tells you how to mitigate
it (and that you can't fully eliminate it).

## The root cause

[[ai/llms/pretraining-next-token|Pretraining]] optimizes one thing: the most probable
next [[ai/llms/tokenization|token]]. "Plausible-sounding" and "true" usually coincide
in the training data — but not always. The model has **no internal database and no
truth check**; it generates the continuation that *looks* right. When it doesn't know,
the most probable continuation is still a fluent, authoritative-sounding guess.

Worsening factors:

- **Knowledge gaps / cutoff** — asked about something rare or post-cutoff, it
  interpolates ([[ai/foundations/distribution-shift|distribution shift]]).
- **Alignment pressure to be helpful** — post-training rewards confident, complete
  answers, nudging models to answer rather than abstain.
- **Sampling** — higher [[ai/llms/decoding-and-sampling|temperature]] increases
  improvisation.

## How to reduce it (not eliminate)

- **Grounding via [[ai/rag-and-retrieval/index|RAG]]** — supply the facts in context
  and instruct the model to answer *only* from them, with citations. The single
  biggest lever for factual tasks.
- **Let it say "I don't know"** — prompt and reward abstention; lower temperature for
  factual work.
- **Verify** — tool use, structured outputs, and a second-pass check for
  high-stakes claims.
- **[[ai/evaluation/index|Evaluate]] groundedness** — measure faithfulness to sources,
  not just fluency.

## The mental model

> An LLM is a fluent improviser, not a database. Treat every factual claim as
> *unverified* until grounded or checked. Design the system around that, rather than
> hoping for a model that "stops making things up."

**Connects to:** [[ai/llms/pretraining-next-token|next-token objective]] ·
[[ai/rag-and-retrieval/index|grounding with RAG]] ·
[[ai/evaluation/index|measuring groundedness]]
