---
title: "Designing the agent-tool interface"
description: Tools for agents are a UX problem. Good names, descriptions, scoping, and error messages do more for reliability than a smarter model.
tags: [agents, tool-design, interface]
order: 3
updated: 2026-06-07
---
# Designing the agent-tool interface

Anthropic frames tools as the **Agent-Computer Interface (ACI)** — the agent's UX. Just
as good human UX prevents user errors, good tool design prevents *agent* errors. This is
where most agent reliability is won or lost, far more than model choice.

## Treat tools like an API you'd give a junior engineer

- **Name and describe for the model** — the description is a prompt the model reads to
  decide *whether and how* to use the tool. Spell out what it does, when to use it, and
  what it returns. Add examples.
- **Scope each tool to one clear job** — overlapping or "do-everything" tools cause
  mis-selection. Consolidate sprawling tools; remove rarely-used ones.
- **Choose formats the model handles well** — return structured, concise results;
  prefer outputs that are natural for an LLM to read over raw dumps.
- **Make errors actionable** — return messages that tell the model how to fix the call
  ("missing field `date`; expected YYYY-MM-DD"), so it can self-correct instead of
  looping.

## Manage the token budget of results

Tool outputs land in the [[ai/llms/context-window-and-kv-cache|context window]]. A tool
that returns 50K tokens of JSON poisons the rest of the task
([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]], cost). Paginate,
summarize, or return IDs the agent can expand on demand.

## Test from the model's point of view

> Read your tool descriptions as if you were the model with no other context. If *you*
> couldn't reliably pick the right tool and arguments, neither can it.

Iterate on descriptions and schemas using real agent traces — it's prompt engineering
for tools.

## Pitfall

Exposing your internal API verbatim rarely works: human-API ergonomics ≠ agent
ergonomics. Design a deliberate, minimal surface *for the agent*.

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/agent-failure-modes|failure modes]] ·
[[ai/prompt-engineering/structured-outputs|schemas]]
