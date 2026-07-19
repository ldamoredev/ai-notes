---
title: Prompting & Context Engineering
description: Prompting techniques plus the larger discipline of context engineering — designing what the model knows before it answers.
tags: [prompt-engineering, context-engineering, prompts]
order: 0
updated: 2026-06-07
---
# Prompting & Context Engineering

Prompting is one layer; **context engineering is the larger discipline.** Prompt
engineering asks *how do I phrase the request?* Context engineering asks *what should
the model know when it processes that request?* — system prompt, examples, retrieved
docs, tool outputs, history, and output shape, all assembled into a finite
[[ai/llms/context-window-and-kv-cache|context window]].

As systems moved from single chats to [[ai/rag-and-retrieval/index|RAG]] and
[[ai/agents-and-tools/index|agents]], leverage shifted from clever wording to **what
goes into the window and in what order.** This branch covers both.

## Mental model

Context engineering constructs the model's temporary information environment. Instructions, examples, retrieved evidence, tool schemas, history, constraints, and output format compete within a finite window; their provenance and ordering shape behavior without changing weights.

## Roadmap: reframe and basics

- [[ai/prompt-engineering/prompt-to-context-engineering|From prompting to context engineering]]
- [[ai/prompt-engineering/anatomy-of-a-prompt|Anatomy of a good prompt]]
- [[ai/prompt-engineering/system-prompts-and-roles|System prompts & roles]]

## Core techniques

- [[ai/prompt-engineering/zero-and-few-shot|Zero-shot & few-shot]]
- [[ai/prompt-engineering/chain-of-thought|Chain-of-thought & when not to use it]]
- [[ai/prompt-engineering/structured-outputs|Structured outputs (JSON & schemas)]]
- [[ai/prompt-engineering/task-decomposition|Task decomposition & prompt chaining]]
- [[ai/prompt-engineering/self-consistency-and-sampling|Self-consistency & sampling]]

## Engineering the context

- [[ai/prompt-engineering/managing-the-context-window|Managing the context window]]
- [[ai/prompt-engineering/assembling-context|Assembling context: order & format]]
- [[ai/prompt-engineering/memory-and-history|Memory & conversation history]]

## Discipline

- [[ai/prompt-engineering/evaluating-and-iterating-prompts|Evaluating & iterating prompts]]

**Connects to:** [[ai/rag-and-retrieval/index|Retrieval and Knowledge]] · [[ai/agents-and-tools/index|Agents and Tools]] · [[ai/evaluation/prompt-regression-testing|Prompt Regression Testing]]

## Core sources

- [Anthropic prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — current instruction, examples, XML, and chaining guidance.
- [Anthropic context engineering for agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — context selection and compaction for long-running systems.
- [OpenAI Cookbook](https://cookbook.openai.com/) — executable structured-output, tool, and evaluation patterns.
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) — the primary paper for reasoning demonstrations in prompts.
