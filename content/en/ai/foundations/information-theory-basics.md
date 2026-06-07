---
title: "Information theory: entropy, cross-entropy & KL"
description: Why classifiers and LLMs are trained with cross-entropy, what perplexity really measures, and how KL keeps fine-tuned models in check.
tags: [foundations, information-theory, cross-entropy, kl-divergence]
order: 11
updated: 2026-06-07
---
# Information theory: entropy, cross-entropy & KL

Information theory gives the vocabulary for "surprise" and "distance between
distributions." It's worth knowing because the loss that trains almost every
classifier and every LLM — **cross-entropy** — comes straight from it.

## Entropy = average surprise

**Entropy** measures how unpredictable a distribution is. A fair coin has high
entropy (you can't predict it); a loaded coin has low entropy. Rare events carry
more information ("surprise") than common ones. Entropy is the average surprise you
expect from a source.

## Cross-entropy = the training loss

**Cross-entropy** measures the cost of using your model's predicted distribution
when the *true* distribution is something else. Minimizing it pushes the model's
predicted probabilities toward the real labels:

- For an LLM, the target distribution puts all mass on the actual next token, so
  cross-entropy reduces to "maximize the probability the model assigned to the
  correct token." That single objective, over trillions of tokens, is how LLMs
  learn. (See [[ai/foundations/types-of-learning|self-supervised learning]].)
- It pairs naturally with softmax outputs and punishes **confident wrong** answers
  hard — which is exactly the pressure you want.

## Perplexity = cross-entropy you can read

**Perplexity** is just `exp(cross-entropy)`. Intuitively, "how many options is the
model effectively choosing between at each step." Lower is better; a perplexity of
1 means perfect prediction. It's the classic intrinsic metric for language models.

## KL divergence = distance between distributions

**KL divergence** measures how far one distribution is from another (it is not
symmetric). Two places it shows up constantly:

- **Preference alignment** — [[ai/fine-tuning-and-alignment/index|RLHF and DPO]] add
  a KL penalty to keep the tuned model from drifting too far from the base model,
  preserving fluency while changing behavior.
- **Distillation** — a student model is trained to match a teacher's full output
  distribution via a KL-style loss.

## The one-paragraph summary

> Entropy = unpredictability. Cross-entropy = the loss that trains classifiers and
> LLMs. Perplexity = cross-entropy made readable. KL = how far two distributions are,
> the leash that keeps fine-tunes anchored.

**Connects to:** [[ai/foundations/how-learning-works|loss & objective]] ·
[[ai/foundations/probability-and-uncertainty|probability]] ·
[[ai/llms/index|LLM training]]
