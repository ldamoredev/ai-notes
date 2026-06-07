---
title: "Evaluating & iterating prompts"
description: Prompts are code with no compiler. Without an eval set you're tuning by vibes — and every "fix" silently breaks something else.
tags: [prompt-engineering, evaluation, iteration, regression]
order: 12
updated: 2026-06-07
---
# Evaluating & iterating prompts

Prompting *feels* like editing text, so people tune by gut: change wording, eyeball one
example, ship. That's how you fix one case and silently break five. Prompts are
**product logic** and deserve the same discipline as code.

## The core practice

1. **Build a small eval set** — 20–100 representative inputs with expected outputs or a
   grading rubric, including the edge cases that bite you ([[ai/evaluation/index|eval]]).
2. **Change one thing**, then run the *whole* set — not a single example.
3. **Compare against the previous version** — a prompt edit is a deploy; check for
   regressions, not just the case you were fixing.
4. **Version prompts** like code (they belong in source control / a prompt registry).

## How to grade

- **Exact/programmatic** — for [[ai/prompt-engineering/structured-outputs|structured]]
  or classification tasks (parse + compare).
- **[[ai/evaluation/index|LLM-as-judge]]** — for open-ended output, scored against a
  rubric (mind judge biases).
- **Human review** — for the highest-stakes or subjective cases; spot-check the judge.

## Why "it worked when I tried it" is a trap

A single success says nothing about the distribution of inputs. Models are sensitive to
phrasing, ordering, and [[ai/llms/decoding-and-sampling|sampling]], so the same prompt
varies run to run. Only an eval set across many inputs tells you whether a change is a
real improvement or noise.

> Treat each prompt change as a code change: it needs a test set, a diff against the
> baseline, and a regression check before it ships.

This is the prompt-engineering end of a spectrum that continues into full
[[ai/evaluation/index|system evaluation]] and [[ai/mlops/index|LLMOps]].

**Connects to:** [[ai/evaluation/index|building eval sets]] ·
[[ai/mlops/index|prompt versioning]] ·
[[ai/prompt-engineering/structured-outputs|grading structured output]]
