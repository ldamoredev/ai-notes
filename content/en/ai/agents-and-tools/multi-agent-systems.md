---
title: "Multi-agent systems & handoffs"
description: Splitting work across specialized agents (orchestrator + sub-agents) buys parallelism and focus — at the cost of coordination, tokens, and new failure modes.
tags: [agents, multi-agent, orchestration, handoffs]
order: 7
updated: 2026-06-10
---
# Multi-agent systems & handoffs

**Mental model:** the real resource being managed is **context, not agents**. A
sub-agent is a fresh context window with a narrow brief — useful exactly when one
window can't hold the whole job, or when subtasks are independent enough to run in
parallel. Multi-agent is context architecture wearing an org chart.

## The evidence, both directions

**For:** Anthropic's
[multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system)
(2025) — an Opus-class lead agent spawning parallel Sonnet-class sub-agents —
outperformed a single-Opus baseline by **90.2%** on their internal research eval.
Their analysis: token usage alone explained ~80% of performance variance on
BrowseComp-style tasks, and multi-agent is fundamentally a way to *spend more tokens
in parallel contexts* on breadth-first problems. The bill: agents use ~**4×** chat
tokens; multi-agent systems ~**15×**.

**Against:** Cognition's
[Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) (2025)
— for *write* tasks (code), parallel sub-agents make conflicting implicit decisions
(two agents "fix" the same module differently), and shared context + single-threaded
execution beats coordination overhead. Both are right, about different task shapes.

**Decision rule:** parallelize **read-heavy, breadth-first** work (research, search,
audit, eval) where sub-results compose by *aggregation*; keep **write-heavy,
consistency-critical** work (coding, doc editing, anything with shared mutable state)
single-threaded with good [[ai/agents-and-tools/agent-memory|memory management]].

## Common shapes

| Shape | Mechanics | Fits |
|---|---|---|
| **Orchestrator–workers** | lead decomposes, spawns N sub-agents, synthesizes | breadth-first research/analysis; the dominant pattern |
| **Handoff** | agent A transfers control + a context package to specialist B | routing across domains (billing → billing agent) |
| **Pipeline** | A's output is B's input, fixed order | really a [[ai/agents-and-tools/workflows-vs-agents|workflow]] — prefer coding it |
| **Critic/verifier** | worker produces, separate agent reviews | when generation and judgment benefit from separate contexts |

## The handoff is the hard part

A sub-agent sees **nothing** the orchestrator doesn't pass explicitly. Vague briefs
("research the competitors") produce duplicated work and gaps; full-history dumps
reproduce the context bloat you were escaping. Anthropic's production lesson: the
orchestrator must give each sub-agent an **objective, output format, tool/source
guidance, and explicit task boundaries**. Treat the brief as an API contract:

```typescript
const subagentTask: Anthropic.Tool = {
  name: "run_subagent",
  description:
    "Delegate ONE self-contained research subtask to a parallel sub-agent. The " +
    "sub-agent sees ONLY what you pass here — include every fact it needs.",
  input_schema: {
    type: "object",
    properties: {
      objective: { type: "string", description: "Single, narrow question to answer" },
      context: { type: "string", description: "Facts/constraints it needs (it has no other memory)" },
      output_format: { type: "string", description: "Exact shape of the result you need back" },
      budget_turns: { type: "integer", description: "Max tool-use turns (keep small: 3-8)" },
    },
    required: ["objective", "context", "output_format", "budget_turns"],
    additionalProperties: false,
  },
};
// Handler: messages.create() with its OWN small system prompt + tool set, fresh
// messages array, cheaper model (sonnet/haiku class) — run N of these with
// Promise.all, return each sub-agent's final text as the tool_result.
```

Architecture choices embedded there: sub-agents get a **cheaper model** (the lead
needs judgment; workers need throughput), a **turn budget** (a runaway sub-agent is
invisible from the parent), and **results return as tool_results** — compact
syntheses, not transcripts.

## The costs (don't ignore them)

- **Tokens** — ~15× chat. Reserve for tasks whose value clears that bar; a
  [[ai/inference-and-optimization/cost-modeling-for-llm-serving|per-task cost model]]
  is mandatory before shipping.
- **Compounding errors** — one wrong sub-result poisons the synthesis silently; the
  lead never saw the sub-agent's dead ends. Verifier steps and citation-carrying
  results ([[ai/rag-and-retrieval/grounding-and-citations|grounding]]) mitigate.
- **Coordination overhead** — decomposition + synthesis turns are pure overhead on
  small tasks; below ~10 minutes of equivalent single-agent work, the orchestration
  tax usually exceeds the parallelism win.
- **Debugging across contexts** — a failure may live in the brief, the sub-agent, or
  the synthesis; without per-agent [[ai/mlops/llm-observability-and-tracing|traces]]
  (one span tree per sub-agent, linked to the parent), attribution is guesswork.

## Production lens

Latency improves only if sub-agents truly run in parallel **and** the synthesis turn
doesn't dwarf them. Stream the lead agent's progress to users
([[ai/ai-product-engineering/streaming-and-perceived-latency|perceived latency]]),
cap *global* spend (sum across agents, not per agent), and log the
decomposition itself — bad briefs are your most common bug and they're only visible
if recorded. Start with **one agent + good tools**; add the orchestrator when traces
show one context genuinely can't hold the job.

**Connects to:** [[ai/agents-and-tools/planning-and-decomposition|decomposition]] ·
[[ai/agents-and-tools/agent-memory|context per agent]] ·
[[ai/agents-and-tools/evaluating-agents|evaluating multi-agent]] ·
[[ai/agents-and-tools/workflows-vs-agents|orchestrator-workers as workflow]]

## Sources

- [Anthropic — How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/multi-agent-research-system) — the 90.2% result, token economics, and hard-won prompting lessons for orchestrators.
- [Cognition — Don't Build Multi-Agents (2025)](https://cognition.ai/blog/dont-build-multi-agents) — the counter-case for write-tasks: shared context beats coordination.
- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — orchestrator-workers as a *workflow* pattern, before reaching for free-form multi-agent.
- [Yao et al. 2024 — τ-bench (arXiv:2406.12045)](https://arxiv.org/abs/2406.12045) — where coordination-style agent reliability gets measured (pass^k); context for why multi-agent reliability is hard to claim.
