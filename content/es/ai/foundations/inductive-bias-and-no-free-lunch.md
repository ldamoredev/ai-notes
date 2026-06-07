---
title: "Sesgo inductivo y la idea de no-free-lunch"
description: Aprender es imposible sin supuestos. El sesgo inductivo es el conjunto de supuestos que hace un modelo, y por eso importan las decisiones de arquitectura.
tags: [foundations, inductive-bias, generalization]
order: 3
updated: 2026-06-07
---
# Sesgo inductivo y la idea de no-free-lunch

Infinitas funciones ajustan cualquier conjunto finito de puntos. Para elegir una y
esperar que generalice, un aprendiz tiene que *preferir* algunas explicaciones sobre
otras. Ese conjunto de preferencias incorporadas es su **sesgo inductivo**.

## No free lunch, breve

Los teoremas de no-free-lunch dicen que, promediado sobre *todos los problemas
posibles*, ningún algoritmo de aprendizaje supera a otro. La trampa: los problemas del
mundo real no son uniformemente aleatorios; tienen estructura (suavidad, localidad,
composicionalidad). **Un modelo gana cuando tiene un sesgo que coincide con la
estructura de tus datos.** No hay un mejor modelo universal, solo el mejor match para
un problema.

## El sesgo inductivo viene horneado en la arquitectura

| Modelo | Sesgo inductivo |
|---|---|
| Modelos lineales | la relación es (más o menos) lineal |
| CNNs | localidad + invariancia a traslación (los píxeles cercanos se relacionan) |
| RNNs | el orden secuencial importa; el contexto reciente domina |
| Transformers | cualquier token puede atender a cualquier otro; prior posicional débil |
| Árboles | cortes por ejes, constantes por partes |

Por eso las CNNs dominan imágenes y los transformers dominan lenguaje: sus sesgos
encajan con el dominio. También por eso los transformers son *data-hungry*: un prior
más débil debe compensarse con más ejemplos.

## Consecuencias prácticas

- Elegir un modelo **es** elegir un sesgo. Matchealo con lo que sabés de los datos.
- Priors fuertes y correctos significan que necesitás **menos datos**. Priors débiles
  significan que necesitás **más** (y más cómputo). Ese es el tradeoff central detrás
  de "solo escalarlo".
- Feature engineering y data augmentation son formas de *inyectar* sesgo a mano.

## Trampa

Un sesgo equivocado pero confiado generaliza mal de una forma que ninguna afinación
arregla, por ejemplo forzar un modelo lineal sobre una relación fundamentalmente no
lineal.

**Se conecta con:** [[ai/foundations/generalization-and-overfitting|sesgo-varianza]] ·
[[ai/foundations/features-and-dimensionality|features y representaciones]] ·
[[ai/deep-learning/index|deep learning]]
