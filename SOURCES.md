# AI Atlas — primary-source registry

Last editorial verification: **2026-07-19**. Prefer papers, standards, official documentation, and complete textbooks. A source being listed does not make every claim in it correct; notes must cite the exact source supporting the exact claim and record uncertainty when evidence is incomplete.

## Cross-cutting

- [Deep Learning](https://www.deeplearningbook.org/) — canonical neural-network and optimization reference.
- [Dive into Deep Learning](https://d2l.ai/) — executable, shape-oriented implementations.
- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/) — current NLP and language-modeling reference.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) — lifecycle risk vocabulary and profiles.
- [ML Reproducibility Checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf) — artifact and reporting expectations.

## mathematics-for-ai

- [Mathematics for Machine Learning](https://mml-book.github.io/) — linear algebra, calculus, probability, and optimization for ML.
- [Probabilistic Machine Learning: An Introduction](https://probml.github.io/pml-book/book1.html) — probability, inference, and decision theory.
- [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/) — convexity, duality, conditioning, and constrained optimization.
- [Information Theory, Inference, and Learning Algorithms](https://www.inference.org.uk/mackay/itila/) — coding, Bayesian inference, and learning.

## computation-and-autodiff

- [Automatic Differentiation in Machine Learning: a Survey](https://jmlr.org/papers/v18/17-468.html) — forward/reverse mode and complexity.
- [PyTorch autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html) — saved tensors, graph behavior, and non-differentiability.
- [JAX automatic differentiation](https://docs.jax.dev/en/latest/automatic-differentiation.html) — JVPs, VJPs, and transformation semantics.
- [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) — finite-precision foundations.

## classical-ai-and-reasoning

- [Artificial Intelligence: A Modern Approach](https://aima.cs.berkeley.edu/) — search, planning, logic, uncertainty, and decisions.
- [Berkeley CS188](https://inst.eecs.berkeley.edu/~cs188/) — executable search, game, MDP, and probabilistic-inference projects.
- [Stanford CS228](https://cs.stanford.edu/~ermon/cs228/index.html) — probabilistic graphical models.
- [Planning Domain Definition Language](https://planning.wiki/ref/pddl) — planning representation reference and links to specifications.

## foundations

- [Understanding Machine Learning](https://www.cs.huji.ac.il/~shais/UnderstandingMachineLearning/) — learnability, generalization, and optimization.
- [An Introduction to Statistical Learning](https://www.statlearning.com/) — statistical-learning theory and labs.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — production sequencing and system rules.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — production-readiness evidence.

## machine-learning

- [The Elements of Statistical Learning](https://hastie.su.domains/ElemStatLearn/) — regression, classification, kernels, ensembles, and unsupervised learning.
- [Pattern Recognition and Machine Learning](https://www.microsoft.com/en-us/research/publication/pattern-recognition-machine-learning/) — probabilistic formulation of classical methods.
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html) — implementation semantics and model-selection guidance.
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — accuracy versus probability calibration.

## data-for-ai

- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — dataset lifecycle and provenance documentation.
- [Data Cards](https://research.google/pubs/data-cards-purposeful-and-transparent-dataset-documentation-for-responsible-ai/) — structured dataset communication.
- [Data Cascades in High-Stakes AI](https://research.google/pubs/data-cascades-in-high-stakes-ai/) — compounding data failures.
- [The Curse of Recursion](https://arxiv.org/abs/2305.17493) — synthetic feedback and model collapse.
- [Hugging Face Datasets](https://huggingface.co/docs/datasets/) — loading, transformation, streaming, and metadata.

## deep-learning

- [Deep Learning](https://www.deeplearningbook.org/) — mechanisms and optimization.
- [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html) — scalar autodiff through GPT.
- [Stanford CS231n](https://cs231n.github.io/) — convolutional networks and training practice.
- [Batch Normalization](https://arxiv.org/abs/1502.03167) — original normalization method and experiments.
- [Deep Residual Learning for Image Recognition](https://arxiv.org/abs/1512.03385) — residual pathways and deep optimization.

## reinforcement-learning

- [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html) — MDPs, values, TD learning, control, and approximation.
- [Algorithms for Reinforcement Learning](https://sites.ualberta.ca/~szepesva/papers/RLAlgsInMDPs.pdf) — concise mathematical core.
- [OpenAI Spinning Up](https://spinningup.openai.com/en/latest/) — equations and reference implementations.
- [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560) — reproducibility and reporting.

## model-architectures

- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) — transformer architecture.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — Vision Transformer.
- [Switch Transformers](https://arxiv.org/abs/2101.03961) — sparse mixture-of-experts scaling.
- [Mamba](https://arxiv.org/abs/2312.00752) — selective state-space sequence modeling.
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — diffusion objective and sampling.

## llms

- [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) — autoregressive objective and byte-pair vocabulary.
- [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — scaling and in-context learning evidence.
- [SentencePiece](https://arxiv.org/abs/1808.06226) — tokenizer training from raw sentences.
- [RoFormer](https://arxiv.org/abs/2104.09864) — rotary position embeddings.
- [Hugging Face generation strategies](https://huggingface.co/docs/transformers/generation_strategies) — decoding and constraint behavior.

## multimodal-and-generative

- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) — CLIP contrastive learning.
- [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — latent diffusion and cross-attention conditioning.
- [Whisper](https://arxiv.org/abs/2212.04356) — large-scale weakly supervised speech recognition.
- [Hugging Face Diffusers](https://huggingface.co/docs/diffusers/) — current diffusion pipeline semantics.
- [C2PA specification](https://c2pa.org/specifications/specifications/2.2/index.html) — media provenance.

## fine-tuning-and-alignment

- [LoRA](https://arxiv.org/abs/2106.09685) — low-rank parameter-efficient adaptation.
- [QLoRA](https://arxiv.org/abs/2305.14314) — quantized base weights with adapters.
- [InstructGPT](https://arxiv.org/abs/2203.02155) — supervised tuning and RLHF with human evaluation.
- [Direct Preference Optimization](https://arxiv.org/abs/2305.18290) — preference optimization without an explicit online RL loop.
- [Hugging Face PEFT](https://huggingface.co/docs/peft/) — current adapter implementation semantics.

## inference-and-optimization

- [vLLM](https://arxiv.org/abs/2309.06180) — PagedAttention and serving throughput.
- [FlashAttention](https://arxiv.org/abs/2205.14135) — IO-aware exact attention.
- [Fast Inference via Speculative Decoding](https://arxiv.org/abs/2211.17192) — exact draft-and-verify acceleration.
- [GPTQ](https://arxiv.org/abs/2210.17323) — post-training quantization.
- [Hugging Face KV cache strategies](https://huggingface.co/docs/transformers/kv_cache) — cache types, offloading, and quantization.

## prompt-engineering

- [Anthropic prompt engineering overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — provider-documented techniques and limits.
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — selection, compaction, and long-running context.
- [OpenAI Cookbook](https://cookbook.openai.com/) — executable prompting, structured-output, and eval patterns.
- [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) — reasoning demonstrations and measured results.

## rag-and-retrieval

- [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) — original retriever-generator formulation.
- [Contextual Retrieval](https://www.anthropic.com/news/contextual-retrieval) — applied contextualization and retrieval measurements.
- [RAGAS](https://docs.ragas.io/) — retrieval/generation component metrics.
- [pgvector](https://github.com/pgvector/pgvector) — PostgreSQL vector search and ANN controls.
- [BEIR](https://arxiv.org/abs/2104.08663) — heterogeneous retrieval benchmark and zero-shot evaluation.

## agents-and-tools

- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — workflow/agent taxonomy.
- [ReAct](https://arxiv.org/abs/2210.03629) — interleaved reasoning and acting.
- [Model Context Protocol specification](https://modelcontextprotocol.io/specification/2025-11-25) — model-tool-resource contracts.
- [A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — orchestration and guardrails.

## evaluation

- [HELM](https://crfm.stanford.edu/helm/) — transparent multi-scenario evaluation.
- [Judging LLM-as-a-Judge](https://arxiv.org/abs/2306.05685) — judge capability and biases.
- [RAGAS](https://docs.ragas.io/) — RAG component evaluation.
- [Statistical Comparisons of Classifiers over Multiple Data Sets](https://jmlr.org/papers/v7/demsar06a.html) — comparison statistics.

## interpretability

- [A Unified Approach to Interpreting Model Predictions](https://arxiv.org/abs/1705.07874) — SHAP formulation.
- [Axiomatic Attribution for Deep Networks](https://arxiv.org/abs/1703.01365) — Integrated Gradients.
- [A Mathematical Framework for Transformer Circuits](https://transformer-circuits.pub/2021/framework/index.html) — mechanistic decomposition.
- [Toy Models of Superposition](https://transformer-circuits.pub/2022/toy_model/index.html) — feature superposition experiments.

## ai-safety-and-security

- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/) — application risk taxonomy.
- [MITRE ATLAS](https://atlas.mitre.org/) — adversarial ML tactics and techniques.
- [NIST Adversarial Machine Learning Taxonomy](https://csrc.nist.gov/pubs/ai/100/2/e2023/final) — standardized terminology.
- [Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) — attacks delivered through external data.
- [Concrete Problems in AI Safety](https://arxiv.org/abs/1606.06565) — specification, robustness, and oversight problems.

## ai-ethics-and-governance

- [EU AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) — official regulation text.
- [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) — risk governance framework.
- [Model Cards](https://arxiv.org/abs/1810.03993) — model documentation.
- [Datasheets for Datasets](https://arxiv.org/abs/1803.09010) — dataset documentation.
- [Fairness and Machine Learning](https://fairmlbook.org/) — formal fairness definitions and trade-offs.

## ai-product-engineering

- [The Shape of AI](https://www.shapeof.ai/) — AI interaction patterns.
- [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — expectation, feedback, and control patterns.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — production sequencing.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — readiness rubric.

## mlops

- [Continuous Delivery for Machine Learning](https://martinfowler.com/articles/cd4ml.html) — versioning, testing, deployment, and feedback.
- [Google MLOps](https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning) — maturity levels and pipeline architecture.
- [Hidden Technical Debt in Machine Learning Systems](https://papers.nips.cc/paper/5656-hidden-technical-debt-in-machine-learning-systems) — coupling and feedback debt.
- [OpenTelemetry specification](https://opentelemetry.io/docs/specs/otel/) — traces, metrics, and logs.
- [MLflow documentation](https://mlflow.org/docs/latest/) — experiment and model lifecycle primitives.

## research-and-experimentation

- [ML Reproducibility Checklist](https://www.cs.mcgill.ca/~jpineau/ReproducibilityChecklist.pdf) — reporting and artifacts.
- [The ML Test Score](https://research.google/pubs/the-ml-test-score-a-rubric-for-ml-production-readiness-and-technical-debt-reduction/) — tests from experiment to production.
- [Stanford CS336](https://stanford-cs336.github.io/spring2025/) — full-stack language-model reconstruction.
- [Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560) — experimental reliability lessons.

## ai-playbooks

- [NIST AI RMF Playbook](https://airc.nist.gov/airmf-resources/playbook/) — operational risk actions.
- [OWASP GenAI Security Project](https://genai.owasp.org/) — security test scopes.
- [Google Rules of ML](https://developers.google.com/machine-learning/guides/rules-of-ml) — concise production procedures.
- [RAGAS](https://docs.ragas.io/) — executable RAG evaluation workflows.

## Source hygiene

- Verify publication date, version, and URL before a deep rewrite.
- Prefer the exact paper, standard, or official documentation page over a secondary summary.
- Use secondary sources for pedagogy only; do not make them the sole support for a technical claim.
- Add `last_verified` when operational semantics or regulation can change.
- Mark unverifiable statements as `> ⚠️ Unverified — needs source` instead of laundering uncertainty into prose.
