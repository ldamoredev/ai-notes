---
title: "Managing the context window"
description: The window is a finite budget shared by instructions, examples, retrieval, and history. How to spend it — compression, selection, and what to cut.
tags: [prompt-engineering, context-engineering, context-window]
order: 9
updated: 2026-06-07
---
# Managing the context window

Every token in the [[ai/llms/context-window-and-kv-cache|context window]] competes for
space, [[ai/ai-product-engineering/index|cost]], and the model's attention. Context
management is the discipline of deciding **what earns its place** — and it's most of
the work in RAG and agent systems.

## The budget and its claimants

System prompt · instructions · few-shot examples · [[ai/rag-and-retrieval/index|retrieved
chunks]] · tool outputs · conversation history · the user's message · room to generate.
They all draw from the same finite pool. When it fills, quality drops or requests
fail — so you must actively curate.

## Levers

- **Select, don't dump** — retrieve and include only what's relevant; more context
  often means *worse* answers ([[ai/llms/long-context-and-lost-in-the-middle|lost in
  the middle]]), not just costlier ones.
- **Compress** — summarize old turns and verbose material; replace raw logs with
  distilled facts.
- **Trim history** — keep recent turns verbatim, summarize or drop older ones
  ([[ai/prompt-engineering/memory-and-history|memory]]).
- **Rank and place** — put the most important content at the **start/end**, not the
  middle.
- **Offload** — keep large/stable knowledge in retrieval or tools, not stuffed into
  every prompt.

## Why "just use a bigger window" isn't the answer

Bigger windows help but don't dissolve the problem: attention still favors the edges,
cost and latency rise with length, and irrelevant context actively distracts the
model. Capacity is not curation.

> Treat context like a tight budget you're spending on the model's behalf. The goal is
> the **smallest** context that makes the task succeed.

**Connects to:** [[ai/llms/context-window-and-kv-cache|context window & cost]] ·
[[ai/prompt-engineering/assembling-context|assembling context]] ·
[[ai/rag-and-retrieval/index|retrieval]]
