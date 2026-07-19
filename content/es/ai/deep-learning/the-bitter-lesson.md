---
title: "The bitter lesson"
description: La observación de Rich Sutton de que los métodos generales que aprovechan cómputo vencen a conocimiento humano hecho a mano en el largo plazo: la lente estratégica detrás de la AI moderna.
tags: [deep-learning, scaling, strategy, mental-model]
order: 14
updated: 2026-06-07
---
# The bitter lesson

"The bitter lesson" de Rich Sutton es la idea estratégica más útil para entender por
qué la AI moderna se ve como se ve: **a lo largo de décadas, los métodos generales que
escalan con cómputo vencieron consistentemente a enfoques construidos sobre conocimiento
humano hecho a mano.** Es "bitter" porque los investigadores siguen invirtiendo en
estructura ingeniosa y específica de dominio, y siguen siendo superados por métodos más
simples que solo usan más cómputo y datos.

## El patrón, repetido

- **Ajedrez / Go** — estrategia programada a mano perdió contra búsqueda masiva y self-play.
- **Habla y visión** — features diseñadas (fonemas, detectores de bordes) perdieron
  contra representaciones aprendidas desde [[ai/deep-learning/cnns|deep nets]].
- **Lenguaje** — gramáticas y pipelines perdieron contra [[ai/llms/pretraining-next-token|predicción
  next-token]] a [[ai/deep-learning/scaling-laws|escala]].

Cada vez, el [[ai/foundations/inductive-bias-and-no-free-lunch|prior humano fuerte]]
ayudó al principio y después limitó el techo; el método general y hambriento de cómputo
seguía mejorando a medida que crecían los recursos.

## Por qué pasa

La estructura diseñada por humanos es satisfactoria y ayuda en el corto plazo, pero no
*escala*: hornea nuestra comprensión limitada. Los métodos generales (búsqueda y
aprendizaje) no tienen ese techo: dales más [[ai/deep-learning/scaling-laws|cómputo y
datos]] y siguen mejorando. Este es el esqueleto estratégico detrás de "just scale it"
y la era de foundation models.

## El matiz (no lo sobreapliques)

The bitter lesson habla de la **frontera de largo plazo**, no de tu martes. En la práctica:

- Con **datos/cómputo limitados**, un buen [[ai/foundations/inductive-bias-and-no-free-lunch|prior]]
  (el modelo correcto, [[ai/machine-learning/feature-engineering|features]]) todavía gana:
  ver [[ai/machine-learning/decision-trees-and-ensembles|árboles en datos tabulares]].
- La lección favorece métodos *generales*, pero **calidad de datos, evals y
  [[ai/ai-product-engineering/the-ai-application-stack|diseño de sistema]]** es donde vive
  la mayor parte del trabajo aplicado.
- Es una observación sobre trayectoria, no una licencia para tirarle cómputo a todo.

## Trampa

Dos errores opuestos: sobreingenierizar estructura ingeniosa que la escala va a borrar,
**y** hacer cargo cult de "solo agregá cómputo" cuando no tenés ni los datos ni el
presupuesto, y un modelo más simple y rico en prior habría ganado. Sostené la lección
como una *dirección*, no como una receta.

**Conecta con:** [[ai/deep-learning/scaling-laws|scaling laws]] ·
[[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] ·
[[ai/llms/emergent-abilities-and-scale|emergence y escala]]
