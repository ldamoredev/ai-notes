---
title: "Tokenization: por qué los modelos ven tokens, no palabras"
description: Los LLMs leen subword tokens, no caracteres ni palabras. Cómo funciona BPE, por qué explica fallas raras (ortografía, matemática, costo fuera del inglés) y la economía de tokens.
tags: [llms, tokenization, bpe, tokens]
order: 2
updated: 2026-06-07
---
# Tokenization: por qué los modelos ven tokens, no palabras

Un LLM nunca ve texto: ve una secuencia de **IDs de tokens** enteros. Tokenization es
la capa de traducción, y una cantidad sorprendente de comportamientos "raros" de los
LLMs se rastrean directamente hasta ella.

## Por qué subwords (BPE)

Los caracteres hacen que las secuencias sean demasiado largas; las palabras completas
hacen que el vocabulario sea enorme y se atragante con palabras raras/nuevas.
**Byte-Pair Encoding (BPE)** parte la diferencia: arranca desde caracteres y fusiona
codiciosamente los pares más frecuentes hasta tener un vocabulario de piezas subword.
Las palabras comunes se vuelven un token; las raras se dividen en partes ("tokeniz",
"ation"). Esto maneja cualquier input, incluso palabras nunca vistas en entrenamiento.

## Qué explica tokenization

- **Fallan tareas de ortografía/caracteres** ("¿cuántas r hay en strawberry?"): el
  modelo ve un token, no letras, así que razonar a nivel carácter le resulta poco
  natural.
- **La aritmética es inestable**: los números se tokenizan de forma inconsistente
  ("1234" puede ser un token, "1235" varios), así que los dígitos no se alinean limpio.
- **Los idiomas no ingleses cuestan más**: los tokenizers se entrenan mayormente en
  inglés, así que otros idiomas se fragmentan en más tokens → más costo y contexto
  efectivo menor.
- **Espacios finales / formatos raros** pueden cambiar la tokenization y mover las
  salidas.

## Economía de tokens

Pagás (en dinero, latencia y [[ai/llms/context-window-and-kv-cache|presupuesto de contexto]])
**por token**, no por palabra. Regla mental aproximada: ~1 token ≈ 4 caracteres ≈ ¾
de palabra en inglés. Estimar cantidad de tokens es esencial para costo y para entrar
en la [[ai/llms/context-window-and-kv-cache|ventana de contexto]].

## Trampa

Los límites de tokens son invisibles pero tienen consecuencias. Cuando un prompt se
comporta raro con números, código o texto no inglés, sospechá de tokenization antes
que de la "inteligencia" del modelo.

**Se conecta con:** [[ai/llms/the-decoder-transformer|la arquitectura]] ·
[[ai/llms/context-window-and-kv-cache|presupuesto de contexto]] ·
[[ai/ai-product-engineering/index|costo por token]]
