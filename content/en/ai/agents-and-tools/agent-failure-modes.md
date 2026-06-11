---
title: "Agent failure modes"
description: Loops, wrong-tool calls, error cascades, context rot, and runaway cost. The characteristic ways agents break and how to contain each.
tags: [agents, failure-modes, debugging, reliability]
order: 10
updated: 2026-06-10
---
# Agent failure modes

**Mental model:** agents fail in recognizable, recurring ways, and almost every fix
is **structural** — a tool, a cap, a context decision — not "use a better model."
Knowing the catalog turns "the agent is flaky" into a specific diagnosis, and the
diagnosis comes from one habit: reading the full trace.

## The compounding-error math (why agents fail more than workflows)

Per-step reliability compounds: `P(task) ≈ p^n` for n dependent steps. At p = 0.95,
ten steps give ~60%; twenty give ~36%. This is the quantitative core of the
[[ai/agents-and-tools/workflows-vs-agents|workflows-first doctrine]] and of every
mitigation below — they work by either **raising p** (better
[[ai/agents-and-tools/agent-computer-interface|tool interfaces]], clearer
observations), **lowering n** (shorter loops, consolidation), or **breaking the
dependency chain** (verification steps that catch errors before they propagate).
τ-bench (Yao et al. 2024, [arXiv:2406.12045](https://arxiv.org/abs/2406.12045))
measured the consequence: agents that pass once often fail on repetition (pass^k ≪
pass@1) — flakiness *is* the dominant failure mode.

## The catalog

| Failure | Looks like in the trace | Structural fix |
|---|---|---|
| **Repetition loop** | same tool, same args, same failing result, ×10 | hard turn cap; duplicate-call detector; error messages that *say what to do differently* |
| **Wrong tool / bad args** | plausible-but-wrong selection; hallucinated ids | fewer, non-overlapping tools; trigger conditions in descriptions; `strict` schemas + semantic validation |
| **Error cascade** | one bad observation, every later step built on it | actionable errors; verification steps mid-plan; checkpoints to roll back to |
| **Context rot** | quality decays after ~20 turns; forgets early constraints | [[ai/agents-and-tools/agent-memory|compaction + scratchpads]]; sub-agent scoping |
| **Goal drift** | output solves a related-but-different task | [[ai/agents-and-tools/planning-and-decomposition|plan artifact]] re-entering context; goal restated in system prompt |
| **False victory** | "Done!" — but the test never ran | require a verifying tool call before completion; eval checks end state, not claims |
| **Runaway cost** | 200-turn task, $40 of tokens, no output | token/turn/spend budgets that hard-stop ([[ai/agents-and-tools/autonomy-and-control|budgets as safety]]) |
| **Injected detour** | actions unrelated to the task after reading external content | treat tool results as data; gates on outward actions ([[ai/ai-safety-and-security/indirect-prompt-injection|indirect injection]]) |

## Programmatic detectors (don't wait for the bill)

The cheap ones catch most incidents — run them inside the loop:

```typescript
function loopHealth(messages: Anthropic.MessageParam[], budget: Budget): string | null {
  const calls = toolCallsOf(messages);
  const last = calls.at(-1);
  // 1. duplicate-call detector
  if (last && calls.slice(0, -1).some((c) => c.name === last.name && deepEqual(c.input, last.input)))
    return "REPEAT_CALL";
  // 2. error-streak detector
  const recentResults = toolResultsOf(messages).slice(-3);
  if (recentResults.length === 3 && recentResults.every((r) => r.is_error)) return "ERROR_STREAK";
  // 3. budget detectors
  if (budget.turns >= budget.maxTurns) return "TURN_CAP";
  if (budget.tokens >= budget.maxTokens) return "TOKEN_CAP";
  return null;
}
// On signal: inject a steering message ("this exact call already failed — change
// approach or report what's blocking you"), escalate to a human, or abort with trace.
```

The graduated response matters: a `REPEAT_CALL` signal with a steering message often
*recovers* the task; an immediate abort wastes the progress.

## Debugging: read the trace, fix the earliest stage

> The single most useful agent-debugging habit is reading the full trajectory —
> thought, action, observation, per turn. The failure is almost always obvious once
> you see what the agent actually saw.

Then fix the **earliest** broken stage. The classic misdiagnosis: a "reasoning
failure" at turn 12 that is actually a garbage observation at turn 3 (a tool that
returned an opaque error, a 40K-token dump the model skimmed). Same discipline as
[[ai/rag-and-retrieval/rag-failure-modes|RAG debugging]]: earliest stage first, one
change at a time, re-run the
[[ai/agents-and-tools/evaluating-agents|eval suite]] after each.

Production telemetry that surfaces failures before users do
([[ai/mlops/llm-observability-and-tracing|tracing]] dashboards): turns-per-task and
tokens-per-task distributions (right-shifting tails = emerging loops), per-tool error
rates (a 40% error tool is an interface bug), abort-reason counts, and
gate-override rates.

## What 2023→2026 changed (and didn't)

Better models raised per-step p substantially — which lengthened *feasible* task
horizons (METR's measurements of the longest tasks agents complete at 50% reliability
show steady growth). What didn't change: the compounding structure, the dominance of
tool/observation quality over model IQ as the practical bottleneck, and false victory
as the most user-visible failure. Model upgrades shift the catalog's frequencies;
they retire none of its rows — design for all of them.

**Connects to:** [[ai/agents-and-tools/react-loop|the loop]] ·
[[ai/agents-and-tools/evaluating-agents|measuring reliability]] ·
[[ai/agents-and-tools/autonomy-and-control|capping blast radius]] ·
[[ai/rag-and-retrieval/rag-failure-modes|the RAG analogue]]

## Sources

- [Yao et al. 2024 — τ-bench (arXiv:2406.12045)](https://arxiv.org/abs/2406.12045) — pass^k: the flakiness measurement that defines the problem.
- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — the workflows-first stance as failure-mode prevention.
- [Anthropic — How we built our multi-agent research system (2025)](https://www.anthropic.com/engineering/multi-agent-research-system) — candid production failure stories (runaway sub-agents, compounding errors) and their structural fixes.
- [Greshake et al. 2023 — Indirect prompt injection (arXiv:2302.12173)](https://arxiv.org/abs/2302.12173) — the injected-detour row of the catalog, demonstrated.
- [METR — Measuring AI ability to complete long tasks (2025)](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/) — task-horizon-vs-reliability data; the macro view of compounding error over time.
