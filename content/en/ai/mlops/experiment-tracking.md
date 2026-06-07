---
title: "Experiment tracking"
description: Track code, data, parameters, metrics, artifacts, and notes so model changes become comparable instead of anecdotal.
tags: [mlops, experiments, tracking, reproducibility]
order: 2
updated: 2026-06-07
---
# Experiment tracking

Experiment tracking turns model work from memory into evidence. Every meaningful run
should record enough context that someone can compare it, reproduce it, and understand
why it mattered.

## What to log

| Item | Examples |
|---|---|
| Code | commit, config, training script |
| Data | dataset version, split, filters, labels |
| Parameters | model, seed, learning rate, batch size, prompt version |
| Metrics | validation score, eval suite, latency, cost |
| Artifacts | model/adapters, prompts, plots, error samples |
| Notes | hypothesis, result, decision |

For LLM apps, include prompt template, retrieved-context configuration, tool schemas,
and judge/eval prompts. Otherwise you cannot explain behavior changes.

## Compare hypotheses, not random runs

Each experiment should answer a question: "Does reranking improve groundedness?" or
"Does LoRA rank 16 beat rank 8 on held-out support tickets?" Without a hypothesis,
tracking becomes a junk drawer.

## Promote only stable artifacts

Raw experiment artifacts are not production releases. Promote a model, prompt, or
retrieval config only after it passes the relevant [[ai/evaluation/index|evals]] and
regression checks.

## Pitfall

Logging metrics without data and code versions creates false precision. A better score
from an unknown dataset version is not evidence.

**Connects to:** [[ai/foundations/data-splits-and-leakage|data splits]] ·
[[ai/fine-tuning-and-alignment/evaluating-a-finetune|fine-tune evaluation]] ·
[[ai/mlops/model-and-prompt-registry|registries]]
