---
title: "El mecanismo de attention"
description: Attention es un lookup aprendido y basado en contenido: cada posición trae información de las posiciones más relevantes para ella. La idea central detrás de todo transformer.
tags: [deep-learning, attention, transformers, qkv]
order: 8
updated: 2026-06-07
---
# El mecanismo de attention

Attention es la idea más importante del deep learning moderno. La intuición: en vez de
forzar información a través de un [[ai/deep-learning/rnns-and-their-limits|estado
recurrente]] de tamaño fijo, dejá que cada posición **mire y traiga desde todas las
otras posiciones**, ponderándolas por relevancia. Es una tabla de lookup suave y aprendible.

## Query, Key, Value

Cada token produce tres vectores (mediante [[ai/foundations/linear-algebra-for-ml|proyecciones
matriciales]] aprendidas):

- **Query** — qué está buscando este token.
- **Key** — qué ofrece cada token / contra qué se puede matchear.
- **Value** — la información que aporta un token si se le presta atención.

El mecanismo: comparar la query de un token contra **todas** las keys (un
[[ai/foundations/linear-algebra-for-ml|producto punto]] = score de relevancia), pasar
los scores por softmax para convertirlos en pesos y después tomar la suma ponderada de
los values. El output de cada token es una mezcla de los values que encontró más relevantes.

> Attention = "para cada token, recuperar suavemente una mezcla ponderada de información
> desde los tokens que le importan". Un lookup diferenciable direccionado por contenido.

## Por qué es potente

- **Enlaces directos de largo alcance** — el token 500 puede atender al token 1 en un
  salto; no hay cadena que se desvanezca.
- **Paralelo** — todas las posiciones se computan a la vez (ideal para GPUs).
- **Dinámico** — el "cableado" depende del contenido, no de una estructura fija.

## Multi-head attention

Corré varias operaciones de attention en paralelo ("heads"), cada una con sus propias
proyecciones. Distintas heads se especializan: una sigue sintaxis, otra correferencia,
otra posición, y sus outputs se concatenan. Más heads = más tipos de relaciones
capturadas al mismo tiempo.

## La contra

Comparar cada token con cada token es **cuadrático** en la longitud de secuencia (n²),
por eso el contexto largo es caro y por eso importan el [[ai/llms/index|KV cache]] y la
investigación en attention eficiente. Este costo es la restricción central de escalado
de los transformers.

Este mecanismo, apilado con capas feed-forward y
[[ai/deep-learning/initialization-and-normalization|LayerNorm]], **es** el transformer:
ver [[ai/llms/index|LLMs]].

**Se conecta con:** [[ai/deep-learning/rnns-and-their-limits|por qué venció a las RNNs]] ·
[[ai/foundations/linear-algebra-for-ml|similitud por producto punto]] ·
[[ai/llms/index|el transformer]]
