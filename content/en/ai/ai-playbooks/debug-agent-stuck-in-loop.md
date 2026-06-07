---
title: "Debug an agent stuck in a loop"
description: A practical procedure for diagnosing agent loops caused by unclear goals, bad tool feedback, weak state, missing stop rules, or excessive autonomy.
tags: [playbook, agents, debugging]
order: 3
updated: 2026-06-07
---
# Debug an agent stuck in a loop

Use this playbook when an agent repeats the same tool call, retries without progress,
oscillates between plans, or burns tokens without reaching a terminal state.

## Inputs

- Full trace with prompts, tool calls, observations, errors, and final state.
- Agent goal, tool list, stop criteria, retry policy, and budget limits.
- Expected successful trajectory for at least one comparable task.

## Procedure

1. Identify the repeated loop segment in the trace.
2. Classify the loop trigger: unclear goal, invalid tool args, missing observation, bad memory, impossible task, or weak stop rule.
3. Check whether the tool returned actionable feedback or only a generic failure.
4. Check whether the agent state changes after each iteration.
5. Add or tighten termination criteria: max steps, max retries per tool, no-progress detector, or confidence threshold.
6. Improve tool errors so the agent receives specific recovery information.
7. Reduce tool access if the agent is exploring irrelevant options.
8. Re-run the task suite multiple times and compare pass rate, steps, cost, and failure type.

## Fix patterns

| Symptom | Likely fix |
|---|---|
| Same invalid call repeats | validate args before execution and return exact error |
| Agent keeps planning | require a next action or final answer after N steps |
| Tool result ignored | shorten observation and make success/failure explicit |
| Task impossible | add refusal or escalation path |

## Pitfall

Do not only raise the step limit. A higher limit turns a loop into a more expensive
loop unless the agent receives new state, better feedback, or a stopping rule.

**Connects to:** [[ai/agents-and-tools/agent-failure-modes|agent failure modes]] ·
[[ai/agents-and-tools/react-loop|ReAct loop]] ·
[[ai/evaluation/evaluating-agent-systems|evaluating agent systems]]
