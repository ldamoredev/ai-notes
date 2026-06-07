---
title: "Red teaming AI systems"
description: Red teaming exercises AI systems against prompt injection, jailbreaks, data leakage, tool misuse, RAG poisoning, and policy bypasses.
tags: [ai-safety, red-teaming, evaluation]
order: 10
updated: 2026-06-07
---
# Red teaming AI systems

Red teaming is adversarial evaluation. The goal is not to prove the system is safe; it
is to find plausible ways it fails before users or attackers do.

## What to attack

- Direct jailbreaks and policy bypass attempts.
- Indirect prompt injection through retrieved documents, webpages, emails, and tool output.
- Data leakage through retrieval, logs, memory, and citations.
- Tool misuse: wrong destination, invalid arguments, excessive permissions.
- Insecure output handling: generated HTML, SQL, code, commands, links.
- Cost and loop attacks that trigger unbounded consumption.
- Social engineering through model-generated persuasion.

## Red-team workflow

1. Define assets, attacker goals, and allowed test scope.
2. Build attack cases for each trust boundary.
3. Run tests against the full product, not only the base model.
4. Capture prompts, retrieved context, tool calls, outputs, and guardrail decisions.
5. Triage failures by impact and exploitability.
6. Add fixed failures to regression tests.

## Measure outcomes

| Metric | Meaning |
|---|---|
| Attack success rate | percent of cases that achieve the adversary goal |
| Guardrail catch rate | percent blocked or routed safely |
| False positive rate | legitimate requests blocked |
| Time to detection | whether monitoring catches the issue |
| Regression rate | whether fixed attacks come back later |

## Pitfall

Red teams that only write scary prompts miss product failures. Include retrieval,
tools, permissions, UI, logs, and human handoffs in the exercise.

**Connects to:** [[ai/evaluation/prompt-regression-testing|regression testing]] ·
[[ai/ai-safety-and-security/threat-modeling-llm-apps|threat modeling]] ·
[[ai/agents-and-tools/agent-failure-modes|agent failure modes]]
