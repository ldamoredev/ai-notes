---
title: "Workflows vs agents: when to use which"
description: The most important agent decision is whether to build one at all. Predetermined workflows beat autonomous agents whenever the steps are knowable.
tags: [agents, workflows, architecture]
order: 1
updated: 2026-06-10
---
# Workflows vs agents: when to use which

**Mental model:** the distinction is *who controls the control flow*. In a **workflow**,
LLM calls are orchestrated through predefined code paths — you decide the steps, the
model fills them in. In an **agent**, the model directs its own process and tool use,
looping until done. The taxonomy comes from Anthropic's
[Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)
(Dec 2024), still the reference framing in 2026: *find the simplest solution, and only
increase complexity when demonstrably needed.*

## The workflow patterns (know these before "agent")

| Pattern | Shape | Use when |
|---|---|---|
| **Prompt chaining** | call A → code check → call B | task decomposes into fixed sequential steps |
| **Routing** | classifier call → one of N specialized prompts | distinct input categories need different handling |
| **Parallelization** | N independent calls → aggregate | sectioning (independent subtasks) or voting (N samples, pick consensus) |
| **Orchestrator–workers** | LLM decides subtasks → workers execute → synthesize | subtasks are dynamic but the *structure* is fixed |
| **Evaluator–optimizer** | generator call ↔ critic call until pass | quality is checkable and iteration helps |

Most products labeled "agent" in the wild are one of these five. They are more
predictable, cheaper, faster, and radically easier to
[[ai/agents-and-tools/evaluating-agents|evaluate]] than a free loop, because every
path through the system is a path you wrote. If you can draw the flowchart, **code the
flowchart**.

A routing workflow in ~20 lines — note the LLM makes *decisions inside* a structure
your code owns:

```typescript
const route = await anthropic.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 10,
  system: "Classify the support ticket. Reply with exactly one word: billing, technical, or refund.",
  messages: [{ role: "user", content: ticket }],
});
const label = route.content[0].type === "text" ? route.content[0].text.trim() : "technical";

const handlers: Record<string, string> = {
  billing: BILLING_SYSTEM_PROMPT,
  technical: TECH_SYSTEM_PROMPT,
  refund: REFUND_SYSTEM_PROMPT,
};
const answer = await anthropic.messages.create({
  model: "claude-opus-4-8",
  max_tokens: 1024,
  system: handlers[label] ?? handlers.technical,
  messages: [{ role: "user", content: ticket }],
});
```

## When an agent earns its keep

Anthropic's criteria, which have held up: use an agent when the task is **open-ended**
— the number and order of steps cannot be predicted, a fixed flow would be a giant
brittle decision tree, and the model must react to intermediate results. Canonical
fits: coding against a test suite (verifiable, unknown path), open-ended research,
operating a computer. Plus three gating questions before you commit:

- **Value** — does the outcome justify 10–100× the tokens of a workflow?
- **Verifiability** — can success be *checked* (tests pass, record updated)? Agents
  without verifiable feedback drift and
  [[ai/agents-and-tools/agent-failure-modes|declare false victory]].
- **Cost of error** — are mistakes recoverable, or does one bad action need
  [[ai/agents-and-tools/guardrails-and-human-in-the-loop|a human gate]] anyway?

## The reliability math that decides it

Autonomy compounds per-step error. A step that's 95% reliable gives `0.95^10 ≈ 60%`
over a 10-step dependent chain. Workflows attack this by *removing* model-controlled
steps (code is ~100% reliable at control flow); agents attack it with verification
loops and retries — which cost tokens. This single calculation explains most of the
2024→2026 industry experience: agent demos at 90% per-step reliability looked magical
and shipped poorly, and what made production agents viable was better models *plus*
shorter loops, tighter [[ai/agents-and-tools/agent-computer-interface|tool design]],
and verifiable feedback — not more autonomy.

## The spectrum in practice

| | Predictability | Cost/latency | Evaluability |
|---|---|---|---|
| Single prompt | highest | lowest | trivial |
| Workflow | high | low–medium | per-step, easy |
| Agent loop | lower | high (often 4×+ chat tokens) | [[ai/agents-and-tools/evaluating-agents|trajectory-level, hard]] |
| Multi-agent | lowest | highest (~15× chat tokens) | hardest |

Real systems are hybrids: a workflow whose middle step is a small bounded agent loop
("fix the failing test, max 5 iterations") gets most of the flexibility with bounded
blast radius. That shape — **agentic step inside a workflow** — is the most
underrated point on the spectrum.

## Failure modes of choosing wrong

- **Agent where a workflow fit**: nondeterministic latency and cost, flaky evals, and
  you debug [[ai/agents-and-tools/agent-failure-modes|trajectories]] instead of steps
  — to solve a problem `if/else` handled.
- **Workflow where an agent fit**: an ever-growing decision tree with a long tail of
  unhandled branches; each patch makes it more brittle. If your routing table has 30
  rows and keeps growing, the steps weren't knowable — flip it.
- **Premature multi-agent**: see [[ai/agents-and-tools/multi-agent-systems|multi-agent
  systems]]; the costs are an order of magnitude before the benefits show.

**Connects to:** [[ai/prompt-engineering/task-decomposition|prompt chaining]] ·
[[ai/agents-and-tools/react-loop|the agent loop]] ·
[[ai/agents-and-tools/autonomy-and-control|autonomy limits]] ·
[[ai/ai-product-engineering/latency-cost-quality-triangle|cost/latency trade]]

## Sources

- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — the workflow taxonomy and the "simplest thing that works" doctrine; still the field's reference.
- [Anthropic — Building Effective Agents Cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/patterns/agents) — runnable implementations of the five workflow patterns.
- [OpenAI — A Practical Guide to Building Agents (2025)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — the competing vendor's framing; converges on the same workflow-first advice.
- [Yao et al. 2022 — ReAct (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) — what the "agent" end of the spectrum is built on.
- [Anthropic — How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/multi-agent-research-system) — source of the ~4×/~15× token-multiplier economics used here.
