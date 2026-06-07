---
title: "Self-consistency & sampling"
description: Sample several answers and aggregate them. Why majority-vote over multiple reasoning paths beats a single greedy answer on hard problems — and what it costs.
tags: [prompt-engineering, self-consistency, sampling, reliability]
order: 8
updated: 2026-06-07
---
# Self-consistency & sampling

A single answer from a model is one draw from a distribution. For hard problems you
can trade compute for reliability by **sampling several answers and aggregating** them
— the simplest form of inference-time scaling you can do from the prompt layer.

## Self-consistency

Generate multiple [[ai/prompt-engineering/chain-of-thought|chain-of-thought]] answers
at non-zero [[ai/llms/decoding-and-sampling|temperature]], then take the **majority
answer**. Different reasoning paths often converge on the correct result even when any
single path may slip, so the vote is more reliable than one greedy decode. Strong on
math and multiple-choice-style problems with a checkable final answer.

## The broader pattern: sample-and-select

- **Majority vote** — for tasks with a discrete answer.
- **Best-of-N** — generate N, score them (a rubric, a verifier, or an
  [[ai/evaluation/index|LLM judge]]), keep the best. Works for open-ended output.
- **Generate-and-verify** — pair generation with a separate check; only accept if it
  passes.

This is the prompt-level cousin of [[ai/llms/reasoning-and-test-time-compute|test-time
compute]]: spend more inference to raise accuracy without changing the model.

## The cost

You pay **N× the tokens and latency**. So reserve it for high-value or genuinely hard
calls; don't multi-sample a simple classification. And it only helps when there's a
meaningful way to **aggregate or score** — for free-form prose without a verifier, the
vote is murky.

## Pitfall

Self-consistency reduces variance, not bias: if the model is *systematically* wrong
(a shared misconception), all paths agree on the wrong answer. It improves reliability,
not ground truth — still [[ai/evaluation/index|evaluate]].

**Connects to:** [[ai/llms/reasoning-and-test-time-compute|test-time compute]] ·
[[ai/llms/decoding-and-sampling|temperature & sampling]] ·
[[ai/evaluation/index|scoring candidates]]
