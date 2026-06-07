---
title: AI Safety and Security
description: Threat models, prompt injection, data leakage, excessive agency, guardrails, red teaming, and governance for AI systems.
tags: [ai-safety, security, risk]
order: 0
updated: 2026-06-07
---
# AI Safety and Security

AI safety and security is the discipline of making AI systems resistant to misuse,
accidents, data exposure, and model-mediated attacks. The core move is to treat the
model as an unreliable component inside a security boundary, not as the boundary.

## Threat landscape

- [[ai/ai-safety-and-security/owasp-llm-top-10-overview|OWASP LLM Top 10 overview]] gives the shared vocabulary for LLM application risk.
- [[ai/ai-safety-and-security/direct-prompt-injection|Direct prompt injection]] covers user-provided instructions that try to override the system.
- [[ai/ai-safety-and-security/indirect-prompt-injection|Indirect prompt injection]] covers malicious instructions hidden in retrieved data, webpages, documents, and tool output.
- [[ai/ai-safety-and-security/jailbreaks|Jailbreaks]] explains adversarial prompts that try to bypass safety behavior.

## Data and action risk

- [[ai/ai-safety-and-security/data-and-pii-leakage|Data and PII leakage]] focuses on sensitive information exposure through prompts, logs, retrieval, and outputs.
- [[ai/ai-safety-and-security/excessive-agency|Excessive agency]] covers agents with too much tool access, autonomy, or permission.
- [[ai/ai-safety-and-security/insecure-output-handling|Insecure output handling]] treats model output as untrusted input to downstream systems.

## Controls and assurance

- [[ai/ai-safety-and-security/threat-modeling-llm-apps|Threat modeling LLM apps]] maps assets, trust boundaries, attackers, and failure modes.
- [[ai/ai-safety-and-security/input-output-guardrails|Input and output guardrails]] places checks before and after the model.
- [[ai/ai-safety-and-security/red-teaming-ai-systems|Red teaming AI systems]] stress-tests prompts, retrieval, tools, and policies.
- [[ai/ai-safety-and-security/defense-in-depth-and-least-privilege|Defense in depth and least privilege]] explains why prompts are only one layer.
- [[ai/ai-safety-and-security/privacy-and-data-governance|Privacy and data governance]] defines data minimization, retention, access, and audit controls.

## Core sources

- OWASP, **Top 10 for LLM Applications (2025)** and **Agentic AI / Agentic Security Top 10**.
- Simon Willison's prompt-injection writing and practical demonstrations.
- Lilian Weng, **Adversarial Attacks on LLMs**.
- NIST AI Risk Management Framework for governance, mapping, measurement, and management.
- MITRE ATLAS for adversarial ML tactics, techniques, and threat-model vocabulary.
