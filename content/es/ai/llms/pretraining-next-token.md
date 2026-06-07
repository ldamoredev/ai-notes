---
title: "Pretraining: predicción del próximo token"
description: Un objetivo — predecir el próximo token — sobre billones de tokens produce un modelo que aprendió implícitamente gramática, hechos y razonamiento. Cómo y por qué funciona.
tags: [llms, pretraining, self-supervised, base-model]
order: 3
updated: 2026-06-07
---
# Pretraining: predicción del próximo token

Toda la capacidad base de un LLM viene de una tarea self-supervised repetida a una
escala inimaginable: **dado el texto hasta ahora, predecir el próximo token**. No hay
labels humanos: la "respuesta" es simplemente el token que realmente vino después
([[ai/foundations/types-of-learning|self-supervision]]).

## Por qué funciona un objetivo tan tonto

Para predecir *bien* el próximo token a lo largo de todo internet, el modelo está
forzado a aprender una cantidad enorme como efecto secundario:

- Gramática y sintaxis (para predecir palabras funcionales).
- Hechos y asociaciones (para completar "La capital de Francia es ...").
- Estilo, formato, estructura de código y razonamiento rudimentario (para continuar
  un argumento o una prueba).

El objetivo es simple; la *única* manera de volverse bueno en eso es construir un
modelo interno rico del lenguaje y del mundo. El entrenamiento minimiza
[[ai/foundations/information-theory-basics|cross-entropy]] (equivalentemente,
perplejidad) sobre el corpus.

## El resultado es un "modelo base"

El pretraining produce un **modelo base**: un completador de texto poderoso, no un
asistente. Hacé una pregunta y quizá continúe con *más preguntas*, porque eso hacen
los documentos. Tiene conocimiento pero ningún instinto de ser útil, honesto o seguro.
Convertirlo en un asistente usable es trabajo del [[ai/llms/base-vs-instruct|post-training]].

## Consecuencias para recordar

- **Knowledge cutoff**: el modelo solo sabe lo que había en sus datos de entrenamiento
  hasta una fecha; el mundo sigue moviéndose ([[ai/foundations/distribution-shift|distribution
  shift]]) → un argumento a favor de [[ai/rag-and-retrieval/index|retrieval]].
- **Modela *plausibilidad*, no verdad**: la semilla de la
  [[ai/llms/why-llms-hallucinate|alucinación]].
- **La calidad de datos lo es todo**: basura y duplicación entran, basura sale;
  curación y dedup ahora son centrales ([[ai/deep-learning/scaling-laws|Chinchilla]]).

**Se conecta con:** [[ai/foundations/types-of-learning|aprendizaje self-supervised]] ·
[[ai/llms/base-vs-instruct|post-training]] ·
[[ai/llms/why-llms-hallucinate|alucinación]]
