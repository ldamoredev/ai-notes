---
title: Mapa de attention del transformer
description: Una nota conceptual corta sobre attention como ruteo entre representaciones de tokens.
tags: [llms, transformers, attention]
order: 1
updated: 2026-06-07
featured: true
---
# Mapa de attention del transformer

Attention permite que la representación de un token lea desde representaciones de
otros tokens. No es memoria mágica; es un patrón de ruteo aprendido sobre el contexto
actual.

## Por qué importa

- Explica por qué el orden y el formato del contexto afectan el comportamiento del
  modelo.
- Ayuda a separar problemas de retrieval de problemas de razonamiento o instrucción.
- Da un modelo mental para límites de contexto, compresión y estructura de prompt.

## Chequeo práctico

Cuando un LLM ignora un detalle, preguntate si el detalle era visible, saliente y
conectado con la tarea. Después probá con un contexto más chico y más nítido antes de
cambiar de modelo.
