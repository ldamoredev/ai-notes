---
title: "Tool & function calling"
description: Tool calling is how an LLM acts — it emits a structured call, your code runs it, the result goes back. The mechanism behind every agent.
tags: [agents, tool-calling, function-calling]
order: 2
updated: 2026-06-07
---
# Tool & function calling

Tools are how an LLM escapes its own head and *does* things — search, run code, query a
DB, call an API. The mechanism is simpler than it looks and is the foundation every
[[ai/agents-and-tools/react-loop|agent loop]] is built on.

## How it works

1. You give the model a set of **tool definitions**: name, description, and a parameter
   **[[ai/prompt-engineering/structured-outputs|schema]]** (JSON Schema).
2. The model, instead of replying in prose, emits a **structured tool call** — which
   tool and what arguments.
3. **Your code executes it** (the model never runs anything itself) and returns the
   result.
4. The result goes back into the [[ai/llms/context-window-and-kv-cache|context]], and
   the model continues — answer the user, or call another tool.

The model only *chooses and fills in* calls; execution, permissions, and safety live in
**your** code. That boundary is the whole security story.

## Why it's reliable

It reuses the same [[ai/prompt-engineering/structured-outputs|schema-constrained
output]] machinery, so the call conforms to your function signature. That turns "the
model said something" into "a typed function invocation my system can run."

## Doing it well

- **Clear names + descriptions** — the model picks tools from these; vague docs →
  wrong tool. The description is a prompt.
- **Few, well-scoped tools** beat many overlapping ones (choice overload causes
  mistakes).
- **Validate arguments** and return **useful errors** the model can recover from.
- **Return concise results** — dumping huge payloads wastes
  [[ai/prompt-engineering/managing-the-context-window|context]].

## Pitfall

Models hallucinate tool arguments or call the wrong tool when definitions are unclear or
too numerous. Tool **design** (next note) is most of the reliability — see
[[ai/agents-and-tools/agent-computer-interface|the agent-tool interface]].

**Connects to:** [[ai/prompt-engineering/structured-outputs|structured output]] ·
[[ai/agents-and-tools/agent-computer-interface|tool design]] ·
[[ai/agents-and-tools/react-loop|the loop]]
