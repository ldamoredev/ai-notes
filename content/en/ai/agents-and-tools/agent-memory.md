---
title: "Agent memory"
description: An agent loop fills the context fast. Working memory, persistent memory, and externalizing state so a long-running agent doesn't drown in its own history.
tags: [agents, memory, context-engineering]
order: 6
updated: 2026-06-07
---
# Agent memory

Every [[ai/agents-and-tools/react-loop|loop iteration]] appends a thought, an action, and
a tool result to the [[ai/llms/context-window-and-kv-cache|context window]]. On a long
task that overflows fast — so "memory" for an agent is the engineering of **what state to
keep, where, and how to bring it back**, building on
[[ai/prompt-engineering/memory-and-history|prompt-level memory]].

## Layers of agent memory

- **Working memory** — the current context: recent steps, the active subgoal, latest
  observations. Finite and precious.
- **Persistent / long-term memory** — facts and progress stored **outside** the model
  (a file, DB, or [[ai/rag-and-retrieval/index|vector store]]) and retrieved when
  relevant. Survives across the task and across sessions.

## Tactics that keep agents coherent

- **Summarize-and-compress** — periodically replace a long history with a running
  summary of decisions, findings, and open subgoals.
- **Externalize state** — write progress to a scratchpad/file the agent reads back,
  instead of holding everything in context (a "notebook" the agent maintains).
- **Retrieve on demand** — store artifacts and pull only what the current step needs.
- **Scope per subtask** — give a [[ai/agents-and-tools/multi-agent-systems|sub-agent]] a
  clean, minimal context for its job rather than the whole history.

## Why it matters

Without memory management, long agents suffer
[[ai/llms/long-context-and-lost-in-the-middle|context rot]]: ballooning cost, slower
steps, and degraded reasoning as the window fills with stale detail. Good memory keeps
the working context **small and relevant** — the same context-engineering goal,
automated over a loop.

## Pitfall

Aggressive summarization can drop the one detail a later step needs; naive
"remember-everything" overflows. Decide deliberately what's safe to compress vs keep
verbatim, and let the agent re-fetch specifics from persistent store.

**Connects to:** [[ai/prompt-engineering/memory-and-history|prompt memory]] ·
[[ai/rag-and-retrieval/index|retrieval memory]] ·
[[ai/llms/long-context-and-lost-in-the-middle|context rot]]
