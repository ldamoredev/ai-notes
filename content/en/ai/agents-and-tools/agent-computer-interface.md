---
title: "Designing the agent-tool interface"
description: Tools for agents are a UX problem. Good names, descriptions, scoping, and error messages do more for reliability than a smarter model.
tags: [agents, tool-design, interface]
order: 3
updated: 2026-06-10
---
# Designing the agent-tool interface

**Mental model:** tools are the agent's user interface — the **Agent-Computer
Interface (ACI)**, a term from SWE-agent (Yang et al. 2024,
[arXiv:2405.15793](https://arxiv.org/abs/2405.15793)), whose headline result is the
point of this note: *interface design moved benchmark performance more than model
choice*. Just as good human UX prevents user errors, good tool design prevents agent
errors. This is where agent reliability is won or lost.

## What SWE-agent actually found

Giving an LLM a raw Linux shell and git performs poorly. Purpose-built interfaces —
a file viewer showing 100 lines with line numbers, an edit command with built-in lint
feedback, a search that returns at most 50 hits with a "narrow your query" message —
took SWE-bench resolution from 3.8% (shell-only baseline) to 12.5% per-instance
with the same underlying model. The general lessons transfer to every agent:

- **Feedback beats capability** — an edit tool that *reports* the syntax error it
  just introduced lets the model fix it; a silent one produces error cascades.
- **Guardrails in the interface** — bounded output sizes, mandatory line ranges,
  confirmation of state after each action.
- **Compact observations** — the model reasons over what it sees; show state, not
  noise.

## Treat tools like an API for a brilliant, context-starved colleague

From Anthropic's
[Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
(2025), the practices that survive contact with evals:

- **The description is a prompt.** What it does, *when to use it* (trigger
  conditions), what it returns, edge cases. Current Opus-class models under-trigger
  on vaguely-described tools.
- **Namespace and consolidate.** `jira_search`, `jira_create`, `jira_comment` — a
  prefixed family of 3 beats 12 overlapping endpoints. Every extra tool dilutes
  selection accuracy and burns context on schemas.
- **Return *meaningful* context, token-efficiently.** Resolve ids to names, include
  the fields the next decision needs, drop everything else. Offer a
  `detail: "summary" | "full"` parameter rather than always dumping.
- **Make errors actionable.** The error string is the model's debugging experience:

```typescript
// ❌ the model can only flail on this
return { ok: false, body: "Error 400" };

// ✅ the model self-corrects on this
return {
  ok: false,
  body: "date must be YYYY-MM-DD (got '3/5/26'). Example: 2026-03-05. " +
        "If the user gave a relative date, resolve it first using today's date.",
};
```

## A bad tool vs a good tool

```typescript
// ❌ mirror of an internal endpoint — agent ergonomics ≠ API ergonomics
{ name: "query", description: "Runs a query",
  input_schema: { type: "object", properties: { q: { type: "string" } } } }

// ✅ designed for the model: intent in the name, triggers in the description,
//    bounded output contract, semantic parameters
{
  name: "search_customer_orders",
  description:
    "Search one customer's orders. Use when the user asks about order status, " +
    "history, or totals. Returns at most 20 orders (newest first) with id, date, " +
    "status, and total. For full line items, follow up with get_order_details.",
  input_schema: {
    type: "object",
    properties: {
      customer_id: { type: "string" },
      status: { type: "string", enum: ["pending", "shipped", "delivered", "cancelled"] },
      since: { type: "string", description: "ISO date; omit for all time" },
    },
    required: ["customer_id"],
    additionalProperties: false,
  },
}
```

`enum`s do double duty: they constrain generation *and* document the domain. The
"at most 20, newest first" contract in the description is load-bearing — the model
plans around what it knows it will get back.

## Manage the token budget of observations

Tool results land in the [[ai/llms/context-window-and-kv-cache|context window]] and
stay there for the rest of the task. A 50K-token JSON response poisons every later
step ([[ai/llms/long-context-and-lost-in-the-middle|attention dilution]]) and
multiplies cost on each subsequent turn. Budget like a pager: cap list sizes,
truncate long fields with `…`, return ids + a fetch-more tool. Anthropic's rule of
thumb: if a human would scroll past it, the model shouldn't receive it.

## Iterate with evals, not vibes

Tool design is empirical. The loop that works: build a 20-task
[[ai/agents-and-tools/evaluating-agents|eval suite]] that exercises the tools → run →
read the transcripts where the agent picked wrong, flailed on errors, or drowned in
output → fix the *interface* → re-run. A surprisingly effective trick from
Anthropic's tool-writing guide: paste failing transcripts into Claude and ask it to
rewrite the tool descriptions — the model knows what models misread. Trace per-tool
call counts, error rates, and result sizes in
[[ai/mlops/llm-observability-and-tracing|observability]]; a tool with a 40% error
rate is an interface bug, not a model limitation.

## Failure modes

- **Exposing the internal API verbatim** — REST semantics, UUID soup, nested nulls.
  Design a deliberate surface; the agent is a *different client* with different needs.
- **Tool sprawl** — 40 tools "for completeness". Selection accuracy degrades;
  schemas eat context. Curate per agent role, or load schemas on demand (tool
  search / [[ai/agents-and-tools/model-context-protocol|MCP]] dynamic discovery).
- **Silent success** — a tool that returns `"ok"` with no state leaves the model
  guessing what changed; return the post-action state it needs for the next decision.
- **Asymmetric trust in results** — tool outputs can carry
  [[ai/ai-safety-and-security/indirect-prompt-injection|injected instructions]]
  (webpage content, ticket text); treat them as data, never as commands — a
  *boundary* concern the interface must own.

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/agent-failure-modes|failure modes]] ·
[[ai/prompt-engineering/structured-outputs|schemas]] ·
[[ai/ai-safety-and-security/indirect-prompt-injection|untrusted tool results]]

## Sources

- [Yang et al. 2024 — SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering (arXiv:2405.15793)](https://arxiv.org/abs/2405.15793) — the paper that named ACI and measured interface design beating model choice.
- [Anthropic — Writing effective tools for agents (2025)](https://www.anthropic.com/engineering/writing-tools-for-agents) — the practical checklist: consolidation, namespacing, token-efficient results, eval-driven iteration.
- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — appendix "Prompt engineering your tools" is the ACI section.
- [Anthropic docs — Tool use best practices](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — current API-level guidance (descriptions, `strict`, parallel calls).
