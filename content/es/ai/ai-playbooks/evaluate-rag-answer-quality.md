---
title: Evaluar calidad de respuestas RAG
description: Un playbook chico para revisar calidad de respuesta, uso de evidencia y ajuste del retrieval.
tags: [playbook, rag, evaluation]
order: 1
updated: 2026-06-07
---
# Evaluar calidad de respuestas RAG

Usá este playbook cuando un prototipo RAG empiece a producir respuestas plausibles y necesite una revisión disciplinada de calidad.

## Pasos

1. Creá 20 preguntas representativas con evidencia esperada.
2. Registrá chunks recuperados, respuesta final, citas y latencia.
3. Puntuá relevancia de retrieval antes de puntuar la respuesta.
4. Marcá fallas como evidencia faltante, evidencia incorrecta, mala síntesis o respuesta insegura.
5. Convertí fallas recurrentes en tests de regresión.

## Salida

Producí una nota corta de evaluación con tasa de aprobación, clusters de falla, ejemplos y el próximo cambio a probar.
