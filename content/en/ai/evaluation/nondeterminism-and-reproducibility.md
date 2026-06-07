---
title: "Nondeterminism & reproducibility"
description: The same prompt can give different answers run to run. Where LLM nondeterminism comes from, why temperature 0 isn't fully deterministic, and how to test around it.
tags: [evaluation, nondeterminism, reproducibility, testing]
order: 14
updated: 2026-06-07
---
# Nondeterminism & reproducibility

A property that trips up everyone coming from traditional software: **the same input can
produce different outputs.** This isn't a bug — it's inherent to how LLMs are
[[ai/llms/decoding-and-sampling|sampled]] and served. You can't eliminate it, so you
design and [[ai/evaluation/index|test]] around it.

## Where the variability comes from

- **Sampling** — [[ai/llms/decoding-and-sampling|temperature > 0]] deliberately draws
  randomly from the distribution. Different draw → different text.
- **Temperature 0 is *not* a guarantee.** Even greedy decoding can vary because of
  floating-point non-associativity, batching, and changing hardware/kernels on the
  provider side — tiny numeric differences flip a token, which cascades.
- **Provider-side changes** — silent model updates and infra changes shift behavior
  ([[ai/mlops/model-deprecation-and-migration|deprecation & migration]]).
- **Context differences** — small prompt or [[ai/prompt-engineering/assembling-context|context]]
  changes (even whitespace) move outputs.

## Reduce it where you need consistency

- **Lower temperature** (≈0) for extraction, classification, and
  [[ai/prompt-engineering/structured-outputs|structured]] tasks.
- **Constrain the output** — schemas/structured outputs shrink the space of valid
  answers.
- **Set a seed** if the API supports it (helps, doesn't fully guarantee).
- **Cache** results for identical inputs when you want a stable answer
  ([[ai/inference-and-optimization/prefix-and-semantic-caching|caching]]).

## Test for distributions, not single runs

Because outputs vary, **one passing run proves nothing**:

- Run each [[ai/evaluation/designing-eval-sets|eval]] case **multiple times** and report
  a **pass rate**, not a single pass/fail.
- Assert on **properties** (valid JSON, contains the fact, no banned content) rather
  than exact string matches.
- Track variance over time — a rising failure rate signals
  [[ai/foundations/distribution-shift|drift]] or a silent model change.

## Pitfall

Writing exact-match tests against LLM output, or trusting "it worked when I ran it." The
test passes once, then flakes in CI and production. Embrace the nondeterminism: pin what
you can, and evaluate behavior as a distribution.

**Connects to:** [[ai/llms/decoding-and-sampling|decoding & sampling]] ·
[[ai/evaluation/eval-driven-development|eval-driven development]] ·
[[ai/mlops/model-deprecation-and-migration|silent model changes]]
