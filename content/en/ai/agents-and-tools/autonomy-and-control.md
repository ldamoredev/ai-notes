---
title: "Autonomy & least privilege"
description: Give an agent the minimum power to do its job. Scoping tools, permissions, and blast radius so a wrong decision can't become a disaster.
tags: [agents, autonomy, least-privilege, security]
order: 12
updated: 2026-06-10
---
# Autonomy & least privilege

**Mental model:** agent risk scales with **what it is allowed to do**, not how smart
it is — and the agent *will*, at some point, do the wrong thing (a confused plan, a
hallucinated argument, or an [[ai/ai-safety-and-security/indirect-prompt-injection|injected
instruction]] it followed faithfully). Least privilege is the security principle
applied to agents: grant the minimum capability for the task, and bound the damage of
any single wrong action. Crucially, these are **design-time engineering properties** —
permissions, credentials, sandboxes — not prompt instructions.

## Why prompting is not the control plane

OWASP's LLM Top 10 (2025) names this **LLM06: Excessive Agency** — excessive
functionality, permissions, or autonomy relative to the task. The threat model that
makes it concrete: prompt injection means *anyone who can get text in front of your
agent* (a webpage it fetches, a ticket it reads, an email it summarizes) can attempt
to steer it. "Please don't delete anything" in the system prompt is a suggestion to
an attacker; a read-only database credential is not. Simon Willison's **lethal
trifecta** is the audit shortcut: private data access + untrusted content exposure +
an external write channel = exploitable by construction. Remove or gate one leg.

## Scope the power (capability layer)

- **Allowlist tools per agent role.** The support agent gets `search_kb` and
  `draft_reply` — not `send_email`-to-anyone and not `run_sql`. Every extra tool is
  attack surface and [[ai/agents-and-tools/agent-computer-interface|selection-error]]
  surface.
- **The agent gets its own identity.** A service account with least-privilege grants
  — never a human's session or an org-admin key. Per-tenant scoping happens in the
  credential/query, not in the prompt
  ([[ai/rag-and-retrieval/rag-first-pass-design|same rule as RAG filtering]]).
- **Constrain arguments structurally**, so a bad call is invalid rather than
  damaging:

```typescript
const refundTool: Anthropic.Tool = {
  name: "issue_refund",
  description: "Refund one order, up to the order's amount, max $200 without approval.",
  input_schema: {
    type: "object",
    properties: {
      order_id: { type: "string" },
      amount_cents: { type: "integer", minimum: 1, maximum: 20_000 }, // hard cap in schema
      reason: { type: "string", enum: ["damaged", "not_delivered", "duplicate_charge"] },
    },
    required: ["order_id", "amount_cents", "reason"],
    additionalProperties: false,
  },
  strict: true,
};
// AND the handler re-validates against the order + rate-limits per customer —
// schema caps are the first fence, never the only one.
```

## Bound the blast radius (consequence layer)

- **Reversibility tiers** — classify every tool: reversible/cheap → auto-run + log;
  reversible/expensive → auto-run + budget; **irreversible or outward-facing**
  (send, pay, delete, deploy) →
  [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval gate]]. This
  classification is the single highest-value hour of agent security work.
- **Sandbox execution.** Code/browse tools run in disposable containers with no
  production secrets, an egress allowlist, and a filesystem that dies with the task.
  Anthropic's own agent sandboxing guidance and Claude Code's permission modes
  (read-only by default, per-action approval, allowlisted commands) are the
  reference shape.
- **Budgets as a safety mechanism** — caps on iterations, tokens, tool calls, and
  *spend per task* turn a [[ai/agents-and-tools/agent-failure-modes|runaway loop]]
  from an incident into a log line.
- **Staged rollout of autonomy** — new agents start in propose-only mode (human
  executes), graduate to auto-run on a tool-by-tool basis as
  [[ai/agents-and-tools/evaluating-agents|eval]] and incident data accumulate.
  Autonomy is earned per capability, not granted per agent.

## The audit checklist

For each agent in production, you should be able to answer:

| Question | Bad answer |
|---|---|
| What credentials does it hold? | "the team's API key" |
| What's the worst single action it can take unattended? | "not sure" |
| Who can put text in front of it? | "only users" (forgetting fetched/retrieved content) |
| Can it read private data AND write externally in one task? | "yes" (trifecta — gate one) |
| What stops a 500-iteration loop? | "it usually stops" |

## Production lens

Least privilege has UX and cost dividends, not just security ones: fewer tools means
better tool selection and fewer wasted turns; budgets make per-task cost predictable
([[ai/inference-and-optimization/cost-modeling-for-llm-serving|cost modeling]]);
scoped identities make audit logs attributable ("the refund agent did X" vs "someone
with the shared key did X"). Log every tool call with its arguments and
authorization decision in [[ai/mlops/llm-observability-and-tracing|traces]] — the
permission system you can't audit is the one you'll discover failed.

## Failure modes

- **Privilege creep** — "just give it admin so the demo works" survives into prod.
  Schedule permission reviews like dependency audits.
- **Shared credentials across agents** — one agent's compromise becomes everyone's;
  one identity per agent role.
- **Prompt-level enforcement** — any control that lives only in the system prompt is
  bypassed by the first good injection.
- **Sandbox with production secrets mounted** — a sandbox that can read `~/.aws` is
  theater.

**Connects to:** [[ai/agents-and-tools/guardrails-and-human-in-the-loop|guardrails & HITL]] ·
[[ai/ai-safety-and-security/excessive-agency|excessive agency]] ·
[[ai/ai-safety-and-security/indirect-prompt-injection|injection]] ·
[[ai/agents-and-tools/agent-failure-modes|runaway loops]]

## Sources

- [OWASP — LLM06:2025 Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) — the canonical risk definition with functionality/permission/autonomy split and mitigations.
- [Simon Willison — The lethal trifecta (2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — the three-legs audit model; the most useful single heuristic in agent security.
- [Anthropic docs — Strengthen guardrails (mitigating prompt injection in agents)](https://platform.claude.com/docs/en/about-claude/use-case-guides/mitigate-prompt-injections) — vendor guidance on permissioning and approval patterns for tool-using Claude.
- [Greshake et al. 2023 — Not what you've signed up for (arXiv:2302.12173)](https://arxiv.org/abs/2302.12173) — the paper that demonstrated indirect prompt injection against tool-using LLMs; why untrusted content = attacker input.
