---
title: "Agent memory"
description: An agent loop fills the context fast. Working memory, persistent memory, and externalizing state so a long-running agent doesn't drown in its own history.
tags: [agents, memory, context-engineering]
order: 6
updated: 2026-06-10
---
# Agent memory

**Mental model:** every [[ai/agents-and-tools/react-loop|loop turn]] appends thought +
action + observation to a finite [[ai/llms/context-window-and-kv-cache|context
window]], and quality degrades well before the window fills (Chroma's 2025 *context
rot* result). "Memory" for an agent is therefore an engineering decision — **what
state to keep in context, what to externalize, and how to bring it back** — not a
feature you bolt on. The architecture blueprint is MemGPT (Packer et al. 2023,
[arXiv:2310.08560](https://arxiv.org/abs/2310.08560)): treat the context like RAM and
external storage like disk, with the LLM paging data in and out via tools — an OS
memory hierarchy for agents.

## The layers

| Layer | Lives | Survives | Mechanism |
|---|---|---|---|
| Working memory | in context | this task, until compaction | recent turns, current plan, active observations |
| Compacted history | in context | the task | summary replacing old turns |
| Task scratchpad | filesystem/DB | the task + audits | notes/plan files the agent reads & writes |
| Persistent memory | filesystem/DB/[[ai/rag-and-retrieval/index|vector store]] | across sessions | facts, preferences, learned procedures |

## Compaction: surviving long tasks

When context approaches budget, replace the oldest turns with a structured summary
and keep recent turns verbatim. What the summary must preserve (learned the hard way
by every agent team): **decisions made and why, current plan state, unresolved
errors, exact identifiers** (paths, ids, URLs — paraphrasing these breaks later
steps). Anthropic ships this server-side as **context compaction** (beta 2026) and
client-side in Claude Code's auto-compact; the same shape hand-rolled:

```typescript
async function compact(messages: Anthropic.MessageParam[]): Promise<Anthropic.MessageParam[]> {
  const keep = messages.slice(-8); // recent turns stay verbatim
  const old = messages.slice(0, -8);
  if (old.length === 0) return messages;
  const res = await anthropic.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 1500,
    system:
      "Summarize this agent transcript for the agent to continue from. Preserve: " +
      "decisions + rationale; current plan and step statuses; unresolved errors; " +
      "ALL file paths, ids, and URLs verbatim. Omit pleasantries and dead ends.",
    messages: [{ role: "user", content: JSON.stringify(old) }],
  });
  const summary = res.content.filter((b) => b.type === "text").map((b) => b.text).join("");
  return [{ role: "user", content: `<compacted_history>\n${summary}\n</compacted_history>` }, ...keep];
}
```

Caveat that matters: compaction **invalidates the prompt cache** (the prefix
changes), so each compaction pays one full-price write — compact rarely and in big
steps, not every turn.

## Externalize state: the file-based pattern

The 2025–26 convergence (MemGPT → Claude Code's `CLAUDE.md` + memory directory →
Anthropic's **memory tool**, `memory_20250818`) is that *files beat exotic memory
stores* for agent state: a scratchpad the agent writes findings to, a plan file, a
notes directory it greps. Files are inspectable, diffable, survive process restarts,
and the agent already has the tools to use them. Anthropic's memory tool is exactly
this with a standard interface — the model emits `view/create/str_replace/delete`
commands against a `/memories` directory **you** store and serve back.

The complementary trick: **retrieve, don't accumulate.** Store large artifacts
(fetched pages, query results) outside context, keep only ids/paths in working
memory, and re-fetch the specific piece a later step needs — the
[[ai/rag-and-retrieval/why-rag|RAG move]] applied to the agent's own outputs.

## Cross-session memory (the hard one)

Persistent memory across sessions ("the user prefers Fastify", "deploys go through
staging") is where ambition outruns reliability. Working approaches, in order of
trustworthiness: **explicit memory files** the agent curates (auditable, editable);
**structured records** keyed by entity; **vector retrieval over past episodes**
(fuzzy, ranking problems). The failure pattern to design against is *unbounded
accumulation*: stale facts crowd out current ones, and a wrong memory is worse than
none — memory needs an *update/delete* story
(supersede-on-conflict, timestamps, periodic consolidation), or it rots. Voyager
(Wang et al. 2023, [arXiv:2305.16291](https://arxiv.org/abs/2305.16291)) showed the
aspirational version — a growing, reusable skill library — in a domain (Minecraft)
with perfect verifiability; most products are not there.

## Cost & latency lens

Memory engineering *is* cost engineering: context tokens are paid every turn, so a
10K-token stale history at turn 30 has been paid ~30 times. Compaction trades one
summary call against that recurring rent. Sub-agent scoping
([[ai/agents-and-tools/multi-agent-systems|clean context per subtask]]) is memory
management by architecture. Watch two metrics in
[[ai/mlops/llm-observability-and-tracing|traces]]: input tokens per turn (sawtooth =
compaction working; monotonic climb = it isn't) and cache hit rate (collapses if you
edit history instead of appending).

## Failure modes

- **Over-compression** — the summary drops the one detail step 19 needs (an error
  string, a flag). Mitigate: preserve identifiers verbatim; keep artifacts
  re-fetchable instead of relying on the summary.
- **Stale memory poisoning** — last month's "API uses v1" memory overrides today's
  reality; memories need recency/supersession semantics.
- **Memory as hoarding** — remember-everything vector stores that retrieve noise;
  curated small memory beats exhaustive fuzzy memory.
- **Secrets in memory files** — memory persists and gets re-injected into prompts;
  never let credentials or [[ai/ai-safety-and-security/data-and-pii-leakage|PII]]
  into it.

**Connects to:** [[ai/prompt-engineering/memory-and-history|prompt memory]] ·
[[ai/rag-and-retrieval/index|retrieval memory]] ·
[[ai/llms/long-context-and-lost-in-the-middle|context rot]] ·
[[ai/agents-and-tools/planning-and-decomposition|plan artifacts]]

## Sources

- [Packer et al. 2023 — MemGPT (arXiv:2310.08560)](https://arxiv.org/abs/2310.08560) — the OS-memory-hierarchy framing; the architecture most agent memory descends from.
- [Anthropic docs — Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) — the standardized file-based memory interface (`memory_20250818`) and its command set.
- [Anthropic — Effective context engineering for AI agents (2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — compaction, scratchpads, and just-in-time retrieval as one discipline.
- [Chroma — Context Rot (2025)](https://research.trychroma.com/context-rot) — why "it fits in the window" is not the bar; degradation starts early.
- [Wang et al. 2023 — Voyager (arXiv:2305.16291)](https://arxiv.org/abs/2305.16291) — skill-library memory in a verifiable domain; the ceiling to aim at, and why it's hard elsewhere.
