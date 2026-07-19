---
title: "Cuándo no usar AI"
description: La habilidad más senior en AI es reconocer cuándo ML/LLMs son la herramienta equivocada. Dónde reglas, humanos o software más simple le ganan a un modelo, y qué preguntas hacer primero.
tags: [foundations, scoping, judgment, decision]
order: 14
updated: 2026-06-07
---
# Cuándo no usar AI

Saber cuándo *no* recurrir a AI es tan valioso como saber construirla. Los modelos
agregan costo, latencia, [[ai/llms/why-llms-hallucinate|imprevisibilidad]] y carga de
mantenimiento. Si una solución determinística funciona, casi siempre es mejor: más
barata, más rápida, testeable y explicable.

## Preferí algo más simple cuando…

- **Una regla o fórmula alcanza.** Si la lógica es conocida y estable ("marcar órdenes
  de más de $10k"), escribí la regla. ML para reaprender una regla conocida es complejidad desperdiciada.
- **No podés tolerar equivocarte.** ML es probabilístico; para tareas que necesitan
  corrección garantizada (contabilidad, interlocks de seguridad), usá código
  determinístico, con AI como mucho asistiendo a un humano.
- **No hay datos** (ML supervisado) o no hay forma de verificar outputs (generativo).
  Sin [[ai/foundations/how-learning-works|señal]] de entrada, no sale nada confiable.
- **El riesgo es alto y no está monitoreado.** Alto blast radius + sin
  [[ai/agents-and-tools/guardrails-and-human-in-the-loop|supervisión humana]] es donde
  las fallas de AI se vuelven incidentes.
- **La explainability es obligatoria** (algunos contextos legales/médicos/crediticios) y
  el modelo no puede proveerla ([[ai/ai-ethics-and-governance/transparency-and-explainability|transparencia]]).
- **Una heurística te da 90%** al 1% del costo y esfuerzo: desplegá eso primero.

## Preguntas antes de agregar un modelo

1. ¿Qué decisión impulsa el output, y cuánto cuesta una respuesta equivocada?
2. ¿Una regla, lookup o software existente podría hacerlo aceptablemente?
3. ¿Hay datos / una forma de evaluar calidad? ([[ai/evaluation/index|Si no podés evaluarlo, no podés confiar en él.]])
4. ¿Podemos tolerar variabilidad y algún error confiado ocasional?
5. ¿Quién es responsable cuando se equivoca, y puede atraparlo un humano?

## El matiz para LLMs

Los LLMs bajaron la barrera: podés "resolver" una tarea con un prompt y sin datos de
entrenamiento. Eso vuelve tentador usarlos *en todas partes*, incluso donde una regex,
una consulta a base de datos o un formulario serían más confiables y mucho más baratos.
Usá el LLM para la parte genuinamente difusa y con forma de lenguaje; usá software común
para el resto.

## Trampa

"AI" como mandato en vez de herramienta: agregar un modelo porque se espera, y después
heredar alucinaciones, costo y latencia para resolver un problema que el código
determinístico ya resolvía. Empezá por el problema, no por la tecnología.

**Conecta con:** [[ai/foundations/mental-models-for-ai|modelos mentales para sistemas de AI]] ·
[[ai/machine-learning/supervised-learning-workflow|encuadrar el problema]] ·
[[ai/ai-product-engineering/the-ai-application-stack|el stack más chico que funciona]]
