---
title: "Types of learning: supervised, unsupervised, self-supervised, RL"
description: The four broad ways models learn, what signal each uses, and why self-supervision is what made LLMs possible.
tags: [foundations, supervised, self-supervised, reinforcement-learning]
order: 4
updated: 2026-06-07
---
# Types of learning: supervised, unsupervised, self-supervised, RL

The categories differ in **what supervision signal** the model gets — where the
"correct answer" comes from during training.

## The four families

- **Supervised** — learn from `(input, label)` pairs. The label is the answer.
  Classification and regression. Powerful but bottlenecked by labeling cost.
- **Unsupervised** — no labels; find structure. Clustering, dimensionality
  reduction, density estimation. Answers "what's in this data?"
- **Self-supervised** — labels are *generated from the data itself*. Hide part of
  the input and predict it. No human annotation needed.
- **Reinforcement learning (RL)** — learn from a **reward** signal by acting in an
  environment. No labeled answer, just better/worse outcomes over time.

## Why self-supervision changed everything

LLMs are trained self-supervised: the "label" for each token is simply **the next
token** in the text. That turns the entire internet into training data without a
single human annotation, which is why pretraining scaled the way it did. The model
learns language, facts, and reasoning patterns as a side effect of getting good at
"predict the next token."

> Self-supervision = unsupervised data, supervised-style training. It is the bridge
> that made foundation models economically possible.

## Where each shows up in modern AI

| Stage | Learning type |
|---|---|
| LLM pretraining | self-supervised (next-token) |
| Instruction tuning / SFT | supervised (prompt → ideal response) |
| Preference alignment (RLHF/DPO) | reinforcement / preference learning |
| Embeddings, clustering | unsupervised / self-supervised |

A frontier model is a *stack* of these, not one. See
[[ai/fine-tuning-and-alignment/index|fine-tuning & alignment]] for how the later
stages work.

**Connects to:** [[ai/llms/index|LLMs]] ·
[[ai/foundations/how-learning-works|how learning works]] ·
[[ai/fine-tuning-and-alignment/index|fine-tuning & alignment]]
