---
title: "Probability & uncertainty for ML"
description: Models output probabilities, not facts. Likelihood, Bayes, and calibration — the difference between a confident model and a correct one.
tags: [foundations, probability, uncertainty, calibration]
order: 6
updated: 2026-06-07
---
# Probability & uncertainty for ML

Most models are **probabilistic**: a classifier outputs `P(class | input)`, an LLM
outputs a probability distribution over the next token. Treating those numbers as
certainties is a category error that causes real failures.

## The three ideas you reuse constantly

- **Likelihood** — how probable the observed data is under the model. Training a
  classifier with cross-entropy *is* maximizing the likelihood of the labels.
- **Bayes' rule** — update a belief with evidence:
  `P(H|E) ∝ P(E|H) · P(H)`. Posterior ∝ likelihood × prior. The prior is your
  starting belief; evidence reshapes it. This is the backbone of reasoning under
  uncertainty.
- **Base rates** — `P(H)` matters enormously. A 99%-accurate test for a 1-in-10,000
  disease produces mostly false positives. Models inherit this; ignoring base rates
  is the classic probability blunder.

## Two kinds of uncertainty

| Type | Source | Reducible? |
|---|---|---|
| **Aleatoric** | inherent noise in the data | no — it's irreducible |
| **Epistemic** | the model's ignorance (too little data, unfamiliar input) | yes — more/better data |

Out-of-distribution inputs spike epistemic uncertainty. A model that can't tell "I
don't know" from "I'm sure" is dangerous in production.

## Calibration: confidence that means something

A model is **calibrated** when its stated probabilities match reality — among
predictions it calls "80% likely," about 80% are correct. Accuracy and calibration
are different: a model can be accurate but overconfident.

- LLMs are often **miscalibrated** after instruction tuning — they sound confident
  whether right or wrong. This is why a fluent answer is not evidence of a correct
  one (see [[ai/llms/index|why LLMs hallucinate]]).
- Check calibration with reliability diagrams; improve with temperature scaling.

## Pitfall

A softmax score is **not** a probability of being correct — it's the model's
internal confidence, which can be wildly off-distribution. Don't gate decisions on
raw scores without checking calibration.

**Connects to:** [[ai/foundations/information-theory-basics|cross-entropy]] ·
[[ai/foundations/evaluation-metrics|metrics]] ·
[[ai/evaluation/index|evaluating models]]
