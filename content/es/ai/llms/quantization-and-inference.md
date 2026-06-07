---
title: "Quantization e inferencia"
description: Quantization achica un modelo bajando la precisión numérica, intercambiando un poco de calidad por grandes mejoras de memoria y velocidad. Las bases y las perillas de inferencia que moldean el costo.
tags: [llms, quantization, inference, serving]
order: 11
updated: 2026-06-07
---
# Quantization e inferencia

Un modelo entrenado es una pila de pesos guardados como números. **Quantization** los
guarda con menor precisión (menos bits), achicando memoria y acelerando inferencia:
la razón principal por la que modelos capaces pueden correr en una sola GPU o incluso
en una laptop.

## Qué hace quantization

Los pesos suelen entrenarse en 16-bit (fp16/bf16). Quantization los convierte a menor
precisión:

| Precisión | Tamaño aproximado vs fp16 | Calidad típica |
|---|---|---|
| fp16 / bf16 | baseline | completa |
| int8 / 8-bit | ~½ | casi completa |
| 4-bit (ej. NF4, GPTQ, AWQ) | ~¼ | pérdida chica, a menudo aceptable |

El tradeoff: menor precisión = menos memoria y compute más rápido, con algún costo en
accuracy. 4-bit es un sweet spot popular para correr modelos grandes en hardware
modesto; la pérdida de calidad suele ser moderada pero depende de la tarea:
**medila**. (4-bit también sostiene el fine-tuning
[[ai/fine-tuning-and-alignment/index|QLoRA]].)

## Las palancas de costo en inferencia

Serving está dominado por **ancho de banda y capacidad de memoria** GPU, no solo por
FLOPs. Las perillas que moldean latencia y costo:

- **Quantization**: pesos más chicos, menos tráfico de memoria, más rápido.
- Tamaño de **[[ai/llms/context-window-and-kv-cache|KV cache]]**: crece con contexto y
  batch; suele ser la restricción de memoria vinculante.
- **Batching**: servir muchos requests juntos sube throughput (bueno para costo), pero
  puede subir la latencia por request.
- **Prefill vs decode**: el prompt se procesa en paralelo (prefill); la generación es
  un token por vez (decode), que es la parte lenta.

## Ideas prácticas

- Para self-hosting, quantizá y usá un serving engine (vLLM, TGI) que haga paged KV
  cache + continuous batching.
- "Latencia" se divide en **time-to-first-token** (prefill) y **tokens/second**
  (decode): optimizá la que siente tu [[ai/ai-product-engineering/index|producto]].
- La calidad después de quantization es empírica: benchmarkeá en *tu* tarea antes de
  confiar ([[ai/evaluation/index|eval]]).

**Se conecta con:** [[ai/llms/context-window-and-kv-cache|KV cache]] ·
[[ai/mlops/index|serving]] ·
[[ai/ai-product-engineering/index|latencia y costo]]
