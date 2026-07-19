---
title: Empezá por acá — IA desde primeros principios a producción
description: Cómo navegar AI Atlas, leer matemática, ejecutar labs Glassbox, validar claims y elegir un recorrido.
tags: [orientation, learning-path, atlas]
order: 1
updated: 2026-07-19
kind: playbook
level: beginner
status: current
last_verified: 2026-07-19
---
# Empezá por acá — IA desde primeros principios a producción

AI Atlas es un mapa canónico y ejecutable de sistemas inteligentes. No intenta resumir cada paper: vuelve inspeccionable el cómputo importante, desde representación, supuestos, objetivo, forward pass, loss, gradientes y parámetros aprendidos hasta inferencia, evaluación, comportamiento de producto y operaciones.

La tesis es **de primeros principios a sistemas de producción**. Tenés que poder explicar qué ocurrió dentro de una llamada al modelo, reproducir un mecanismo acotado, medir si funcionó e identificar qué cambió al convertirse en producto.

## Prerequisitos

Necesitás fluidez básica de programación: variables, funciones, loops, tests, command line y lectura de stack traces. Python es el lenguaje principal para labs matemáticos y de modelos; TypeScript aparece cuando agentes, herramientas y límites de producto lo vuelven más claro.

No necesitás matemática avanzada antes de empezar. Sí necesitás frenar cuando la notación no está definida, resolver ejemplos numéricos y no confundir familiaridad visual con comprensión.

## El grafo de aprendizaje

1. Leé las páginas de fase en orden.
2. Ojeá los índices de rama antes de entrar en notas individuales.
3. Seguí prerequisitos antes de saltar a mecanismos avanzados.
4. Ejecutá los labs; predecí el output antes.
5. Compará comportamiento esperado y observado.
6. Registrá fallas, incertidumbre, entorno y versiones.
7. Usá playbooks cuando un concepto deba volverse procedimiento repetible.

```text
formulación del problema
→ datos y representación
→ objetivo y supuestos
→ arquitectura
→ forward computation
→ loss
→ gradientes y optimización
→ representación aprendida
→ inferencia y decoding
→ evaluación
→ comportamiento de producto y operación
```

## Elegí un recorrido

### Primeros Principios

[[ai/mathematics-for-ai/index|Matemática]] → [[ai/computation-and-autodiff/index|computación y autodiff]] → [[ai/deep-learning/index|deep learning]] → [[ai/model-architectures/index|arquitecturas]] → [[ai/llms/index|modelos de lenguaje y fundacionales]]. Usalo si las abstracciones de frameworks todavía parecen magia.

### AI Engineer

[[ai/machine-learning/index|ML Estadístico]] → [[ai/data-for-ai/index|datos]] → [[ai/deep-learning/index|deep learning]] → [[ai/fine-tuning-and-alignment/index|entrenamiento y adaptación]] → [[ai/inference-and-optimization/index|inferencia]] → [[ai/evaluation/index|evaluación]] → [[ai/mlops/index|MLOps]]. Usalo para llevar sistemas desde experimento hasta servicio confiable.

### Sistemas LLM

[[ai/model-architectures/self-attention-from-first-principles|Self-attention]] → [[ai/llms/from-prompt-to-generated-token|prompt a token]] → [[ai/prompt-engineering/index|context engineering]] → [[ai/rag-and-retrieval/index|retrieval]] → [[ai/agents-and-tools/index|agentes]] → [[ai/evaluation/index|evals]] → [[ai/ai-safety-and-security/index|seguridad]]. Usalo si ya construís con APIs pero querés exponer el stack oculto.

### Research Literacy

[[ai/mathematics-for-ai/index|Matemática]] → [[ai/research-and-experimentation/index|lectura y reproducción]] → [[ai/evaluation/nondeterminism-and-reproducibility|reproducibilidad]] → [[ai/interpretability/index|interpretación]] → logs de evidencia. Usalo para evaluar claims en lugar de seguir narrativas de releases.

### Producto y Producción

[[ai/foundations/when-not-to-use-ai|Formulación]] → [[ai/data-for-ai/index|datos]] → baseline → [[ai/evaluation/index|evals]] → [[ai/ai-product-engineering/index|producto]] → deployment → [[ai/mlops/monitoring-and-drift|monitoreo]]. Usalo cuando el éxito es una decisión del usuario, no un score del modelo.

## Cómo leer la matemática

1. Identificá símbolo, tipo y shape.
2. Declará qué queda fijo y qué puede cambiar.
3. Calculá un ejemplo numérico mínimo.
4. Revisá unidades, rangos y normalización.
5. Implementá la operación sin el helper de alto nivel.
6. Compará resultado analítico y chequeo numérico cuando haya derivadas.

Si una nota usa matemática sin permitir estos pasos, tratala como incompleta.

## Cómo usar Glassbox AI Lab

Glassbox AI Lab es el proyecto vertebrador en [[ai/research-and-experimentation/index|Investigación y Experimentación]]. Empezá por `labs/glassbox/README.md`, corré los tests y rompé deliberadamente una invariante. El objetivo no es juntar demos: es conectar una falla observada con un supuesto matemático o de sistema.

Cada milestone completo incluye pregunta, arquitectura, código, fixture o dataset, tests, seed, métricas, expected output, failure modes y postmortem.

## Cómo validar un claim

1. Escribilo lo bastante acotado como para falsarlo.
2. Encontrá el paper, spec, source code o texto legal primario.
3. Registrá fecha, versión, dataset, hardware, métrica y baseline.
4. Separá medición de los autores de tu inferencia.
5. Buscá ablations, intervalos, resultados negativos y contaminación.
6. Reproducí el comportamiento mínimo que importa.
7. Marcá qué sigue incierto.

“State of the art”, “emergent”, “aligned”, “interpretable” y “production-ready” son claims incompletos sin tarea, métrica, comparación, fecha y alcance.

## Labels editoriales

- `kind`: concept, derivation, implementation, system, playbook, paper guide o lab.
- `level`: beginner, intermediate o advanced.
- `status`: current, review-needed, outdated, planned o experimental.
- `last_verified`: hubo revisión real de fuentes y mecanismo; nunca se completa en masa.

## Tu primer loop

Leé [[ai/must-know|Imprescindible]], después [[ai/mathematics-for-ai/vectors-matrices-and-tensors|Vectores, matrices y tensores]], [[ai/mathematics-for-ai/probability-likelihood-and-uncertainty|Probabilidad, likelihood e incertidumbre]], [[ai/mathematics-for-ai/gradient-descent-and-optimization|Gradient Descent y Optimización]] y [[ai/computation-and-autodiff/backpropagation-from-first-principles|Backpropagation desde primeros principios]]. Corré Glassbox v0 y v1. Recién después saltá a [[ai/model-architectures/self-attention-from-first-principles|Self-Attention desde primeros principios]].

**Conecta con:** [[ai/phase-00-orientation|Fase 00 — Orientación]] · [[ai/research-and-experimentation/index|Investigación y Experimentación]] · [[ai/ai-playbooks/index|Playbooks de IA]]

## Fuentes

- [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/) — mapa amplio de IA clásica y estadística.
- [Mathematics for Machine Learning](https://mml-book.github.io/) — matemática conectada con mecanismos de ML.
- [Dive into Deep Learning](https://d2l.ai/) — texto ejecutable con shapes explícitos.
- [Full Stack Deep Learning](https://fullstackdeeplearning.com/) — puente de modelos a producción.
