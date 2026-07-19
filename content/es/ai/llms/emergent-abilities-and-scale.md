---
title: "Emergent abilities e in-context learning"
description: El payoff sorprendente de la escala: los modelos aprenden de ejemplos en el prompt sin actualizar pesos. Qué es real sobre emergence y qué es artefacto de métrica.
tags: [llms, in-context-learning, emergence, scale]
order: 8
updated: 2026-06-07
---
# Emergent abilities e in-context learning

La razón por la que los LLMs se sienten distintos del ML anterior es un conjunto de
comportamientos que aparecen con [[ai/deep-learning/scaling-laws|scale]]: sobre todo,
aprender una tarea nueva a partir de ejemplos en el prompt sin ningún entrenamiento.

## In-context learning (ICL)

Mostrale a un modelo algunos ejemplos input→output en el prompt y realiza la tarea en
un input nuevo: **sin actualizaciones de pesos, sin fine-tuning**. Esto es prompting
*few-shot*. El modelo no está "aprendiendo" en el sentido de gradientes; el pretraining
lo volvió bueno para inferir el patrón de un documento y continuarlo. ICL es la base
del [[ai/prompt-engineering/index|prompting]] y la razón por la que un único modelo
congelado puede hacer miles de tareas.

> Los ejemplos few-shot no actualizan el modelo: orientan un modelo fijo armando un
> patrón que completa. El "aprendizaje" ocurre en inferencia, dentro de la ventana de
> contexto.

## Emergent abilities, con una salvedad

Algunas capacidades (aritmética multi-step, ciertos razonamientos) parecen aparecer
de golpe después de un umbral de escala en vez de mejorar suavemente: *emergent
abilities*. La versión honesta:

- El efecto es en parte **real**: modelos más grandes realmente desbloquean
  comportamientos cualitativamente nuevos.
- Es en parte un **artefacto de métrica**: métricas duras de todo-o-nada (exact match)
  hacen que un progreso subyacente suave *parezca* un salto repentino. Con métricas
  más blandas, la curva es más continua.

Tomá las afirmaciones dramáticas de "de repente pudo hacer X" con escepticismo
calibrado, pero no descartes que la escala compra comportamiento nuevo.

## Por qué importa

- **A menudo podés saltear fine-tuning**: ICL + buen prompting resuelve muchas tareas
  en un modelo congelado ([[ai/fine-tuning-and-alignment/index|la escalera de adaptación]]).
- **La capacidad es difícil de predecir** a nivel tarea aunque la
  [[ai/deep-learning/scaling-laws|loss]] sea predecible; entonces **evaluá**, no
  asumas ([[ai/evaluation/index|eval]]).

**Conecta con:** [[ai/deep-learning/scaling-laws|scaling laws]] ·
[[ai/prompt-engineering/index|prompting few-shot]] ·
[[ai/llms/reasoning-and-test-time-compute|reasoning]]
