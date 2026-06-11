---
title: "Planning & decomposition"
description: For multi-step goals, agents break work into subtasks and sequence them. Plan-and-execute vs reactive looping, and why plans must stay revisable.
tags: [agents, planning, decomposition]
order: 5
updated: 2026-06-10
---
# Planning & decomposition

**Mental model:** a purely reactive agent decides each step from the last observation
— adaptive, but it loses the thread on ten-step goals. Planning adds a persistent,
*revisable* structure: break the goal into checkable subtasks, keep that structure
visible across turns, and update it when reality disagrees. A plan is a hypothesis,
not a contract; its value is direction plus the ability to *notice* a failed step.

## The research lineage (and what actually shipped)

- **Least-to-most prompting** (Zhou et al. 2022,
  [arXiv:2205.10625](https://arxiv.org/abs/2205.10625)) — decompose into subproblems,
  solve easiest-first, feed answers forward. The decomposition half of every modern
  planner.
- **Tree of Thoughts** (Yao et al. 2023,
  [arXiv:2305.10601](https://arxiv.org/abs/2305.10601)) — explore multiple reasoning
  branches with lookahead/backtracking. Influential idea, rarely deployed as-is: the
  token cost of exploring trees lost to better single-path models with
  [[ai/llms/reasoning-and-test-time-compute|test-time thinking]].
- **Reflexion** (Shinn et al. 2023,
  [arXiv:2303.11366](https://arxiv.org/abs/2303.11366)) — after a failed attempt,
  verbalize what went wrong and retry with that critique in context. Survives as the
  "re-plan on failure" step.

What shipped in 2026 production agents is humbler than any of these: **a todo list
the model maintains** (Claude Code's task list, Manus-style plan files) — write the
plan as an artifact, check items off, re-write when stuck. The artifact matters more
than the algorithm: it survives [[ai/agents-and-tools/agent-memory|context
compaction]], it re-anchors attention every turn (recency beats the
[[ai/llms/long-context-and-lost-in-the-middle|buried original instruction]]), and
humans can audit it.

## Plan-as-artifact (the pattern that works)

Give the agent a plan tool instead of asking it to "think step by step":

```typescript
const planTool: Anthropic.Tool = {
  name: "update_plan",
  description:
    "Maintain your task plan. Call FIRST on any multi-step task, and again whenever " +
    "a step completes or fails. Keep 3-7 steps, each independently checkable.",
  input_schema: {
    type: "object",
    properties: {
      steps: {
        type: "array",
        items: {
          type: "object",
          properties: {
            text: { type: "string" },
            status: { type: "string", enum: ["pending", "in_progress", "done", "failed"] },
          },
          required: ["text", "status"],
          additionalProperties: false,
        },
      },
    },
    required: ["steps"],
    additionalProperties: false,
  },
};
// Handler: persist the plan, and RETURN it as the tool result — so the current
// plan re-enters context at the end of every planning turn, where attention is strongest.
```

Two design choices doing the work: the plan **re-enters context on every update**
(fights goal drift), and statuses make progress **checkable** — a step stuck at
`in_progress` for five turns is a machine-detectable
[[ai/agents-and-tools/agent-failure-modes|stall signal]].

## Reactive vs plan-and-execute: decision rule

| Task shape | Stance |
|---|---|
| ≤3 steps, feedback-rich (a test suite to run) | plain [[ai/agents-and-tools/react-loop|ReAct]] — planning is overhead |
| 4–10 dependent steps, one agent | plan-as-artifact + reactive execution per step |
| Parallelizable subtasks | plan once, delegate to [[ai/agents-and-tools/multi-agent-systems|sub-agents]] |
| Structure knowable in advance | not an agent problem — [[ai/agents-and-tools/workflows-vs-agents|code the workflow]] |

And the meta-rule: **re-plan on contradiction, not on schedule.** Re-planning every
turn burns tokens re-deriving the same plan; never re-planning turns the plan into a
straitjacket. Trigger re-planning on events — a step failed, an observation
invalidates an assumption, the user changed the goal.

## Decomposition quality is testable

Good subtasks are (1) **independently checkable** — "make the test pass" not "improve
the code"; (2) **ordered by information gain** — do the step that resolves the most
uncertainty first (read the failing test before editing the source); (3) **scoped to
the agent's tools** — a plan step with no corresponding tool is a hallucination about
capability. When reviewing agent transcripts, bad plans are visible: vague steps,
no verification steps, plans that never change despite failures.

## Cost & latency lens

Planning is cheap insurance: one extra tool call per re-plan (~hundreds of tokens)
against the cost of a wandering agent (thousands of tokens per wasted turn). The
expensive anti-pattern is *elaborate upfront* planning — a 2,000-token plan for a
3-step task, or [[ai/llms/reasoning-and-test-time-compute|deep thinking]] spent
producing structure the task didn't need. Match planning depth to horizon; on short
tasks, skip it entirely.

## Failure modes

- **Plan theater** — beautiful plan, then the agent ignores it. Fix: the plan re-enters
  context via tool results (above), and the system prompt ties actions to the current
  `in_progress` step.
- **Rigid adherence** — executing step 4 after step 2's failure invalidated it. Fix:
  failure status forces re-plan before proceeding.
- **Over-decomposition** — 14 micro-steps for a rename; each step pays loop overhead.
  3–7 steps is the working band.
- **Plans without verification steps** — every plan should end with "verify the
  outcome" or the agent [[ai/agents-and-tools/agent-failure-modes|declares success
  unverified]].

**Connects to:** [[ai/agents-and-tools/react-loop|ReAct]] ·
[[ai/agents-and-tools/multi-agent-systems|delegation]] ·
[[ai/llms/reasoning-and-test-time-compute|reasoning models]] ·
[[ai/prompt-engineering/task-decomposition|prompt-level decomposition]]

## Sources

- [Zhou et al. 2022 — Least-to-Most Prompting (arXiv:2205.10625)](https://arxiv.org/abs/2205.10625) — decomposition as an explicit prompting strategy; the foundation.
- [Yao et al. 2023 — Tree of Thoughts (arXiv:2305.10601)](https://arxiv.org/abs/2305.10601) — search over reasoning branches; read to understand why it mostly didn't ship.
- [Shinn et al. 2023 — Reflexion (arXiv:2303.11366)](https://arxiv.org/abs/2303.11366) — verbal self-critique driving re-planning.
- [Anthropic — Effective context engineering for AI agents (2025)](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — covers plans/todo lists as persistent context artifacts and attention re-anchoring.
- [Lilian Weng — LLM-Powered Autonomous Agents (2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — the planning/memory/tools framing this branch inherits.
