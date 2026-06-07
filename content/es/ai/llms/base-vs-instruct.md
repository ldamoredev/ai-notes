---
title: "Modelos base vs instruct vs chat"
description: Un modelo base completa texto; un modelo instruct/chat sigue pedidos. El stack de post-training (SFT + preference alignment) que convierte uno en otro.
tags: [llms, instruction-tuning, rlhf, post-training]
order: 7
updated: 2026-06-07
---
# Modelos base vs instruct vs chat

El modelo que usás realmente no es el [[ai/llms/pretraining-next-token|pretrained]]
crudo. Una segunda etapa, **post-training**, remodela un completador de texto en un
asistente que sigue instrucciones y se comporta. Conocer la diferencia aclara mucho.

## Tres sabores

| Tipo | Se comporta como | Bueno para |
|---|---|---|
| **Base** | autocompletado de internet | generación cruda, investigación, tu propia base de fine-tuning |
| **Instruct** | sigue una instrucción única | tareas one-shot (resumir, clasificar, extraer) |
| **Chat** | conversación multi-turn con roles | asistentes, agents, cualquier cosa con estado |

Preguntale a un modelo *base* "¿Cuál es la capital de Francia?" y quizá responda con
una lista de preguntas de quiz similares: está completando un documento, no
contestándote.

## El stack de post-training

1. **SFT (supervised fine-tuning / instruction tuning)**: entrenar con pares curados
   `(prompt → respuesta ideal)` para que el modelo aprenda el *formato* de ser útil y
   seguir instrucciones.
2. **Preference alignment**: [[ai/fine-tuning-and-alignment/index|RLHF o DPO]] ajusta
   *cuál* de varias respuestas válidas prefiere el modelo, usando datos de preferencias
   humanas, para volverlo más útil, honesto e inocuo.

De acá salen los chat templates, system prompts y comportamientos de rechazo. El
[[ai/llms/pretraining-next-token|modelo base]] aporta el conocimiento; el post-training
aporta los modales.

## Por qué importa en la práctica

- **Prompting difiere**: los modelos base quieren ejemplos few-shot/continuación; los
  modelos chat quieren instrucciones y un system prompt ([[ai/prompt-engineering/index|prompting]]).
- **Los chat templates son reales**: los tokens especiales que delimitan roles deben
  coincidir con el modelo, o la calidad cae.
- **Alignment es impuesto y regalo**: agrega seguridad y usabilidad, pero puede causar
  rechazos excesivos y un pequeño "alignment tax" de capacidad.

**Se conecta con:** [[ai/llms/pretraining-next-token|pretraining]] ·
[[ai/fine-tuning-and-alignment/index|SFT, RLHF y DPO]] ·
[[ai/prompt-engineering/index|prompting base vs chat]]
