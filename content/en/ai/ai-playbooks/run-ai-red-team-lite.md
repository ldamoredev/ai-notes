---
title: "Run an AI red team lite"
description: A lightweight red-team procedure for small teams to test jailbreaks, prompt injection, data leakage, tool misuse, and guardrail failures.
tags: [playbook, red-team, security]
order: 12
updated: 2026-07-20
kind: playbook
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/red-teaming-ai-systems]
last_verified: 2026-07-20
---
# Run an AI red team lite

**Mental model:** test attacker goals against the assembled system—data, retrieval, tools, identity, UI, and logging—not a prompt in isolation.

## Mechanism: attacker goal → trace → exploitability → regression

Use this playbook when a small team needs a focused adversarial pass before releasing
or expanding an AI feature. It is not a full security assessment, but it catches many
obvious failures early.

## Inputs

- Product workflow, system prompt, retrieval sources, tool list, guardrails, and threat model.
- Test account with realistic permissions.
- Logging enabled for prompts, context, tool calls, guardrail decisions, and outputs.

## Procedure

1. Pick 5-10 attacker goals: reveal secrets, bypass policy, misuse tools, exfiltrate data, poison context, or burn resources.
2. Test direct jailbreaks and prompt injection against normal user input.
3. Test indirect injection inside documents, webpages, support tickets, or tool output.
4. Test data leakage with cross-tenant, unauthorized, and hidden-context attempts.
5. Test tool misuse with unsafe destinations, malformed arguments, and excessive actions.
6. Test output handling with generated HTML, links, code, commands, and SQL-like payloads.
7. Record whether the system blocks, refuses, escalates, or fails silently.
8. Rank findings by impact, exploitability, and ease of mitigation.
9. Convert confirmed failures into regression tests.

## Report template

| Field | Content |
|---|---|
| Scenario | attacker goal and path |
| Evidence | trace, prompt, context, output, tool call |
| Impact | data, action, cost, safety, trust |
| Control gap | missing or weak mitigation |
| Fix | owner and next test |

## Pitfall

Do not stop at model-only jailbreaks. The riskiest failures often involve retrieval,
tools, permissions, caches, logs, and UI decisions.

**Connects to:** [[ai/ai-safety-and-security/red-teaming-ai-systems|red teaming AI systems]] ·
[[ai/ai-safety-and-security/input-output-guardrails|input and output guardrails]] ·
[[ai/evaluation/prompt-regression-testing|regression testing]]

## Executable severity triage

```python
impact, exploitability = 4, 3
print("priority", impact * exploitability)
```

Run with `python3`; expected output is `priority 12`. Confirmed failures need an owner, mitigation, retest, and regression fixture.

## Sources

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — application-risk taxonomy.
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial-ML techniques.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk-management process.
