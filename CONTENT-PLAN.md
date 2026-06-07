# AI Atlas — Content Plan

Living plan for filling the atlas with rich, source-backed notes (target **10–15
per branch**, atomic and dense, no marketing fluff). Written EN-first; ES overlays
are a second pass (the build falls back to EN with a banner meanwhile).

## Taxonomy (phase → branch)

- **00 Orientation** — entry notes only (start-here, must-know)
- **01 Foundations** — `foundations` · `machine-learning`
- **02 Models** — `deep-learning` · `llms`
- **03 Engineering** — `prompt-engineering` (Prompting & Context Engineering) · `rag-and-retrieval` · `agents-and-tools` · `fine-tuning-and-alignment` · `mlops` · `ai-product-engineering`
- **04 Evaluation** — `evaluation` · `ai-safety-and-security`
- **★ Always-on** — `ai-playbooks`

Taxonomy decisions (applied 2026-06): removed `research-notes` (a log, not a
knowledge domain); promoted `fine-tuning-and-alignment` out of LLMs; reframed
`prompt-engineering` → Prompting & Context Engineering. Optional branches NOT added
(kept LLM-centric): *Inference & Optimization*, *Multimodal & Generative*.

## Progress

- [x] **foundations** — 13 notes (flagship; quality bar)
- [x] **machine-learning** — 12 notes
- [x] **deep-learning** — 12 notes
- [x] **llms** — 13 notes
- [x] **prompt-engineering** — 12 notes
- [x] **rag-and-retrieval** — 12 notes
- [x] **agents-and-tools** — 12 notes
- [x] **fine-tuning-and-alignment** — 12 notes
- [x] **mlops** — 12 notes
- [x] **ai-product-engineering** — 12 notes
- [ ] evaluation
- [ ] ai-safety-and-security
- [ ] ai-playbooks (procedural; grows organically)
- [ ] **ES overlay pass** (after EN notes land)

## Per-branch note outlines + core sources

### machine-learning
*Sources: ISLP, Géron "Hands-On ML", Andrew Ng ML, scikit-learn docs*
Supervised workflow end-to-end · Linear & logistic regression · Trees & ensembles
(RF, gradient boosting) · kNN & SVM · Regularization (L1/L2) · Feature engineering ·
Cross-validation & splits · Class imbalance · Hyperparameter tuning · Clustering &
PCA · Error analysis · Pipelines & preprocessing leakage

### deep-learning
*Sources: Karpathy Zero-to-Hero, d2l.ai, Goodfellow DL book, CS231n, Distill.pub*
Backprop as a compute graph · MLPs & nonlinearities · Init & normalization · Optimizers
(SGD→Adam) · Regularization (dropout, weight decay) · CNNs · RNNs & their limits ·
Attention · Embeddings & latent spaces · Loss functions · Training dynamics (LR
schedules, grad clipping) · Scaling laws

### llms
*Sources: Karpathy "Let's build GPT", Raschka "Build an LLM from Scratch", Alammar Illustrated Transformer, HF LLM course, Jurafsky & Martin SLP3*
The decoder transformer · Tokenization (BPE) · Pretraining (next-token) · Self-attention
& multi-head · Positional encodings (RoPE) · Context window & KV cache · Decoding/sampling ·
Emergent abilities & scale · Instruction-tuned vs base · Quantization (what's lost) ·
Why LLMs hallucinate · Long context & lost-in-the-middle

### prompt-engineering (Prompting & Context Engineering)
*Sources: Anthropic (prompt + context engineering), DAIR.ai Prompt Guide, OpenAI Cookbook, Lilian Weng*
Prompt → context engineering · Anatomy of a good prompt · Zero/few-shot · Chain-of-thought
& when not · Structured outputs (JSON/schema) · System prompts & roles · Task decomposition ·
Self-consistency · Managing the context window · Memory & history · Ordering/formatting
context · Evaluating & iterating prompts

### rag-and-retrieval
*Sources: Anthropic Contextual Retrieval, Pinecone/Weaviate guides, LlamaIndex Advanced RAG, RAGAS*
Why RAG (vs fine-tune) · Chunking that respects structure · Embeddings & embedding models ·
Vector DBs & indexes (HNSW) · Hybrid search (BM25 + dense) · Reranking (cross-encoder) ·
Query rewriting/expansion · HyDE & multi-query · Grounding & citations · Evaluating
retriever vs generator · RAG failure modes · Contextual/Graph RAG

### agents-and-tools
*Sources: Anthropic "Building Effective Agents" + tools + multi-agent, MCP, OpenAI agents guide, Lilian Weng agents*
Workflow vs agent (when each) · Tool/function calling · Agent-computer interface design ·
ReAct · Planning & decomposition · Agent memory · Multi-agent & handoffs · MCP · Guardrails
& human approval · Failure modes (loops, bad tools) · Evaluating agents · Autonomy limits

### fine-tuning-and-alignment
*Sources: HF PEFT, Unsloth docs, LoRA/QLoRA/DPO papers, Raschka*
When FT vs RAG vs prompt · SFT (instruction tuning) · LoRA & why it works · QLoRA (4-bit) ·
RLHF (PPO) concept · DPO (and why it replaced RLHF) · Data quality > quantity · Building the
dataset · Catastrophic forgetting · Distillation · Evaluating a fine-tune · Cost & hardware

### mlops
*Sources: Chip Huyen "Designing ML Systems" + "AI Engineering", Made With ML, Google MLOps, MLflow/W&B*
MLOps → LLMOps · Experiment tracking · Model/prompt registry & versioning · Reproducible
pipelines · Monitoring & drift · Observability (tracing, the 5 pillars) · CI/CD for ML ·
Feature stores · Serving & inference (latency/throughput) · Cost optimization · HITL in prod ·
Feedback loops

### ai-product-engineering
*Sources: "The Shape of AI" UX patterns, Chip Huyen AI Engineering, Anthropic/OpenAI cookbooks, Jakob Nielsen AI UX*
UX patterns for AI · Streaming & perceived latency · Latency vs cost vs quality · Fallbacks
& graceful degradation · Semantic caching · Human-in-the-loop & trust · Handling errors/
hallucination in UI · Product metrics · Product guardrails · Onboarding & expectations ·
Pricing vs compute cost · Evals inside the product

### evaluation
*Sources: Hamel Husain (LLM-as-judge), Eugene Yan (evals), Shreya Shankar, RAGAS, Chip Huyen*
Model vs product eval · Designing an eval set / golden dataset · LLM-as-judge (& its biases) ·
Exact/semantic/groundedness metrics · Task-specific eval · Hallucination detection · Prompt
regression testing · Human eval done right · Public benchmarks (& limits) · Systematic error
analysis · Evaluating RAG · Evaluating agents

### ai-safety-and-security
*Sources: OWASP Top 10 for LLM Apps (2025), OWASP Agentic Top 10, Simon Willison (injection), Lilian Weng adversarial*
OWASP LLM Top 10 overview · Direct prompt injection · Indirect injection (data) · Jailbreaks ·
Data/PII leakage · Excessive agency (agents) · Insecure output handling · Threat modeling LLM
apps · Guardrails (input/output) · Red teaming · Defense-in-depth & least privilege · Privacy
& data governance

### ai-playbooks (procedural)
Evaluate RAG answer quality · Build an eval set from scratch · Debug an agent stuck in a loop ·
Audit an app for prompt injection · Decide prompt vs RAG vs fine-tune · Measure & cut inference
cost · Ship a prompt change safely · Stand up LLM observability

## Conventions

- Atomic notes: H1 + short framing + 2–4 sections (bullets/tables) + a **Pitfall**/**In
  practice** angle + a **Connects to** line of `[[wikilinks]]`.
- Cite real, authoritative, current sources; put them in the branch index "Core sources"
  (and/or a per-branch reference registry). No marketing summaries.
- `featured: true` on one standout note; `draft: true` to stage WIP.
- Internal links use `[[ai/<branch>/<slug>|Label]]`; never leave unresolved links.
