---
title: Context Engineering
description: Diseñar instrucciones, ejemplos, estructura, memoria y contexto ensamblado para producir comportamiento verificable de modelos.
tags: [prompting, context-engineering, structured-output]
order: 0
updated: 2026-07-19
---
# Context Engineering

Un prompt es una parte del contexto. El sistema real ensambla instrucciones, ejemplos, datos recuperados, estado, tool results y presupuesto de tokens; el orden, formato y autoridad de cada parte cambian el comportamiento.

## Modelo mental

Context engineering construye el entorno temporal de información del modelo. Cada fragmento compite dentro de una ventana finita y tiene que conservar procedencia, autoridad y prioridad explícitas.

## Hoja de ruta

- [[ai/prompt-engineering/prompt-to-context-engineering|De prompting a context engineering]]
- [[ai/prompt-engineering/anatomy-of-a-prompt|Anatomía de un buen prompt]]
- [[ai/prompt-engineering/system-prompts-and-roles|System prompts y roles]]
- [[ai/prompt-engineering/zero-and-few-shot|Zero-shot y few-shot]]
- [[ai/prompt-engineering/structured-outputs|Structured outputs]]
- [[ai/prompt-engineering/assembling-context|Armado de contexto]]
- [[ai/prompt-engineering/managing-the-context-window|Gestión de la ventana de contexto]]
- [[ai/prompt-engineering/memory-and-history|Memoria e historial]]
- [[ai/prompt-engineering/task-decomposition|Descomposición de tareas]]
- [[ai/prompt-engineering/chain-of-thought|Chain-of-thought y límites]]
- [[ai/prompt-engineering/self-consistency-and-sampling|Self-consistency y sampling]]
- [[ai/prompt-engineering/evaluating-and-iterating-prompts|Evaluar e iterar prompts]]

**Conecta con:** [[ai/rag-and-retrieval/index|Retrieval y Conocimiento]] · [[ai/agents-and-tools/index|Agentes y Herramientas]] · [[ai/ai-safety-and-security/indirect-prompt-injection|Prompt injection indirecta]]

## Fuentes principales

- [Anthropic prompting docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — técnicas y límites documentados por el proveedor.
- [OpenAI Cookbook](https://cookbook.openai.com/) — patrones ejecutables para structured outputs y evals.
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) — paper primario sobre demostraciones de razonamiento.
