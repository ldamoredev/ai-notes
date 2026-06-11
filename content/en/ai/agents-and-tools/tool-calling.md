---
title: "Tool & function calling"
description: Tool calling is how an LLM acts — it emits a structured call, your code runs it, the result goes back. The mechanism behind every agent.
tags: [agents, tool-calling, function-calling]
order: 2
updated: 2026-06-10
---
# Tool & function calling

**Mental model:** the model never executes anything. It emits a **structured request**
("call `get_invoice` with `{id: "inv_42"}`"), your code executes it and returns the
result, and the model continues with that observation in context. Execution,
permissions, and safety live entirely on your side of that boundary — which is the
whole security story, and why
[[ai/agents-and-tools/autonomy-and-control|least privilege]] is an engineering
property, not a prompt.

## The wire protocol (Anthropic Messages API)

1. Request includes `tools`: name, description, and a JSON Schema `input_schema`.
2. If the model decides to act, the response has `stop_reason: "tool_use"` and one or
   more `tool_use` content blocks (`id`, `name`, parsed `input`).
3. You execute, then append the assistant turn *verbatim* plus a user turn containing
   `tool_result` blocks whose `tool_use_id` matches. Errors go back as
   `is_error: true` with a message the model can act on.
4. Repeat until `stop_reason: "end_turn"`.

The reliability comes from the same constrained-decoding machinery as
[[ai/prompt-engineering/structured-outputs|structured outputs]] — with
`strict: true` (Anthropic, GA 2025) the arguments are *guaranteed* schema-valid, so
"the model said something" becomes "a typed invocation my system can run." Models are
trained specifically for this; the conceptual ancestor is Toolformer (Schick et al.
2023, [arXiv:2302.04761](https://arxiv.org/abs/2302.04761)).

## A complete, typed loop (TypeScript)

```typescript
import Anthropic from "@anthropic-ai/sdk";
const anthropic = new Anthropic();

const tools: Anthropic.Tool[] = [{
  name: "get_invoice",
  description:
    "Fetch one invoice by its id (format inv_<digits>). Use when the user asks " +
    "about a specific invoice's amount, status, or due date.",
  input_schema: {
    type: "object",
    properties: { id: { type: "string", description: "Invoice id, e.g. inv_42" } },
    required: ["id"],
    additionalProperties: false,
  },
  strict: true, // API-enforced: input will match the schema exactly
}];

async function execute(name: string, input: unknown): Promise<{ ok: boolean; body: string }> {
  try {
    if (name === "get_invoice") {
      const { id } = input as { id: string };
      const inv = await db.query.invoices.findFirst({ where: eq(invoices.id, id) });
      if (!inv) return { ok: false, body: `No invoice ${id}. Valid ids look like inv_42.` };
      return { ok: true, body: JSON.stringify({ id: inv.id, total: inv.total, status: inv.status }) };
    }
    return { ok: false, body: `Unknown tool ${name}` };
  } catch (e) {
    return { ok: false, body: `Tool failed: ${(e as Error).message}. Retry or tell the user.` };
  }
}

export async function run(question: string): Promise<string> {
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: question }];
  for (let turn = 0; turn < 10; turn++) {           // hard cap — non-negotiable
    const res = await anthropic.messages.create({
      model: "claude-opus-4-8", max_tokens: 2048, tools, messages,
    });
    if (res.stop_reason !== "tool_use") {
      return res.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    }
    messages.push({ role: "assistant", content: res.content }); // verbatim, incl. thinking
    const results: Anthropic.ToolResultBlockParam[] = [];
    for (const block of res.content) {
      if (block.type !== "tool_use") continue;
      const { ok, body } = await execute(block.name, block.input);
      results.push({ type: "tool_result", tool_use_id: block.id, content: body, is_error: !ok });
    }
    messages.push({ role: "user", content: results });
  }
  throw new Error("tool loop exceeded 10 turns");
}
```

Load-bearing details people get wrong: append `res.content` **unmodified** (dropping
blocks breaks the protocol and the prompt cache); answer **every** `tool_use` block —
the model can emit several in one turn (parallel tool use); put all results in **one**
user message; and make error strings *instructions* ("valid ids look like inv_42"),
because the model will read them and self-correct —
[[ai/agents-and-tools/agent-computer-interface|errors are part of the interface]].

## Doing it well

- **The description is a prompt.** State what the tool does, *when to call it*, and
  what it returns. Current Opus-class models reach for tools more conservatively than
  2024 models; prescriptive "use when..." trigger conditions in the description
  measurably lift call rates.
- **Few, non-overlapping tools** beat many. Overlap (`search_docs` vs `query_kb`)
  causes mis-selection; consolidate.
- **`tool_choice`** gives you control when you need it: `auto` (default), `any`
  (must call something), `{type: "tool", name}` (forced — useful to make a workflow
  step deterministic).
- **Concise results.** Tool output lands in the
  [[ai/prompt-engineering/managing-the-context-window|context window]]; a 50KB JSON
  dump costs tokens and attention on every subsequent turn. Return what the model
  needs, with ids it can expand on demand.

## Cost & latency lens

Every tool round-trip is a full model call over the **entire accumulated
conversation** — input tokens grow roughly quadratically with turn count. Defenses:
prompt caching (Anthropic cache hits ~0.1× input price — keep `tools` and `system`
byte-stable, append-only messages), small models for tool-heavy/low-reasoning steps,
and trace per-turn token counts in
[[ai/mlops/llm-observability-and-tracing|Langfuse/OTel]] so cost regressions are
visible per tool, not per month.

## Failure modes

- **Schema-valid, semantically wrong args** — `strict` guarantees shape, not sense
  (`id: "inv_42"` may not exist). Validate semantics in the tool; return actionable
  errors.
- **Hallucinated tool names** — emerge when descriptions overlap or the tool list is
  huge; the fix is curation, not scolding.
- **Lost `tool_use_id` pairing** — mismatched ids hard-fail the API call; always
  thread `block.id` through.
- **Unbounded loops** — a model that keeps calling tools forever is a billing
  incident; the cap in the code above is the floor, not the ceiling, of
  [[ai/agents-and-tools/agent-failure-modes|loop defenses]].

**Connects to:** [[ai/prompt-engineering/structured-outputs|structured output]] ·
[[ai/agents-and-tools/agent-computer-interface|tool design]] ·
[[ai/agents-and-tools/react-loop|the loop]] ·
[[ai/agents-and-tools/model-context-protocol|MCP]]

## Sources

- [Anthropic docs — Tool use overview](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — the authoritative wire protocol: blocks, `tool_choice`, parallel calls, `strict`.
- [Anthropic — Writing effective tools for agents (2025)](https://www.anthropic.com/engineering/writing-tools-for-agents) — measured guidance on descriptions, consolidation, and token-efficient results.
- [Schick et al. 2023 — Toolformer (arXiv:2302.04761)](https://arxiv.org/abs/2302.04761) — the research origin of models teaching themselves API calls.
- [Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) — the standard eval for tool-call correctness across models; useful when picking a model for tool-heavy work.
- [Anthropic docs — Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — the `strict: true` guarantee tool calling inherits.
