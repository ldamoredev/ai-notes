---
title: "Build an eval set from scratch"
description: A step-by-step procedure for creating a small, high-signal eval set with slices, rubrics, expected outputs, and regression ownership.
tags: [playbook, evaluation, datasets]
order: 2
updated: 2026-06-07
---
# Build an eval set from scratch

Use this playbook when an AI feature has examples but no repeatable way to compare
prompts, models, retrieval changes, or product releases.

## Inputs

- Product workflow or task description.
- Real traces, support tickets, internal examples, or domain expert examples.
- Known failure modes and high-risk cases.
- A first version of the output contract or rubric.

## Procedure

1. Write the product contract in one sentence: what the system must do for the user.
2. Collect 30-100 candidate cases from real usage, edge cases, and high-value workflows.
3. Add metadata for each case: task type, difficulty, language, domain, source, and risk.
4. Define expected output, reference evidence, deterministic check, or judge rubric.
5. Include negative cases where the system should refuse, abstain, ask, or escalate.
6. Split cases into dev, regression, and holdout sets.
7. Run the current baseline and record failures before changing anything.
8. Assign an owner and review cadence for keeping the set fresh.

## Definition of done

| Requirement | Check |
|---|---|
| Representative | covers main workflows and known edge cases |
| Sliceable | metadata supports segment-level analysis |
| Graded | each case has expected behavior or rubric |
| Versioned | cases and rubrics live with the product change history |

## Pitfall

Do not start with hundreds of random cases. A small suite that covers critical slices
will guide decisions better than a large set nobody understands.

**Connects to:** [[ai/evaluation/designing-eval-sets|designing eval sets]] ·
[[ai/evaluation/task-specific-evals|task-specific evals]] ·
[[ai/mlops/feedback-loops|feedback loops]]
