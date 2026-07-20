---
title: "Designing the agent-tool interface"
description: An Agent-Computer Interface turns model proposals into bounded, observable actions; names, schemas, results, and errors are part of the control system.
tags: [agents, tool-design, interface]
order: 3
updated: 2026-07-20
kind: implementation
level: intermediate
status: current
prerequisites: [ai/agents-and-tools/tool-calling, ai/prompt-engineering/structured-outputs]
last_verified: 2026-07-20
---
# Designing the agent-tool interface

**Mental model:** a tool is not an internal endpoint exposed to an LLM. It is an
**Agent-Computer Interface (ACI)**: a deliberately small language through which an
untrusted planner observes state and proposes changes. The interface determines what
the model can select, what it can misunderstand, and what evidence reaches its next
turn. Model quality cannot repair an ambiguous verb, an unbounded response, or a
silent mutation.

## The contract: intent → validated action → useful observation

Every tool needs four parts: a distinct verb, a narrow input schema, deterministic
server-side validation, and a bounded result that names the new state. Consider an
order assistant. `query(q)` leaks database vocabulary; `search_customer_orders`
states the object, operation, and return budget.

```json
{
  "name": "search_customer_orders",
  "description": "Find at most 20 newest orders for one customer. Use for status, history, or totals; use get_order_details for line items.",
  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {"type": "string"},
      "status": {"type": "string", "enum": ["pending", "shipped", "delivered", "cancelled"]},
      "since": {"type": "string", "description": "ISO-8601 date"}
    },
    "required": ["customer_id"],
    "additionalProperties": false
  }
}
```

The schema is necessary but insufficient: validate tenant ownership, policy, and
semantic constraints after parsing. An error is also an observation. Return
`"since must be YYYY-MM-DD; received 3/5/26; example 2026-03-05"`, not `400`.

## Numerical walkthrough: observation is a budget

If a task takes eight turns and a tool dumps 4,000 tokens each time, later prompts
carry roughly 32,000 observation tokens before instructions and reasoning. Returning
20 rows × 80 tokens plus a summary costs about 1,700 instead. That 19× difference
affects latency, cost, and whether earlier constraints remain salient. Use pagination,
field projection, stable ordering, and a follow-up detail tool; never make the model
reconstruct meaning from opaque IDs.

## Executable contract test

Run this with `python3` to test the boundary before involving a model. Expected:
`rejected: unknown field: limit` and one valid request.

```python
allowed = {"customer_id", "status", "since"}
def validate(payload):
    extra = set(payload) - allowed
    if extra: raise ValueError(f"unknown field: {sorted(extra)[0]}")
    if not payload.get("customer_id"): raise ValueError("customer_id is required")
    return {"ok": True, "returned": min(20, 20), "order": "newest-first"}

try: validate({"customer_id": "c_7", "limit": 500})
except ValueError as err: print("rejected:", err)
print(validate({"customer_id": "c_7", "status": "shipped"}))
```

## What frameworks hide

Function-calling APIs validate JSON shape, not whether a refund belongs to the tenant,
whether an ID exists, whether an action is reversible, or whether the returned record
contains hostile instructions. Keep those checks in deterministic code. Treat every
tool result as untrusted data; presentation text from a ticket or web page never
authorizes a subsequent action.

## Failure modes and decision rule

- **Overlapping tools:** the model chooses among synonyms. Merge them or give each a
  unique trigger condition.
- **Unbounded results:** context fills with logs or JSON. Cap lists and offer detail
  retrieval.
- **Silent writes:** the next turn guesses whether a mutation happened. Return an ID,
  version, and relevant post-state.
- **Internal-API mirroring:** UUIDs, null-heavy objects, and transport errors leak
  implementation rather than task semantics.

If two tools could plausibly serve the same user sentence, redesign the surface before
tuning the prompt. Measure selection accuracy, validation-error rate, result tokens,
and successful end state on a fixed task suite.

## Exercises

1. Add an ISO-date check to the artifact and a failing test for `2026-2-3`.
2. Rewrite a raw `POST /v1/refund` endpoint as a proposed action plus an approval
   boundary; name the irreversible state change explicitly.

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] · [[ai/agents-and-tools/evaluating-agents|agent evaluation]] · [[ai/agents-and-tools/agent-failure-modes|failure modes]] · [[ai/ai-safety-and-security/indirect-prompt-injection|untrusted observations]]

## Sources

- [SWE-agent](https://arxiv.org/abs/2405.15793) — introduces the ACI framing and demonstrates the effect of interface design on software-agent performance.
- [Anthropic: Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) — operational guidance on descriptions, consolidation, schemas, and result design.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25) — protocol-level contracts for tools, resources, and model-facing servers.
- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — why tool inputs and outputs are security boundaries, not merely UX.
