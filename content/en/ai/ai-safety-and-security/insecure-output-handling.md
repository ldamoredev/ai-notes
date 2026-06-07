---
title: "Insecure output handling"
description: Model output is untrusted input; passing it directly to browsers, shells, databases, tools, or users can create injection and safety failures.
tags: [ai-safety, output-handling, injection]
order: 7
updated: 2026-06-07
---
# Insecure output handling

Insecure output handling happens when an application treats model output as trusted.
The model can produce HTML, SQL, code, commands, tool arguments, links, or policy
claims that downstream systems might execute or display unsafely.

## Output is input to something else

| Destination | Failure mode |
|---|---|
| Browser | XSS or unsafe rendered HTML |
| Shell | command injection or destructive command |
| Database | SQL injection or bad query generation |
| Tool call | unsafe arguments or wrong destination |
| Email/chat | social engineering or data exposure |
| User decision | persuasive misinformation or missing caveats |

## Controls

- Parse structured output against a schema.
- Escape or sanitize HTML and Markdown before rendering.
- Use parameterized queries and controlled SQL builders.
- Validate generated code and commands in a sandbox.
- Require approvals before executing generated actions.
- Separate generated explanation from executable payload.

## Structured output is not enough

JSON validity only proves shape, not safety. A valid JSON tool call can still target
the wrong account, exceed a budget, include private data, or perform an unauthorized
action.

## Pitfall

Never put model output directly into an interpreter, browser, database, or external
tool because "the prompt told it to be safe". Treat it like hostile user input.

**Connects to:** [[ai/prompt-engineering/structured-outputs|structured outputs]] ·
[[ai/agents-and-tools/tool-calling|tool calling]] ·
[[ai/ai-product-engineering/product-guardrails|product guardrails]]
