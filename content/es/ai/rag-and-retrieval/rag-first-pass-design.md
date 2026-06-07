---
title: Diseño RAG de primera pasada
description: Una checklist chica para diseñar un primer sistema RAG útil.
tags: [rag, retrieval, engineering]
order: 1
updated: 2026-06-07
---
# Diseño RAG de primera pasada

Un primer sistema RAG debería optimizar inspectabilidad antes que ingenio. Si no podés explicar de dónde salió una respuesta, no podés evaluarla.

## Diseño mínimo

1. Definí el conjunto de preguntas respondibles.
2. Elegí documentos fuente y reglas de ownership.
3. Elegí límites de chunks que preserven significado.
4. Guardá citas junto con los chunks recuperados.
5. Evaluá retrieval separado de la calidad de la respuesta final.

## Señales de falla

Prestá atención a respuestas correctas en apariencia pero sin citas, hits de retrieval semánticamente cercanos pero irrelevantes para la tarea, y prompts que ocultan evidencia en vez de exponerla.
