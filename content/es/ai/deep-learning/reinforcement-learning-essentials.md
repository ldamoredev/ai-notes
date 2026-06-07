---
title: "Reinforcement learning, lo esencial"
description: Aprender desde recompensa en vez de respuestas etiquetadas: agente, entorno, policy y el problema de exploración. El paradigma detrás de RLHF, modelos de razonamiento y agentes.
tags: [reinforcement-learning, rl, policy, reward]
order: 13
updated: 2026-06-07
---
# Reinforcement learning, lo esencial

[[ai/foundations/types-of-learning|El aprendizaje supervisado]] necesita respuestas
etiquetadas. **Reinforcement learning (RL)** aprende de una *señal de recompensa*
actuando y viendo qué funciona: sin clave de respuestas, solo resultados mejores y
peores a lo largo del tiempo. Es el paradigma detrás de
[[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF]],
[[ai/llms/reasoning-and-test-time-compute|modelos de razonamiento]] y aprender
[[ai/agents-and-tools/index|agentes]], así que vale el vocabulario central.

## El setup

Un **agente** toma **acciones** en un **entorno**, que devuelve un nuevo **estado** y
una **recompensa**. El objetivo: aprender una **policy** (un mapeo de estado a acción)
que maximice la recompensa acumulada en el tiempo.

- **Policy** — la estrategia: qué hacer en cada estado.
- **Reward** — la señal escalar de feedback (lo que se maximiza).
- **Value** — recompensa futura esperada desde un estado (¿qué tan bueno es estar acá?).
- **Return** — recompensa total (a menudo descontada) a lo largo de una trayectoria.

El encuadre es un Markov Decision Process; no necesitás la matemática para usar las ideas.

## Qué hace difícil a RL

- **Recompensa demorada / credit assignment** — la recompensa puede llegar mucho después
  de la acción que la ganó; ¿qué movimiento importó realmente?
- **Exploration vs exploitation** — ¿explotar lo que funciona o explorar para encontrar
  algo mejor? Muy poca exploración → quedarse en un pozo; demasiada → nunca converge.
- **Sample efficiency** — RL suele necesitar enormes cantidades de interacción, por eso
  brilla en simuladores/juegos y es más difícil en el mundo real.

## Por qué importa para AI moderna

- **RLHF / alineación por preferencias** — convertir preferencias humanas en una
  recompensa y optimizar el modelo hacia ella ([[ai/fine-tuning-and-alignment/direct-preference-optimization|DPO]]
  reformula esto sin un loop RL separado).
- **Modelos de razonamiento** — entrenados con RL sobre recompensas **verificables**
  (¿la matemática/código salió bien?) para producir largas [[ai/prompt-engineering/chain-of-thought|cadenas
  de pensamiento]].
- **Agentes** — toma de decisiones secuencial bajo feedback es exactamente el marco de
  RL, incluso cuando los agentes actuales están mayormente prompteados en vez de
  entrenados con RL.

## Trampa

**Reward hacking** (un problema de Goodhart): el agente maximiza la recompensa *medida*
de formas no intencionadas; el proxy diverge de lo que realmente querías. Diseñar
recompensas es tan difícil y tan consecuente como diseñar un
[[ai/foundations/how-learning-works|loss]].

**Se conecta con:** [[ai/foundations/types-of-learning|tipos de aprendizaje]] ·
[[ai/fine-tuning-and-alignment/rlhf-with-ppo|RLHF]] ·
[[ai/llms/reasoning-and-test-time-compute|razonamiento y test-time compute]]
