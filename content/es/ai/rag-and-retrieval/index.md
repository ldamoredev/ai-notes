---
title: Retrieval y Conocimiento
description: Corpus, chunking, embeddings, búsqueda híbrida, reranking, grounding, citas y evaluación RAG.
tags: [rag, retrieval]
order: 0
updated: 2026-07-19
---
# Retrieval y Conocimiento

RAG es un sistema de recuperación cuya evidencia seleccionada se convierte en input del modelo. Consulta, índice, candidates, reranking, armado de contexto y respuesta son etapas con presupuestos de recall, precisión, costo y latencia distintos.

## Modelo mental

Depurá retrieval antes que generación. Si la evidencia necesaria no entra al contexto, el generador no puede recuperarla con prompting.

## Hoja de ruta

- [[ai/rag-and-retrieval/why-rag|Por qué usar RAG]]
- [[ai/rag-and-retrieval/chunking|Chunking]]
- [[ai/rag-and-retrieval/embeddings-for-retrieval|Embeddings para retrieval]]
- [[ai/rag-and-retrieval/hybrid-search|Búsqueda híbrida]]
- [[ai/rag-and-retrieval/reranking|Reranking]]
- [[ai/rag-and-retrieval/evaluating-rag|Evaluar RAG]]

**Conecta con:** [[ai/data-for-ai/index|Datos para IA]] · [[ai/prompt-engineering/index|Context Engineering]] · [[ai/evaluation/evaluating-rag-systems|Evaluar Sistemas RAG]]

## Fuentes principales

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — factorización original retriever-generador.
- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — técnica aplicada y mediciones.
- [RAGAS](https://docs.ragas.io/) — métricas de faithfulness, context precision y recall.
- [pgvector](https://github.com/pgvector/pgvector) — vector search y tuning ANN en PostgreSQL.
