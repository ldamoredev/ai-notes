---
title: "Por qué alucinan los LLMs"
description: La alucinación no es un bug agregado encima: es consecuencia directa de entrenar un modelo para producir texto plausible. Por qué pasa y cómo reducirla.
tags: [llms, hallucination, grounding, reliability]
order: 9
updated: 2026-06-07
---
# Por qué alucinan los LLMs

Una **alucinación** es una afirmación confiada y fluida que es falsa o no está
respaldada. No es un glitch: es lo esperable de un sistema entrenado para producir
texto *plausible*, no texto *verdadero*. Entender la causa te dice cómo mitigarla
(y que no podés eliminarla por completo).

## La causa raíz

[[ai/llms/pretraining-next-token|Pretraining]] optimiza una sola cosa: el próximo
[[ai/llms/tokenization|token]] más probable. "Suena plausible" y "es verdadero" suelen
coincidir en los datos de entrenamiento, pero no siempre. El modelo **no tiene una
base de datos interna ni chequeo de verdad**; genera la continuación que *parece*
correcta. Cuando no sabe, la continuación más probable sigue siendo una conjetura
fluida y autoritativa.

Factores que empeoran:

- **Huecos de conocimiento / cutoff**: si le preguntan sobre algo raro o posterior al
  cutoff, interpola ([[ai/foundations/distribution-shift|distribution shift]]).
- **Presión de alignment para ser útil**: el post-training recompensa respuestas
  confiadas y completas, empujando a los modelos a responder en vez de abstenerse.
- **Sampling**: una [[ai/llms/decoding-and-sampling|temperature]] más alta aumenta la
  improvisación.

## Cómo reducirla (no eliminarla)

- **Grounding vía [[ai/rag-and-retrieval/index|RAG]]**: suministrá los hechos en
  contexto e instruí al modelo a responder *solo* desde ellos, con citas. Es la palanca
  más grande para tareas factuales.
- **Dejalo decir "no sé"**: prompteá y premiá la abstención; bajá temperature para
  trabajo factual.
- **Verificá**: uso de tools, salidas estructuradas y un chequeo de segunda pasada
  para afirmaciones de alto impacto.
- **[[ai/evaluation/index|Evaluá]] groundedness**: medí fidelidad a fuentes, no solo
  fluidez.

## El modelo mental

> Un LLM es un improvisador fluido, no una base de datos. Tratá cada afirmación
> factual como *no verificada* hasta que esté grounded o chequeada. Diseñá el sistema
> alrededor de eso, en vez de esperar un modelo que "deje de inventar cosas".

**Se conecta con:** [[ai/llms/pretraining-next-token|objetivo next-token]] ·
[[ai/rag-and-retrieval/index|grounding con RAG]] ·
[[ai/evaluation/index|medición de groundedness]]
