---
title: "Long context y lost in the middle"
description: Una ventana de 200K tokens no significa que el modelo use todo bien. Por qué los modelos atienden mejor al inicio y al final, y qué hacer con eso.
tags: [llms, long-context, retrieval, context-engineering]
order: 10
updated: 2026-06-07
---
# Long context y lost in the middle

Las ventanas de contexto explotaron: cientos de miles de tokens, a veces millones.
Pero **una ventana grande no es lo mismo que usarla bien**. Los modelos subatienden
de manera confiable el medio de inputs largos, así que "meter todo adentro" es una
trampa.

## Lost in the middle

En muchos modelos, la precisión sobre un hecho ubicado en un contexto largo tiene
forma de **U**: alta cuando la información relevante está cerca del **inicio** o el
**final**, y notablemente más baja cuando está enterrada en el **medio**. Un modelo
puede tener una ventana de 200K y aun así "perderse" una oración en la posición 100K.
La ventana es la *capacidad*, no una garantía de attention.

Una preocupación relacionada y más nueva es **context rot**: a medida que los inputs
se vuelven muy largos, la confiabilidad general deriva hacia abajo aunque la respuesta
esté técnicamente presente.

## Por qué pasa

Los datos de entrenamiento tienen muchos menos documentos genuinamente largos y de
importancia uniforme que documentos cortos, y los efectos
[[ai/llms/positional-encodings|posicionales]] + la dilución de attention hacen que la
saliencia se concentre en los bordes. El modelo aprendió que los inicios y finales
llevan más señal.

## Qué hacer

- **Recuperá y después ubicá bien**: usá [[ai/rag-and-retrieval/index|RAG]] para traer
  solo lo relevante en vez de volcar todo; poné el contexto más importante al
  **inicio o final**, no en el medio.
- **Comprimí**: resumí historial y material vencido; mantené la ventana densa en señal
  ([[ai/prompt-engineering/index|context engineering]]).
- **[[ai/rag-and-retrieval/reranking|Rerankeá]]** para que los mejores chunks
  queden en las posiciones de alta attention.
- **No pagues por contexto que no necesitás**: más tokens = más
  [[ai/llms/context-window-and-kv-cache|costo y latencia]] para resultados a menudo
  *peores*.

> Tratá la ventana de contexto como espacio caro y sesgado por attention, no como un
> balde. Curación le gana a capacidad.

**Conecta con:** [[ai/llms/context-window-and-kv-cache|ventana de contexto]] ·
[[ai/rag-and-retrieval/index|retrieval y reranking]] ·
[[ai/prompt-engineering/index|context engineering]]
