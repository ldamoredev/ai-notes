---
title: "Memory & conversation history"
description: LLMs are stateless — "memory" is something you engineer by deciding what past context to carry forward. Sliding windows, summarization, and external memory.
tags: [prompt-engineering, memory, history, context-engineering]
order: 10
updated: 2026-06-07
---
# Memory & conversation history

An LLM has **no memory** between calls. Each request is processed fresh; the only thing
it "remembers" is what you put back into the [[ai/llms/context-window-and-kv-cache|context
window]] this turn. "Memory" in a chatbot or [[ai/agents-and-tools/index|agent]] is an
engineering construct, not a model feature.

## The problem

A long conversation can't all fit in the window, and even if it did, attention favors
the edges and cost grows with length. So you must decide, every turn, **what slice of
the past to carry forward.**

## Strategies

| Strategy | How | Tradeoff |
|---|---|---|
| **Full history** | resend everything | simple; breaks at length/cost limits |
| **Sliding window** | keep the last N turns | cheap; forgets early context |
| **Summarization** | compress old turns into a running summary | keeps gist; loses detail, costs a summarize call |
| **Retrieval memory** | store turns/facts externally, [[ai/rag-and-retrieval/index|retrieve]] relevant ones | scales to long-term; adds retrieval complexity |

Production systems often **combine**: recent turns verbatim + a rolling summary +
retrieval of relevant older facts.

## Short-term vs long-term memory

- **Short-term** — this conversation's recent turns (window management).
- **Long-term** — durable facts about the user/task persisted across sessions
  (a store you write to and retrieve from), e.g. preferences or prior decisions.

## Pitfall

Naively appending every turn eventually overflows the window or quietly degrades via
[[ai/llms/long-context-and-lost-in-the-middle|context rot]]. And summaries can drop the
exact detail that mattered — decide deliberately what's safe to compress versus keep
verbatim.

**Connects to:** [[ai/prompt-engineering/managing-the-context-window|context management]] ·
[[ai/rag-and-retrieval/index|retrieval memory]] ·
[[ai/agents-and-tools/index|agent memory]]
