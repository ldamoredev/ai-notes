---
title: "Emergent abilities & in-context learning"
description: The surprising payoff of scale — models learn from examples in the prompt with no weight updates. What's real about emergence and what's metric artifact.
tags: [llms, in-context-learning, emergence, scale]
order: 8
updated: 2026-06-07
---
# Emergent abilities & in-context learning

The reason LLMs feel different from earlier ML is a cluster of behaviors that appear
with [[ai/deep-learning/scaling-laws|scale]] — most importantly, learning a new task
from examples in the prompt without any training.

## In-context learning (ICL)

Show a model a few input→output examples in the prompt and it performs the task on a
new input — **no weight updates, no fine-tuning**. This is *few-shot* prompting. The
model isn't "learning" in the gradient sense; pretraining made it good at inferring
the pattern of a document and continuing it. ICL is the foundation of
[[ai/prompt-engineering/index|prompting]] and the reason a single frozen model can do
thousands of tasks.

> Few-shot examples don't update the model — they steer a fixed model by setting up a
> pattern it completes. "Learning" happens at inference, in the context window.

## Emergent abilities — with a caveat

Some capabilities (multi-step arithmetic, certain reasoning) seem to appear suddenly
past a scale threshold rather than improving smoothly — *emergent abilities*. The
honest version:

- The effect is partly **real**: bigger models genuinely unlock qualitatively new
  behavior.
- It's partly a **metric artifact**: harsh all-or-nothing metrics (exact match) make
  smooth underlying progress *look* like a sudden jump. Under softer metrics, the
  curve is more continuous.

Treat dramatic "it suddenly could do X" claims with calibrated skepticism — but don't
dismiss that scale buys new behavior.

## Why it matters

- **You can often skip fine-tuning** — ICL + good prompting solves many tasks on a
  frozen model ([[ai/fine-tuning-and-alignment/index|the adaptation ladder]]).
- **Capability is hard to predict** at the task level even when
  [[ai/deep-learning/scaling-laws|loss]] is predictable — so **evaluate**, don't
  assume ([[ai/evaluation/index|eval]]).

**Connects to:** [[ai/deep-learning/scaling-laws|scaling laws]] ·
[[ai/prompt-engineering/index|few-shot prompting]] ·
[[ai/llms/reasoning-and-test-time-compute|reasoning]]
