---
title: "Synthetic data"
description: Synthetic data is sampling from a model's approximation of a distribution; recursive training on generated data compounds that approximation error into model collapse.
tags: [data-for-ai, synthetic-data, model-collapse]
order: 6
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/data-for-ai/dataset-design-and-sampling]
last_verified: 2026-07-20
---
# Synthetic data

**Mental model:** a generator is an approximation of a true distribution, and synthetic
data is a sample drawn from that approximation, not from the world. Training on your
own generator's output means training on the generator's error — repeat it across
generations and the error compounds, a statistical version of photocopying a
photocopy. That failure mode is called **model collapse**.

## Mechanism: why finite sampling erases the tail

Every generation of a dataset is a finite sample from some distribution. Rare events —
tail cases — have a real chance of simply not appearing in any given sample. If a value
occurs with true probability \(p\) and you draw \(n\) independent samples, the
probability that value is **absent entirely** is:

\[
P(\text{absent}) = (1-p)^n.
\]

If the next generation treats that sample's empirical distribution as ground truth
(the recursive-training setup), an absent rare value has probability exactly 0 in the
new distribution — and once a value's probability hits 0, it stays 0 forever after,
because you cannot resample what isn't there. This is an absorbing state: tail loss can
only accumulate across generations, never reverse itself.

## Worked example

Take a distribution where five common outcomes each carry probability 0.196 and one
rare outcome carries \(p = 0.02\) (sums to 1.0). Compute \((1-p)^n\) for a few sample
sizes:

| Sample size \(n\) | \(P(\text{rare value absent from the sample})\) |
|---:|---:|
| 20 | \(0.98^{20} \approx 0.668\) |
| 100 | \(0.98^{100} \approx 0.133\) |
| 1000 | \(0.98^{1000} \approx 2\times10^{-9}\) |

At \(n=20\) — a completely realistic size for a synthetic-data batch drawn per
prompt-template — there is better than a **two-thirds chance** the rare case is
entirely missing from a single generation's sample, before any model-approximation
error is even considered. Small synthetic batches lose tails fast; the fix is scale,
not just filtering.

## Executable artifact

Run with `python3`; expected output is the three probabilities from the table above,
`0.6676`, `0.1326`, `0.0` (rounded to 4 decimals — the true value at n=1000 underflows
to display as zero):

```python
def prob_absent(p, n):
    return (1 - p) ** n

p_rare = 0.02
for n in (20, 100, 1000):
    print(n, round(prob_absent(p_rare, n), 4))
```

## Good uses

- Creating rare but important edge cases *by construction* (explicitly targeting the
  tail) rather than hoping a general-purpose sample happens to include them.
- Bootstrapping instruction-following examples from a small human-written seed set —
  Self-Instruct and similar pipelines generate, filter, and deduplicate at scale.
- Paraphrasing for robustness testing, and simulation data where real collection is
  expensive, slow, or unsafe.

## What generation pipelines hide

A "1M synthetic examples" dataset card reports volume, not the effective diversity of
that volume. A generator sampled at low temperature from a narrow prompt template can
produce a million examples that collapse to a handful of underlying patterns — high
count, low true coverage — and nothing in the file size or example count reveals that
without measuring diversity directly (e.g. embedding-cluster count, n-gram overlap).

## Failure modes and a decision rule

- **Model collapse.** Repeated training on generated data narrows the distribution
  generation over generation, disproportionately losing tails and rare styles first.
- **Bias amplification.** The generator reproduces and can intensify source bias,
  since it is itself a model trained on biased data.
- **False diversity.** Many examples that read as different actually probe the same
  underlying behavior — measure diversity structurally, not by example count.
- **Leakage.** Generated examples can reveal private seed data if the generator
  memorized it; see [[ai/data-for-ai/privacy-and-pii-in-datasets|privacy and PII in
  datasets]] for why "it's just generated text" is not a safe assumption.
- **Evaluation contamination.** Synthetic eval sets built with the same generator (or
  family) as the system under test become too aligned to that generator's blind spots.

**Decision rule:** synthetic data is safe to scale when (a) it targets a specific,
named coverage gap rather than replacing real data wholesale, (b) it is mixed with real
data at a tracked ratio, and (c) evaluation always runs on a real, held-out set. If any
of those three is missing, treat the resulting model as untested against the real
distribution regardless of synthetic-set size.

## Production lens

Record generator model/version, prompt template, sampling settings (temperature,
top-p), and filters applied, in the dataset's documentation — these are the "collection
method" for synthetic data the same way a survey instrument is for human-collected
data. Track the synthetic-to-real ratio per training run over time; a ratio silently
creeping upward across model generations is the leading indicator of collapse risk
before it shows up in eval scores.

## Exercises

1. Recompute the table above for a rare outcome at \(p = 0.005\) and \(n = 50\); at
   what \(n\) does the absence probability drop below 5%?
2. Design a filter that would catch "false diversity": paraphrases that differ in
   wording but test the identical model behavior.
3. Sketch a dataset-documentation entry recording generator, prompt template, sampling
   settings, and synthetic:real ratio for a hypothetical instruction-tuning batch.

**Connects to:** [[ai/fine-tuning-and-alignment/distillation|distillation]] · [[ai/data-for-ai/datasheets-and-data-documentation|dataset documentation]] · [[ai/evaluation/designing-eval-sets|eval sets]] · [[ai/data-for-ai/privacy-and-pii-in-datasets|privacy and PII in datasets]]

## Sources

- [The Curse of Recursion](https://arxiv.org/abs/2305.17493) — formal analysis of how recursive training on generated data causes model collapse.
- [Self-Instruct: Aligning Language Models with Self-Generated Instructions](https://arxiv.org/abs/2212.10560) — a concrete pipeline for generating, filtering, and deduplicating synthetic instruction data.
- [Textbooks Are All You Need](https://arxiv.org/abs/2306.11644) — synthetic, quality-filtered training data used to reach strong results with a small model.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — how upstream data shortcuts, including synthetic shortcuts, compound downstream.
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/) — practical tooling for mixing, tracking ratios, and versioning synthetic and real data together.
