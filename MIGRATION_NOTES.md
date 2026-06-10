# MIGRATION_NOTES.md — Deep Rewrite of AI Atlas

Working log for the multi-batch deep rewrite (survey-level → operational-depth notes).
Created during Phase 0 (2026-06-10). This file is the source of truth for the audit,
the batch plan, the EN/ES divergence tracker, and the per-batch changelog.

---

## 1. Phase 0 findings — how the repo actually works

### Content layout
- `content/en/ai/<branch>/<slug>.md` — canonical EN notes (source of truth).
- `content/en/ai/<branch>/index.md` — branch landing page; links every note and ends
  with `## Core sources` (3–5 sources pulled from `SOURCES.md`).
- `content/es/ai/...` — ES overlay at the **same path**. Missing ES file → build falls
  back to EN content with a "not translated yet" banner (see `localized_note()` in
  `build.py`). ES register is **Rioplatense voseo**.
- Root pages (`start-here.md`, `must-know.md`, `phase-*.md`, `reference-registry.md`,
  `ai/index.md`) are navigation/orientation pages — out of rewrite scope.

### Frontmatter schema (must be preserved)
```yaml
title: "..."          # quoted string
description: ...      # one-line SEO/search description
tags: [a, b, c]
order: N              # position within branch (index = 0)
updated: YYYY-MM-DD
# featured: true      # at most ONE note across the whole atlas
# draft: true         # excluded from build/search/sitemap
```
Unknown keys are parsed and ignored by `build.py` (`parse_frontmatter` keeps them in
`note.meta`), so an additive tracking flag is build-safe.

### Links
- Wikilinks: `[[ai/<branch>/<slug>|Label]]` (path form), `[[slug|Label]]` (slug form),
  anchors `[[ai/x/y#h|Label]]`. Resolved by `resolve_link()`; unresolved links render
  as `<span class="unresolved-link">` and are counted in the build summary.
- **Hard gate:** build summary must end `(unresolved links: 0)` and
  `grep -rl 'class="unresolved-link"' site/en site/es | wc -l` must print 0.

### Build system
- `python3 build.py` — plain Python, zero required deps. Deletes and regenerates
  `site/` every run (never hand-edit `site/`). Baseline verified 2026-06-10:
  **490 localized pages from 244 notes, unresolved links: 0**.
- Taxonomy lives in `BRANCHES` / `BRANCHES_ES` / `PHASES` dicts in `build.py`;
  `validate_taxonomy()` warns on drift. No taxonomy changes needed for this rewrite.
- **Renderer gotcha:** local builds use a built-in Markdown fallback (the `markdown`
  pip package is usually absent). Author for the fallback: ATX headings, **flat**
  lists only (no nesting), tables, blockquotes, fenced code, inline code/bold/links.
  CI installs `markdown`+`pygments`, so fenced code gets syntax highlighting in prod.
- Deploy: GitHub Pages via `.github/workflows/deploy.yml`, builds from `main`.
  **Every push to `main` publishes.**

### Inventory
- 244 EN markdown files = 217 content notes + 17 branch indexes + 10 nav/root pages.
- 17 branches across 6 phases (00 Orientation → ★ Always Active).
- ES overlay: 76 files. **4 branches fully translated** (`foundations`,
  `machine-learning`, `deep-learning`, `llms`), all 17 phase/root pages translated,
  everything else is index-only or missing (build falls back to EN + banner).

---

## 2. Depth audit

### Method
Scored every EN note 1–5 per the rubric (1–2 superficial · 3 survey · 4–5 operational),
using mechanical signals (lines, code fences, tables, external links, named/dated
sources) calibrated against manual reads across 8 branches.

### Headline finding
The corpus is **uniformly survey-level (score 2–3)**. It is well-written and the
mental models are correct, but across all 217 notes there are:
- **3 code blocks total** (one sklearn snippet, two pseudo-code `text` fences),
- **0 external links and 0 paper citations in note bodies** (sources exist only as
  3–5 unlinked bullets in branch indexes),
- **0 notes with a `## Sources` section**,
- no version/date anchors (e.g. "OWASP LLM Top 10" cited without year/version),
- **3 stub notes** (≤22 lines): `foundations/mental-models-for-ai`,
  `rag-and-retrieval/rag-first-pass-design`, `llms/transformer-attention-map`.

No note currently scores 4+. The gap to "operational" is the same everywhere:
executable artifacts, named+dated+linked sources, quantified trade-offs, and
production failure modes. Score 3 = solid survey worth keeping as skeleton;
score 2 = needs a near-total rewrite; score 1 = stub, rewrite from scratch.

### Audit table

(Generated 2026-06-10. `prio` = rewrite priority; P1 = daily-use branches per owner.)

**Score distribution** (234 files): score 1: 3 · score 2: 67 · score 3: 164

| path | branch | score | gap | prio | batch |
|---|---|---|---|---|---|
| `ai/rag-and-retrieval/advanced-rag-patterns.md` | rag-and-retrieval | 3 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/chunking.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/embeddings-for-retrieval.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/evaluating-rag.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/grounding-and-citations.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/hybrid-search.md` | rag-and-retrieval | 3 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/index.md` | rag-and-retrieval | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 1 |
| `ai/rag-and-retrieval/query-transformations.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/rag-failure-modes.md` | rag-and-retrieval | 3 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/rag-first-pass-design.md` | rag-and-retrieval | 1 | STUB (~20 lines) — rewrite from scratch | P1 | 1 |
| `ai/rag-and-retrieval/rag-vs-long-context.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/reranking.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/vector-databases-and-indexes.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/rag-and-retrieval/why-rag.md` | rag-and-retrieval | 2 | solid mental model; no retrieval/rerank code (pgvector, HNSW params), no Lewis 2020 / contextual-retrieval / ColBERT anchors, no eval numbers | P1 | 1 |
| `ai/agents-and-tools/agent-computer-interface.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/agent-failure-modes.md` | agents-and-tools | 3 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/agent-memory.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/autonomy-and-control.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/evaluating-agents.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/guardrails-and-human-in-the-loop.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/index.md` | agents-and-tools | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 2 |
| `ai/agents-and-tools/model-context-protocol.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/multi-agent-systems.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/planning-and-decomposition.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/react-loop.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/tool-calling.md` | agents-and-tools | 2 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/agents-and-tools/workflows-vs-agents.md` | agents-and-tools | 3 | loop/MCP described abstractly; no Anthropic SDK tool-use code, no MCP spec refs, no ReAct/SWE-bench citations | P1 | 2 |
| `ai/prompt-engineering/anatomy-of-a-prompt.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/assembling-context.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/chain-of-thought.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/evaluating-and-iterating-prompts.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/index.md` | prompt-engineering | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 3 |
| `ai/prompt-engineering/managing-the-context-window.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/memory-and-history.md` | prompt-engineering | 3 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/prompt-to-context-engineering.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/self-consistency-and-sampling.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/structured-outputs.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/system-prompts-and-roles.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/task-decomposition.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/prompt-engineering/zero-and-few-shot.md` | prompt-engineering | 2 | zero prompt artifacts or code in a prompting branch; no Anthropic/OpenAI doc links, no concrete templates | P1 | 3 |
| `ai/evaluation/designing-eval-sets.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/eval-driven-development.md` | evaluation | 2 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/evaluating-agent-systems.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/evaluating-rag-systems.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/hallucination-detection.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/human-evaluation.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/index.md` | evaluation | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 4 |
| `ai/evaluation/llm-as-judge.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/metrics-for-llm-evals.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/model-vs-product-evals.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/nondeterminism-and-reproducibility.md` | evaluation | 2 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/prompt-regression-testing.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/public-benchmarks-and-limits.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/systematic-error-analysis.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/evaluation/task-specific-evals.md` | evaluation | 3 | process guidance only; no harness code or judge prompts, no RAGAS/promptfoo configs, no named benchmarks with dates | P1 | 4 |
| `ai/mlops/build-vs-buy-api-vs-self-hosting.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/ci-cd-for-ml.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/cost-optimization.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/experiment-tracking.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/feature-stores.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/feedback-loops.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/human-in-the-loop-production.md` | mlops | 2 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/index.md` | mlops | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 5 |
| `ai/mlops/llm-observability-and-tracing.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/mlops-to-llmops.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/model-and-prompt-registry.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/model-deprecation-and-migration.md` | mlops | 2 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/monitoring-and-drift.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/reproducible-pipelines.md` | mlops | 2 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/mlops/serving-and-inference.md` | mlops | 3 | no OTel/Langfuse instrumentation code or configs; vendor landscape unnamed/undated | P1 | 5 |
| `ai/ai-safety-and-security/data-and-pii-leakage.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/defense-in-depth-and-least-privilege.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/direct-prompt-injection.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/excessive-agency.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/index.md` | ai-safety-and-security | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P1 | 6 |
| `ai/ai-safety-and-security/indirect-prompt-injection.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/input-output-guardrails.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/insecure-output-handling.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/jailbreaks.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/owasp-llm-top-10-overview.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/privacy-and-data-governance.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/red-teaming-ai-systems.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-safety-and-security/threat-modeling-llm-apps.md` | ai-safety-and-security | 3 | OWASP cited without version; no attack/defense examples, guardrail configs, or red-team prompts | P1 | 6 |
| `ai/ai-playbooks/add-human-approval-gate.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/audit-prompt-injection.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/build-eval-set-from-scratch.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/choose-model-for-production.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/debug-agent-stuck-in-loop.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/debug-hallucination.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/decide-prompt-vs-rag-vs-finetune.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/evaluate-rag-answer-quality.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/index.md` | ai-playbooks | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P2 | 7 |
| `ai/ai-playbooks/measure-and-cut-inference-cost.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/run-ai-red-team-lite.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/ship-prompt-change-safely.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/ai-playbooks/stand-up-llm-observability.md` | ai-playbooks | 3 | sound procedure; steps lack commands, code, and numeric thresholds to execute as written | P2 | 7 |
| `ai/inference-and-optimization/batching-for-llm-serving.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/cost-modeling-for-llm-serving.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/flashattention-and-efficient-attention.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/gpu-and-hardware-basics.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/index.md` | inference-and-optimization | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P2 | 8 |
| `ai/inference-and-optimization/kv-cache-and-memory.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/latency-vs-throughput.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/prefix-and-semantic-caching.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/quantization-for-inference.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/right-sizing-models.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/serving-engines.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/speculative-decoding.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/inference-and-optimization/why-inference-is-the-real-cost.md` | inference-and-optimization | 3 | good cost framing; no 2026 pricing, no vLLM configs, no PagedAttention/FlashAttention citations | P2 | 8 |
| `ai/ai-product-engineering/choosing-a-model.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/evals-inside-the-product.md` | ai-product-engineering | 2 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/fallbacks-and-graceful-degradation.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/handling-errors-and-hallucinations-in-ui.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/human-in-the-loop-and-trust.md` | ai-product-engineering | 2 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/index.md` | ai-product-engineering | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P2 | 9 |
| `ai/ai-product-engineering/latency-cost-quality-triangle.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/onboarding-and-expectations.md` | ai-product-engineering | 2 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/pricing-vs-compute-cost.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/product-guardrails.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/product-metrics-for-ai.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/semantic-caching.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/streaming-and-perceived-latency.md` | ai-product-engineering | 2 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/the-ai-application-stack.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/ai-product-engineering/ux-patterns-for-ai.md` | ai-product-engineering | 3 | decision tables exist; no streaming/fallback code (SSE/Fastify), no real pricing data | P2 | 9 |
| `ai/fine-tuning-and-alignment/building-the-finetuning-dataset.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/catastrophic-forgetting.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/cost-and-hardware.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/data-quality-for-finetuning.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/direct-preference-optimization.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/distillation.md` | fine-tuning-and-alignment | 2 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/evaluating-a-finetune.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/index.md` | fine-tuning-and-alignment | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P2 | 10 |
| `ai/fine-tuning-and-alignment/lora-and-adapters.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/qlora-and-4bit-finetuning.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/rlhf-with-ppo.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/supervised-fine-tuning.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/fine-tuning-and-alignment/when-to-fine-tune.md` | fine-tuning-and-alignment | 3 | techniques described without math or configs; no Hu 2021 / Rafailov 2023 anchors, no TRL/Axolotl examples | P2 | 10 |
| `ai/llms/base-vs-instruct.md` | llms | 3 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/context-window-and-kv-cache.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/decoding-and-sampling.md` | llms | 3 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/emergent-abilities-and-scale.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/index.md` | llms | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P3 | 11 |
| `ai/llms/long-context-and-lost-in-the-middle.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/positional-encodings.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/pretraining-next-token.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/quantization-and-inference.md` | llms | 3 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/reasoning-and-test-time-compute.md` | llms | 3 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/the-decoder-transformer.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/tokenization.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/llms/transformer-attention-map.md` | llms | 1 | STUB (~20 lines) — rewrite from scratch | P3 | 11 |
| `ai/llms/why-llms-hallucinate.md` | llms | 2 | architecture prose without equations (attention, RoPE); no tokenizer demos, no paper anchors | P3 | 11 |
| `ai/data-for-ai/data-centric-ai.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/data-cleaning-and-deduplication.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/data-contamination-and-benchmark-leakage.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/data-for-llms.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/data-pipelines-versioning-and-lineage.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/data-quality-dimensions.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/dataset-design-and-sampling.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/datasheets-and-data-documentation.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/feedback-data-and-active-learning.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/index.md` | data-for-ai | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P3 | 12 |
| `ai/data-for-ai/labeling-and-annotation.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/privacy-and-pii-in-datasets.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/synthetic-data.md` | data-for-ai | 3 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/data-for-ai/the-data-flywheel.md` | data-for-ai | 2 | frameworks loosely named; no dedup/cleaning code, no C4/FineWeb/Datasheets citations | P3 | 12 |
| `ai/deep-learning/activation-functions.md` | deep-learning | 3 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/attention-mechanism.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/cnns.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/embeddings-and-latent-spaces.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/index.md` | deep-learning | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P3 | 13 |
| `ai/deep-learning/initialization-and-normalization.md` | deep-learning | 3 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/loss-functions-in-dl.md` | deep-learning | 3 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/neural-networks-and-backprop.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/optimizers.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/regularization-in-deep-nets.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/reinforcement-learning-essentials.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/rnns-and-their-limits.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/scaling-laws.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/the-bitter-lesson.md` | deep-learning | 2 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/deep-learning/training-dynamics.md` | deep-learning | 3 | concepts without math/notation or minimal PyTorch; canonical papers (Adam, BatchNorm, Chinchilla) unnamed | P3 | 13 |
| `ai/foundations/data-splits-and-leakage.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/distribution-shift.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/evaluation-metrics.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/features-and-dimensionality.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/generalization-and-overfitting.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/gradient-descent-intuition.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/how-learning-works.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/index.md` | foundations | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P4 | 14 |
| `ai/foundations/inductive-bias-and-no-free-lunch.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/information-theory-basics.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/linear-algebra-for-ml.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/mental-models-for-ai.md` | foundations | 1 | STUB (~20 lines) — rewrite from scratch | P4 | 14 |
| `ai/foundations/probability-and-uncertainty.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/types-of-learning.md` | foundations | 3 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/foundations/when-not-to-use-ai.md` | foundations | 2 | strong prose (flagship); lacks named sources and small numeric examples | P4 | 14 |
| `ai/machine-learning/class-imbalance.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/clustering-and-pca.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/cross-validation.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/decision-trees-and-ensembles.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/error-analysis.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/feature-engineering.md` | machine-learning | 2 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/hyperparameter-tuning.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/index.md` | machine-learning | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P4 | 15 |
| `ai/machine-learning/knn-and-svm.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/linear-and-logistic-regression.md` | machine-learning | 2 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/ml-pipelines-and-leakage.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/regularization-l1-l2.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/machine-learning/supervised-learning-workflow.md` | machine-learning | 3 | closest to fit-for-scope; lacks sklearn snippets and ISLP/sklearn doc links | P4 | 15 |
| `ai/multimodal-and-generative/audio-and-speech.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/clip-and-shared-embedding-spaces.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/controlling-image-generation.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/deepfakes-provenance-and-watermarking.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/diffusion-models-intuitively.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/evaluating-generative-media.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/index.md` | multimodal-and-generative | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P4 | 16 |
| `ai/multimodal-and-generative/latent-diffusion-and-stable-diffusion.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/multimodal-landscape.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/text-to-image-conditioning-and-cfg.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/video-generation.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/vision-language-models.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/multimodal-and-generative/vision-transformers.md` | multimodal-and-generative | 3 | survey-level; no diffusion math/code, no CLIP/LDM/ViT paper anchors | P4 | 16 |
| `ai/ai-ethics-and-governance/accountability-and-human-oversight.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/ai-governance-frameworks.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/bias-and-fairness-sources-and-types.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/environmental-cost-of-ai.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/eu-ai-act-risk-tiers.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/fairness-metrics-and-impossibility-tradeoffs.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/index.md` | ai-ethics-and-governance | 3 | branch landing — refresh note links + convert Core sources bullets to real URLs | P4 | 17 |
| `ai/ai-ethics-and-governance/measuring-and-mitigating-bias.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/model-cards-and-documentation.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/privacy-consent-and-data-rights.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/responsible-ai-landscape.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/societal-and-labor-impact.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |
| `ai/ai-ethics-and-governance/transparency-and-explainability.md` | ai-ethics-and-governance | 3 | frameworks summarized; no EU AI Act article refs, NIST AI RMF mapping, or model-card/fairlearn artifacts | P4 | 17 |

---

## 3. Batch plan (proposed — awaiting approval)

One batch per branch, in priority order. Branch `index.md` is refreshed in the same
batch (link new notes, convert `## Core sources` bullets into real links). Batches of
13–14 slightly exceed the 8–12 guideline; splitting any branch into "parte 1/2" is
trivial if preferred.

| Batch | Branch | Notes | Prio |
|---|---|---|---|
| 1 | rag-and-retrieval | 13 (incl. 1 stub) | P1 |
| 2 | agents-and-tools | 12 | P1 |
| 3 | prompt-engineering | 12 | P1 |
| 4 | evaluation | 14 | P1 |
| 5 | mlops | 14 | P1 |
| 6 | ai-safety-and-security | 12 | P1 |
| 7 | ai-playbooks | 12 | P2 |
| 8 | inference-and-optimization | 12 | P2 |
| 9 | ai-product-engineering | 14 | P2 |
| 10 | fine-tuning-and-alignment | 12 | P2 |
| 11 | llms | 13 (incl. 1 stub) | P3 |
| 12 | data-for-ai | 13 | P3 |
| 13 | deep-learning | 14 | P3 |
| 14 | foundations | 14 (incl. 1 stub) | P4 |
| 15 | machine-learning | 12 | P4 |
| 16 | multimodal-and-generative | 12 | P4 |
| 17 | ai-ethics-and-governance | 12 | P4 |

Per batch: rewrite → `python3 build.py` (must end `unresolved links: 0`) → grep gate →
commit `deep-rewrite(<branch>): batch N — <slugs>` → critical self-review → **pause
for go/no-go**.

### Per-note rewrite standard
~150–250 lines, density first: mental model → mechanism (real math where it matters) →
executable artifact (TypeScript/Anthropic SDK/Fastify/pgvector/Drizzle preferred;
Python where the ecosystem demands) → named+dated techniques → failure modes &
decision rules → production lens (latency/cost/observability, Langfuse/OTel) →
cross-links → `## Fuentes`-equivalent `## Sources` (3–8 links, one line each on why
it's worth reading). Web research per note; primary sources only; unverifiable claims
get `> ⚠️ Unverified — needs source`. Never rename/move files; preserve frontmatter
schema, titles, slugs, `order`.

---

## 4. EN/ES handling — proposal

**Recommendation: option (a)** — rewrite EN deeply now; mark ES counterparts stale.

Rationale: only 4 of 17 branches have ES note translations, and none of them are P1/P2
branches (they are `foundations`, `machine-learning`, `deep-learning`, `llms` — P3/P4).
For 13 of 17 branches the build already serves EN + banner, so there is nothing to
diverge. Doubling every batch with same-batch ES (option b) would halve rewrite
throughput for branches nobody can read in ES yet.

Divergence tracking mechanism (no silent drift):
1. When an EN note with an existing ES counterpart is rewritten, add
   `translation: stale` to the **ES** file's frontmatter (additive key, ignored by
   `build.py`, verified build-safe) and list it in the tracker below.
2. The ES overlay pass (already planned in `CONTENT-PLAN.md`) later clears the flag.

### ES divergence tracker
(EN note rewritten while a real ES translation exists — empty until batches 11–15.)

| ES file | EN rewritten in batch | Status |
|---|---|---|
| `content/es/ai/rag-and-retrieval/index.md` | 1 | `translation: stale` flagged |
| `content/es/ai/rag-and-retrieval/rag-first-pass-design.md` | 1 | `translation: stale` flagged |

---

## 5. Flags & decision points for the owner

1. **Note length**: house style in `AGENTS.md` says ≈40–80 lines; this rewrite targets
   ~150–250. Proceeding with the rewrite spec (it overrides), but `AGENTS.md` §"How to
   write a note" will be left stale unless you want it updated after Batch 1.
2. **Publishing cadence**: pushes to `main` deploy immediately. Options: commit batches
   to `main` as we go (site improves incrementally, mixed-depth atlas meanwhile), or
   work on a `deep-rewrite` branch and merge at checkpoints. **Default unless told
   otherwise: work on a `deep-rewrite` branch, you merge when you like.**
3. **`CONTENT-PLAN.md`**: its progress checklist describes the original shallow pass.
   Proposal: leave untouched; this file tracks the rewrite.
4. **Stubs** (3 listed above) get full from-scratch writes within their branch batch.
5. `SOURCES.md` lists curated domains without full URLs; rewrites will resolve and link
   exact URLs per note (verified, 2026-current).

---

## 6. Changelog

(One entry per batch: notes rewritten, claims corrected, sources that failed to
resolve, items flagged for manual review.)

- 2026-06-10 — Phase 0: inventory, audit, batch plan. No content edited.
- 2026-06-10 — **Batch 1: rag-and-retrieval** (13 notes + index rewritten to the
  deep standard). Decisions taken: bilingual option (a); commits per batch to `main`;
  `AGENTS.md` note-writing section updated to the new standard.
  Claims corrected vs old notes: none factually wrong, but "long context vs RAG"
  rewritten around 2026 economics (1M windows + prompt caching ~0.1× reads → stuff+cache
  below ~200K tokens); HyDE demoted from headline technique to zero-shot niche.
  Key sourced numbers added: Contextual Retrieval −35/−49/−67% failure rates and
  $1.02/M tokens; pgvector 0.8 iterative scans + defaults (m=16, ef_construction=64,
  ef_search=40); RRF k=60 (Cormack 2009); Context Rot (Chroma 2025).
  Not fully verifiable, marked for manual review: hosted reranker latency
  (~100–600 ms, vendor-published only); 2026 embedding API price range
  ($0.02–$0.18/M tokens, varies by vendor); "refusals 5–15% of traffic" is
  experience-based judgment, not a sourced stat (phrased as such in the note).
  ES tracker: 2 files flagged stale.
