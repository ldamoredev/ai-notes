---
title: "Ventana de contexto y KV cache"
description: La ventana de contexto es la memoria de trabajo del modelo; el KV cache es lo que vuelve rápida la generación. Ambos explican por qué los prompts largos cuestan más y por qué la latencia se comporta así.
tags: [llms, context-window, kv-cache, inference]
order: 5
updated: 2026-06-07
---
# Ventana de contexto y KV cache

La **ventana de contexto** es todo lo que el modelo puede "ver" a la vez: system
prompt, historial, documentos recuperados, el mensaje del usuario y los tokens que ya
generó. Es toda la memoria de trabajo del modelo; nada fuera de ella existe para el
modelo.

## La ventana es un presupuesto duro

Medida en [[ai/llms/tokenization|tokens]], la ventana es finita (desde unos pocos K
hasta ~1M según el modelo). Todo compite por ella: instrucciones, ejemplos few-shot,
[[ai/rag-and-retrieval/index|contexto recuperado]] y la conversación en curso. Cuando
se llena, algo debe descartarse o resumirse: ese es todo el trabajo de
[[ai/prompt-engineering/index|context engineering]]. El modelo **no tiene memoria entre
llamadas**; la persistencia es algo que *vos* diseñás poniendo de nuevo las cosas
correctas en la ventana.

## El KV cache: por qué la generación es rápida

La generación es autoregresiva: un token por vez, cada uno condicionado por todos los
anteriores. Ingenuamente, cada token nuevo tendría que reprocesar toda la secuencia.
El **KV cache** guarda las Keys y Values de attention ya calculadas para tokens
previos, así cada paso nuevo solo calcula attention para el *nuevo* token contra el
pasado cacheado. Sin eso, las generaciones largas serían insoportablemente lentas.

El costo: el cache **crece con la longitud de secuencia** y consume memoria GPU; a
menudo ese es el límite real de cuán largo puede ser el contexto que servís y cuántos
requests entran en una GPU. Por eso los contextos largos son caros tanto en latencia
como en dinero.

## Implicancias prácticas

- **Prompt caching**: los providers pueden cachear el KV de un prefijo estable (un
  system prompt o documento largo), así las llamadas repetidas evitan recalcularlo:
  más barato y rápido. Poné lo estable primero.
- **Más contexto ≠ mejor**: más allá del costo, la calidad se degrada
  ([[ai/llms/long-context-and-lost-in-the-middle|lost in the middle]]). Curá, no
  vuelques todo.
- El costo cuadrático de [[ai/deep-learning/attention-mechanism|attention]] es la
  razón por la que todo esto importa.

**Se conecta con:** [[ai/llms/tokenization|presupuesto de tokens]] ·
[[ai/llms/long-context-and-lost-in-the-middle|límites de long context]] ·
[[ai/prompt-engineering/index|context engineering]]
