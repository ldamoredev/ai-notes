---
title: "Prompt regression testing"
description: Prompt changes should be evaluated like code changes: versioned, compared against a baseline, and gated by regression tests.
tags: [evaluation, prompt-engineering, regression, ci]
order: 7
updated: 2026-06-07
---
# Prompt regression testing

Prompts are product logic. A wording change can fix one example, break a different
slice, increase cost, or reduce safety, so prompt edits need regression tests.

## Regression workflow

1. Version the prompt and any retrieved-context template.
2. Run the eval set against the current baseline.
3. Change one thing.
4. Run the same eval set against the candidate.
5. Compare scores, failures, cost, latency, and safety checks.
6. Inspect diffs for important cases before shipping.

This is the prompt-level version of [[ai/mlops/ci-cd-for-ml|ML CI/CD]].

## What to test

- Expected behavior on common tasks.
- Edge cases and previous production failures.
- Structured output validity.
- Refusal and escalation behavior.
- Sensitivity to input order, length, language, and ambiguity.
- Token use, latency, and model routing cost.

## Release gates

| Gate | Example |
|---|---|
| Quality | no statistically meaningful drop on the regression suite |
| Safety | no new failures on refusal or policy cases |
| Format | 100% valid JSON for structured tasks |
| Cost | candidate stays within budget or justifies the increase |
| Latency | p95 remains below the product target |

## Pitfall

Never judge a prompt edit only on the case that motivated the edit. That case is now a
dev example. The decision comes from the full suite and the slices that matter.

**Connects to:** [[ai/prompt-engineering/evaluating-and-iterating-prompts|evaluating prompts]] ·
[[ai/evaluation/designing-eval-sets|eval sets]] ·
[[ai/mlops/model-and-prompt-registry|prompt registry]]
