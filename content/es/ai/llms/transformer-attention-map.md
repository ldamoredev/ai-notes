---
title: Mapa de atención en transformers
description: Una nota conceptual corta sobre atención como ruteo entre representaciones de tokens.
tags: [llms, transformers, attention]
order: 1
updated: 2026-06-07
---
# Mapa de atención en transformers

La atención deja que la representación de un token lea desde representaciones de otros tokens. No es memoria mágica; es un patrón aprendido de ruteo sobre el contexto actual.

## Por qué importa

- Explica por qué el orden y el formato del contexto afectan el comportamiento.
- Ayuda a separar problemas de retrieval de problemas de razonamiento o instrucción.
- Da un modelo mental para límites de contexto, compresión y estructura de prompts.

## Check práctico

Cuando un LLM ignora un detalle, preguntá si el detalle era visible, saliente y conectado con la tarea. Después probá con un contexto más chico y más nítido antes de cambiar de modelo.
