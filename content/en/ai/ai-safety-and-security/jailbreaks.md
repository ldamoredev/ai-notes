---
title: "Jailbreaks"
description: Jailbreaks are adversarial prompts that try to bypass model safety behavior, policy refusals, or task constraints.
tags: [ai-safety, jailbreaks, adversarial]
order: 4
updated: 2026-06-07
---
# Jailbreaks

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
