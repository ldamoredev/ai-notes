---
title: "Anatomy of a good prompt"
description: The reusable structure behind reliable prompts — role, task, context, constraints, output format, and examples.
tags: [prompt-engineering, prompts, structure]
order: 2
updated: 2026-06-07
---
# Anatomy of a good prompt

Good prompts aren't magic words; they're **clear specifications**. A reliable prompt
usually has the same parts, whether you write them as prose or sections.

## The components

- **Role / persona** — who the model is acting as ("You are a senior security
  reviewer"). Sets tone and domain framing.
- **Task** — the single, explicit objective. Ambiguity here is the #1 cause of bad
  output.
- **Context** — the material the task operates on (the document, data, examples).
- **Constraints** — what to do and avoid: length, style, what to skip, how to handle
  uncertainty ("if the answer isn't in the context, say so").
- **Output format** — the exact shape expected ([[ai/prompt-engineering/structured-outputs|JSON,
  schema]], headings, bullet list).
- **Examples** — one or more demonstrations ([[ai/prompt-engineering/zero-and-few-shot|few-shot]])
  when the task is hard to describe but easy to show.

## Principles that consistently help

- **Be specific and concrete** — replace "summarize nicely" with "summarize in 3
  bullets, ≤15 words each, no jargon."
- **Show, don't just tell** — an example often beats a paragraph of instructions.
- **Put instructions and the most important context at the edges**, not buried in the
  middle ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]).
- **Give an out** — tell the model what to do when it can't comply, to curb
  [[ai/llms/why-llms-hallucinate|hallucination]].
- **One prompt, one job** — split compound tasks ([[ai/prompt-engineering/task-decomposition|decomposition]]).

## Pitfall

Over-stuffing a prompt with caveats can confuse the model as much as too little.
Write the minimum that makes the task unambiguous, then
[[ai/prompt-engineering/evaluating-and-iterating-prompts|test and trim]].

**Connects to:** [[ai/prompt-engineering/system-prompts-and-roles|system prompts]] ·
[[ai/prompt-engineering/zero-and-few-shot|few-shot]] ·
[[ai/prompt-engineering/structured-outputs|output format]]
