---
title: "Audit an app for prompt injection"
description: A focused audit procedure for direct and indirect prompt injection across prompts, retrieval, tools, user uploads, and external content.
tags: [playbook, security, prompt-injection]
order: 4
updated: 2026-06-07
---
# Audit an app for prompt injection

Use this playbook when an AI app reads user input, retrieved documents, webpages,
emails, support tickets, tool output, or any other untrusted text.

## Inputs

- System prompt, user prompt templates, retrieved-context template, and tool schemas.
- List of data sources the model can read.
- List of tools the model can call and what each tool can change.
- Sample traces from normal use.

## Procedure

1. Map every place untrusted text enters the model.
2. Mark which sources are direct user input and which are indirect data sources.
3. Check whether instructions and data are clearly separated in the prompt format.
4. Try direct attacks that ask the model to ignore instructions, reveal hidden context, or misuse tools.
5. Try indirect attacks embedded in documents, webpages, emails, or tool responses.
6. Verify tool calls are validated against the original user intent, not retrieved text.
7. Confirm sensitive actions require scoped permissions or human approval.
8. Add successful attacks to a regression suite and assign mitigations.

## Evidence to collect

| Evidence | Why |
|---|---|
| Prompt and context | shows whether data can override instructions |
| Retrieved source | identifies poisoned or untrusted content |
| Tool call | proves whether injection reached action |
| Guardrail decision | shows where detection worked or failed |

## Pitfall

Do not treat "the model refused my first injection" as proof of safety. Indirect
injection through retrieved content and tools is usually the more important test.

**Connects to:** [[ai/ai-safety-and-security/direct-prompt-injection|direct prompt injection]] ·
[[ai/ai-safety-and-security/indirect-prompt-injection|indirect prompt injection]] ·
[[ai/ai-safety-and-security/threat-modeling-llm-apps|threat modeling LLM apps]]
