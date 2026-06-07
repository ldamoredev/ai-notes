---
title: "Zero-shot & few-shot"
description: When a plain instruction is enough and when examples earn their token cost. How to pick and order few-shot examples without overfitting the prompt.
tags: [prompt-engineering, few-shot, in-context-learning]
order: 3
updated: 2026-06-07
---
# Zero-shot & few-shot

The cheapest way to specify a task is to describe it (**zero-shot**); the next is to
*show* it with examples (**few-shot**), exploiting the model's
[[ai/llms/emergent-abilities-and-scale|in-context learning]]. Knowing which to reach
for saves tokens and improves reliability.

## Zero-shot: just ask

A clear instruction with no examples. Modern [[ai/llms/base-vs-instruct|instruct
models]] are strong zero-shot for common tasks. Start here — it's the cheapest and
often enough.

## Few-shot: show the pattern

Include a handful of `input → output` demonstrations. Use it when:

- The task is **easier to show than to describe** (a specific format, a nuanced
  labeling rule, a tone).
- You need **output consistency** — examples pin down the exact shape.
- Zero-shot is close but unreliable on edge cases.

## Doing few-shot well

- **Match the distribution** — examples should resemble real inputs, including tricky
  cases; the model imitates what it sees.
- **Be consistent** — identical format across examples; the format *is* the
  instruction.
- **Cover the classes** — for classification, include each label (and watch ordering;
  models can pick up position bias).
- **2–5 is usually enough** — more costs [[ai/llms/tokenization|tokens]] and context
  for diminishing returns; for many tasks one good example beats three mediocre ones.

## Pitfall

Few-shot examples can **over-anchor** the model to their surface form (it copies a
quirk you didn't intend). And they consume [[ai/prompt-engineering/managing-the-context-window|context
budget]] on every call — for high-volume tasks, consider whether
[[ai/fine-tuning-and-alignment/index|fine-tuning]] beats permanent few-shot.

**Connects to:** [[ai/llms/emergent-abilities-and-scale|in-context learning]] ·
[[ai/prompt-engineering/chain-of-thought|chain-of-thought]] ·
[[ai/fine-tuning-and-alignment/index|few-shot vs fine-tune]]
