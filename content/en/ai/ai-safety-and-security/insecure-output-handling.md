---
title: "Insecure output handling"
description: Model output is untrusted input; passing it directly to browsers, shells, databases, tools, or users can create injection and safety failures.
tags: [ai-safety, output-handling, injection]
order: 7
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/input-output-guardrails]
last_verified: 2026-07-20
---
# Insecure output handling

## Mechanism: model output → typed validation → safe renderer or executor

```python
output = {"url": "javascript:alert(1)"}
print("block" if output["url"].startswith("javascript:") else "render")
```

Run with `python3`; expected output is `block`. Parse and validate by context—HTML, URL, SQL, shell, JSON, or tool arguments—before rendering or execution; never treat model text as trusted code.

## Sources

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — insecure-output handling risk.
- [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) — validation controls.

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
