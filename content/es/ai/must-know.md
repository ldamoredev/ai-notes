---
title: Imprescindible — Doce reglas para pensar con claridad sobre IA
description: Doce reglas first-principles sobre objetivos, datos, incertidumbre, evaluación, deployment, agentes y oversight.
tags: [orientation, fundamentals, vocabulary]
order: 2
updated: 2026-07-19
kind: concept
level: beginner
status: current
last_verified: 2026-07-19
---
# Imprescindible — Doce reglas para pensar con claridad sobre IA

La alfabetización mínima en IA no es una lista de tools. Es un conjunto de restricciones sobre qué podés afirmar de un sistema.

## 1. La IA no es magia

Un modelo computa una función parametrizada. Aunque sea enorme, el camino sigue siendo inputs → representaciones → operaciones → outputs. Training agrega objetivo, señal de error, derivadas u otra regla de update y datos. Si una explicación saltea esos objetos, ocultó el mecanismo.

## 2. Los modelos optimizan objetivos

Un sistema mejora aquello que recompensa su proceso de training y selección, no “inteligencia” en general. Cross-entropy, preference scores, rewards, rankings y elecciones humanas son proxies. Cuando un proxy se vuelve target, el comportamiento puede explotar la brecha.

Preguntá: ¿qué escalar u ordenamiento seleccionó estos parámetros, outputs o policies?

## 3. Los datos definen comportamiento

Los datos determinan cobertura, correlaciones, labels, omisiones y daños. Arquitectura y escala no recuperan evidencia ausente ni distinguen una correlación espuria sin señal útil. Construir el dataset es especificar parte del modelo.

Preguntá: ¿qué población, período, muestreo, política de anotación y contaminación produjo los ejemplos?

## 4. La generalización es empírica

Training error bajo no prueba performance en casos nuevos. Generalizar depende de train data, sesgo inductivo, capacidad, regularización, selección y distribución de deployment. Medí sobre datos que representen la decisión real.

Preguntá: ¿no visto respecto de qué proceso y con qué intervalo de confianza?

## 5. Correlación no es causalidad

Una asociación predictiva puede servir sin identificar un efecto de intervención. Datos observacionales contienen proxies y confounders. No conviertas feature importance, attention o un score alto en relato causal sin diseño causal.

Preguntá: ¿qué intervención o supuesto de identificación justifica lenguaje causal?

## 6. Los benchmarks son parciales

Un benchmark es dataset, protocolo, métrica y comparación fechada. Puede saturarse, filtrarse al training, premiar atajos u omitir restricciones de producto. Un ranking prueba algo sobre ese protocolo, no una capacidad universal.

Preguntá: versión, protocolo, contaminación, presupuesto de cómputo, incertidumbre y relevancia para la tarea.

## 7. Los modelos generativos modelan distribuciones

Un LLM autoregresivo estima una distribución condicional del siguiente token. Un diffusion model aprende un proceso de denoising relacionado con la distribución de datos. Sampling elige un output posible. Fluidez y error factual son compatibles porque likelihood y verdad son objetivos distintos.

Preguntá: ¿qué distribución representa, cómo se samplea y qué evidencia externa lo restringe?

## 8. Confianza no es verdad

La probabilidad de token no es confianza factual calibrada. Un score de clasificación también pierde calibración bajo shift. Calibración es una relación empírica entre confianza predicha y frecuencia observada para una población definida.

Preguntá: ¿confianza en qué evento, calibrada dónde y verificada cuándo?

## 9. La evaluación debe coincidir con el producto

Calidad offline es un componente. Evaluá retrieval, tools, latencia, costo, abstención, seguridad, comprensión del usuario, decisiones downstream y recuperación. Un benchmark puede mejorar mientras empeora el producto.

Preguntá: ¿qué decisión del usuario o resultado operativo representa la métrica?

## 10. El deployment cambia el sistema

Usuarios se adaptan, adversarios prueban, tráfico cambia, feedback loops reforman datos e infraestructura falla. Prompts, modelos, datasets, índices, tools, policies y UI son componentes versionados. Monitoreo y rollback son parte de correctness.

Preguntá: ¿qué detecta degradación, quién atiende la alerta y cuál es el fallback seguro?

## 11. Tools y agentes expanden la superficie de ataque

Un modelo que lee contenido no confiable e invoca tools conecta interpretación probabilística con autoridad real. Prompt injection, excessive agency, confused deputy, retries no idempotentes y outputs inseguros pasan a ser riesgos de sistema. Capacidad y permiso deben estar separados.

Preguntá: ¿qué puede leer, decidir, escribir, gastar, enviar o borrar el agente, y dónde se impone aprobación fuera del modelo?

## 12. El oversight humano debe diseñarse

“Hay un humano en el loop” no es control si esa persona no tiene tiempo, contexto, autoridad, interfaz usable y escalamiento. Automation bias y alert fatigue pueden volverlo peor que un stop automático explícito.

Preguntá: ¿qué evidencia ve, qué puede hacer, qué pasa en timeout y cómo se registra desacuerdo?

## Checklist compacto

1. Problema y decisión.
2. Representación y provenance.
3. Supuestos y objetivo.
4. Forward computation y parámetros.
5. Inferencia y decoding.
6. Evaluación e incertidumbre.
7. Failure modes y adversarios.
8. Latencia, costo, observabilidad y fallback.
9. Responsabilidad humana y rollback.

Si varias entradas son desconocidas, el sistema todavía no está entendido.

**Conecta con:** [[ai/start-here|Empezá por acá]] · [[ai/foundations/mental-models-for-ai|Modelos Mentales para Sistemas de IA]] · [[ai/evaluation/index|Evaluación y Medición]] · [[ai/ai-safety-and-security/index|Seguridad de IA]]

## Fuentes

- [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) — claim histórico sobre métodos generales y cómputo; leelo críticamente.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — mapear, medir, gestionar y gobernar riesgo.
- [Model Cards](https://arxiv.org/abs/1810.03993) — intended use, evaluación y límites.
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565) — especificación, robustez y oversight como problemas técnicos.
