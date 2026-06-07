---
title: Agents and Tools
description: LLMs that act — tool calling, the agent loop, planning, memory, multi-agent systems, MCP, and the guardrails that keep autonomy safe.
tags: [agents, tools]
order: 0
updated: 2026-06-07
---
# Agents and Tools

An **agent** is an [[ai/llms/index|LLM]] that runs in a loop, using **tools** to act on
the world and deciding its own next step until a task is done. That autonomy is powerful
and risky — so the discipline here is as much about *control* as capability.

> Anthropic's core advice: **don't build an agent if a [[ai/prompt-engineering/task-decomposition|workflow]]
> will do.** Start simple, add autonomy only when the steps genuinely can't be
> predetermined, and keep the system transparent.

## The basics

- [[ai/agents-and-tools/workflows-vs-agents|Workflows vs agents: when to use which]]
- [[ai/agents-and-tools/tool-calling|Tool & function calling]]
- [[ai/agents-and-tools/agent-computer-interface|Designing the agent-tool interface]]
- [[ai/agents-and-tools/model-context-protocol|The Model Context Protocol (MCP)]]

## How agents work

- [[ai/agents-and-tools/react-loop|The ReAct loop: reason + act]]
- [[ai/agents-and-tools/planning-and-decomposition|Planning & decomposition]]
- [[ai/agents-and-tools/agent-memory|Agent memory]]
- [[ai/agents-and-tools/multi-agent-systems|Multi-agent systems & handoffs]]

## Keeping them safe & working

- [[ai/agents-and-tools/guardrails-and-human-in-the-loop|Guardrails & human-in-the-loop]]
- [[ai/agents-and-tools/autonomy-and-control|Autonomy & least privilege]]
- [[ai/agents-and-tools/agent-failure-modes|Agent failure modes]]
- [[ai/agents-and-tools/evaluating-agents|Evaluating agents]]

## Core sources

- Anthropic — *Building Effective Agents*, *Writing effective tools for agents*, *How we built our multi-agent research system*.
- Anthropic — *Model Context Protocol* (MCP) docs and spec.
- OpenAI — *A practical guide to building agents*.
- Lilian Weng — *LLM-Powered Autonomous Agents*.
