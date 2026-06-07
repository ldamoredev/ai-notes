---
title: "Autonomy & least privilege"
description: Give an agent the minimum power to do its job. Scoping tools, permissions, and blast radius so a wrong decision can't become a disaster.
tags: [agents, autonomy, least-privilege, security]
order: 12
updated: 2026-06-07
---
# Autonomy & least privilege

Agent risk scales with **what it's allowed to do**, not how smart it is. The governing
principle is borrowed from security: **least privilege** — grant the agent the minimum
capabilities needed for its task, and bound the damage any single mistake can cause.

## Scope the power

- **Allowlist tools** — expose only the tools this agent needs; every extra tool is extra
  attack/error surface ([[ai/agents-and-tools/agent-computer-interface|tool design]]).
- **Scope credentials** — the agent acts with **its own** least-privilege identity, not
  a human's broad access. Read-only where possible.
- **Constrain arguments** — validate and bound parameters (rate limits, value caps,
  allowed targets) so a bad call can't do unbounded harm.

## Bound the blast radius

- **Reversibility tiers** — auto-run reversible/cheap actions; gate irreversible/costly
  ones behind [[ai/agents-and-tools/guardrails-and-human-in-the-loop|human approval]].
- **Sandboxing** — run code/tools in isolated environments without access to production
  secrets or systems.
- **Spend limits** — cap iterations, tokens, and tool calls so a
  [[ai/agents-and-tools/agent-failure-modes|loop]] can't run up cost or actions
  indefinitely.

## The excessive-agency risk

OWASP names **excessive agency** as a top LLM risk: an agent with more permissions,
autonomy, or tool access than the task warrants can be manipulated (via
[[ai/ai-safety-and-security/index|prompt injection]]) or simply err into damaging
actions. The mitigation is design-time scoping, not better prompting.

> Assume the agent *will*, at some point, do the wrong thing. Engineer the system so the
> worst case is contained and recoverable.

## Pitfall

Convenience pushes toward broad permissions ("just give it admin so it works"). That's
exactly how a single injection or hallucinated action becomes a breach. Start minimal;
widen only with a guardrail.

**Connects to:** [[ai/agents-and-tools/guardrails-and-human-in-the-loop|guardrails & HITL]] ·
[[ai/ai-safety-and-security/index|excessive agency & injection]] ·
[[ai/agents-and-tools/agent-failure-modes|runaway loops]]
