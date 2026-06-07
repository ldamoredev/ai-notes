---
title: "LLM-as-judge"
description: LLM judges can grade open-ended outputs at scale, but they need rubrics, calibration, bias checks, and human audits.
tags: [evaluation, llm-as-judge, rubrics]
order: 3
updated: 2026-06-07
---
# LLM-as-judge

LLM-as-judge uses a model to grade another model's output against a rubric. It is
useful when exact matching is too brittle, but it is still a measurement system with
biases, variance, and failure modes.

## What judges are good at

- Comparing two responses on helpfulness, groundedness, completeness, or tone.
- Applying a task-specific rubric to open-ended text.
- Explaining why a response failed so humans can inspect the issue faster.
- Scaling review across large eval sets before sampling with humans.

## Judge setup

| Design choice | Safer default |
|---|---|
| Rubric | explicit criteria, failure examples, score scale anchors |
| Inputs | include task, answer, reference/context, and expected constraints |
| Output | structured JSON with score, pass/fail, and concise rationale |
| Calibration | compare against human labels on a small gold sample |
| Stability | run repeated samples or deterministic settings where possible |

Judges should grade the behavior you care about, not generic "quality".

## Common biases

- Position bias: preferring the first or second answer in pairwise comparisons.
- Verbosity bias: rewarding longer responses even when concise is better.
- Self-preference: favoring outputs from the same model family.
- Authority bias: over-trusting confident unsupported claims.
- Rubric drift: applying criteria differently across domains or examples.

## Pitfall

An LLM judge can make evals look objective while encoding a vague rubric. If humans
cannot predict what the judge will consider a pass, the judge is measuring vibes with
a JSON wrapper.

**Connects to:** [[ai/evaluation/human-evaluation|human evaluation]] ·
[[ai/evaluation/metrics-for-llm-evals|LLM eval metrics]] ·
[[ai/prompt-engineering/structured-outputs|structured outputs]]
