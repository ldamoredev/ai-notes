---
title: Evaluation
description: Evaluation patterns for LLM products, RAG systems, agents, judges, datasets, metrics, and regression checks.
tags: [evaluation, evals, quality]
order: 0
updated: 2026-06-07
---
# Evaluation

Evaluation is the control system for AI work. It turns product behavior, model
quality, safety, cost, latency, and user trust into things that can be measured,
compared, and improved without tuning by vibes.

## Evaluation foundations

- [[ai/evaluation/model-vs-product-evals|Model vs product evals]] separates benchmark quality from the product contract users experience.
- [[ai/evaluation/designing-eval-sets|Designing eval sets]] explains golden datasets, slices, and leakage control.
- [[ai/evaluation/metrics-for-llm-evals|Metrics for LLM evals]] maps exact, semantic, groundedness, and cost metrics.
- [[ai/evaluation/task-specific-evals|Task-specific evals]] turns "good output" into a rubric for each workflow.

## Judges, humans, and benchmarks

- [[ai/evaluation/llm-as-judge|LLM-as-judge]] covers rubric-based grading and judge bias.
- [[ai/evaluation/human-evaluation|Human evaluation]] designs review workflows that are consistent and useful.
- [[ai/evaluation/public-benchmarks-and-limits|Public benchmarks and limits]] explains when external benchmarks help and when they mislead.

## Regression and failure analysis

- [[ai/evaluation/prompt-regression-testing|Prompt regression testing]] treats prompts as versioned product logic.
- [[ai/evaluation/systematic-error-analysis|Systematic error analysis]] turns failures into an improvement backlog.
- [[ai/evaluation/hallucination-detection|Hallucination detection]] separates unsupported claims from merely imperfect wording.

## System evals

- [[ai/evaluation/evaluating-rag-systems|Evaluating RAG systems]] decomposes retriever, context, generator, and citation quality.
- [[ai/evaluation/evaluating-agent-systems|Evaluating agent systems]] scores outcomes, trajectories, tool use, and autonomy control.
- [[ai/ai-product-engineering/evals-inside-the-product|Evals inside the product]] shows where these checks live in delivery.

## Core sources

- Hamel Husain, **Your AI Product Needs Evals** and **LLM-as-a-Judge**.
- Eugene Yan, **Evaluating the Effectiveness of LLM-Evaluators** and AlignEval writing.
- Shreya Shankar and Hamel Husain, **AI Evals for Engineers & PMs**.
- RAGAS documentation for RAG faithfulness, relevance, and retrieval metrics.
- HELM, LMSYS Chatbot Arena, MMLU, and Chip Huyen's AI Engineering writing on evaluation practice.
