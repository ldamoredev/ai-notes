# AI Atlas — migration map

Refoundation date: **2026-07-19**. This document records structural decisions that affect canonical IDs, navigation, and external URLs.

## Policy

- Preserve a published branch slug when a clearer display label is sufficient.
- Move a note only when the target branch is unambiguous and improves prerequisite order.
- Update every source wikilink to the new canonical ID.
- Keep an explicit permanent mapping in `LEGACY_REDIRECTS`; the build emits EN, ES, and default-locale redirect pages.
- Redirect targets must exist and are checked by source and generated-site validators.
- Spanish overlays do not define canonical IDs. If a moved overlay is not rewritten, delete it and let `/es/` show the current English note honestly.
- Historical moves stay in this registry even after search engines and readers have migrated.

## Taxonomy: before and after

The previous source tree had 17 branch slugs. The refoundation keeps all 17 URLs and adds seven missing conceptual branches, for 24 total.

| Existing slug | New display role | Phase | URL action |
|---|---|---|---|
| `foundations` | Learning Foundations | 01 Foundations | keep |
| `machine-learning` | Statistical Machine Learning | 01 Foundations | keep |
| `data-for-ai` | Data for AI | 01 Foundations | keep |
| `deep-learning` | Deep Learning | 02 Learning & Models | keep |
| `llms` | Language & Foundation Models | 02 Learning & Models | keep |
| `multimodal-and-generative` | Vision, Audio & Multimodal AI | 02 Learning & Models | keep |
| `fine-tuning-and-alignment` | Training & Adaptation | 03 Training & Inference | keep |
| `inference-and-optimization` | Inference Systems | 03 Training & Inference | keep |
| `prompt-engineering` | Context Engineering | 04 Context & Agency | keep; label broadened |
| `rag-and-retrieval` | Retrieval & Knowledge | 04 Context & Agency | keep |
| `agents-and-tools` | Agents & Tools | 04 Context & Agency | keep |
| `evaluation` | Evaluation & Measurement | 05 Measurement & Trust | keep |
| `ai-safety-and-security` | AI Safety & Security | 05 Measurement & Trust | keep |
| `ai-ethics-and-governance` | AI Ethics & Governance | 05 Measurement & Trust | keep |
| `ai-product-engineering` | AI Product Engineering | 06 Product & Operations | keep |
| `mlops` | MLOps & Operations | 06 Product & Operations | keep |
| `ai-playbooks` | AI Playbooks | Always active | keep |
| — | `mathematics-for-ai` | 01 Foundations | new branch |
| — | `computation-and-autodiff` | 01 Foundations | new branch |
| — | `classical-ai-and-reasoning` | 01 Foundations | new branch |
| — | `reinforcement-learning` | 02 Learning & Models | new branch |
| — | `model-architectures` | 02 Learning & Models | new branch |
| — | `interpretability` | 05 Measurement & Trust | new branch |
| — | `research-and-experimentation` | Always active | new branch |

## Canonical note moves

| Previous canonical ID | New canonical ID | Reason |
|---|---|---|
| `ai/foundations/linear-algebra-for-ml` | `ai/mathematics-for-ai/vectors-matrices-and-tensors` | representation math is now an explicit prerequisite branch; content rewritten as a flagship |
| `ai/foundations/probability-and-uncertainty` | `ai/mathematics-for-ai/probability-likelihood-and-uncertainty` | separates probability, likelihood, calibration, and decision semantics; flagship rewrite |
| `ai/foundations/gradient-descent-intuition` | `ai/mathematics-for-ai/gradient-descent-and-optimization` | moves optimization out of the conceptual catch-all and adds derivation/artifact depth |
| `ai/foundations/information-theory-basics` | `ai/mathematics-for-ai/information-theory-entropy-and-divergence` | entropy and divergence belong beside probability and objectives |
| `ai/deep-learning/neural-networks-and-backprop` | `ai/computation-and-autodiff/backpropagation-from-first-principles` | backprop is a general computation-graph mechanism, not a layer taxonomy |
| `ai/deep-learning/attention-mechanism` | `ai/model-architectures/self-attention-from-first-principles` | attention is an architectural routing mechanism; flagship rewrite |
| `ai/deep-learning/reinforcement-learning-essentials` | `ai/reinforcement-learning/reinforcement-learning-essentials` | RL is a separate decision-learning paradigm, not a neural-network subtype |

The old source files were removed after wikilinks were updated. Their EN and ES URLs remain redirect stubs.

## Phase route moves

| Previous phase ID | New phase ID | Reason |
|---|---|---|
| `ai/phase-02-models-and-architectures` | `ai/phase-02-learning-and-models` | includes RL and modality-specific learning, not only architecture |
| `ai/phase-03-building-and-engineering` | `ai/phase-03-training-and-inference` | separates model execution systems from context/product work |
| `ai/phase-04-evaluation-and-security` | `ai/phase-05-measurement-and-trust` | evaluation, interpretability, security, ethics, and governance form a broader trust phase |

Phase 04 Context & Agency and Phase 06 Product & Operations are new canonical pages. The always-active phase now owns research/labs and playbooks.

## Link compatibility

`build.py` adds the old IDs as aliases in the wikilink index, so an overlooked old source link still resolves during migration. This compatibility is defensive; canonical Markdown has been rewritten to the new IDs and `rg` should only find old paths inside `LEGACY_REDIRECTS`, this document, audit history, or Git history.

Generated redirects use:

```text
/en/<legacy>.html → /en/<canonical>.html
/es/<legacy>.html → /es/<canonical>.html
/<legacy>.html    → /en/<canonical>.html
```

They include canonical metadata, `noindex, follow`, meta refresh, JavaScript replacement, and a visible fallback link.

## Spanish overlay impact

The seven moved atomic ES overlays represented the short pre-refoundation notes and were removed rather than presented as translations of the new flagship content. Their old ES URLs redirect to new ES routes; because the new flagships do not yet have complete ES overlays, those routes visibly render current English content under Spanish navigation with correct fallback metadata.

All 24 branch indexes and all eight phase pages do have current ES overlays. Atomic translation work follows the stabilized EN rewrite queue in `CONTENT-PLAN.md`.

## Verification

```bash
python3 build.py
python3 scripts/validate_content.py
python3 scripts/validate_site.py
rg -n 'ai/(foundations/(linear-algebra-for-ml|probability-and-uncertainty|gradient-descent-intuition|information-theory-basics)|deep-learning/(neural-networks-and-backprop|attention-mechanism|reinforcement-learning-essentials))' content
```

The final `rg` command should return no canonical content references. The redirect registry and this migration document intentionally retain the old IDs.
