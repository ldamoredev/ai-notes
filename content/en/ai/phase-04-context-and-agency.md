---
title: Phase 04 — Context and Agency
description: Assemble context, retrieve evidence, call tools, manage state, and bound autonomous behavior.
tags: [phase, context, retrieval, agents]
order: 7
updated: 2026-07-19
---
# Phase 04 — Context and Agency

Models do not act in isolation. Products assemble context, retrieve evidence, expose tools, persist state, recover from failure, and decide when a human must approve an action.

## Mental model

Context supplies temporary knowledge; retrieval selects evidence; tools add effects; orchestration owns state and authority. Keep those layers separable so each can be evaluated and constrained.

## Roadmap through the branches

- [[ai/prompt-engineering/index|Context Engineering]]
- [[ai/rag-and-retrieval/index|Retrieval and Knowledge]]
- [[ai/agents-and-tools/index|Agents and Tools]]

## Exit criteria

You can distinguish context from model memory, evaluate a retriever separately from generation, specify tool contracts and permissions, prefer deterministic workflows when possible, and design retries and approval gates as explicit state transitions.

**Connects to:** [[ai/phase-03-training-and-inference|Phase 03 — Training and Inference]] · [[ai/phase-05-measurement-and-trust|Phase 05 — Measurement and Trust]]

## Core sources

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — retriever-generator factorization.
- [ReAct](https://arxiv.org/abs/2210.03629) — reasoning and acting loop.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — workflow and agent design boundaries.
