---
title: Seguridad de IA
description: Trust boundaries, prompt injection, fuga de datos, agencia excesiva y defense in depth.
tags: [ai-safety, security, risk]
order: 0
updated: 2026-07-19
---
# Seguridad de IA

Una aplicación de IA cruza un trust boundary cuando datos no confiables influyen al modelo y su salida puede alcanzar información, código, dinero o personas. El modelo es un componente no confiable dentro del perímetro; nunca es el perímetro.

## Modelo mental

Limitá autoridad, validá efectos fuera del modelo, aislá datos e instrucciones, y prepará detección y respuesta. Un prompt no reemplaza un control de acceso.

## Hoja de ruta

- [[ai/ai-safety-and-security/threat-modeling-llm-apps|Threat modeling de apps LLM]]
- [[ai/ai-safety-and-security/direct-prompt-injection|Prompt injection directo]]
- [[ai/ai-safety-and-security/indirect-prompt-injection|Prompt injection indirecto]]
- [[ai/ai-safety-and-security/excessive-agency|Agencia excesiva]]
- [[ai/ai-safety-and-security/defense-in-depth-and-least-privilege|Defense in depth y mínimo privilegio]]
- [[ai/ai-safety-and-security/red-teaming-ai-systems|Red teaming]]

**Conecta con:** [[ai/agents-and-tools/autonomy-and-control|Autonomía y control]] · [[ai/evaluation/index|Evaluación]] · [[ai/ai-ethics-and-governance/index|Ética y Gobernanza]]

## Fuentes principales

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — taxonomía de riesgos y mitigaciones.
- [MITRE ATLAS](https://atlas.mitre.org/) — tácticas, técnicas y casos adversariales de ML.
- [NIST Adversarial Machine Learning Taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) — terminología de ataques y defensas.
- [Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — análisis sistemático del ataque vía datos externos.
