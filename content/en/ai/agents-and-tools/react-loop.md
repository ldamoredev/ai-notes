---
title: "The ReAct loop: reason + act"
description: The core agent pattern — think, call a tool, observe the result, repeat until done. Why interleaving reasoning and action works.
tags: [agents, react, agent-loop, reasoning]
order: 4
updated: 2026-06-10
---
# The ReAct loop: reason + act

**Mental model:** strip any agent to its skeleton and you find one loop — **reason
about the goal and current state, take an action (a
[[ai/agents-and-tools/tool-calling|tool call]]), observe the result, repeat** until
done. This is **ReAct** (Yao et al. 2022,
[arXiv:2210.03629](https://arxiv.org/abs/2210.03629)). The paper's insight is that
*interleaving* reasoning traces with actions beats either alone: reasoning grounds the
next action in the latest evidence; observations ground the reasoning in reality.

## From paper to production (what changed)

The original ReAct was a *prompting pattern*: few-shot examples teaching the model to
emit `Thought: / Action: / Observation:` text that a parser executed. In 2026 the
pattern is *native*: models are trained for tool use, "Thought" is the model's
[[ai/llms/reasoning-and-test-time-compute|extended/adaptive thinking]], "Action" is a
structured `tool_use` block, and the loop is ~30 lines around the API. The conceptual
structure survived; the brittle text parsing did not.

```typescript
export async function agentLoop(task: string, opts = { maxTurns: 15, maxTokens: 150_000 }) {
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: task }];
  let spent = 0;

  for (let turn = 0; turn < opts.maxTurns; turn++) {
    const res = await anthropic.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096,
      thinking: { type: "adaptive" },   // the "Reason" half, handled by the model
      system: SYSTEM,                    // goal framing + stop criteria live here
      tools,
      messages,
    });
    spent += res.usage.input_tokens + res.usage.output_tokens;
    if (spent > opts.maxTokens) throw new AgentBudgetError(messages);

    if (res.stop_reason !== "tool_use") {
      return res.content.filter((b) => b.type === "text").map((b) => b.text).join("");
    }
    messages.push({ role: "assistant", content: res.content });
    messages.push({ role: "user", content: await executeAll(res.content) }); // the "Observe" half
  }
  throw new AgentTurnLimitError(messages); // surface the trace, don't swallow it
}
```

Three things make this production-shaped rather than demo-shaped: a **turn cap**, a
**token budget**, and errors that **carry the trace** (you will need it —
[[ai/agents-and-tools/agent-failure-modes|debugging is trace reading]]).

## Why interleaving beats plan-then-execute alone

Pure upfront planning is brittle — the world rarely matches the plan (the file isn't
where the plan assumed; the API returns an error the plan didn't anticipate). Pure
acting is blind — without a reasoning step, the model pattern-matches its way into
repeated failing actions. ReAct's per-step adaptation is why it became the default;
[[ai/agents-and-tools/planning-and-decomposition|planning]] survives as a layer *on
top* of the loop (a revisable todo list), not a replacement for it.

The empirical caveat from the original paper still holds: ReAct's gains come mostly
from **grounding** (fewer hallucinated facts, because the model checks), at some cost
in flexibility — the model can over-anchor on an uninformative observation. Reflexion
(Shinn et al. 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)) adds
verbal self-critique between attempts; modern models do a weaker version of this
natively inside their thinking blocks.

## What makes the loop work or fail

- **Observation quality is everything.** The model decides the next step from what
  the tool returned — noisy, huge, or silent results derail the loop
  ([[ai/agents-and-tools/agent-computer-interface|ACI design]]).
- **Stop criteria must be explicit.** Tell the model in the system prompt what "done"
  looks like ("when the test passes, reply with SUMMARY: ..."), and enforce caps in
  code. A loop with neither runs until the budget does.
- **Context grows every turn** — thought + action + observation, accumulated. Past
  ~20 turns, [[ai/agents-and-tools/agent-memory|memory management]] (compaction,
  external scratchpads) stops being optional.
- **Verification closes the loop.** The strongest agents end with a checking action
  (run the tests, re-fetch the record) rather than trusting their own claim of
  success — cheap insurance against
  [[ai/agents-and-tools/agent-failure-modes|false-victory declarations]].

## Cost & latency lens

Each turn re-sends the whole accumulated conversation: token spend grows roughly
quadratically in turn count, and per-task agent usage runs ~4× a chat interaction on
Anthropic's production numbers. Defenses: **prompt caching** (append-only messages +
byte-stable `system`/`tools` make every prior turn a ~0.1× cache read), **a small
model for mechanical turns** if you route, and **per-turn token telemetry** in
[[ai/mlops/llm-observability-and-tracing|tracing]] — the loop is one span per turn,
with tool spans nested, or you're blind. Latency is `turns × (model latency + tool
latency)`; the lever is fewer/parallel tool calls per turn, not faster prose.

## Failure modes

- **Repetition loops** — same action, same failing result, again. Detect
  programmatically (hash recent actions; two identical consecutive calls → inject a
  "this exact call already failed, change approach" message or abort).
- **Unbounded cost** — the cap-less loop is a billing incident in waiting.
- **Context rot at long horizons** — quality decays as the window fills with stale
  observations; see [[ai/agents-and-tools/agent-memory|agent memory]].
- **Anchoring on a bad observation** — one misleading tool result steers everything
  after; actionable errors and verification steps are the antidote.

**Connects to:** [[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/agents-and-tools/planning-and-decomposition|planning]] ·
[[ai/agents-and-tools/agent-failure-modes|loops]] ·
[[ai/agents-and-tools/agent-memory|context management]]

## Sources

- [Yao et al. 2022 — ReAct: Synergizing Reasoning and Acting (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) — the pattern's origin; §4's error analysis (grounding vs reasoning failures) is still the best taxonomy.
- [Shinn et al. 2023 — Reflexion (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) — self-critique between attempts; the ancestor of modern verify-then-retry loops.
- [Anthropic — Building Effective Agents (Dec 2024)](https://www.anthropic.com/engineering/building-effective-agents) — defines the agent as "LLM using tools in a loop based on environmental feedback" and the stop-condition discipline.
- [Anthropic docs — Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) — the API mechanics the modern loop is built on.
- [Lilian Weng — LLM-Powered Autonomous Agents (2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — the survey that placed ReAct among planning/memory/tools; dated on specifics, still the cleanest map.
