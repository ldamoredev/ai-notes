# AI Atlas — content plan

This is the editorial source of truth after the July 2026 refoundation. Counts and translation coverage shown on the site are generated from source; this file tracks intent, depth, and completion criteria.

## North star

AI Atlas explains artificial intelligence from first principles to production systems. A reader should be able to move through:

```text
representation → objective → computation → learning → model → inference
→ context/tools → evaluation/trust → product/operations
```

without a framework or vendor hiding the mechanism. Every mature topic connects theory to an inspectable artifact, failure behavior, and operational evidence.

## Editorial states

- `PLANNED` — branch/index exists; atomic coverage is not yet sufficient.
- `EXPERIMENTAL` — useful artifacts exist, but APIs or conclusions remain intentionally unstable.
- `REVIEW NEEDED` — inherited content exists and needs source/mechanism/reproducibility work.
- `CURRENT` — flagship or branch material meets the current editorial contract.
- `STALE` — factual or translation review is overdue; the build must not advertise it as current localized content.

Status is not a quality score. `AI-ATLAS-AUDIT.md` records the static evidence signals per page.

## Taxonomy and branch roadmap

### Phase 00 — Orientation

- [x] EN/ES `Start Here` rebuilt around learning paths, depth, evidence, and navigation.
- [x] EN/ES `Must Know` rebuilt as 12 durable rules.
- [x] Phase and root maps describe the complete 8-phase curriculum.
- [ ] Add a one-command learner environment check and source-verification walkthrough.

### Phase 01 — Foundations

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Mathematics for AI | CURRENT | vectors/tensors; probability; optimization; information theory | calculus/chain rule; statistics; distributions; Bayesian inference; numerical stability |
| Computation & Autodiff | CURRENT | backpropagation from first principles | arrays/strides; vectorization; forward-mode AD; floating point; GPU kernels |
| Classical AI & Reasoning | PLANNED | branch map | search; A*; CSP; planning; logic; Bayesian networks; decision theory |
| Learning Foundations | REVIEW NEEDED | generalization, splits, shift, metrics | source-backed rewrites; assumption ledger; decision-focused examples |
| Statistical Machine Learning | REVIEW NEEDED | supervised workflow and classical algorithms | calibration; uncertainty; tree/kernel implementations; error-analysis labs |
| Data for AI | REVIEW NEEDED | data-centric lifecycle | contamination; synthetic data; lineage; sampling; annotation agreement |

### Phase 02 — Learning and Models

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Deep Learning | REVIEW NEEDED | activations, training dynamics, scale | MLP from scratch; initialization lab; residual streams; training diagnostics |
| Reinforcement Learning | PLANNED | RL essentials | MDPs; Bellman; TD; Q-learning; policy gradients; offline RL; reward failure |
| Model Architectures | CURRENT | self-attention from first principles | transformer block; CNNs; RNNs; MoE; state-space models; diffusion architecture |
| Language & Foundation Models | REVIEW NEEDED | prompt-to-token trace | pretraining objective; tokenizer lab; decoder block; long context; reasoning |
| Vision, Audio & Multimodal AI | REVIEW NEEDED | existing multimodal map | ViT/CLIP lab; diffusion derivation; speech pipeline; provenance and evaluation |

### Phase 03 — Training and Inference

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Training & Adaptation | REVIEW NEEDED | SFT, LoRA/QLoRA, RLHF, DPO | dataset contract; distributed training; checkpoint/recovery; adaptation evaluation |
| Inference Systems | REVIEW NEEDED | KV cache, batching, quantization, engines | measured serving lab; scheduler; paged cache; profiling; capacity planning |

### Phase 04 — Context and Agency

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Context Engineering | REVIEW NEEDED | prompts, assembly, memory | authority/provenance model; compaction; grammar constraints; context evals |
| Retrieval & Knowledge | REVIEW NEEDED | mature RAG set | dependency-free retrieval lab; hybrid/reranking measurements; corpus lifecycle |
| Agents & Tools | REVIEW NEEDED | workflow/agent, tools, MCP, controls | state machine lab; durable execution; permissions; trajectory evaluation |

### Phase 05 — Measurement and Trust

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Evaluation & Measurement | REVIEW NEEDED | eval sets, judges, RAG/agent evals | uncertainty intervals; calibration; decision thresholds; contamination tests |
| Interpretability | PLANNED | branch map | attribution; probes; causal intervention; circuits; sparse autoencoders; faithfulness |
| AI Safety & Security | REVIEW NEEDED | OWASP-oriented application security | executable threat model; injection fixtures; tool sandboxing; incident response |
| AI Ethics & Governance | REVIEW NEEDED | fairness, documentation, governance | claim-control-evidence mappings; monitoring; appeal; current legal verification |

### Phase 06 — Product and Operations

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| AI Product Engineering | REVIEW NEEDED | UX, trade-offs, guardrails, product evals | non-AI baseline; rollout lab; trust/recovery UX; unit economics |
| MLOps & Operations | REVIEW NEEDED | registry, tracing, CI/CD, monitoring | end-to-end OTel lab; data/model lineage; rollback drill; SLOs and incidents |

### Always active

| Branch | State | Current anchor | Next deep notes |
|---|---|---|---|
| Research & Experimentation | EXPERIMENTAL | Glassbox artifacts and research protocol | paper-reading; evidence matrix; reproduction report; benchmark-gaming checks |
| AI Playbooks | REVIEW NEEDED | 12 operating procedures | add prerequisites, fixtures, expected artifacts, rollback, and validation commands |

## Flagship set

The first six notes define the new content bar:

- [x] `mathematics-for-ai/vectors-matrices-and-tensors`
- [x] `mathematics-for-ai/probability-likelihood-and-uncertainty`
- [x] `mathematics-for-ai/gradient-descent-and-optimization`
- [x] `computation-and-autodiff/backpropagation-from-first-principles`
- [x] `model-architectures/self-attention-from-first-principles`
- [x] `llms/from-prompt-to-generated-token`

Each must retain expanded frontmatter, defined notation and shapes, a numerical example, executable verification, framework-hidden details, failure modes, production implications, exercises, graph links, and primary sources.

## Glassbox AI Lab v0→v10

| Milestone | Deliverable | State |
|---|---|---|
| v0 | scalar/vector operations, stable softmax, cross-entropy, seeded sampling | CURRENT |
| v1 | scalar reverse-mode autodiff, topology, accumulation, gradient checking | CURRENT |
| v2 | neural network and optimizer from scratch | PLANNED |
| v3 | minimal tensor framework and image model | PLANNED |
| v4 | tokenizer, causal attention, mini-transformer, token trace | EXPERIMENTAL |
| v5 | training and parameter-efficient adaptation | PLANNED |
| v6 | inference runtime, batching, KV cache, profiling | PLANNED |
| v7 | retrieval system with component evals | PLANNED |
| v8 | tool-using agent with explicit state and authority | PLANNED |
| v9 | multimodal pipeline and provenance checks | PLANNED |
| v10 | production system with tracing, SLOs, release, rollback, and postmortem | PLANNED |

Milestone definition of done:

- Dependency and environment contract.
- Seeded fixture or versioned dataset.
- Unit tests plus one failure-injection test.
- Expected output and a verification command.
- Metrics appropriate to the mechanism.
- Known limits, operational cost, and short postmortem.
- Links from the associated branch and note.

## Migration program

- [x] Expand taxonomy from 17 to 24 branches without gratuitous branch-slug churn.
- [x] Move seven high-confidence foundational notes and generate ten redirect families including phases.
- [x] Update all source wikilinks to canonical targets.
- [x] Rebuild all EN/ES phase pages and branch indexes with mental models, roadmaps, connections, primary sources, and internal links.
- [x] Make Spanish fallback explicit in HTML language, canonical, robots, hreflang, sitemap, and search metadata.
- [ ] Rewrite remaining inherited atomic notes by audit priority.
- [ ] Translate current flagships after their EN interfaces stabilize.

See `MIGRATION-MAP.md` for exact routes and `AI-ATLAS-AUDIT.md` for page-level decisions.

## Atomic rewrite order

1. Notes with no Sources section and no executable/example artifact.
2. High-traffic dependency notes referenced by three or more branches.
3. Mechanism notes that currently explain only vocabulary.
4. Fast-moving operational notes whose `last_verified` is missing.
5. Playbooks without fixtures, output contracts, or rollback.
6. ES translation only after the canonical English note is current.

## Per-note acceptance contract

- Core frontmatter plus `kind`, `level`, `status`, prerequisites, and `last_verified` where useful.
- Mental model survives independently of the rest of the note.
- Mechanism defines symbols, shapes, data flow, and assumptions.
- At least one numerical, traced, or executable artifact.
- Verification command and expected behavior.
- Named failure modes and a decision rule.
- Production lens where the topic reaches a running system.
- 3–8 primary sources with full URLs and reading value.
- Existing `[[wikilinks]]`; zero unresolved links after build.
- ES overlay marked `translation: stale` when an EN rewrite invalidates it.

## Required verification

```bash
python3 -m py_compile build.py scripts/*.py
python3 build.py
python3 scripts/validate_content.py
python3 scripts/validate_site.py
python3 -m unittest labs.glassbox.test_glassbox -v
```

The build and validators are release gates, not suggestions.
