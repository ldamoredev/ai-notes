---
title: "Generalización, overfitting y el tradeoff sesgo-varianza"
description: Un modelo solo sirve si funciona sobre datos que nunca vio. Overfitting, underfitting y el tradeoff que gobierna ambos.
tags: [foundations, generalization, overfitting, bias-variance]
order: 2
updated: 2026-06-07
---
# Generalización, overfitting y el tradeoff sesgo-varianza

**Generalización** es lo único que importa: rendimiento sobre datos con los que el
modelo no entrenó. Un modelo que memoriza perfectamente su training set y falla en
inputs nuevos no aprendió nada útil.

## Underfitting vs overfitting

- **Underfitting** — el modelo es demasiado simple (o quedó subentrenado) para capturar
  el patrón. Error alto en datos de entrenamiento y de test.
- **Overfitting** — el modelo ajustó los datos de entrenamiento *demasiado* bien,
  incluyendo su ruido y rarezas. Error bajo en train, error alto en test.

La firma es la **brecha** entre error de entrenamiento y validación. Brecha chica con
error alto → underfit. Brecha grande → overfit.

## El tradeoff sesgo-varianza

El error total se descompone (informalmente) en:

| Término | Significado | Empujado por |
|---|---|---|
| **Sesgo** | error por supuestos equivocados / modelo demasiado simple | underfitting |
| **Varianza** | error por sensibilidad a la muestra particular de entrenamiento | overfitting |
| **Irreducible** | ruido que ningún modelo puede eliminar | los datos mismos |

Más capacidad (modelo más grande, más features) baja el sesgo pero sube la varianza.
El objetivo clásico es el punto dulce entre ambos. (Los modelos muy grandes complican
esta historia ordenada — ver *double descent* — pero la intuición sigue guiando el
trabajo diario.)

## Palancas que mejoran la generalización

- **Más/mejores datos** — el arreglo más confiable; reduce varianza.
- **Regularización** — penalizaciones L2/L1, dropout, early stopping; intercambiá un
  poco de sesgo por menos varianza.
- **Modelo más simple o menos features** cuando los datos son escasos.
- **Cross-validation** para estimar la brecha honestamente en vez de confiar en un solo split.

## Trampa

El validation set es un presupuesto que gastás al mirarlo. Ajustá contra él suficientes
veces y empezás a hacer overfitting *al validation set*, que es justamente por lo que
existe un [[ai/foundations/data-splits-and-leakage|test set]] final e intacto.

**Se conecta con:** [[ai/foundations/data-splits-and-leakage|splits y leakage]] ·
[[ai/foundations/inductive-bias-and-no-free-lunch|sesgo inductivo]] ·
[[ai/foundations/distribution-shift|distribution shift]]
