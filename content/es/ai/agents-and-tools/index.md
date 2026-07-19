---
title: Agentes y Herramientas
description: Tool calling, loops de control, estado, memoria, handoffs y límites de autonomía.
tags: [agents, tools]
order: 0
updated: 2026-07-19
---
# Agentes y Herramientas

Un agente es un modelo dentro de un loop con observaciones, herramientas, estado, presupuestos y condiciones de corte. La capacidad surge del loop; la seguridad surge de tratar la salida del modelo como una propuesta sin autoridad propia.

## Modelo mental

Usá workflows deterministas cuando los pasos se conocen. Agregá autonomía sólo donde la decisión dependa de evidencia que aparece durante la ejecución, y mantené permisos, validaciones y efectos en infraestructura determinista.

## Hoja de ruta

- [[ai/agents-and-tools/workflows-vs-agents|Workflows versus agentes]]
- [[ai/agents-and-tools/tool-calling|Tool calling]]
- [[ai/agents-and-tools/agent-computer-interface|Interfaz agente-herramienta]]
- [[ai/agents-and-tools/react-loop|Loop ReAct]]
- [[ai/agents-and-tools/autonomy-and-control|Autonomía y control]]
- [[ai/agents-and-tools/evaluating-agents|Evaluación de agentes]]

**Conecta con:** [[ai/prompt-engineering/index|Context Engineering]] · [[ai/ai-safety-and-security/index|Seguridad de IA]] · [[ai/evaluation/evaluating-agent-systems|Evaluación de agentes]]

## Fuentes principales

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — taxonomía práctica entre workflows y agentes.
- [Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25) — contrato abierto entre modelos, herramientas y recursos.
- [ReAct](https://arxiv.org/abs/2210.03629) — razonamiento y acción intercalados.
- [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — diseño, orquestación y guardrails.
