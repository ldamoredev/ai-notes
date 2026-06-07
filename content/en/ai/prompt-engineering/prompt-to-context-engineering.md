---
title: "From prompting to context engineering"
description: The shift from wording a single prompt to designing the whole context the model sees — the dominant skill for RAG and agents.
tags: [prompt-engineering, context-engineering]
order: 1
updated: 2026-06-07
---
# From prompting to context engineering

Early LLM use was about phrasing a clever instruction. As soon as systems added
retrieval, tools, and multi-turn state, the bottleneck moved: quality now depends on
**everything in the [[ai/llms/context-window-and-kv-cache|context window]]**, not just
the user's sentence.

## Two related disciplines

- **Prompt engineering** — how you phrase instructions and examples for a task.
- **Context engineering** — deciding *what information* fills the window: system
  prompt, examples, retrieved chunks, tool results, memory, history — and in what
  order and format.

Prompt engineering is a subset of context engineering. For a chatbot the prompt may
be most of it; for a [[ai/rag-and-retrieval/index|RAG]] or [[ai/agents-and-tools/index|agent]]
system, the assembled context dominates.

## Why the shift happened

- The window is a finite, attention-biased budget ([[ai/llms/long-context-and-lost-in-the-middle|lost
  in the middle]]) — what you include and where matters more than clever wording.
- Most of what the model "knows" at answer time is what you *put there*: a model with
  no relevant context can't be prompted into facts it doesn't have.
- Agents accumulate tool outputs and history that must be curated, summarized, or
  dropped each turn.

## The mental model

> Stop asking only "what's the best prompt?" and start asking "what's the smallest,
> most relevant context that lets the model succeed — and in what order?"

Everything else in this branch — [[ai/prompt-engineering/anatomy-of-a-prompt|prompt
anatomy]], [[ai/prompt-engineering/assembling-context|assembling context]],
[[ai/prompt-engineering/memory-and-history|memory]] — is a tool in that larger job.

**Connects to:** [[ai/llms/context-window-and-kv-cache|context window]] ·
[[ai/rag-and-retrieval/index|RAG]] · [[ai/agents-and-tools/index|agents]]
