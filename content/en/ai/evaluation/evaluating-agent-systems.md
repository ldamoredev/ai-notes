---
title: "Evaluating agent systems"
description: Agent evals must score the final outcome, the trajectory, tool use, cost, safety, and recovery from failed steps.
tags: [evaluation, agents, trajectories, tools]
order: 12
updated: 2026-06-07
---
# Evaluating agent systems

Agents are evaluated by what they accomplish and how they get there. A final answer can
look correct while the trajectory was expensive, unsafe, brittle, or dependent on luck.

## What to score

- Outcome success: did the external task finish correctly?
- Trajectory quality: did the agent take a reasonable path?
- Tool selection: did it choose the right tools at the right time?
- Tool arguments: were calls valid, minimal, and authorized?
- Recovery: did it handle missing data, errors, and tool failures?
- Efficiency: steps, latency, tokens, retries, and cost.
- Safety: permissions, approvals, data exposure, and escalation behavior.

## Evaluation artifacts

| Artifact | Why it matters |
|---|---|
| Task suite | representative goals with checkable end states |
| Trace | every model call, tool call, observation, and decision |
| Tool schema tests | catches invalid or risky tool arguments |
| Human review | inspects autonomy and judgment on ambiguous runs |
| Repeated runs | estimates reliability under non-determinism |

## Agent-specific metrics

- Pass rate over repeated runs.
- Average steps to success.
- Tool-call error rate.
- Unauthorized-action attempts.
- Human approval rate and escalation correctness.
- Cost per successful task, not just cost per run.

## Pitfall

Single-run demos hide agent reliability. Evaluate distributions over repeated runs and
trace the path, especially when tools can create side effects.

**Connects to:** [[ai/agents-and-tools/evaluating-agents|agent evaluation]] ·
[[ai/agents-and-tools/agent-failure-modes|agent failure modes]] ·
[[ai/agents-and-tools/autonomy-and-control|autonomy and control]]
