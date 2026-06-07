# SOURCES.md — curated reference sources for AI Atlas

Authoritative, current sources gathered during the content research (June 2026), to
ground notes per branch. Cite the relevant ones in each branch `index.md` under
`## Core sources`. Prefer primary/expert sources over blog aggregators. Verify a URL
before relying on it; treat these as the canonical starting points, not gospel.

## Cross-cutting / general

- **Andrej Karpathy** — *Neural Networks: Zero to Hero* course (micrograd → makemore →
  GPT); "Intro to LLMs" / "Deep Dive into LLMs" talks. karpathy.ai · github.com/karpathy/nn-zero-to-hero
- **3Blue1Brown** — *Essence of Linear Algebra*, *Neural Networks* (visual intuition). youtube.com/@3blue1brown
- **Dive into Deep Learning** — runnable textbook. d2l.ai
- **Chip Huyen** — books *Designing Machine Learning Systems* and *AI Engineering* (2025); blog huyenchip.com
- **Hugging Face** — *LLM Course* and docs. huggingface.co/learn
- **Lilian Weng** — research blog (agents, prompt engineering, hallucination, adversarial). lilianweng.github.io
- **Jay Alammar** — *The Illustrated Transformer / GPT-2*. jalammar.github.io
- **Sebastian Raschka** — *Build a Large Language Model (From Scratch)*; blog magazine.sebastianraschka.com

## foundations
- *An Introduction to Statistical Learning* (James, Witten, Hastie, Tibshirani) — statlearning.com
- Aurélien Géron — *Hands-On Machine Learning* (3rd ed.)
- StatQuest with Josh Starmer (bias/variance, cross-validation, metrics) — youtube.com/@statquest
- Google — *Machine Learning Crash Course* — developers.google.com/machine-learning/crash-course
- 3Blue1Brown (linear algebra, calculus, probability)

## machine-learning
- *An Introduction to Statistical Learning* (ISLP)
- Géron — *Hands-On Machine Learning*
- Andrew Ng — *Machine Learning Specialization* (Coursera / DeepLearning.AI)
- **scikit-learn User Guide** — the canonical practical reference. scikit-learn.org/stable/user_guide.html
- StatQuest (trees, boosting, ROC/PR)

## deep-learning
- Karpathy — *Zero to Hero*
- d2l.ai
- Goodfellow, Bengio, Courville — *Deep Learning* (deeplearningbook.org)
- Stanford **CS231n** (CNNs / vision) — cs231n.github.io
- **Distill.pub** (visual explanations)

## llms
- Karpathy — *Let's build GPT*, *Deep Dive into LLMs*
- Raschka — *Build a Large Language Model (From Scratch)*
- Jay Alammar — *Illustrated Transformer*
- Hugging Face — *LLM Course*
- Jurafsky & Martin — *Speech and Language Processing* (SLP3, free draft) — web.stanford.edu/~jurafsky/slp3
- Stanford **CS336** (Language Modeling from Scratch); CS25 (Transformers)

## prompt-engineering (Prompting & Context Engineering)
- **Anthropic** — *Prompt engineering* docs (docs.anthropic.com) and *Effective context
  engineering for AI agents* (anthropic.com/engineering)
- **DAIR.ai** — *Prompt Engineering Guide* — promptingguide.ai
- **OpenAI Cookbook** — cookbook.openai.com (structured outputs, prompting)
- Lilian Weng — *Prompt Engineering*

## rag-and-retrieval
- **Anthropic** — *Contextual Retrieval* — anthropic.com/news/contextual-retrieval
- **Pinecone** / **Weaviate** learning guides (chunking, hybrid, reranking)
- **LlamaIndex** & **LangChain** advanced-RAG docs
- **RAGAS** — retrieval/generation eval — docs.ragas.io
- Jason Liu (instructor / RAG patterns); Eugene Yan (RAG patterns) — eugeneyan.com

## agents-and-tools
- **Anthropic** — *Building Effective Agents*; *Writing effective tools for agents*;
  *How we built our multi-agent research system* (anthropic.com/engineering)
- **Model Context Protocol** — modelcontextprotocol.io (spec + docs)
- **OpenAI** — *A practical guide to building agents* (PDF)
- Lilian Weng — *LLM-Powered Autonomous Agents*

## fine-tuning-and-alignment
- **Hugging Face PEFT** docs — huggingface.co/docs/peft
- **Unsloth** docs (practical low-VRAM fine-tuning) — docs.unsloth.ai
- Papers: *LoRA* (Hu et al.), *QLoRA* (Dettmers et al.), *Direct Preference
  Optimization / DPO* (Rafailov et al.), *InstructGPT / RLHF* (Ouyang et al.)
- Sebastian Raschka — fine-tuning articles & LoRA experiments

## mlops
- Chip Huyen — *Designing Machine Learning Systems* + *AI Engineering*
- **Made With ML** (Goku Mohandas) — madewithml.com
- **Google Cloud** — *MLOps: Continuous delivery and automation pipelines in ML*
  (whitepaper)
- MLflow / Weights & Biases docs; LLM observability tools (LangSmith, Langfuse, Arize Phoenix)
- Eugene Yan — production ML/LLM writing

## ai-product-engineering
- **The Shape of AI** — UX patterns for AI — shapeof.ai
- Chip Huyen — *AI Engineering*
- **Anthropic** / **OpenAI** cookbooks (latency, streaming, caching, prod patterns)
- Jakob Nielsen / NN/g — AI UX writing
- a16z / LangChain engineering posts on LLM app architecture

## evaluation
- **Hamel Husain** — *Your AI Product Needs Evals*; *LLM-as-a-Judge* — hamel.dev
- **Eugene Yan** — *Evaluating the Effectiveness of LLM-Evaluators (LLM-as-Judge)*;
  AlignEval — eugeneyan.com
- **Shreya Shankar** + Hamel — *AI Evals for Engineers & PMs* (course)
- **RAGAS** — docs.ragas.io
- Benchmarks: HELM (crfm.stanford.edu/helm), LMSYS Chatbot Arena, MMLU

## ai-safety-and-security
- **OWASP Top 10 for LLM Applications (2025)** — genai.owasp.org
- **OWASP Agentic AI / Agentic Security Top 10** — genai.owasp.org
- **Simon Willison** — prompt-injection writing — simonwillison.net/tags/prompt-injection
- Lilian Weng — *Adversarial Attacks on LLMs*
- NIST AI Risk Management Framework; MITRE ATLAS (adversarial ML threat matrix)

## ai-playbooks (procedural)
Draw on the relevant branch sources above; playbooks turn those concepts into
step-by-step procedures.
