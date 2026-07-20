---
title: "Jailbreaks"
description: Jailbreaks are adversarial prompts that try to bypass model safety behavior, policy refusals, or task constraints.
tags: [ai-safety, jailbreaks, adversarial]
order: 4
updated: 2026-07-20
kind: concept
level: intermediate
status: current
prerequisites: [ai/ai-safety-and-security/input-output-guardrails]
last_verified: 2026-07-20
---
# Jailbreaks

## Mechanism: adversarial request → model behavior → policy and capability check

```python
policy, request = {"disallowed": {"exfiltrate"}}, "exfiltrate"
print("refuse" if request in policy["disallowed"] else "continue")
```

Run with `python3`; expected output is `refuse`. Evaluate attacks as distributions, log bypasses, remove dangerous capabilities, and require deterministic controls for actions; a refusal string is not containment.

## Sources

- [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) — jailbreak-related application risks.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — testing and mitigation lifecycle.

Jailbreaks are adversarial prompts designed to make a model violate its intended
behavior. They often use roleplay, obfuscation, emotional pressure, translation,
multi-step setup, or policy confusion to push the model outside its guardrails.

## Common patterns

- Roleplay that asks the model to simulate an unrestricted assistant.
- Instruction conflict that reframes policy as a test or obsolete rule.
- Encoding, translation, or formatting tricks that hide harmful intent.
- Gradual escalation from benign questions to disallowed assistance.
- Requesting "fictional" or "educational" output that is directly actionable.
- Asking the model to critique, complete, or transform unsafe content.

## What jailbreaks test

| Layer | Question |
|---|---|
| Model alignment | does the model refuse unsafe requests? |
| System prompt | are task boundaries clear and stable? |
| Input guardrail | are risky requests caught before generation? |
| Output guardrail | are unsafe completions blocked or revised? |
| Product design | does the UI route users to safe alternatives? |

## Defense posture

Jailbreak resistance improves with layered defenses: tuned model behavior, explicit
policy prompts, input classifiers, output checks, rate limits, abuse monitoring, and
human review for high-risk categories.

## Pitfall

Do not confuse jailbreak safety with application security. A model may refuse harmful
instructions while still leaking data, calling an unsafe tool, or trusting poisoned
retrieval content.

**Connects to:** [[ai/ai-safety-and-security/input-output-guardrails|input and output guardrails]] ·
[[ai/evaluation/task-specific-evals|task-specific evals]] ·
[[ai/evaluation/prompt-regression-testing|prompt regression testing]]
