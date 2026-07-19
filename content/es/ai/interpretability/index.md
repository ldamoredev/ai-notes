---
title: Interpretabilidad
description: Métodos para investigar decisiones y representaciones internas sin confundir explicaciones plausibles con mecanismos fieles.
tags: [interpretability, explainability, representations, causality]
order: 0
updated: 2026-07-19
status: planned
level: intermediate
---
# Interpretabilidad

Interpretabilidad pregunta qué evidencia sostiene un claim sobre comportamiento o cómputo interno. Una explicación plausible no es automáticamente fiel al mecanismo que produjo el output.

## Modelo mental

Empezá por la pregunta y la unidad de análisis: feature, ejemplo, neurona, dirección de activación, representación, circuito o camino causal. Elegí un método observacional o de intervención cuyos límites coincidan con el claim y validalo con controles y efectos conductuales.

## Roadmap

Feature importance · LIME y SHAP · saliency e Integrated Gradients · probes · activaciones y steering · mechanistic interpretability · circuits · sparse autoencoders · intervenciones causales · faithfulness y explanation theater.

## Límite

Interpretabilidad no prueba por sí sola safety, fairness, verdad o causalidad en el mundo. Puede generar y testear hipótesis sobre un modelo bajo intervenciones concretas.

**Conecta con:** [[ai/evaluation/systematic-error-analysis|Análisis sistemático de errores]] · [[ai/ai-ethics-and-governance/transparency-and-explainability|Transparencia y explicabilidad]] · [[ai/ai-safety-and-security/red-teaming-ai-systems|Red teaming de sistemas de IA]]

## Fuentes principales

- [SHAP](https://arxiv.org/abs/1705.07874) — framing formal de atribución.
- [Integrated Gradients](https://arxiv.org/abs/1703.01365) — axiomas y método.
- [Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) — descomposición mecanicista fundacional.
