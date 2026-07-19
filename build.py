#!/usr/bin/env python3
"""Build AI Atlas as a static bilingual knowledge site.

The canonical notes live in content/en/. Translated overlays live in
content/<locale>/ with the same relative paths. The generated site is written
to site/<locale>/ plus a small language landing page at site/index.html.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_ROOT = ROOT / "content"
CANONICAL_CONTENT = CONTENT_ROOT / "en"
STATIC = ROOT / "static"
OUT = ROOT / "site"

SECTION = "ai"
LOCALES = ("en", "es")
DEFAULT_LOCALE = "en"
CURRENT_LOCALE = DEFAULT_LOCALE

SITE_NAME = "AI Atlas"
SITE_SHORT_NAME = "AI Atlas"
SITE_AUTHOR = "Lautaro Damore"
SITE_URL = os.environ.get("SITE_URL", "https://ldamoredev.github.io/ai-notes").rstrip("/")
GITHUB_URL = os.environ.get("GITHUB_URL", "https://github.com/ldamoredev/ai-notes")
THEME_COLOR = "#31C7D9"

SITE_DESCRIPTION = (
    "AI from first principles to production systems: mathematics, learning mechanics, "
    "models, evaluation, safety, infrastructure, and reproducible Glassbox labs."
)
SITE_DESCRIPTION_ES = (
    "IA desde primeros principios hasta sistemas de producción: matemática, mecanismos "
    "de aprendizaje, modelos, evaluación, seguridad, infraestructura y labs Glassbox reproducibles."
)
SITE_KEYWORDS = [
    "AI",
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "large language models",
    "RAG",
    "agents",
    "AI evaluation",
    "AI safety",
    "MLOps",
    "automatic differentiation",
    "reinforcement learning",
    "interpretability",
    "AI systems",
]

OG_LOCALE = {"en": "en_US", "es": "es_ES"}
LOCALE_LABEL = {"en": "EN", "es": "ES"}
LOCALE_NAME = {"en": "English", "es": "Español"}

PHASES = (
    {
        "key": "Orientation",
        "num": "00",
        "href": "ai/phase-00-orientation.html",
        "icon": "compass",
    },
    {
        "key": "Foundations",
        "num": "01",
        "href": "ai/phase-01-foundations.html",
        "icon": "layers",
    },
    {
        "key": "Learning",
        "num": "02",
        "href": "ai/phase-02-learning-and-models.html",
        "icon": "nodes",
    },
    {
        "key": "Training",
        "num": "03",
        "href": "ai/phase-03-training-and-inference.html",
        "icon": "chip",
    },
    {
        "key": "Context",
        "num": "04",
        "href": "ai/phase-04-context-and-agency.html",
        "icon": "workflow",
    },
    {
        "key": "Measurement",
        "num": "05",
        "href": "ai/phase-05-measurement-and-trust.html",
        "icon": "gauge",
    },
    {
        "key": "Operations",
        "num": "06",
        "href": "ai/phase-06-product-and-operations.html",
        "icon": "terminal",
    },
    {
        "key": "Always-on",
        "num": "★",
        "href": "ai/phase-always-active.html",
        "icon": "spark",
    },
)
PHASE_KEYS = tuple(p["key"] for p in PHASES)

# Cards shown in the Orientation phase section on the home page. Orientation has
# no branches, so it surfaces the entry-layer notes instead of a branch grid.
# (root slug, icon, accent)
ORIENTATION_ENTRY_CARDS = (
    ("start-here", "compass", "cyan"),
    ("must-know", "spark", "violet"),
    ("index", "nodes", "sky"),
)

# Old canonical IDs resolve during Markdown rendering and generate redirect stubs.
# Keys and values intentionally omit extensions and locale prefixes.
LEGACY_REDIRECTS = {
    "ai/foundations/linear-algebra-for-ml": "ai/mathematics-for-ai/vectors-matrices-and-tensors",
    "ai/foundations/probability-and-uncertainty": "ai/mathematics-for-ai/probability-likelihood-and-uncertainty",
    "ai/foundations/gradient-descent-intuition": "ai/mathematics-for-ai/gradient-descent-and-optimization",
    "ai/foundations/information-theory-basics": "ai/mathematics-for-ai/information-theory-entropy-and-divergence",
    "ai/deep-learning/neural-networks-and-backprop": "ai/computation-and-autodiff/backpropagation-from-first-principles",
    "ai/deep-learning/reinforcement-learning-essentials": "ai/reinforcement-learning/reinforcement-learning-essentials",
    "ai/deep-learning/attention-mechanism": "ai/model-architectures/self-attention-from-first-principles",
    "ai/phase-02-models-and-architectures": "ai/phase-02-learning-and-models",
    "ai/phase-03-building-and-engineering": "ai/phase-03-training-and-inference",
    "ai/phase-04-evaluation-and-security": "ai/phase-05-measurement-and-trust",
}

LEARNING_PATHS = {
    "en": (
        ("First Principles", "Math → probability → optimization → autodiff → neural networks → transformers", "mathematics-for-ai"),
        ("AI Engineer", "ML → deep learning → data → training → inference → evaluation → MLOps", "machine-learning"),
        ("LLM Systems", "Transformers → language models → context → retrieval → agents → evals → security", "model-architectures"),
        ("Research Literacy", "Math → papers → reproduction → experiments → interpretation → evidence", "research-and-experimentation"),
        ("Product & Production", "Problem framing → data → baseline → evals → product → deployment → monitoring", "ai-product-engineering"),
    ),
    "es": (
        ("Primeros Principios", "Matemática → probabilidad → optimización → autodiff → redes neuronales → transformers", "mathematics-for-ai"),
        ("AI Engineer", "ML → deep learning → datos → entrenamiento → inferencia → evaluación → MLOps", "machine-learning"),
        ("Sistemas LLM", "Transformers → modelos de lenguaje → contexto → retrieval → agentes → evals → seguridad", "model-architectures"),
        ("Alfabetización Científica", "Matemática → papers → reproducción → experimentos → interpretación → evidencia", "research-and-experimentation"),
        ("Producto y Producción", "Problema → datos → baseline → evals → producto → deployment → monitoreo", "ai-product-engineering"),
    ),
}

GLASSBOX_ROADMAP = (
    ("v0", "Numbers, vectors & probability", "Números, vectores y probabilidad", "CURRENT", ("mathematics-for-ai",)),
    ("v1", "Autodiff from scratch", "Autodiff desde cero", "CURRENT", ("computation-and-autodiff",)),
    ("v2", "Neural network from scratch", "Red neuronal desde cero", "PLANNED", ("deep-learning",)),
    ("v3", "Tensor framework & image model", "Framework de tensores y modelo de imagen", "PLANNED", ("deep-learning", "multimodal-and-generative")),
    ("v4", "Tokenizer & mini-transformer", "Tokenizer y mini-transformer", "EXPERIMENTAL", ("model-architectures", "llms")),
    ("v5", "Training & adaptation", "Entrenamiento y adaptación", "PLANNED", ("fine-tuning-and-alignment",)),
    ("v6", "Inference runtime", "Runtime de inferencia", "PLANNED", ("inference-and-optimization",)),
    ("v7", "Retrieval system", "Sistema de retrieval", "PLANNED", ("rag-and-retrieval",)),
    ("v8", "Tool-using agent", "Agente que usa herramientas", "PLANNED", ("agents-and-tools",)),
    ("v9", "Multimodal pipeline", "Pipeline multimodal", "PLANNED", ("multimodal-and-generative",)),
    ("v10", "Production AI system", "Sistema de IA en producción", "PLANNED", ("mlops", "ai-product-engineering")),
)

RELATED_ATLASES = (
    ("Low-Level", "https://ldamoredev.github.io/lowlevel-notes/", "https://github.com/ldamoredev/lowlevel-notes"),
    ("WebAssembly AI", "https://ldamoredev.github.io/wasm-ai-notes/", "https://github.com/ldamoredev/wasm-ai-notes"),
    ("Blockchain Engineering", "https://ldamoredev.github.io/blockchain-notes/", "https://github.com/ldamoredev/blockchain-notes"),
)

BRANCHES = {
    "mathematics-for-ai": {
        "label": "Mathematics for AI",
        "group": "Foundations",
        "summary": "Linear algebra, calculus, probability, statistics, information theory, optimization, and numerical stability.",
        "accent": "cyan",
        "icon": "chart",
        "editorial_status": "CURRENT",
    },
    "computation-and-autodiff": {
        "label": "Computation & Autodiff",
        "group": "Foundations",
        "summary": "Tensors as arrays, vectorization, compute graphs, reverse-mode autodiff, floating point, parallelism, and reproducibility.",
        "accent": "amber",
        "icon": "chip",
        "editorial_status": "CURRENT",
    },
    "classical-ai-and-reasoning": {
        "label": "Classical AI & Reasoning",
        "group": "Foundations",
        "summary": "Search, heuristics, constraints, planning, logic, knowledge representation, probabilistic reasoning, and decision theory.",
        "accent": "indigo",
        "icon": "workflow",
        "editorial_status": "PLANNED",
    },
    "foundations": {
        "label": "Learning Foundations",
        "group": "Foundations",
        "summary": "Problem formulation, generalization, inductive bias, distribution shift, leakage, metrics, and when learning is the wrong tool.",
        "accent": "sky",
        "icon": "book",
        "editorial_status": "REVIEW NEEDED",
    },
    "machine-learning": {
        "label": "Statistical Machine Learning",
        "group": "Foundations",
        "summary": "Regression, classification, trees, ensembles, kernels, clustering, dimensionality reduction, calibration, and error analysis.",
        "accent": "indigo",
        "icon": "chart",
        "editorial_status": "REVIEW NEEDED",
    },
    "data-for-ai": {
        "label": "Data for AI",
        "group": "Foundations",
        "summary": "Data-centric AI: quality, labeling, dataset design, synthetic data, contamination, documentation, and pipelines.",
        "accent": "slate",
        "icon": "database",
        "editorial_status": "REVIEW NEEDED",
    },
    "deep-learning": {
        "label": "Deep Learning",
        "group": "Learning",
        "summary": "Neural networks, representation learning, optimization, embeddings, and scaling behavior.",
        "accent": "violet",
        "icon": "layers",
        "editorial_status": "REVIEW NEEDED",
    },
    "reinforcement-learning": {
        "label": "Reinforcement Learning",
        "group": "Learning",
        "summary": "Sequential decisions, Bellman equations, value learning, policy gradients, exploration, offline RL, world models, and alignment links.",
        "accent": "emerald",
        "icon": "workflow",
        "editorial_status": "PLANNED",
    },
    "model-architectures": {
        "label": "Model Architectures",
        "group": "Learning",
        "summary": "CNNs, sequence models, attention, transformers, mixture of experts, state-space models, diffusion, and architectural trade-offs.",
        "accent": "violet",
        "icon": "nodes",
        "editorial_status": "CURRENT",
    },
    "llms": {
        "label": "Language & Foundation Models",
        "group": "Learning",
        "summary": "Tokenization, decoder transformers, pretraining, data mixtures, scaling, decoding, instruction tuning, reasoning behavior, and model families.",
        "accent": "sky",
        "icon": "nodes",
        "editorial_status": "REVIEW NEEDED",
    },
    "multimodal-and-generative": {
        "label": "Vision, Audio & Multimodal AI",
        "group": "Learning",
        "summary": "Images, vision models, detection, segmentation, speech, multimodal fusion, diffusion, video, evaluation, data, and safety.",
        "accent": "fuchsia",
        "icon": "image",
        "editorial_status": "REVIEW NEEDED",
    },
    "prompt-engineering": {
        "label": "Context Engineering",
        "group": "Context",
        "summary": "Prompting techniques plus context engineering: what the model knows — system prompts, examples, structured output, memory, and assembled context.",
        "accent": "amber",
        "icon": "message",
        "editorial_status": "REVIEW NEEDED",
    },
    "agents-and-tools": {
        "label": "Agents & Tools",
        "group": "Context",
        "summary": "Tool calling, planning loops, memory, handoffs, autonomy boundaries, and operator controls.",
        "accent": "teal",
        "icon": "wrench",
        "editorial_status": "CURRENT",
    },
    "rag-and-retrieval": {
        "label": "Retrieval & Knowledge",
        "group": "Context",
        "summary": "Sparse and dense retrieval, chunking, embeddings, ranking, query transformation, grounding, citations, memory, and retrieval evaluation.",
        "accent": "emerald",
        "icon": "database",
        "editorial_status": "CURRENT",
    },
    "evaluation": {
        "label": "Evaluation & Measurement",
        "group": "Measurement",
        "summary": "Splits, metrics, calibration, uncertainty, human evaluation, statistical evidence, product evals, regressions, and error taxonomies.",
        "accent": "rose",
        "icon": "gauge",
        "editorial_status": "REVIEW NEEDED",
    },
    "interpretability": {
        "label": "Interpretability",
        "group": "Measurement",
        "summary": "Feature attribution, probes, activations, representations, circuits, sparse autoencoders, causal interventions, and faithfulness limits.",
        "accent": "amber",
        "icon": "nodes",
        "editorial_status": "PLANNED",
    },
    "ai-safety-and-security": {
        "label": "AI Safety & Security",
        "group": "Measurement",
        "summary": "Threat modeling, misuse, prompt injection, data leakage, safety cases, and deployment controls.",
        "accent": "red",
        "icon": "shield",
        "editorial_status": "REVIEW NEEDED",
    },
    "ai-ethics-and-governance": {
        "label": "AI Ethics & Governance",
        "group": "Measurement",
        "summary": "Fairness and bias, transparency, model documentation, privacy, regulation (EU AI Act), governance frameworks, and societal impact.",
        "accent": "amber",
        "icon": "scale",
        "editorial_status": "REVIEW NEEDED",
    },
    "mlops": {
        "label": "MLOps",
        "group": "Operations",
        "summary": "Pipelines, datasets, monitoring, model releases, reproducibility, and production feedback loops.",
        "accent": "blue",
        "icon": "workflow",
        "editorial_status": "REVIEW NEEDED",
    },
    "ai-product-engineering": {
        "label": "AI Product Engineering",
        "group": "Operations",
        "summary": "UX, latency, cost, observability, human review, product metrics, and delivery tradeoffs.",
        "accent": "orange",
        "icon": "layout",
        "editorial_status": "REVIEW NEEDED",
    },
    "fine-tuning-and-alignment": {
        "label": "Training & Adaptation",
        "group": "Training",
        "summary": "Training loops, distributed execution, mixed precision, checkpointing, SFT, LoRA/QLoRA, preference optimization, distillation, and continual learning.",
        "accent": "violet",
        "icon": "spark",
        "editorial_status": "REVIEW NEEDED",
    },
    "inference-and-optimization": {
        "label": "Inference Systems",
        "group": "Training",
        "summary": "Model loading, kernels, memory bandwidth, quantization, prefill/decode, KV cache, batching, routing, edge inference, latency, throughput, and cost.",
        "accent": "cyan",
        "icon": "chip",
        "editorial_status": "REVIEW NEEDED",
    },
    "research-and-experimentation": {
        "label": "Research & Experimentation",
        "group": "Always-on",
        "summary": "Read papers, reconstruct claims, reproduce results, test statistical evidence, detect benchmark gaming, and maintain a research log.",
        "accent": "indigo",
        "icon": "book",
        "editorial_status": "PLANNED",
    },
    "ai-playbooks": {
        "label": "AI Playbooks",
        "group": "Always-on",
        "summary": "Repeatable procedures for building, evaluating, debugging, and shipping AI systems.",
        "accent": "fuchsia",
        "icon": "playbook",
        "editorial_status": "REVIEW NEEDED",
    },
}

BRANCHES_ES = {
    "mathematics-for-ai": {"label": "Matemática para IA", "summary": "Álgebra lineal, cálculo, probabilidad, estadística, teoría de la información, optimización y estabilidad numérica."},
    "computation-and-autodiff": {"label": "Computación y Autodiff", "summary": "Tensores como arrays, vectorización, compute graphs, autodiff reverso, floating point, paralelismo y reproducibilidad."},
    "classical-ai-and-reasoning": {"label": "IA Clásica y Razonamiento", "summary": "Búsqueda, heurísticas, restricciones, planificación, lógica, representación de conocimiento, razonamiento probabilístico y teoría de decisión."},
    "foundations": {"label": "Fundamentos del Aprendizaje", "summary": "Formulación de problemas, generalización, sesgo inductivo, distribution shift, leakage, métricas y cuándo no usar aprendizaje."},
    "machine-learning": {"label": "Machine Learning Estadístico", "summary": "Regresión, clasificación, árboles, ensembles, kernels, clustering, reducción dimensional, calibración y análisis de errores."},
    "data-for-ai": {"label": "Datos para IA", "summary": "IA centrada en datos: calidad, labeling, diseño de datasets, datos sintéticos, contaminación, documentación y pipelines."},
    "deep-learning": {"label": "Deep Learning", "summary": "Redes neuronales, representaciones, optimización, embeddings y comportamiento al escalar."},
    "reinforcement-learning": {"label": "Reinforcement Learning", "summary": "Decisiones secuenciales, ecuaciones de Bellman, value learning, policy gradients, exploración, offline RL, world models y conexiones con alignment."},
    "model-architectures": {"label": "Arquitecturas de Modelos", "summary": "CNNs, modelos de secuencia, attention, transformers, mixture of experts, state-space models, difusión y tradeoffs arquitectónicos."},
    "llms": {"label": "Modelos de Lenguaje y Fundacionales", "summary": "Tokenización, decoder transformers, pretraining, data mixtures, scaling, decoding, instruction tuning, razonamiento y familias de modelos."},
    "multimodal-and-generative": {"label": "Visión, Audio e IA Multimodal", "summary": "Imágenes, visión, detección, segmentación, speech, fusión multimodal, difusión, video, evaluación, datos y seguridad."},
    "prompt-engineering": {"label": "Context Engineering", "summary": "System prompts, ejemplos, salidas estructuradas, armado y compresión de contexto, memoria y tradeoffs de long context."},
    "agents-and-tools": {"label": "Agentes y Herramientas", "summary": "Tool calling, bucles de planificación, memoria, handoffs, límites de autonomía y controles de operador."},
    "rag-and-retrieval": {"label": "Retrieval y Conocimiento", "summary": "Retrieval sparse y dense, chunking, embeddings, ranking, transformaciones de consulta, grounding, citas, memoria y evaluación."},
    "evaluation": {"label": "Evaluación y Medición", "summary": "Splits, métricas, calibración, incertidumbre, evaluación humana, evidencia estadística, product evals, regresiones y taxonomías de error."},
    "interpretability": {"label": "Interpretabilidad", "summary": "Atribución de features, probes, activaciones, representaciones, circuitos, sparse autoencoders, intervenciones causales y límites de fidelidad."},
    "ai-safety-and-security": {"label": "Seguridad de IA", "summary": "Modelado de amenazas, misuse, prompt injection, fuga de datos, safety cases y controles de despliegue."},
    "ai-ethics-and-governance": {"label": "Ética y Gobernanza de IA", "summary": "Fairness y sesgo, transparencia, documentación de modelos, privacidad, regulación (EU AI Act), frameworks de gobernanza e impacto social."},
    "mlops": {"label": "MLOps y Operaciones", "summary": "Pipelines, registries, CI/CD, observabilidad, monitoreo, drift, feedback, releases, rollback, confiabilidad y capacidad."},
    "ai-product-engineering": {"label": "Ingeniería de Producto con IA", "summary": "UX, latencia, costo, observabilidad, revisión humana, métricas de producto y tradeoffs de entrega."},
    "fine-tuning-and-alignment": {"label": "Entrenamiento y Adaptación", "summary": "Training loops, entrenamiento distribuido, mixed precision, checkpointing, SFT, LoRA/QLoRA, preference optimization, distillation y aprendizaje continuo."},
    "inference-and-optimization": {"label": "Sistemas de Inferencia", "summary": "Carga de modelos, kernels, memory bandwidth, quantization, prefill/decode, KV cache, batching, routing, edge, latencia, throughput y costo."},
    "research-and-experimentation": {"label": "Investigación y Experimentación", "summary": "Leer papers, reconstruir claims, reproducir resultados, probar evidencia estadística, detectar benchmark gaming y mantener un research log."},
    "ai-playbooks": {"label": "Playbooks de IA", "summary": "Procedimientos repetibles para construir, evaluar, depurar y entregar sistemas con IA."},
}

GROUP_LABELS = {
    "en": {
        "Orientation": "Orientation",
        "Foundations": "Foundations",
        "Learning": "Learning & Models",
        "Training": "Training & Inference",
        "Context": "Context & Agency",
        "Measurement": "Measurement & Trust",
        "Operations": "Product & Operations",
        "Always-on": "Labs, Research & Playbooks",
    },
    "es": {
        "Orientation": "Orientación",
        "Foundations": "Fundamentos",
        "Learning": "Aprendizaje y Modelos",
        "Training": "Entrenamiento e Inferencia",
        "Context": "Contexto y Agencia",
        "Measurement": "Medición y Confianza",
        "Operations": "Producto y Operaciones",
        "Always-on": "Labs, Investigación y Playbooks",
    },
}

UI_STRINGS = {
    "en": {
        "brand_sub": "Knowledge Atlas",
        "theme_toggle": "Toggle theme",
        "light_mode": "Light",
        "dark_mode": "Dark",
        "atlas_home": "Atlas Home",
        "entry_layer": "Entry Layer",
        "ai_index": "AI Index",
        "learning_path": "Learning Path",
        "reference_system": "Reference System",
        "registries": "Registries",
        "overview": "Overview",
        "updated_short": "updated",
        "nav_toggle": "Toggle navigation",
        "skip_to_content": "Skip to content",
        "search_placeholder": "Search notes, playbooks, tags...",
        "bc_home": "Home",
        "bc_ai": "AI",
        "min_read": "min read",
        "reading_time_title": "Estimated reading time",
        "updated": "Updated",
        "last_updated_title": "Last updated",
        "on_this_page": "On This Page",
        "on_this_page_aria": "On this page",
        "back_to_top": "Back to top",
        "previous": "Previous",
        "next": "Next",
        "related_notes": "Related notes",
        "lang_switch_aria": "Language",
        "translation_pending": "This note is not translated yet, so the English source is shown.",
        "home_title": "AI Atlas",
        "home_subtitle": "From first principles to production systems.",
        "home_lede": "An executable map of intelligent systems: from vectors, probability, search, objectives, gradients, and learned representations to inference, retrieval, agents, evaluation, safety, and operations.",
        "home_explore": "Start here",
        "home_playbooks": "Open Glassbox AI Lab",
        "stat_notes": "Canonical pages",
        "stat_branches": "Branches",
        "stat_playbooks": "Executable labs",
        "stat_registries": "ES coverage",
        "path_eyebrow": "Learning paths",
        "path_h2": "Choose a route; keep the computation visible.",
        "path_p": "Every route names prerequisites and crosses theory, implementation, evidence, failure modes, and production behavior.",
        "path_cta": "Open Start Here",
        "phase_label": "Phase",
        "phase_overview": "Phase page",
        "branch_singular": "branch",
        "branch_plural": "branches",
        "note_singular": "note",
        "note_plural": "notes",
        "branch_explore": "Explore",
        "branch_notes_suffix": "notes",
        "branch_status": "Editorial status",
        "featured_label": "Featured note",
        "ref_eyebrow": "Reference layer",
        "ref_h2": "Registries and operating memory",
        "ref_p": "Registries keep external references, decisions, datasets, tools, and evaluation assets normalized behind short atomic notes.",
        "footer_about": "A framework-free bilingual atlas by Lautaro Damore. Observable computation, reproducible evidence, production consequences.",
        "footer_start": "Start Here",
        "footer_index": "Full index",
        "landing_title": "Choose your language",
        "landing_sub": "AI Atlas",
        "title_index": "AI Notes Index",
        "title_notes": "Notes",
        "tag_Orientation": "Map the field",
        "tag_Foundations": "Represent and reason",
        "tag_Learning": "Learn representations",
        "tag_Training": "Train and serve",
        "tag_Context": "Ground and act",
        "tag_Measurement": "Measure and trust",
        "tag_Operations": "Ship and operate",
        "tag_Always-on": "Build and investigate",
        "intent_Orientation": "How to use the atlas, read its notation, validate claims, and choose a route.",
        "intent_Foundations": "Mathematics, computation, classical reasoning, statistical learning, data, assumptions, and uncertainty.",
        "intent_Learning": "Neural learning, sequential decisions, architectures, language, vision, audio, and multimodality.",
        "intent_Training": "Training systems, model adaptation, inference runtimes, hardware, latency, throughput, and cost.",
        "intent_Context": "Prompts, assembled context, retrieval, memory, tool use, agents, permissions, and recovery.",
        "intent_Measurement": "Evaluation, interpretability, safety, security, governance, uncertainty, and release evidence.",
        "intent_Operations": "Product framing, MLOps, observability, monitoring, feedback, reliability, and human review.",
        "intent_Always-on": "Glassbox labs, paper reproduction, research logs, and repeatable playbooks.",
        "verified": "Verified",
        "roadmap_status": "PLANNED",
    },
    "es": {
        "brand_sub": "Atlas de Conocimiento",
        "theme_toggle": "Cambiar tema",
        "light_mode": "Claro",
        "dark_mode": "Oscuro",
        "atlas_home": "Inicio del Atlas",
        "entry_layer": "Capa de entrada",
        "ai_index": "Índice de IA",
        "learning_path": "Ruta de aprendizaje",
        "reference_system": "Sistema de referencia",
        "registries": "Registros",
        "overview": "Resumen",
        "updated_short": "actualizado",
        "nav_toggle": "Alternar navegación",
        "skip_to_content": "Saltar al contenido",
        "search_placeholder": "Buscar notas, playbooks, tags...",
        "bc_home": "Inicio",
        "bc_ai": "IA",
        "min_read": "min de lectura",
        "reading_time_title": "Tiempo estimado de lectura",
        "updated": "Actualizado",
        "last_updated_title": "Última actualización",
        "on_this_page": "En esta página",
        "on_this_page_aria": "En esta página",
        "back_to_top": "Volver arriba",
        "previous": "Anterior",
        "next": "Siguiente",
        "related_notes": "Notas relacionadas",
        "lang_switch_aria": "Idioma",
        "translation_pending": "Esta nota todavía no está traducida, así que se muestra la fuente en inglés.",
        "home_title": "AI Atlas",
        "home_subtitle": "De primeros principios a sistemas de producción.",
        "home_lede": "Un mapa ejecutable de sistemas inteligentes: desde vectores, probabilidad, búsqueda, objetivos, gradientes y representaciones aprendidas hasta inferencia, retrieval, agentes, evaluación, seguridad y operaciones.",
        "home_explore": "Empezar acá",
        "home_playbooks": "Abrir Glassbox AI Lab",
        "stat_notes": "Páginas canónicas",
        "stat_branches": "Ramas",
        "stat_playbooks": "Labs ejecutables",
        "stat_registries": "Cobertura ES",
        "path_eyebrow": "Recorridos de aprendizaje",
        "path_h2": "Elegí un recorrido; mantené visible el cómputo.",
        "path_p": "Cada recorrido explicita prerequisitos y cruza teoría, implementación, evidencia, modos de falla y comportamiento en producción.",
        "path_cta": "Abrir Start Here",
        "phase_label": "Fase",
        "phase_overview": "Página de fase",
        "branch_singular": "rama",
        "branch_plural": "ramas",
        "note_singular": "nota",
        "note_plural": "notas",
        "branch_explore": "Explorar",
        "branch_notes_suffix": "notas",
        "branch_status": "Estado editorial",
        "featured_label": "Nota destacada",
        "ref_eyebrow": "Capa de referencia",
        "ref_h2": "Registros y memoria operativa",
        "ref_p": "Los registros mantienen referencias externas, decisiones, datasets, herramientas y activos de evaluación normalizados detrás de notas atómicas cortas.",
        "footer_about": "Un atlas bilingüe sin framework de Lautaro Damore. Cómputo observable, evidencia reproducible y consecuencias de producción.",
        "footer_start": "Empezar acá",
        "footer_index": "Índice completo",
        "landing_title": "Elegí tu idioma",
        "landing_sub": "AI Atlas",
        "title_index": "Índice de Notas de IA",
        "title_notes": "Notas",
        "tag_Orientation": "Mapear el campo",
        "tag_Foundations": "Representar y razonar",
        "tag_Learning": "Aprender representaciones",
        "tag_Training": "Entrenar y servir",
        "tag_Context": "Fundamentar y actuar",
        "tag_Measurement": "Medir y confiar",
        "tag_Operations": "Entregar y operar",
        "tag_Always-on": "Construir e investigar",
        "intent_Orientation": "Cómo usar el Atlas, leer su notación, validar claims y elegir un recorrido.",
        "intent_Foundations": "Matemática, computación, razonamiento clásico, aprendizaje estadístico, datos, supuestos e incertidumbre.",
        "intent_Learning": "Aprendizaje neuronal, decisiones secuenciales, arquitecturas, lenguaje, visión, audio y multimodalidad.",
        "intent_Training": "Sistemas de entrenamiento, adaptación, runtimes de inferencia, hardware, latencia, throughput y costo.",
        "intent_Context": "Prompts, contexto ensamblado, retrieval, memoria, herramientas, agentes, permisos y recuperación.",
        "intent_Measurement": "Evaluación, interpretabilidad, safety, seguridad, gobernanza, incertidumbre y evidencia de release.",
        "intent_Operations": "Formulación de producto, MLOps, observabilidad, monitoreo, feedback, confiabilidad y revisión humana.",
        "intent_Always-on": "Labs Glassbox, reproducción de papers, research logs y playbooks repetibles.",
        "verified": "Verificado",
        "roadmap_status": "PLANIFICADO",
    },
}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]\|]+)(?:\|([^\]]+))?\]\]")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
TAG_RE = re.compile(r"(?<!\w)#([A-Za-z][A-Za-z0-9_\-/]*)")


@dataclass
class Note:
    section: str
    rel_path: Path
    title: str
    slug: str
    body_md: str
    tags: list[str] = field(default_factory=list)
    frontmatter: dict = field(default_factory=dict)
    source_path: Path | None = None
    content_locale: str = DEFAULT_LOCALE
    is_fallback: bool = False

    @property
    def out_path(self) -> Path:
        return OUT / CURRENT_LOCALE / self.rel_path.with_suffix(".html")

    @property
    def url(self) -> str:
        return self.rel_path.with_suffix(".html").as_posix()


def t(key: str) -> str:
    loc = UI_STRINGS.get(CURRENT_LOCALE, UI_STRINGS[DEFAULT_LOCALE])
    return loc.get(key, UI_STRINGS[DEFAULT_LOCALE].get(key, key))


def parse_scalar(value: str):
    value = value.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(part.strip()) for part in inner.split(",")]
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(raw)
    if not m:
        return {}, raw
    fm: dict = {}
    current_key: str | None = None
    for line in m.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") and current_key:
            fm.setdefault(current_key, []).append(parse_scalar(line[4:]))
            continue
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            key = key.strip()
            if value.strip():
                fm[key] = parse_scalar(value)
                current_key = None
            else:
                fm[key] = []
                current_key = key
    return fm, raw[m.end():]


def title_from_markdown(body: str, fallback: str) -> str:
    m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    if m:
        return strip_markdown_inline(m.group(1)).strip()
    return fallback


_TITLE_CACHE: dict[tuple[str, str], str] = {}


def display_title(note: Note) -> str:
    """Locale-aware title for navigation elements rendered from canonical notes."""
    if CURRENT_LOCALE == DEFAULT_LOCALE:
        return note.title
    key = (CURRENT_LOCALE, note.rel_path.as_posix())
    if key in _TITLE_CACHE:
        return _TITLE_CACHE[key]
    overlay = CONTENT_ROOT / CURRENT_LOCALE / note.rel_path
    title = note.title
    if overlay.exists():
        fm, body = parse_frontmatter(overlay.read_text(encoding="utf-8"))
        stale = str(fm.get("translation", "")).strip().lower() == "stale"
        draft = fm.get("draft") is True or str(fm.get("draft", "")).strip().lower() == "true"
        if body.strip() and not stale and not draft:
            title = str(fm.get("title") or title_from_markdown(body, note.title))
    _TITLE_CACHE[key] = title
    return title


def load_note(path: Path) -> Note:
    raw = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(raw)
    rel = path.relative_to(CANONICAL_CONTENT)
    title = str(fm.get("title") or title_from_markdown(body, path.stem.replace("-", " ").title()))
    tags = fm.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    return Note(
        section=rel.parts[0] if rel.parts else "",
        rel_path=rel,
        title=title,
        slug=path.stem,
        body_md=body,
        tags=[str(tag).lstrip("#") for tag in tags],
        frontmatter=fm,
        source_path=path,
    )


def is_draft(note: Note) -> bool:
    value = note.frontmatter.get("draft")
    return value is True or str(value).strip().lower() == "true"


def load_notes() -> list[Note]:
    root = CANONICAL_CONTENT / SECTION
    if not root.exists():
        print(f"[error] missing content root: {root}", file=sys.stderr)
        return []
    notes = [load_note(path) for path in sorted(root.rglob("*.md"))]
    published = [n for n in notes if not is_draft(n)]
    drafts = len(notes) - len(published)
    if drafts:
        print(f"[info] skipped {drafts} draft note(s).", file=sys.stderr)
    return published


def loc_root() -> Path:
    return OUT / CURRENT_LOCALE


def branch_slug(note: Note | None) -> str:
    if note and len(note.rel_path.parts) >= 3 and note.rel_path.parts[0] == SECTION:
        return note.rel_path.parts[1]
    return ""


def page_kind(note: Note) -> str:
    branch = branch_slug(note)
    declared = str(note.frontmatter.get("kind", "")).strip().lower()
    if declared in {"concept", "derivation", "implementation", "system", "playbook", "paper-guide", "lab"}:
        return declared
    if note.slug.startswith("reference-registry"):
        return "registry"
    if branch == "ai-playbooks":
        return "playbook"
    if note.rel_path.name == "index.md":
        return "index"
    if note.slug.startswith("phase-"):
        return "phase"
    if note.slug in {"start-here", "must-know"}:
        return "entry"
    return "concept"


def branch_group(slug: str) -> str:
    return BRANCHES.get(slug, {}).get("group", "Always-on")


def group_label(group: str) -> str:
    return GROUP_LABELS.get(CURRENT_LOCALE, GROUP_LABELS[DEFAULT_LOCALE]).get(group, group)


def branch_label(slug: str) -> str:
    if CURRENT_LOCALE == "es" and slug in BRANCHES_ES:
        return BRANCHES_ES[slug]["label"]
    return BRANCHES.get(slug, {}).get("label", slug.replace("-", " ").title())


def branch_summary(slug: str) -> str:
    if CURRENT_LOCALE == "es" and slug in BRANCHES_ES:
        return BRANCHES_ES[slug]["summary"]
    return BRANCHES.get(slug, {}).get("summary", "")


def branch_accent(slug: str) -> str:
    return BRANCHES.get(slug, {}).get("accent", "cyan")


def build_slug_index(notes: list[Note]) -> tuple[dict[str, list[Note]], dict[str, Note]]:
    by_slug: dict[str, list[Note]] = {}
    by_path: dict[str, Note] = {}
    for note in notes:
        for key in {note.slug, note.slug.lower(), slugify(note.title)}:
            by_slug.setdefault(key, []).append(note)
        path_key = note.rel_path.with_suffix("").as_posix()
        by_path[path_key] = note
        by_path[path_key.lower()] = note
    for legacy, target in LEGACY_REDIRECTS.items():
        target_note = by_path.get(target) or by_path.get(target.lower())
        if target_note:
            by_path[legacy] = target_note
            by_path[legacy.lower()] = target_note
    return by_slug, by_path


def resolve_link(raw: str, source: Note, by_slug: dict[str, list[Note]], by_path: dict[str, Note]) -> Note | None:
    raw = raw.strip().removesuffix(".md")
    if "/" in raw:
        return by_path.get(raw.strip("/")) or by_path.get(raw.strip("/").lower())
    candidates = by_slug.get(raw) or by_slug.get(raw.lower()) or by_slug.get(slugify(raw))
    if not candidates:
        return None
    unique: list[Note] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = candidate.rel_path.as_posix()
        if key not in seen:
            unique.append(candidate)
            seen.add(key)
    if len(unique) == 1:
        return unique[0]
    source_folder = source.rel_path.parent.as_posix()
    for candidate in unique:
        if candidate.rel_path.parent.as_posix() == source_folder:
            return candidate
    for candidate in unique:
        if candidate.section == source.section:
            return candidate
    return unique[0]


def rewrite_links(md_text: str, note: Note, by_slug: dict[str, list[Note]], by_path: dict[str, Note]) -> str:
    here = (loc_root() / note.rel_path).parent

    def rel_href(target: Note) -> str:
        return os.path.relpath(loc_root() / target.rel_path.with_suffix(".html"), here)

    def wikilink_sub(match: re.Match) -> str:
        target_raw = match.group(1).strip()
        label = (match.group(2) or target_raw.split("/")[-1]).strip()
        target_ref, _, anchor = target_raw.partition("#")
        target = resolve_link(target_ref, note, by_slug, by_path)
        if not target:
            return f'<span class="unresolved-link" title="Unresolved: {html.escape(target_ref)}">{html.escape(label)}</span>'
        href = rel_href(target)
        if anchor:
            href += "#" + slugify(anchor)
        return f"[{label}]({href})"

    def mdlink_sub(match: re.Match) -> str:
        label = match.group(1)
        href = match.group(2).strip()
        if href.startswith(("http://", "https://", "mailto:", "#", "/")):
            return match.group(0)
        if href.endswith(".md") or ".md#" in href:
            return f"[{label}]({href.replace('.md#', '.html#').replace('.md', '.html')})"
        return match.group(0)

    return MD_LINK_RE.sub(mdlink_sub, WIKILINK_RE.sub(wikilink_sub, md_text))


def localized_note(note: Note) -> tuple[Note, bool]:
    if CURRENT_LOCALE == DEFAULT_LOCALE:
        return note, False
    overlay = CONTENT_ROOT / CURRENT_LOCALE / note.rel_path
    if not overlay.exists():
        return Note(
            section=note.section, rel_path=note.rel_path, title=note.title,
            slug=note.slug, body_md=note.body_md, tags=note.tags,
            frontmatter=dict(note.frontmatter), source_path=note.source_path,
            content_locale=DEFAULT_LOCALE, is_fallback=True,
        ), True
    fm, body = parse_frontmatter(overlay.read_text(encoding="utf-8"))
    overlay_draft = fm.get("draft") is True or str(fm.get("draft", "")).strip().lower() == "true"
    if str(fm.get("translation", "")).strip().lower() == "stale" or overlay_draft or not body.strip():
        return Note(
            section=note.section, rel_path=note.rel_path, title=note.title,
            slug=note.slug, body_md=note.body_md, tags=note.tags,
            frontmatter=dict(note.frontmatter), source_path=note.source_path,
            content_locale=DEFAULT_LOCALE, is_fallback=True,
        ), True
    merged = dict(note.frontmatter)
    merged.update(fm)
    title = str(merged.get("title") or title_from_markdown(body, note.title))
    return Note(
        section=note.section,
        rel_path=note.rel_path,
        title=title,
        slug=note.slug,
        body_md=body,
        tags=note.tags,
        frontmatter=merged,
        source_path=overlay,
        content_locale=CURRENT_LOCALE,
    ), False


def display_description(note: Note) -> str:
    localized, _ = localized_note(note)
    return note_description(localized)


def build_sidebar_tree(notes: list[Note]) -> dict[str, dict[str, list[Note]]]:
    tree: dict[str, dict[str, list[Note]]] = {}
    for note in notes:
        sub = "/".join(note.rel_path.parts[1:-1])
        tree.setdefault(note.section, {}).setdefault(sub, []).append(note)
    for section in tree:
        for sub in tree[section]:
            tree[section][sub].sort(key=lambda n: (int(n.frontmatter.get("order", 99)) if str(n.frontmatter.get("order", "")).isdigit() else 99, n.slug != "index", n.title.lower()))
    return tree


def branch_notes(tree: dict[str, dict[str, list[Note]]], slug: str) -> list[Note]:
    return tree.get(SECTION, {}).get(slug, [])


def branch_note_count(tree: dict[str, dict[str, list[Note]]], slug: str) -> int:
    return sum(1 for note in branch_notes(tree, slug) if note.slug != "index")


def relpath_from(note: Note | None, target: Path) -> str:
    here = (loc_root() / note.rel_path).parent if note else loc_root()
    return os.path.relpath(target, here)


def render_sidebar(tree: dict[str, dict[str, list[Note]]], current: Note | None) -> str:
    home_href = relpath_from(current, loc_root() / "index.html")
    current_branch = branch_slug(current)
    current_group = branch_group(current_branch) if current_branch else ""
    section_root = tree.get(SECTION, {}).get("", [])
    root_by_slug = {n.slug: n for n in section_root}
    entry_notes = [root_by_slug[s] for s in ("index", "start-here", "must-know") if s in root_by_slug]
    registry_notes = [n for n in section_root if n.slug.startswith("reference-registry")]

    lines = ['<nav id="primary-sidebar" class="sidebar" aria-label="Primary navigation">']
    lines.append(
        '<div class="sidebar-head">'
        f'<a class="sidebar-brand" href="{html.escape(home_href)}">{icon_svg("nodes", "brand-icon")}'
        f'<span class="brand-text"><span class="brand-title">AI Atlas</span><span class="brand-sub">{html.escape(t("brand_sub"))}</span></span></a>'
        f'<button class="theme-toggle" id="theme-toggle" type="button" aria-pressed="false" aria-label="{html.escape(t("theme_toggle"))}">'
        f'<span class="label-light">{icon_svg("sun")} {html.escape(t("light_mode"))}</span>'
        f'<span class="label-dark">{icon_svg("moon")} {html.escape(t("dark_mode"))}</span>'
        '<span class="toggle-pill"></span></button>'
        '</div>'
    )
    lines.append('<div class="sidebar-body">')
    lines.append(f'<a class="sidebar-home" href="{html.escape(home_href)}">{icon_svg("home")}<span>{html.escape(t("atlas_home"))}</span></a>')

    if entry_notes:
        lines.append(f'<section class="sidebar-section"><h3>{html.escape(t("entry_layer"))}</h3>')
        for note in entry_notes:
            label = t("ai_index") if note.slug == "index" else display_title(note)
            lines.append(render_sidebar_link(note, current, label=label))
        lines.append("</section>")

    lines.append(f'<section class="sidebar-section"><h3>{html.escape(t("learning_path"))}</h3>')
    for phase in PHASES:
        group = phase["key"]
        branches = [slug for slug in BRANCHES if branch_group(slug) == group and branch_notes(tree, slug)]
        phase_note = root_by_slug.get(Path(str(phase["href"])).stem)
        if not branches and not phase_note:
            continue
        count = sum(branch_note_count(tree, slug) for slug in branches)
        is_current_phase = bool(current and phase_note and current.rel_path == phase_note.rel_path)
        open_attr = " open" if (group == current_group and current_branch) or is_current_phase else ""
        count_html = f'<span class="count">{count}</span>' if count else ""
        lines.append(
            f'<details class="nav-group"{open_attr}><summary>'
            f'<span class="nav-summary-left">{icon_svg(str(phase["icon"]), "sec-ico")}<span><span class="phase-num">{html.escape(str(phase["num"]))}</span>{html.escape(group_label(group))}</span></span>'
            f'<span class="nav-summary-right">{count_html}{icon_svg("chevron", "chev")}</span>'
            '</summary><div class="nav-children">'
        )
        if phase_note:
            phase_href = relpath_from(current, loc_root() / phase_note.rel_path.with_suffix(".html"))
            phase_active = " active" if is_current_phase else ""
            lines.append(f'<a class="nav-leaf nav-leaf-overview{phase_active}" href="{html.escape(phase_href)}">{html.escape(t("phase_overview"))}</a>')
        for slug in branches:
            notes = branch_notes(tree, slug)
            index_note = next((n for n in notes if n.slug == "index"), notes[0])
            leaves = [n for n in notes if n.slug != "index"]
            active = " active" if current_branch == slug else ""
            open_branch = " open" if current_branch == slug else ""
            lines.append(
                f'<details class="nav-branch accent-{html.escape(branch_accent(slug))}{active}"{open_branch}>'
                '<summary>'
                f'<span class="nav-summary-left">{icon_svg(BRANCHES[slug]["icon"], "branch-ico")}<span>{html.escape(branch_label(slug))}</span></span>'
                f'<span class="nav-summary-right"><span class="count">{len(notes)}</span>{icon_svg("chevron", "chev")}</span>'
                '</summary><div class="nav-leaves">'
            )
            overview_href = relpath_from(current, loc_root() / index_note.rel_path.with_suffix(".html"))
            overview_active = " active" if current and current.rel_path == index_note.rel_path else ""
            lines.append(f'<a class="nav-leaf nav-leaf-overview{overview_active}" href="{html.escape(overview_href)}">{html.escape(t("overview"))}</a>')
            for leaf in leaves:
                href = relpath_from(current, loc_root() / leaf.rel_path.with_suffix(".html"))
                leaf_active = " active" if current and current.rel_path == leaf.rel_path else ""
                leaf_title = display_title(leaf)
                visible = leaf_title if len(leaf_title) < 58 else leaf_title[:55] + "..."
                lines.append(f'<a class="nav-leaf{leaf_active}" href="{html.escape(href)}" title="{html.escape(leaf_title)}">{html.escape(visible)}</a>')
            lines.append("</div></details>")
        lines.append("</div></details>")
    lines.append("</section>")

    if registry_notes:
        open_attr = " open" if current and page_kind(current) == "registry" else ""
        lines.append(f'<section class="sidebar-section"><h3>{html.escape(t("reference_system"))}</h3>')
        lines.append(
            f'<details class="nav-group"{open_attr}><summary>'
            f'<span class="nav-summary-left">{icon_svg("database", "sec-ico")}<span>{html.escape(t("registries"))}</span></span>'
            f'<span class="nav-summary-right"><span class="count">{len(registry_notes)}</span>{icon_svg("chevron", "chev")}</span>'
            '</summary><div class="nav-children">'
        )
        for note in registry_notes:
            lines.append(render_sidebar_link(note, current, extra_class="nav-child"))
        lines.append("</div></details></section>")

    lines.append("</div>")
    lines.append(f'<div class="sidebar-footer"><span>{html.escape(t("updated_short"))} · {date.today().isoformat()}</span><span>v0.1</span></div>')
    lines.append("</nav>")
    return "\n".join(lines)


def render_sidebar_link(note: Note, current: Note | None, label: str | None = None, extra_class: str = "sidebar-link") -> str:
    href = relpath_from(current, loc_root() / note.rel_path.with_suffix(".html"))
    active = " active" if current and current.rel_path == note.rel_path else ""
    return f'<a class="{extra_class} kind-{page_kind(note)}{active}" href="{html.escape(href)}">{html.escape(label or display_title(note))}</a>'


def breadcrumb_html(note: Note) -> str:
    crumbs = [f'<a href="{html.escape(relpath_from(note, loc_root() / "index.html"))}">{html.escape(t("bc_home"))}</a>']
    ai_index = loc_root() / SECTION / "index.html"
    crumbs.append(f'<a href="{html.escape(relpath_from(note, ai_index))}">{html.escape(t("bc_ai"))}</a>')
    slug = branch_slug(note)
    if slug:
        branch_index = loc_root() / SECTION / slug / "index.html"
        crumbs.append(f'<a href="{html.escape(relpath_from(note, branch_index))}">{html.escape(branch_label(slug))}</a>')
    crumbs.append(f'<span>{html.escape(note.title)}</span>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + '<span class="sep">/</span>'.join(crumbs) + "</nav>"


def reading_time_minutes(note: Note) -> int:
    if page_kind(note) in {"index", "registry"}:
        return 0
    text = strip_markdown(note.body_md)
    words = len(re.findall(r"\w+", text))
    return max(1, round(words / 220))


def note_last_modified(note: Note) -> str:
    if isinstance(note.frontmatter.get("updated"), str):
        return str(note.frontmatter["updated"])
    try:
        return date.fromtimestamp((note.source_path or (CANONICAL_CONTENT / note.rel_path)).stat().st_mtime).isoformat()
    except OSError:
        return date.today().isoformat()


def note_last_verified(note: Note) -> str:
    value = note.frontmatter.get("last_verified")
    return str(value) if isinstance(value, str) else ""


def page_meta_html(note: Note) -> str:
    chips = [f'<span class="meta-chip">{html.escape(page_kind(note))}</span>']
    for key in ("level", "status"):
        value = str(note.frontmatter.get(key, "")).strip()
        if value:
            chips.append(f'<span class="meta-chip meta-{html.escape(key)}">{html.escape(value.replace("-", " "))}</span>')
    slug = branch_slug(note)
    if slug:
        chips.append(f'<span class="meta-chip accent-{html.escape(branch_accent(slug))}">{html.escape(branch_label(slug))}</span>')
    minutes = reading_time_minutes(note)
    if minutes:
        chips.append(f'<span class="meta-chip" title="{html.escape(t("reading_time_title"))}">~{minutes} {html.escape(t("min_read"))}</span>')
    if page_kind(note) not in {"index"}:
        verified = note_last_verified(note)
        label = t("verified") if verified else t("updated")
        chips.append(f'<span class="meta-chip" title="{html.escape(t("last_updated_title"))}">{html.escape(label)} {html.escape(verified or note_last_modified(note))}</span>')
    chips.extend(f'<span class="meta-chip tag">#{html.escape(tag)}</span>' for tag in note.tags)
    return '<div class="page-meta">' + "".join(chips) + "</div>"


def extract_toc(html_body: str) -> list[tuple[int, str, str]]:
    headings = []
    for m in re.finditer(r'<h([23]) id="([^"]+)">(.*?)</h\1>', html_body, re.DOTALL):
        label = html.unescape(strip_html(m.group(3))).strip()
        if label:
            headings.append((int(m.group(1)), m.group(2), label))
    return headings[:18]


def render_toc(html_body: str) -> str:
    headings = extract_toc(html_body)
    if not headings:
        return ""
    lines = [f'<aside class="toc" aria-label="{html.escape(t("on_this_page_aria"))}"><div class="toc-inner"><h2>{html.escape(t("on_this_page"))}</h2>']
    for level, anchor, label in headings:
        lines.append(f'<a class="toc-level-{level}" href="#{html.escape(anchor)}">{html.escape(label)}</a>')
    lines.append(f'<a class="back-to-top" href="#top">{html.escape(t("back_to_top"))}</a></div></aside>')
    return "\n".join(lines)


def root_asset(root_href: str, asset_path: str) -> str:
    return f"{root_href.rstrip('/')}/{asset_path.lstrip('/')}" if root_href not in {"", "."} else asset_path.lstrip("/")


def absolute_site_url(path: str) -> str:
    return f"{SITE_URL}/{path.lstrip('/')}"


def locale_url(note: Note, loc: str) -> str:
    if note.section == "" and note.rel_path == Path("index.md"):
        return f"{SITE_URL}/{loc}/"
    return f"{SITE_URL}/{loc}/{note.url}"


def has_real_translation(note: Note, loc: str) -> bool:
    if loc == DEFAULT_LOCALE or note.section == "":
        return True
    overlay = CONTENT_ROOT / loc / note.rel_path
    if not overlay.exists():
        return False
    fm, body = parse_frontmatter(overlay.read_text(encoding="utf-8"))
    draft = fm.get("draft") is True or str(fm.get("draft", "")).strip().lower() == "true"
    return bool(body.strip()) and not draft and str(fm.get("translation", "")).strip().lower() != "stale"


def canonical_url(note: Note) -> str:
    locale = DEFAULT_LOCALE if note.is_fallback else CURRENT_LOCALE
    return locale_url(note, locale)


def site_description() -> str:
    return SITE_DESCRIPTION_ES if CURRENT_LOCALE == "es" else SITE_DESCRIPTION


def page_title(note: Note) -> str:
    slug = branch_slug(note)
    if note.section == "" and note.rel_path == Path("index.md"):
        return f"{t('home_title')} | {t('home_subtitle')}"
    if note.rel_path == Path(f"{SECTION}/index.md"):
        return f"{t('title_index')} | {SITE_NAME}"
    if page_kind(note) == "index" and slug:
        return f"{branch_label(slug)} {t('title_notes')} | {SITE_NAME}"
    if slug:
        return f"{note.title} - {branch_label(slug)} | {SITE_NAME}"
    return f"{note.title} | {SITE_NAME}"


def note_description(note: Note) -> str:
    for key in ("description", "summary"):
        if isinstance(note.frontmatter.get(key), str) and note.frontmatter[key].strip():
            return truncate(strip_html(str(note.frontmatter[key])))
    if note.section == "" and note.rel_path == Path("index.md"):
        return site_description()
    slug = branch_slug(note)
    if page_kind(note) == "index" and slug:
        return truncate(branch_summary(slug))
    paragraph = first_content_paragraph(note.body_md)
    if paragraph:
        return truncate(paragraph)
    return site_description()


def page_keywords(note: Note) -> list[str]:
    values = list(SITE_KEYWORDS)
    slug = branch_slug(note)
    if slug:
        values.append(branch_label(slug))
    values.append(note.title)
    values.extend(note.tags)
    seen: set[str] = set()
    result = []
    for value in values:
        key = str(value).lower()
        if key not in seen:
            seen.add(key)
            result.append(str(value))
    return result[:14]


def breadcrumb_items(note: Note) -> list[tuple[str, str]]:
    canonical_locale = DEFAULT_LOCALE if note.is_fallback else CURRENT_LOCALE
    items = [(t("bc_home"), f"{SITE_URL}/{canonical_locale}/")]
    if note.section:
        items.append((t("bc_ai"), f"{SITE_URL}/{canonical_locale}/{SECTION}/index.html"))
    slug = branch_slug(note)
    if slug:
        items.append((branch_label(slug), f"{SITE_URL}/{canonical_locale}/{SECTION}/{slug}/index.html"))
    if not (note.section == "" and note.rel_path == Path("index.md")):
        items.append((note.title, canonical_url(note)))
    return items


def json_ld_for(note: Note) -> str:
    canonical = canonical_url(note)
    site = {"@type": "WebSite", "@id": SITE_URL + "/#website", "name": SITE_NAME, "url": SITE_URL + "/"}
    author = {"@type": "Person", "@id": SITE_URL + "/#author", "name": SITE_AUTHOR}
    page_type = "WebSite" if note.section == "" else "CollectionPage" if page_kind(note) == "index" else "TechArticle"
    page = {
        "@context": "https://schema.org",
        "@type": page_type,
        "@id": canonical + ("#website" if page_type == "WebSite" else "#page"),
        "name": page_title(note),
        "headline": note.title,
        "description": note_description(note),
        "url": canonical,
        "inLanguage": note.content_locale,
        "isPartOf": site,
        "author": author,
    }
    if page_type != "WebSite":
        page["dateModified"] = note_last_modified(note)
        page["keywords"] = page_keywords(note)
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(breadcrumb_items(note))
        ],
    }
    return json.dumps([page, breadcrumb], ensure_ascii=False, separators=(",", ":"))


def seo_head(note: Note, root_href: str) -> str:
    title = page_title(note)
    description = note_description(note)
    canonical = canonical_url(note)
    kind = "article" if page_kind(note) not in {"index"} else "website"
    og_image = absolute_site_url("assets/og-image.png")
    lines = [
        f"<title>{html.escape(title)}</title>",
        f'<meta name="description" content="{html.escape(description)}">',
        f'<meta name="author" content="{html.escape(SITE_AUTHOR)}">',
        f'<meta name="application-name" content="{html.escape(SITE_SHORT_NAME)}">',
        f'<meta name="keywords" content="{html.escape(", ".join(page_keywords(note)))}">',
        f'<meta name="theme-color" content="{THEME_COLOR}">',
        '<meta name="color-scheme" content="light dark">',
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        ('<meta name="robots" content="noindex, follow">' if note.is_fallback else '<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">'),
        f'<link rel="canonical" href="{html.escape(canonical)}">',
        f'<link rel="icon" href="{html.escape(root_asset(root_href, "favicon.svg"))}" type="image/svg+xml">',
        f'<link rel="icon" sizes="192x192" href="{html.escape(root_asset(root_href, "assets/icon-192.png"))}" type="image/png">',
        f'<link rel="apple-touch-icon" href="{html.escape(root_asset(root_href, "apple-touch-icon.png"))}">',
        f'<link rel="manifest" href="{html.escape(root_asset(root_href, "site.webmanifest"))}">',
        f'<meta property="og:site_name" content="{html.escape(SITE_NAME)}">',
        f'<meta property="og:locale" content="{OG_LOCALE.get(note.content_locale, "en_US")}">',
        *[f'<meta property="og:locale:alternate" content="{OG_LOCALE[loc]}">' for loc in LOCALES if loc != note.content_locale and has_real_translation(note, loc)],
        f'<meta property="og:type" content="{kind}">',
        f'<meta property="og:title" content="{html.escape(title)}">',
        f'<meta property="og:description" content="{html.escape(description)}">',
        f'<meta property="og:url" content="{html.escape(canonical)}">',
        f'<meta property="og:image" content="{html.escape(og_image)}">',
        '<meta property="og:image:type" content="image/png">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{html.escape(SITE_NAME)}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{html.escape(title)}">',
        f'<meta name="twitter:description" content="{html.escape(description)}">',
        f'<meta name="twitter:image" content="{html.escape(og_image)}">',
        f'<script type="application/ld+json">{json_ld_for(note).replace("</", "<\\/")}</script>',
    ]
    for loc in LOCALES:
        if has_real_translation(note, loc):
            lines.append(f'<link rel="alternate" hreflang="{loc}" href="{html.escape(locale_url(note, loc))}">')
    x_default = f"{SITE_URL}/" if note.section == "" else locale_url(note, DEFAULT_LOCALE)
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{html.escape(x_default)}">')
    return "\n".join(lines)


PAGE_TEMPLATE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{seo_head}
<script>(function(){{try{{var t=localStorage.getItem('theme');if(!t)t=matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light';document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();</script>
<link rel="stylesheet" href="{css_href}?v={asset_ver}">
</head>
<body id="top" data-root="{root_href}" data-locale-root="{locale_root}" data-locale="{ui_locale}" data-content-locale="{content_locale}">
<a class="skip-link" href="#main">{skip_to_content}</a>
<div class="app {layout_class}">
{sidebar}
<div class="main-col">
<header class="topbar">
  <button id="sidebar-toggle" class="icon-btn menu-toggle" title="{nav_toggle}" aria-label="{nav_toggle}" aria-controls="primary-sidebar" aria-expanded="false">{menu_icon}</button>
  <div class="topbar-search search-shell">
    {search_icon}
    <input id="search" type="search" placeholder="{search_placeholder}" autocomplete="off" aria-label="{search_placeholder}" aria-controls="search-results" aria-expanded="false" aria-autocomplete="list">
    <kbd>⌘K</kbd>
  </div>
  <div class="topbar-actions">
    {lang_switcher}
    <a class="github-link" href="{github_url}" target="_blank" rel="noopener" aria-label="GitHub">{github_icon}<span class="gh-label">GitHub</span></a>
  </div>
</header>
<div id="search-results" role="listbox" aria-live="polite" hidden></div>
<div class="main-row">
<main class="content" id="main" tabindex="-1">
{breadcrumbs}
<header class="page-hero">
{page_meta}
</header>
<article class="{article_class}">
{body}
</article>
</main>
{toc}
</div>
</div>
<script src="{search_js_href}?v={asset_ver}"></script>
</body>
</html>
"""


def render_lang_switcher(note: Note, here: Path) -> str:
    links = []
    for loc in LOCALES:
        target = OUT / loc / note.rel_path.with_suffix(".html")
        href = os.path.relpath(target, here)
        active = loc == CURRENT_LOCALE
        links.append(
            f'<a class="lang-link{" active" if active else ""}" hreflang="{loc}" href="{html.escape(href)}" '
            f'aria-current="{"page" if active else "false"}">{html.escape(LOCALE_LABEL[loc])}</a>'
        )
    return f'<div class="lang-switch" role="group" aria-label="{html.escape(t("lang_switch_aria"))}">{"".join(links)}</div>'


def render_page(note: Note, body: str, sidebar: str, tree: dict[str, dict[str, list[Note]]], all_notes: list[Note]) -> str:
    here = note.out_path.parent
    root_href = os.path.relpath(OUT, here) or "."
    locale_root = os.path.relpath(loc_root(), here) or "."
    css_href = os.path.relpath(OUT / "assets" / "atlas.css", here)
    search_js_href = os.path.relpath(OUT / "assets" / "search.js", here)
    is_home = note.section == "" and note.rel_path == Path("index.md")
    toc = "" if is_home else render_toc(body)
    if not is_home:
        body += branch_nav_html(note, all_notes)
        body += related_notes_html(note, all_notes)
    return PAGE_TEMPLATE.format(
        lang=note.content_locale,
        seo_head=seo_head(note, root_href),
        css_href=html.escape(css_href),
        asset_ver=ASSET_VER,
        root_href=html.escape(root_href),
        locale_root=html.escape(locale_root),
        ui_locale=CURRENT_LOCALE,
        content_locale=note.content_locale,
        layout_class="with-toc" if toc else "no-toc",
        sidebar=sidebar,
        nav_toggle=html.escape(t("nav_toggle")),
        skip_to_content=html.escape(t("skip_to_content")),
        menu_icon=icon_svg("menu"),
        search_icon=icon_svg("search", "search-ico"),
        search_placeholder=html.escape(t("search_placeholder")),
        lang_switcher=render_lang_switcher(note, here),
        github_url=html.escape(GITHUB_URL),
        github_icon=icon_svg("github"),
        breadcrumbs="" if is_home else breadcrumb_html(note),
        page_meta="" if is_home else page_meta_html(note),
        article_class="article-home" if is_home else "article-note",
        body=body,
        toc=toc,
        search_js_href=html.escape(search_js_href),
    )


def branch_nav_html(note: Note, all_notes: list[Note]) -> str:
    article_kinds = {"concept", "derivation", "implementation", "system", "playbook", "paper-guide", "lab"}
    if page_kind(note) not in article_kinds:
        return ""
    slug = branch_slug(note)
    if not slug:
        return ""
    siblings = sorted(
        [n for n in all_notes if branch_slug(n) == slug and page_kind(n) in article_kinds],
        key=lambda n: (int(n.frontmatter.get("order", 99)) if str(n.frontmatter.get("order", "")).isdigit() else 99, n.title.lower()),
    )
    try:
        idx = next(i for i, n in enumerate(siblings) if n.rel_path == note.rel_path)
    except StopIteration:
        return ""
    here = note.out_path.parent
    parts = ['<nav class="branch-nav" aria-label="Within this branch">']
    prev_note = siblings[idx - 1] if idx > 0 else None
    next_note = siblings[idx + 1] if idx + 1 < len(siblings) else None
    if prev_note:
        href = os.path.relpath(loc_root() / prev_note.rel_path.with_suffix(".html"), here)
        parts.append(f'<a class="branch-nav-link" href="{html.escape(href)}"><span>{html.escape(t("previous"))}</span><strong>{html.escape(display_title(prev_note))}</strong></a>')
    else:
        parts.append('<span></span>')
    if next_note:
        href = os.path.relpath(loc_root() / next_note.rel_path.with_suffix(".html"), here)
        parts.append(f'<a class="branch-nav-link next" href="{html.escape(href)}"><span>{html.escape(t("next"))}</span><strong>{html.escape(display_title(next_note))}</strong></a>')
    parts.append("</nav>")
    return "\n" + "".join(parts)


def related_notes_html(note: Note, all_notes: list[Note]) -> str:
    if page_kind(note) in {"index", "registry"}:
        return ""
    note_tags = {tag.lower() for tag in note.tags}
    slug = branch_slug(note)
    scored = []
    for other in all_notes:
        if other.rel_path == note.rel_path or page_kind(other) in {"index", "registry"}:
            continue
        score = 0
        if slug and branch_slug(other) == slug:
            score += 5
        score += len(note_tags.intersection({tag.lower() for tag in other.tags})) * 3
        if score:
            scored.append((score, other.title.lower(), other))
    if not scored:
        return ""
    here = note.out_path.parent
    cards = []
    for _, _, other in sorted(scored, key=lambda item: (-item[0], item[1]))[:4]:
        href = os.path.relpath(loc_root() / other.rel_path.with_suffix(".html"), here)
        label = branch_label(branch_slug(other)) if branch_slug(other) else t("bc_ai")
        cards.append(
            f'<a class="related-card" href="{html.escape(href)}"><span>{html.escape(label)}</span>'
            f'<strong>{html.escape(display_title(other))}</strong><small>{html.escape(display_description(other))}</small></a>'
        )
    return f'\n<section class="related-notes"><h2>{html.escape(t("related_notes"))}</h2><div class="related-grid">{"".join(cards)}</div></section>'


def build_home(tree: dict[str, dict[str, list[Note]]], notes: list[Note]) -> str:
    section_root = tree.get(SECTION, {}).get("", [])
    root_by_slug = {n.slug: n for n in section_root}
    registry_notes = [n for n in section_root if n.slug.startswith("reference-registry")]
    atomic_count = sum(1 for note in notes if len(note.rel_path.parts) == 3 and note.rel_path.name != "index.md")
    lab_count = len(list((ROOT / "labs" / "glassbox").glob("v*.py"))) if (ROOT / "labs" / "glassbox").exists() else 0
    real_es = sum(1 for note in notes if has_real_translation(note, "es"))
    es_coverage = round(100 * real_es / len(notes)) if notes else 0
    lines: list[str] = []

    lines.append('<section class="home-hero glassbox-hero">')
    lines.append('<div class="hero-copy">')
    lines.append('<div class="hero-crumb"><span>ai.console</span><span>/</span><span>ai-atlas</span><span>/</span><span>glassbox.trace</span></div>')
    lines.append(f'<h1>{html.escape(t("home_title"))}</h1>')
    lines.append(f'<p class="hero-subtitle">{html.escape(t("home_subtitle"))}</p>')
    lines.append(f'<p class="lede">{html.escape(t("home_lede"))}</p>')
    lines.append('<div class="cta-row">')
    lines.append(f'<a class="btn btn-primary" href="ai/start-here.html">{icon_svg("compass")}{html.escape(t("home_explore"))}</a>')
    lines.append(f'<a class="btn btn-ghost" href="#glassbox">{icon_svg("workflow")}{html.escape(t("home_playbooks"))}</a>')
    lines.append('</div></div>')
    diagram_label = (
        "Glassbox computation map: input becomes a tensor, flows through learned parameters to logits and a prediction; evaluation produces a loss and backward gradients update parameters."
        if CURRENT_LOCALE == "en" else
        "Mapa de cómputo Glassbox: el input se vuelve tensor, atraviesa parámetros aprendidos hasta logits y una predicción; la evaluación produce un loss y los gradientes actualizan parámetros."
    )
    lines.append(
        f'<div class="glassbox-computation-map" role="img" aria-label="{html.escape(diagram_label)}">'
        '<div class="gb-caption"><span>GLASSBOX COMPUTATION MAP</span><b>trace #0001</b></div>'
        '<div class="gb-forward-label"><span>FORWARD</span><i>→</i></div>'
        '<div class="gb-node gb-input"><small>INPUT</small><strong>tokens / pixels</strong><div class="input-cells"><i>0.2</i><i>-0.7</i><i>1.0</i></div></div>'
        '<div class="gb-arrow">→<small>[B, N, D]</small></div>'
        '<div class="gb-node gb-tensor"><small>TENSOR</small><strong>x ∈ ℝ<sup>B×N×D</sup></strong><div class="tensor-grid"><i></i><i></i><i></i><i></i><i></i><i></i></div></div>'
        '<div class="gb-arrow">→<small>matmul + nonlinearity</small></div>'
        '<div class="gb-node gb-model"><small>MODEL / REPRESENTATION</small><strong>h = f<sub>θ</sub>(x)</strong><div class="attention-mini"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>'
        '<div class="gb-arrow">→<small>[B, V]</small></div>'
        '<div class="gb-node gb-output"><small>LOGITS → PREDICTION</small><strong>softmax(z)</strong><div class="logit-bars"><i></i><i></i><i></i><i></i></div></div>'
        '<div class="gb-eval"><span>EVAL</span><b>✓ evidence</b><em>uncertainty 0.18</em></div>'
        '<div class="gb-loss"><small>LOSS</small><strong>ℒ(ŷ, y)</strong></div>'
        '<div class="gb-backward"><span>BACKWARD</span><b>∂ℒ/∂θ</b><i>← GRADIENT ← UPDATE θ</i></div>'
        '</div>'
    )
    lines.append('<div class="hero-stats">')
    for value, label, icon in (
        (len(notes), t("stat_notes"), "file"),
        (len(BRANCHES), t("stat_branches"), "nodes"),
        (lab_count, t("stat_playbooks"), "terminal"),
        (f"{es_coverage}%", t("stat_registries"), "book"),
    ):
        lines.append(f'<div class="hero-stat">{icon_svg(icon)}<div><strong>{value}</strong><span>{html.escape(label)}</span></div></div>')
    lines.append("</div></section>")

    thesis = (
        ("AI is observable computation, not a magic box.", "Each note asks what is represented, computed, optimized, learned, measured, hidden by frameworks, and changed by production constraints.")
        if CURRENT_LOCALE == "en" else
        ("La IA es cómputo observable, no una caja mágica.", "Cada nota pregunta qué se representa, computa, optimiza, aprende, mide, oculta un framework y cambia bajo restricciones de producción.")
    )
    lines.append(f'<section class="glassbox-thesis"><span class="section-eyebrow">GLASSBOX INTELLIGENCE</span><h2>{html.escape(thesis[0])}</h2><p>{html.escape(thesis[1])}</p></section>')

    lines.append('<section class="path-intro">')
    lines.append(f'<div><span class="section-eyebrow">{html.escape(t("path_eyebrow"))}</span><h2>{html.escape(t("path_h2"))}</h2><p>{html.escape(t("path_p"))}</p></div>')
    lines.append(f'<a class="path-intro-cta" href="ai/start-here.html">{html.escape(t("path_cta"))}{icon_svg("arrow")}</a>')
    lines.append("</section>")
    lines.append('<section class="learning-paths"><div class="learning-path-grid">')
    for index, (title, route, branch) in enumerate(LEARNING_PATHS.get(CURRENT_LOCALE, LEARNING_PATHS[DEFAULT_LOCALE]), 1):
        lines.append(
            f'<a class="learning-path-card" href="ai/{html.escape(branch)}/index.html">'
            f'<span>{index:02d}</span><h3>{html.escape(title)}</h3><p>{html.escape(route)}</p>{icon_svg("arrow")}</a>'
        )
    lines.append('</div></section>')

    roadmap_copy = (
        ("Glassbox AI Lab", "Build the stack progressively: scalars and probability → autodiff → models → runtimes → retrieval → agents → production evidence.")
        if CURRENT_LOCALE == "en" else
        ("Glassbox AI Lab", "Construí el stack progresivamente: escalares y probabilidad → autodiff → modelos → runtimes → retrieval → agentes → evidencia de producción.")
    )
    lines.append('<section class="glassbox-roadmap" id="glassbox">')
    lines.append(f'<span class="section-eyebrow">SPINE PROJECT · v0→v10</span><h2>{html.escape(roadmap_copy[0])}</h2><p>{html.escape(roadmap_copy[1])}</p><div class="glassbox-roadmap-grid">')
    for version, title_en, title_es, status, branches in GLASSBOX_ROADMAP:
        title = title_es if CURRENT_LOCALE == "es" else title_en
        branch_links = "".join(f'<a href="ai/{slug}/index.html">{html.escape(branch_label(slug))}</a>' for slug in branches)
        lines.append(
            f'<article class="glassbox-step status-{status.lower().replace(" ", "-")}"><header><b>{version}</b><span>{html.escape(status)}</span></header>'
            f'<h3>{html.escape(title)}</h3><div>{branch_links}</div></article>'
        )
    lines.append('</div><a class="spine-cta" href="ai/research-and-experimentation/index.html">' + ("Open the lab specification" if CURRENT_LOCALE == "en" else "Abrir la especificación del lab") + icon_svg("arrow") + '</a></section>')

    legend_title = "Depth and editorial state" if CURRENT_LOCALE == "en" else "Profundidad y estado editorial"
    lines.append(f'<section class="depth-legend"><span class="section-eyebrow">ATLAS LEGEND</span><h2>{html.escape(legend_title)}</h2>')
    lines.append('<div class="legend-row"><strong>TYPE</strong><span>OVERVIEW</span><span>FOUNDATIONAL</span><span>DERIVATION</span><span>IMPLEMENTATION</span><span>SYSTEM</span><span>PLAYBOOK</span><span>PAPER GUIDE</span><span>LAB</span></div>')
    lines.append('<div class="legend-row"><strong>LEVEL</strong><span>BEGINNER</span><span>INTERMEDIATE</span><span>ADVANCED</span></div>')
    lines.append('<div class="legend-row"><strong>STATUS</strong><span class="legend-current">CURRENT</span><span class="legend-review">REVIEW NEEDED</span><span class="legend-outdated">OUTDATED</span><span>PLANNED</span><span>EXPERIMENTAL</span></div></section>')

    for phase in PHASES:
        group = str(phase["key"])
        branches = [slug for slug in BRANCHES if branch_group(slug) == group and branch_notes(tree, slug)]
        entry_cards = ORIENTATION_ENTRY_CARDS if group == "Orientation" else []
        if not branches and not entry_cards:
            continue
        lines.append(f'<section class="phase-section" id="phase-{slugify(group)}">')
        lines.append(
            '<header class="phase-section-head">'
            f'<div class="phs-num">{html.escape(str(phase["num"]))}</div><div>'
            f'<div class="phs-eyebrow">{html.escape(t("phase_label"))} {html.escape(str(phase["num"]))} · {html.escape(t("tag_" + group))}</div>'
            f'<h2>{html.escape(group_label(group))}</h2><p>{html.escape(t("intent_" + group))}</p></div>'
            f'<a class="phs-open" href="{html.escape(str(phase["href"]))}">{html.escape(t("phase_overview"))}{icon_svg("arrow")}</a>'
            '</header>'
        )
        lines.append('<div class="branch-grid">')
        for slug, icon, accent in entry_cards:
            note = root_by_slug.get(slug)
            if not note:
                continue
            label = t("ai_index") if slug == "index" else display_title(note)
            lines.append(
                f'<a class="branch-card entry-card accent-{accent}" href="{html.escape(note.url)}">'
                f'<div class="bc-head"><span class="bc-icon">{icon_svg(icon)}</span></div>'
                f'<h3>{html.escape(label)}</h3><p>{html.escape(display_description(note))}</p>'
                f'<span class="bc-link">{html.escape(t("branch_explore"))}{icon_svg("arrow")}</span></a>'
            )
        for slug in branches:
            notes_for_branch = branch_notes(tree, slug)
            href = f"ai/{slug}/index.html"
            index_note = next((n for n in notes_for_branch if n.slug == "index"), None)
            if index_note:
                href = index_note.url
            status = str(BRANCHES[slug].get("editorial_status", "REVIEW NEEDED"))
            lines.append(
                f'<a class="branch-card accent-{html.escape(branch_accent(slug))}" href="{html.escape(href)}">'
                f'<div class="bc-head"><span class="bc-icon">{icon_svg(BRANCHES[slug]["icon"])}</span><span class="bc-status">{html.escape(status)}</span></div>'
                f'<h3>{html.escape(branch_label(slug))}</h3><p>{html.escape(branch_summary(slug))}</p>'
                f'<div class="bc-foot"><span class="bc-count">{count_label(branch_note_count(tree, slug), "note_singular", "note_plural")}</span><span class="bc-link">{html.escape(t("branch_explore"))}{icon_svg("arrow")}</span></div></a>'
            )
        lines.append("</div>")
        lines.append("</section>")

    featured = (
        next((n for n in notes if n.frontmatter.get("featured") is True and page_kind(n) not in {"index", "phase", "entry", "registry"}), None)
        or next((n for n in notes if page_kind(n) in {"derivation", "implementation", "concept"}), None)
        or next((n for n in notes if page_kind(n) == "playbook"), None)
    )
    if featured:
        lines.append('<section class="featured-section">')
        lines.append(f'<div class="section-eyebrow">{html.escape(t("featured_label"))}</div>')
        lines.append(
            f'<a class="featured-card" href="{html.escape(featured.url)}"><div>'
            f'<span class="pill">{html.escape(branch_label(branch_slug(featured)))}</span>'
            f'<h2>{html.escape(display_title(featured))}</h2><p>{html.escape(display_description(featured))}</p>'
            f'<div class="tag-row">{"".join(f"<span>#{html.escape(tag)}</span>" for tag in featured.tags[:4])}</div>'
            f'</div>{icon_svg("arrow", "featured-arrow")}</a></section>'
        )

    if registry_notes:
        lines.append('<section class="reference-panel" id="registries">')
        lines.append(f'<span class="section-eyebrow">{html.escape(t("ref_eyebrow"))}</span><h2>{html.escape(t("ref_h2"))}</h2><p>{html.escape(t("ref_p"))}</p>')
        lines.append('<div class="reference-list">')
        for note in registry_notes:
            lines.append(f'<a href="{html.escape(note.url)}">{html.escape(note.title)}</a>')
        lines.append("</div></section>")

    continuity_title = "The Atlas series is one systems curriculum." if CURRENT_LOCALE == "en" else "La serie Atlas es un único currículum de sistemas."
    continuity_copy = "Low-level mechanics explain the substrate; WebAssembly explains portable execution; blockchain explains replicated adversarial state; AI Atlas explains learning and intelligent behavior." if CURRENT_LOCALE == "en" else "Low-level explica el sustrato; WebAssembly, la ejecución portable; blockchain, el estado replicado adversarial; AI Atlas, el aprendizaje y comportamiento inteligente."
    lines.append(f'<section class="related-atlases"><span class="section-eyebrow">RELATED ATLASES</span><h2>{html.escape(continuity_title)}</h2><p>{html.escape(continuity_copy)}</p><div class="related-atlas-grid">')
    for title, site_url, github_url in RELATED_ATLASES:
        localized_site = f'{site_url.rstrip("/")}/{CURRENT_LOCALE}/index.html'
        lines.append(f'<article><h3>{html.escape(title)} Atlas</h3><div><a href="{html.escape(localized_site)}" target="_blank" rel="noopener">Site</a><a href="{html.escape(github_url)}" target="_blank" rel="noopener">GitHub</a></div></article>')
    lines.append('</div></section>')

    lines.append('<footer class="home-footer">')
    lines.append(f'<div><strong>AI Atlas · Lautaro Damore</strong><p>{html.escape(t("footer_about"))}</p></div>')
    lines.append(f'<div class="footer-links"><a href="{html.escape(GITHUB_URL)}" target="_blank" rel="noopener">GitHub</a><a href="ai/start-here.html">{html.escape(t("footer_start"))}</a><a href="ai/index.html">{html.escape(t("footer_index"))}</a></div>')
    lines.append("</footer>")
    return "\n".join(lines)


def count_label(count: int, singular_key: str, plural_key: str) -> str:
    return f"{count} {t(singular_key) if count == 1 else t(plural_key)}"


def md_to_html(md_text: str) -> str:
    try:
        import markdown  # type: ignore

        return markdown.Markdown(
            extensions=["extra", "tables", "fenced_code", "sane_lists", "toc"],
            extension_configs={"toc": {"permalink": False}},
        ).convert(md_text)
    except Exception:
        return simple_markdown_to_html(md_text)


def simple_markdown_to_html(md_text: str) -> str:
    lines = md_text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False
    code_lang = ""

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            out.append("<p>" + parse_inline(" ".join(line.strip() for line in paragraph)) + "</p>")
            paragraph = []

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                out.append(f'<pre><code class="language-{html.escape(code_lang)}">{html.escape("\\n".join(code))}</code></pre>')
                code = []
                code_lang = ""
                in_code = False
            else:
                flush_paragraph()
                in_code = True
                code_lang = stripped[3:].strip()
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue
        if not stripped:
            flush_paragraph()
            i += 1
            continue
        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            label = strip_markdown_inline(heading.group(2))
            out.append(f'<h{level} id="{slugify(label)}">{parse_inline(heading.group(2))}</h{level}>')
            i += 1
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            quotes = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quotes.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote><p>" + parse_inline(" ".join(quotes)) + "</p></blockquote>")
            continue
        if is_table_start(lines, i):
            flush_paragraph()
            headers = split_table_row(lines[i])
            aligns = split_table_row(lines[i + 1])
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i]:
                rows.append(split_table_row(lines[i]))
                i += 1
            out.append(render_table(headers, aligns, rows))
            continue
        ul_match = re.match(r"^[-*+]\s+(.+)$", stripped)
        ol_match = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ul_match or ol_match:
            flush_paragraph()
            tag = "ol" if ol_match else "ul"
            pattern = r"^\d+\.\s+(.+)$" if ol_match else r"^[-*+]\s+(.+)$"
            items: list[str] = []
            current: str | None = None
            while i < len(lines):
                s = lines[i].strip()
                m = re.match(pattern, s)
                if m:
                    if current is not None:
                        items.append(current)
                    current = m.group(1)
                    i += 1
                    continue
                # Lazy continuation: a wrapped line that is not a new block joins
                # the current item (mirrors how real Markdown treats soft wraps).
                if (current is not None and s and "|" not in s
                        and not s.startswith(("#", ">", "```", "- ", "* ", "+ "))
                        and not re.match(r"^\d+\.\s", s)):
                    current += " " + s
                    i += 1
                    continue
                break
            if current is not None:
                items.append(current)
            out.append(f"<{tag}>" + "".join("<li>" + parse_inline(it) + "</li>" for it in items) + f"</{tag}>")
            continue
        paragraph.append(line)
        i += 1
    flush_paragraph()
    return "\n".join(out)


def is_table_start(lines: list[str], i: int) -> bool:
    if i + 1 >= len(lines) or "|" not in lines[i]:
        return False
    return bool(re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1]))


def split_table_row(row: str) -> list[str]:
    return [cell.strip() for cell in row.strip().strip("|").split("|")]


def render_table(headers: list[str], aligns: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{parse_inline(cell)}</th>" for cell in headers)
    body_rows = []
    for row in rows:
        body_rows.append("<tr>" + "".join(f"<td>{parse_inline(cell)}</td>" for cell in row) + "</tr>")
    return "<table><thead><tr>" + head + "</tr></thead><tbody>" + "".join(body_rows) + "</tbody></table>"


def parse_inline(text: str) -> str:
    code_tokens: list[str] = []

    def code_sub(match: re.Match) -> str:
        code_tokens.append(f"<code>{html.escape(match.group(1))}</code>")
        return f"@@CODE{len(code_tokens)-1}@@"

    text = re.sub(r"`([^`]+)`", code_sub, text)
    safe = html.escape(text, quote=False)
    safe = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", lambda m: f'<img src="{html.escape(m.group(2), quote=True)}" alt="{html.escape(m.group(1), quote=True)}">', safe)
    safe = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: f'<a href="{html.escape(html.unescape(m.group(2)), quote=True)}">{m.group(1)}</a>', safe)
    safe = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", safe)
    safe = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", safe)
    for idx, token in enumerate(code_tokens):
        safe = safe.replace(f"@@CODE{idx}@@", token)
    return safe


def strip_markdown_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"[*_~#>`]", "", text)
    return html.unescape(text).strip()


def strip_markdown(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text)
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = WIKILINK_RE.sub(lambda m: m.group(2) or m.group(1).split("/")[-1], text)
    text = re.sub(r"^#{1,6}\s+.*$", "", text, flags=re.MULTILINE)
    text = TAG_RE.sub(r"\1", text)
    return normalize_ws(text)


def first_content_paragraph(md_text: str) -> str:
    cleaned = strip_markdown(md_text)
    for block in re.split(r"\n\s*\n", cleaned):
        block = normalize_ws(block)
        if len(block) >= 40:
            return block
    return cleaned[:180]


def strip_html(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value)


def normalize_ws(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def truncate(value: str, limit: int = 165) -> str:
    value = normalize_ws(value)
    if len(value) <= limit:
        return value
    clipped = value[: limit - 1]
    if " " in clipped:
        clipped = clipped.rsplit(" ", 1)[0]
    return clipped.rstrip(".,;:-") + "..."


def slugify(value: str) -> str:
    value = strip_markdown_inline(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def compute_asset_version() -> str:
    h = hashlib.sha1()
    for path in (STATIC / "assets" / "atlas.css", STATIC / "assets" / "search.js", STATIC / "favicon.svg"):
        if path.exists():
            h.update(path.read_bytes())
    return h.hexdigest()[:10]


def copy_static_assets() -> None:
    if not STATIC.exists():
        return
    for path in STATIC.rglob("*"):
        if path.is_dir():
            continue
        target = OUT / path.relative_to(STATIC)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def write_manifest() -> None:
    manifest = {
        "name": SITE_NAME,
        "short_name": SITE_SHORT_NAME,
        "description": SITE_DESCRIPTION,
        "start_url": "./",
        "display": "standalone",
        "background_color": "#08111D",
        "theme_color": THEME_COLOR,
        "icons": [
            {"src": "favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
    }
    (OUT / "site.webmanifest").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def xml_escape(value: str) -> str:
    return html.escape(value, quote=True)


def write_sitemap(notes: list[Note]) -> None:
    today = date.today().isoformat()
    pages: list[tuple[str, str]] = [(SITE_URL + "/", today)]
    pages.extend((f"{SITE_URL}/{loc}/", today) for loc in LOCALES)
    for note in notes:
        lastmod = note_last_modified(note)
        for loc in LOCALES:
            if has_real_translation(note, loc):
                pages.append((locale_url(note, loc), lastmod))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, lastmod in pages:
        lines.append("  <url>")
        lines.append(f"    <loc>{xml_escape(url)}</loc>")
        lines.append(f"    <lastmod>{html.escape(lastmod)}</lastmod>")
        lines.append("  </url>")
    lines.append("</urlset>\n")
    (OUT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")


def write_robots() -> None:
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {absolute_site_url('sitemap.xml')}\n", encoding="utf-8")


def write_language_landing() -> None:
    global CURRENT_LOCALE
    CURRENT_LOCALE = DEFAULT_LOCALE
    links = "".join(f'<a class="lang-choice" href="{loc}/" hreflang="{loc}">{html.escape(LOCALE_NAME[loc])}</a>' for loc in LOCALES)
    alts = "\n".join(f'<link rel="alternate" hreflang="{loc}" href="{SITE_URL}/{loc}/">' for loc in LOCALES)
    html_doc = f"""<!doctype html>
<html lang="{DEFAULT_LOCALE}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(SITE_NAME)}</title>
<meta name="description" content="{html.escape(SITE_DESCRIPTION)}">
<meta name="robots" content="index, follow">
<link rel="canonical" href="{SITE_URL}/">
{alts}
<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta name="theme-color" content="{THEME_COLOR}">
<style>
html,body{{height:100%;margin:0}}body{{display:grid;place-items:center;background:#08111D;color:#E8EEF7;font-family:Inter,system-ui,sans-serif;padding:24px}}.landing{{display:grid;gap:18px;text-align:center}}.landing-sub{{color:#31C7D9;font-weight:700}}h1{{font-size:2rem;margin:0}}.lang-choices{{display:flex;gap:10px;justify-content:center;flex-wrap:wrap}}.lang-choice{{color:#E8EEF7;text-decoration:none;border:1px solid #33445C;background:#101B2A;padding:10px 18px;border-radius:8px;font-weight:700}}.lang-choice:hover{{border-color:#31C7D9;color:#31C7D9}}
</style>
<script>
(function(){{var locales={json.dumps(list(LOCALES))};var saved;try{{saved=localStorage.getItem('preferred-locale')}}catch(e){{}}var nav=(navigator.language||'en').slice(0,2).toLowerCase();var pick=(saved&&locales.indexOf(saved)>=0)?saved:(locales.indexOf(nav)>=0?nav:'{DEFAULT_LOCALE}');location.replace(pick+'/');}})();
</script>
</head>
<body><main class="landing"><div class="landing-sub">{html.escape(t("landing_sub"))}</div><h1>{html.escape(t("landing_title"))}</h1><div class="lang-choices">{links}</div></main></body>
</html>
"""
    (OUT / "index.html").write_text(html_doc, encoding="utf-8")


def redirect_html(target: str) -> str:
    target_attr = html.escape(target, quote=True)
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        f'<title>Redirecting...</title><link rel="canonical" href="{target_attr}">'
        '<meta name="robots" content="noindex, follow">'
        f'<meta http-equiv="refresh" content="0; url={target_attr}">'
        f'<script>location.replace({json.dumps(target)});</script></head>'
        f'<body>Redirecting to <a href="{target_attr}">{target_attr}</a>.</body></html>'
    )


def write_redirect_stubs(notes: list[Note]) -> None:
    for note in notes:
        target_path = OUT / note.rel_path.with_suffix(".html")
        if target_path.exists():
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(redirect_html(locale_url(note, DEFAULT_LOCALE)), encoding="utf-8")

    for legacy, canonical in LEGACY_REDIRECTS.items():
        canonical_url_path = canonical + ".html"
        for loc in LOCALES:
            legacy_path = OUT / loc / f"{legacy}.html"
            target = f"{SITE_URL}/{loc}/{canonical_url_path}"
            legacy_path.parent.mkdir(parents=True, exist_ok=True)
            legacy_path.write_text(redirect_html(target), encoding="utf-8")
        unprefixed = OUT / f"{legacy}.html"
        unprefixed.parent.mkdir(parents=True, exist_ok=True)
        unprefixed.write_text(redirect_html(f"{SITE_URL}/{DEFAULT_LOCALE}/{canonical_url_path}"), encoding="utf-8")


ICON_PATHS = {
    "arrow": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
    "chart": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>',
    "chip": '<rect x="5" y="5" width="14" height="14" rx="2"/><rect x="9" y="9" width="6" height="6"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><path d="m21 15-4.5-4.5L7 20"/>',
    "scale": '<path d="M12 3v18"/><path d="M8 21h8"/><line x1="4" y1="7" x2="20" y2="7"/><path d="M4 7l-2 6h4z"/><path d="M20 7l-2 6h4z"/>',
    "chevron": '<polyline points="6 9 12 15 18 9"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>',
    "gauge": '<path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/><path d="M12 12l4-4"/><path d="M7.5 15.5h9"/>',
    "github": '<path fill="currentColor" stroke="none" d="M12 .5C5.7.5.7 5.6.7 12c0 5.1 3.3 9.4 7.9 10.9.6.1.8-.3.8-.6v-2c-3.2.7-3.9-1.4-3.9-1.4-.5-1.3-1.3-1.7-1.3-1.7-1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1 1.8 2.7 1.3 3.4 1 .1-.8.4-1.3.7-1.6-2.6-.3-5.2-1.3-5.2-5.7 0-1.3.5-2.3 1.2-3.1-.1-.3-.5-1.5.1-3.1 0 0 1-.3 3.2 1.2a11 11 0 0 1 5.8 0c2.2-1.5 3.2-1.2 3.2-1.2.6 1.6.2 2.8.1 3.1.7.8 1.2 1.8 1.2 3.1 0 4.4-2.7 5.4-5.3 5.7.4.4.8 1.1.8 2.1v3.1c0 .3.2.7.8.6 4.6-1.5 7.9-5.8 7.9-10.9C23.3 5.6 18.3.5 12 .5z"/>',
    "home": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "layout": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18"/><path d="M9 21V9"/>',
    "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
    "message": '<path d="M21 15a4 4 0 0 1-4 4H7l-4 4V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"/>',
    "nodes": '<circle cx="6" cy="6" r="3"/><circle cx="18" cy="7" r="3"/><circle cx="12" cy="18" r="3"/><path d="M8.6 7.4 15.4 6.6M7.5 8.5 10.5 15.5M16.5 9.5 13.5 15.5"/>',
    "playbook": '<path d="M8 3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3"/><path d="M16 3h3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-3"/><path d="m10 8 4 4-4 4"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "spark": '<path d="M13 2 3 14h7l-1 8 10-12h-7z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M6.3 17.7l-1.4 1.4M19.1 4.9l-1.4 1.4"/>',
    "terminal": '<polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/>',
    "workflow": '<rect x="3" y="4" width="6" height="6" rx="1"/><rect x="15" y="14" width="6" height="6" rx="1"/><path d="M9 7h3a3 3 0 0 1 3 3v4"/>',
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-8 8l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 8-8z"/>',
}


def icon_svg(name: str, cls: str = "") -> str:
    class_attr = f' class="{html.escape(cls)}"' if cls else ""
    paths = ICON_PATHS.get(name, ICON_PATHS["file"])
    fill = ' fill="none"'
    if name == "github":
        fill = ""
    return f'<svg{class_attr} viewBox="0 0 24 24"{fill} stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{paths}</svg>'


def build_locale(notes: list[Note], tree: dict[str, dict[str, list[Note]]], by_slug: dict[str, list[Note]], by_path: dict[str, Note]) -> tuple[int, int, list[dict]]:
    pages = 0
    unresolved = 0
    search_entries: list[dict] = []
    for base_note in notes:
        note, fallback = localized_note(base_note)
        rewritten = rewrite_links(note.body_md, note, by_slug, by_path)
        unresolved += rewritten.count("unresolved-link")
        body = md_to_html(rewritten)
        if fallback and CURRENT_LOCALE != DEFAULT_LOCALE:
            body = f'<div class="translation-pending" role="note">{html.escape(t("translation_pending"))}</div>\n' + body
        sidebar = render_sidebar(tree, note)
        page = render_page(note, body, sidebar, tree, notes)
        note.out_path.parent.mkdir(parents=True, exist_ok=True)
        note.out_path.write_text(page, encoding="utf-8")
        slug = branch_slug(note)
        search_entries.append(
            {
                "title": note.title,
                "url": note.url,
                "section": note.section,
                "branch": branch_label(slug) if slug else t("bc_ai"),
                "group": group_label(branch_group(slug)) if slug else t("reference_system"),
                "kind": page_kind(note),
                "tags": note.tags,
                "description": note_description(note),
                "keywords": page_keywords(note),
                "text": strip_html(body)[:2200],
                "content_language": note.content_locale,
                "translation_status": "fallback" if fallback else "native",
                "level": str(note.frontmatter.get("level", "")),
                "status": str(note.frontmatter.get("status", "review-needed")),
            }
        )
        pages += 1

    home = Note(section="", rel_path=Path("index.md"), title=t("home_title"), slug="index", body_md="", frontmatter={}, source_path=None, content_locale=CURRENT_LOCALE)
    home_body = build_home(tree, notes)
    sidebar = render_sidebar(tree, home)
    home.out_path.parent.mkdir(parents=True, exist_ok=True)
    home.out_path.write_text(render_page(home, home_body, sidebar, tree, notes), encoding="utf-8")
    (loc_root() / "search.json").write_text(json.dumps(search_entries, ensure_ascii=False), encoding="utf-8")
    return pages + 1, unresolved, search_entries


ASSET_VER = "0"


def validate_taxonomy(notes: list[Note]) -> int:
    """Warn about structural drift between content and the BRANCHES/PHASES config.

    Non-fatal: a typo in a branch group or a content folder without a BRANCHES
    entry would otherwise silently drop cards/labels from the site.
    """
    warnings: list[str] = []
    if set(BRANCHES_ES) != set(BRANCHES):
        warnings.append(
            f"BRANCHES_ES parity failure (missing={sorted(set(BRANCHES) - set(BRANCHES_ES))}, "
            f"extra={sorted(set(BRANCHES_ES) - set(BRANCHES))})"
        )
    for slug, meta in BRANCHES.items():
        if meta.get("group") not in PHASE_KEYS:
            warnings.append(f"branch '{slug}' has group '{meta.get('group')}' with no matching phase")
    content_branches = {branch_slug(n) for n in notes if branch_slug(n)}
    for slug in sorted(content_branches):
        if slug not in BRANCHES:
            warnings.append(f"content folder 'ai/{slug}/' has no BRANCHES entry (no card, label, or accent)")
    for slug in BRANCHES:
        if slug not in content_branches:
            warnings.append(f"branch '{slug}' is configured but has no notes in content/ yet")
    by_path = {note.rel_path.with_suffix("").as_posix() for note in notes}
    for legacy, target in LEGACY_REDIRECTS.items():
        if target not in by_path:
            warnings.append(f"redirect target is missing: {legacy} -> {target}")
    for message in warnings:
        print(f"[warn] {message}", file=sys.stderr)
    return len(warnings)


def main() -> int:
    global ASSET_VER, CURRENT_LOCALE
    ASSET_VER = compute_asset_version()
    notes = load_notes()
    if not notes:
        print("[error] loaded 0 notes; refusing to clear site/.", file=sys.stderr)
        return 1
    validate_taxonomy(notes)
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True, exist_ok=True)

    by_slug, by_path = build_slug_index(notes)
    tree = build_sidebar_tree(notes)
    total_pages = 0
    total_unresolved = 0
    for loc in LOCALES:
        CURRENT_LOCALE = loc
        pages, unresolved, _ = build_locale(notes, tree, by_slug, by_path)
        total_pages += pages
        total_unresolved += unresolved

    CURRENT_LOCALE = DEFAULT_LOCALE
    copy_static_assets()
    write_manifest()
    write_sitemap(notes)
    write_robots()
    write_language_landing()
    write_redirect_stubs(notes)
    (OUT / ".nojekyll").write_text("", encoding="utf-8")
    atomic_count = sum(1 for note in notes if len(note.rel_path.parts) == 3 and note.rel_path.name != "index.md")
    real_es = sum(1 for note in notes if has_real_translation(note, "es"))
    print(
        f"Built {total_pages} localized pages from {len(notes)} canonical pages into {OUT} "
        f"(atomic notes: {atomic_count}, branches: {len(BRANCHES)}, redirects: {len(LEGACY_REDIRECTS)}, "
        f"ES coverage: {real_es}/{len(notes)} [{100 * real_es / len(notes):.1f}%], unresolved links: {total_unresolved})."
    )
    if total_unresolved:
        print("[error] unresolved internal links are a hard build failure.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
