---
title: "The Model Context Protocol (MCP)"
description: MCP is an open standard for connecting models to tools and data — "USB-C for AI". What it standardizes and why it matters for agent ecosystems.
tags: [agents, mcp, tools, integration]
order: 8
updated: 2026-06-10
---
# The Model Context Protocol (MCP)

**Mental model:** before MCP, connecting M apps to N tool providers meant M×N bespoke
integrations. MCP (Anthropic, open-sourced **November 2024**; adopted by OpenAI and
Google DeepMind in spring 2025) standardizes the wire between them: a tool provider
ships one MCP **server**, any MCP **client** (Claude, IDEs, your agent) can use it —
M+N instead of M×N. "USB-C for AI" is the right analogy with the right caveat: USB-C
also standardized a new place for attacks to plug in.

## The protocol, concretely

JSON-RPC 2.0 over two transports: **stdio** (local child process) and **streamable
HTTP** (remote). Versioned by date; the current spec revision is **2025-11-25**
(lineage: 2024-11-05 initial → 2025-03-26 streamable HTTP + OAuth → 2025-06-18
elicitation, structured tool outputs, OAuth resource-server model → 2025-11-25),
governed via SEPs and working groups at
[modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-11-25).

Server-side primitives:

| Primitive | What it is | Maps to |
|---|---|---|
| **Tools** | model-invocable actions with JSON Schema | [[ai/agents-and-tools/tool-calling|tool calling]], standardized |
| **Resources** | readable data (files, records) addressed by URI | context the host can load |
| **Prompts** | reusable, parameterized prompt templates | slash-commands / canned workflows |

Client-side primitives flow the other way: **sampling** (server asks the client's LLM
to complete something — keeps the server model-agnostic and keeps API keys with the
client), **elicitation** (server asks the human for input mid-operation), **roots**
(client tells the server which directories are in scope).

## A working server (TypeScript SDK)

```typescript
// npm i @modelcontextprotocol/sdk zod
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "invoices", version: "1.0.0" });

server.registerTool(
  "get_invoice",
  {
    description:
      "Fetch one invoice by id (inv_<digits>). Use for questions about a specific " +
      "invoice's amount, status, or due date.",
    inputSchema: { id: z.string().regex(/^inv_\d+$/) },
  },
  async ({ id }) => {
    const inv = await db.query.invoices.findFirst({ where: eq(invoices.id, id) });
    if (!inv) return { content: [{ type: "text", text: `No invoice ${id}.` }], isError: true };
    return { content: [{ type: "text", text: JSON.stringify(inv) }] };
  },
);

await server.connect(new StdioServerTransport());
```

Everything in [[ai/agents-and-tools/agent-computer-interface|ACI design]] applies
unchanged — MCP standardizes the *plumbing*, not the *quality* of your tool surface.
A badly-described MCP tool fails exactly like a badly-described native tool.

## When MCP, when native tools (decision rule)

- **Native tool definitions** when you own both sides — your agent calling your
  database needs no protocol layer; it's less moving parts and one less trust
  boundary.
- **MCP server** when the capability has **many consumers** (your invoice tools used
  by Claude Desktop, the support agent, and an IDE), or you consume **third-party**
  capabilities (GitHub, Sentry, Postgres servers already exist).
- **MCP client in your product** when users should plug in *their own* integrations —
  the ecosystem play.

The trap is resume-driven protocol adoption: wrapping your single-consumer internal
API in MCP adds a server process, version negotiation, and a trust boundary for zero
reuse benefit.

## Security: the same risks, concentrated at a new boundary

MCP doesn't create new attack *classes* — it industrializes existing ones
([[ai/ai-safety-and-security/indirect-prompt-injection|indirect prompt injection]],
[[ai/ai-safety-and-security/excessive-agency|excessive agency]]) by making
capabilities pluggable:

- **Malicious/compromised servers** — a server's tool descriptions enter your prompt
  (tool-description injection) and its results enter your context. Vet and pin
  servers like dependencies; prefer official ones.
- **The lethal trifecta** (Simon Willison, 2025): an agent with (1) access to private
  data, (2) exposure to untrusted content, and (3) an exfiltration channel is
  exploitable *by construction* — and casually stacking MCP servers is the easiest
  way to assemble all three without noticing. Audit the *combination*, not each
  server alone.
- **OAuth/credential scope** — remote servers act with delegated credentials; scope
  them per-server, per-tenant, least-privilege
  ([[ai/agents-and-tools/autonomy-and-control|autonomy & control]]).
- **Confused deputy** — the server executes with *its* privileges what the model
  asked with *user* intent mixed with injected text; gate state-changing MCP tools
  behind [[ai/agents-and-tools/guardrails-and-human-in-the-loop|approval]] like any
  other tool.

## Production lens

Each connected server adds startup latency (process spawn / connection + `list_tools`
round-trip), context cost (every exposed tool's schema rides in your prompt — a
10-server setup can burn thousands of tokens before the first user message), and an
availability dependency. Mitigations: expose only needed tools per agent role, lazy
tool discovery, cache tool lists, and trace MCP calls as spans like any tool call.
And pin server versions — a server silently updating its tool descriptions is a
prompt change you didn't review
([[ai/evaluation/prompt-regression-testing|regression-test]] against it).

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/agent-computer-interface|tool design]] ·
[[ai/ai-safety-and-security/indirect-prompt-injection|injection at the boundary]] ·
[[ai/agents-and-tools/autonomy-and-control|least privilege]]

## Sources

- [MCP specification (2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25) — the authoritative spec: primitives, transports, lifecycle, authorization.
- [Anthropic — Introducing the Model Context Protocol (Nov 2024)](https://www.anthropic.com/news/model-context-protocol) — the launch framing and the M×N problem statement.
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk) — the reference implementation the server example above uses.
- [Simon Willison — The lethal trifecta (2025)](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/) — the clearest security mental model for agent+MCP deployments.
- [MCP blog — 2026 roadmap](https://blog.modelcontextprotocol.io/posts/2026-mcp-roadmap/) — where the protocol is heading (statelessness, async tasks); useful before building deep on current shapes.
