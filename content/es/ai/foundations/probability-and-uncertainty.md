---
title: "Probabilidad e incertidumbre para ML"
description: Los modelos devuelven probabilidades, no hechos. Likelihood, Bayes y calibración: la diferencia entre un modelo confiado y uno correcto.
tags: [foundations, probability, uncertainty, calibration]
order: 6
updated: 2026-06-07
---
# Probabilidad e incertidumbre para ML

La mayoría de los modelos son **probabilísticos**: un clasificador devuelve
`P(class | input)`, un LLM devuelve una distribución de probabilidad sobre el próximo
token. Tratar esos números como certezas es un error de categoría que causa fallas reales.

## Las tres ideas que reutilizás constantemente

- **Likelihood** — qué tan probables son los datos observados bajo el modelo. Entrenar
  un clasificador con cross-entropy *es* maximizar el likelihood de las etiquetas.
- **Regla de Bayes** — actualizar una creencia con evidencia:
  `P(H|E) ∝ P(E|H) · P(H)`. Posterior ∝ likelihood × prior. El prior es tu creencia
  inicial; la evidencia la reconfigura. Es la columna vertebral de razonar bajo incertidumbre.
- **Base rates** — `P(H)` importa muchísimo. Un test 99% preciso para una enfermedad
  de 1 en 10.000 produce mayormente falsos positivos. Los modelos heredan esto; ignorar
  los base rates es el error clásico de probabilidad.

## Dos tipos de incertidumbre

| Tipo | Fuente | ¿Reducible? |
|---|---|---|
| **Aleatoria** | ruido inherente en los datos | no; es irreducible |
| **Epistémica** | ignorancia del modelo (pocos datos, input desconocido) | sí; más/mejores datos |

Los inputs out-of-distribution disparan incertidumbre epistémica. Un modelo que no puede
distinguir "no sé" de "estoy seguro" es peligroso en producción.

## Calibración: confianza que significa algo

Un modelo está **calibrado** cuando sus probabilidades declaradas coinciden con la
realidad: entre predicciones que llama "80% probables", alrededor del 80% son correctas.
Accuracy y calibración son distintas: un modelo puede ser preciso pero sobreconfiado.

- Los LLMs suelen estar **mal calibrados** después del instruction tuning: suenan
  confiados estén bien o mal. Por eso una respuesta fluida no es evidencia de una
  respuesta correcta (ver [[ai/llms/index|por qué alucinan los LLMs]]).
- Revisá calibración con reliability diagrams; mejorala con temperature scaling.

## Trampa

Un score softmax **no** es una probabilidad de estar correcto: es la confianza interna
del modelo, que puede estar totalmente fuera de distribución. No gates decisiones sobre
scores crudos sin revisar calibración.

**Se conecta con:** [[ai/foundations/information-theory-basics|cross-entropy]] ·
[[ai/foundations/evaluation-metrics|métricas]] ·
[[ai/evaluation/index|evaluar modelos]]
