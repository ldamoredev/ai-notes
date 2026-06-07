---
title: AI Playbooks
description: Repeatable procedures for evaluating, debugging, shipping, and operating AI systems.
tags: [playbooks, operations, procedures]
order: 0
updated: 2026-06-07
---
# AI Playbooks

Playbooks turn the atlas into operating practice. Use them when you need a repeatable
procedure with inputs, steps, outputs, and a definition of done.

## Evaluation and quality

- [[ai/ai-playbooks/evaluate-rag-answer-quality|Evaluate RAG answer quality]]
- [[ai/ai-playbooks/build-eval-set-from-scratch|Build an eval set from scratch]]
- [[ai/ai-playbooks/debug-hallucination|Debug a hallucination]]
- [[ai/ai-playbooks/ship-prompt-change-safely|Ship a prompt change safely]]

## Architecture and delivery

- [[ai/ai-playbooks/decide-prompt-vs-rag-vs-finetune|Decide prompt vs RAG vs fine-tune]]
- [[ai/ai-playbooks/choose-model-for-production|Choose a model for production]]
- [[ai/ai-playbooks/measure-and-cut-inference-cost|Measure and cut inference cost]]
- [[ai/ai-playbooks/stand-up-llm-observability|Stand up LLM observability]]

## Agents and security

- [[ai/ai-playbooks/debug-agent-stuck-in-loop|Debug an agent stuck in a loop]]
- [[ai/ai-playbooks/add-human-approval-gate|Add a human approval gate]]
- [[ai/ai-playbooks/audit-prompt-injection|Audit an app for prompt injection]]
- [[ai/ai-playbooks/run-ai-red-team-lite|Run an AI red team lite]]

## Core sources

- Draw on the relevant branch sources for each procedure: RAGAS, Hamel Husain, Eugene Yan, Shreya Shankar, Chip Huyen, Anthropic/OpenAI cookbooks, OWASP LLM Top 10, and Simon Willison's prompt-injection writing.
- Use [[ai/evaluation/index|Evaluation]], [[ai/rag-and-retrieval/index|RAG and retrieval]], [[ai/agents-and-tools/index|Agents and tools]], [[ai/mlops/index|MLOps]], [[ai/ai-product-engineering/index|AI Product Engineering]], and [[ai/ai-safety-and-security/index|AI Safety and Security]] as the conceptual backbone.
