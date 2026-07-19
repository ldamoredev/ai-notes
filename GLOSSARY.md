# Guía de traducción ES — glosario y convenciones

Anchor de estilo y terminología para traducir las notas del atlas al español. Leé
esto antes de traducir y respetalo en **todas** las notas para mantener consistencia.
El objetivo: que un overlay ES se lea como notas de estudio de un ingeniero de IA
rioplatense — técnico, denso, directo — no como una traducción literal.

## Contrato editorial 2026

Una traducción vigente espeja la **interfaz intelectual** de la nota EN: modelo mental, mecanismo, símbolos y shapes, ejemplo numérico, artefacto ejecutable, fallas, lente de producción, ejercicios, conexiones y fuentes. No alcanza con traducir el resumen o conservar una versión anterior del concepto.

Metadata compartida:

| Campo | Uso | Regla ES |
|---|---|---|
| `kind` | `concept`, `derivation`, `implementation`, `system-walkthrough`, `playbook`, `overview` | no traducir el valor |
| `level` | profundidad previa esperada: `beginner`, `foundational`, `intermediate`, `advanced` | no traducir el valor |
| `status` | `current`, `review-needed`, `experimental`, `planned`, `stale` | no traducir el valor |
| `prerequisites` | IDs canónicos requeridos | conservar slugs EN |
| `last_verified` | última revisión factual/operativa | copiar la fecha sólo si la traducción se revisó contra esa versión EN |

`translation: stale` significa que el overlay existe pero ya no representa la nota canónica. El build lo trata como fallback EN visible: no lo publica como traducción indexable ni emite `hreflang="es"`.

## Arquitectura de la traducción (importante)

Este proyecto **no** usa vault externo ni script de extracción. Cada nota canónica
vive en `content/en/ai/<rama>/<slug>.md` y su overlay español va en
`content/es/ai/<rama>/<slug>.md` (**misma ruta, mismo nombre de archivo**).

- El overlay es el markdown **completo** de la nota (frontmatter + cuerpo), traducido.
- El build (`build.py`) regenera todo el chrome (sidebar, breadcrumbs, prev/next,
  related-cards, TOC, meta-chips) — **eso no se traduce ni va en el overlay**.
- Si falta el overlay, la página `/es/` cae al inglés con un banner. Por eso traducir
  es **incremental y seguro**: una rama a la vez.
- El build mergea el frontmatter EN con el del overlay, así que el overlay solo
  necesita pisar `title` y `description`; igual conviene copiar el frontmatter entero.

Flujo por rama:
1. Listá las notas EN: `ls content/en/ai/<rama>/`.
2. Por cada `<slug>.md`, creá `content/es/ai/<rama>/<slug>.md` con la **misma
   estructura** (mismos headings, mismas tablas, mismos wikilinks).
3. `python3 build.py` y verificá `(unresolved links: 0)`; mirá la página en `/es/`.

## Registro

- **Español rioplatense / voseo.** Imperativos en vos: `Usá`, `Pensá`, `Tené en
  cuenta`, `Evitá`, `Medí`, `Empezá`, `Fijate`, `Acordate`, `Asegurate`, `Elegí`.
- 2ª persona: `podés`, `tenés`, `querés`, `sabés`, `vas a` (nunca "puedes/tienes").
- Tono técnico, directo y conciso. **Espejá la densidad del original**: misma cantidad
  de oraciones e ideas, sin relleno ni adornos.
- No traduzcas de más: si una frase suena más natural con el término inglés (ver
  listas abajo), dejalo en inglés. La prueba: ¿cómo lo diría alguien del rubro en una
  charla técnica real?
- Cursivas/negritas (`*...*`, `**...**`) y comillas: conservalas en las mismas palabras.

## Formato del overlay

- **Frontmatter YAML**: copialo del inglés y traducí solo `title` y `description`.
  `tags`, `order`, `updated`, `featured`, `draft` **se copian igual** (no se traducen;
  los tags son slugs en inglés).
- **`# H1`**: traducí la parte genérica y dejá en inglés los términos canónicos.
  Ej: "Why LLMs hallucinate" → "Por qué alucinan los LLMs"; "LoRA and adapters" →
  "LoRA y adapters"; "The KV cache and memory" → "El KV cache y la memoria". El H1 del
  cuerpo debe coincidir con el `title` del frontmatter.
- **`## H2` / `### H3`**: se traducen. Encabezados recurrentes del atlas (forma canónica):

  | Inglés | Español |
  |---|---|
  | Pitfall | Trampa |
  | In practice | En la práctica |
  | Why it matters | Por qué importa |
  | Why it works | Por qué funciona |
  | When to use … / When not to | Cuándo usar… / Cuándo no |
  | Rule of thumb | Regla práctica |
  | The takeaway / The mental model | La idea clave / El modelo mental |
  | What this branch covers | Qué cubre esta rama |
  | Planned notes | Notas planificadas |
  | Core sources | Fuentes principales |
  | Mental model | Modelo mental |
  | Roadmap | Hoja de ruta |
  | Production lens | Lente de producción |
  | Failure modes and limits | Modos de falla y límites |
  | Exercises | Ejercicios |
  | Connects to: | Conecta con: |

- **Wikilinks**: el **target queda en inglés**, se traduce solo el **label**:
  `[[ai/llms/why-llms-hallucinate|Por qué alucinan los LLMs]]`. **Nunca** cambies la
  ruta/slug del target (esas notas existen en inglés; si tocás el target, el link se
  rompe). Si un wikilink no tiene label (`[[ai/x/y]]`), agregale uno en español:
  `[[ai/x/y|Etiqueta en español]]`.
- **Tablas**: traducí encabezados y celdas de prosa; respetá los términos que van en
  inglés. Mantené el mismo número de columnas y filas.
- **Blockquotes (`> …`)**: traducí la prosa de adentro.
- **Code blocks, código inline (`` `...` ``), comandos, rutas, URLs, identificadores,
  nombres de librerías/modelos/papers**: NO se tocan.

## Se deja en INGLÉS (no traducir inline)

Jerga que en el rubro se dice igual en inglés. Se puede pluralizar con "s" español
(`los prompts`, `los tokens`, `los embeddings`):

`prompt` · `prompting` · `system prompt` · `token` · `embedding` · `chunk` /
`chunking` · `fine-tuning` · `RAG` · `retrieval`* · `reranker` / `reranking` ·
`transformer` · `attention`* / `self-attention` / `multi-head` · `dataset` ·
`feature` / `feature engineering` · `baseline` · `pipeline` · `benchmark` ·
`overfitting` / `underfitting` · `dropout` · `batch` / `batching` · `throughput` ·
`quantization` · `cache` / `caching` · `KV cache` · `guardrails` · `grounding` ·
`jailbreak` · `prompt injection` · `tool calling` · `agent`** · `checkpoint` ·
`epoch` · `logits` · `softmax` · `tokenizer` · `encoder` / `decoder` ·
`scaling laws` · `distillation` · `loss`* · `temperature` (parámetro) ·
`top-p` / `top-k` · `LLM` · `MLOps` / `LLMOps` · `embeddings` · `prefill` / `decode`

\* Términos **mixtos** (el corpus admite ambos): preferí
`retrieval`→ a veces "recuperación"; `attention`→ "atención" es estándar y válido;
`loss`→ "función de pérdida (loss)" la primera vez, después "loss" o "la pérdida".
Elegí uno por nota y sé consistente.

\*\* `agent`→ "agente" se traduce y es natural (ver tabla); se deja `agentic` en inglés.

Nombres propios que **no** se traducen: `Transformer`, `ReAct`, `LoRA`, `QLoRA`,
`DPO`, `RLHF`, `PPO`, `CLIP`, `ViT`, `MCP`, `vLLM`, `HNSW`, `BM25`, `FlashAttention`,
`PagedAttention`, `OWASP`, `EU AI Act`, `NIST`, siglas y títulos de papers/fuentes.

Términos nuevos del spine project que se conservan: `Glassbox AI Lab`, `forward pass`,
`backward pass`, `autodiff`, `compute graph`, `gradient check`, `fixture`, `expected
output`, `failure injection`, `postmortem`, `prefill`, `decode`, `KV cache`, `VJP`,
`JVP`, `log-sum-exp`, `dtype`, `device`, `stride`, `kernel`, `tensor core`.

## Se TRADUCE (forma canónica)

| Inglés | Español |
|---|---|
| training | entrenamiento |
| to train | entrenar |
| inference | inferencia |
| weights | pesos |
| bias (modelo) | sesgo · (inductive bias) sesgo inductivo |
| bias (fairness) | sesgo |
| label | etiqueta (o `label`) |
| sampling | muestreo (o `sampling`) |
| gradient | gradiente |
| loss function | función de pérdida |
| hyperparameter | hiperparámetro |
| regularization | regularización |
| normalization | normalización |
| latency | latencia |
| cost | costo |
| serving / to serve | servir / serving (despliegue de inferencia) |
| deployment / to deploy | despliegue / desplegar |
| context window | ventana de contexto |
| hallucination | alucinación |
| agent / tool | agente / herramienta |
| retrieval-augmented | aumentado con retrieval |
| dataset design | diseño de datasets |
| fairness | fairness (equidad) — preferí `fairness` |
| accountability | responsabilidad (accountability) |
| trust | confianza |
| reward (RL) | recompensa |
| policy (RL) | política |
| trade-off | tradeoff (o "compromiso") — preferí `tradeoff` |
| pitfall | trampa |
| grounded / grounding | grounding / fundamentado en las fuentes |

## Género y artículos (préstamos del inglés)

`el prompt` · `el token` · `el embedding` · `el dataset` · `el chunk` ·
`el fine-tuning` · `el reranker` · `el pipeline` · `el benchmark` · `el overfitting` ·
`el transformer` · `el agente` · `la herramienta` · `la inferencia` · `la latencia` ·
`la ventana de contexto` · `el KV cache` · `la atención` · `los pesos` ·
`la feature` / `las features` · `el loss` / `la pérdida` · `los guardrails`.

Verbos "españolizados" aceptados cuando suenan natural: `fine-tunear`, `tokenizar`,
`parsear`, `loggear`, `chunkear` (o "dividir en chunks"). Preferí el verbo español si
existe y no suena forzado (`desplegar` mejor que "deployar").

## Qué NO tocar

- El chrome de la página (sidebar, breadcrumbs, prev/next, related-cards, TOC,
  meta-chips, botones): lo genera el build, no va en el overlay.
- Slugs de archivo, **targets** de wikilinks, anclas de heading, `tags`, fechas, URLs,
  código, nombres de modelos/librerías/papers.
- La UI chrome y las etiquetas de rama: ya están en español en `build.py`
  (`UI_STRINGS`, `BRANCHES_ES`). No las re-traduzcas en las notas.
