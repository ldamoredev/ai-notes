---
title: "Text-to-image conditioning and CFG"
description: Text-to-image models condition diffusion on prompts, negative prompts, and classifier-free guidance to steer samples toward requested concepts.
tags: [text-to-image, diffusion, conditioning, cfg]
order: 4
updated: 2026-06-07
---
# Text-to-image conditioning and CFG

Text-to-image generation works by steering a visual denoising process with a text
representation. The prompt does not draw the image; it biases each denoising step
toward visual features associated with the text.

## Conditioning path

- A tokenizer splits the prompt into text tokens.
- A text encoder turns tokens into embeddings.
- The denoising network attends to those embeddings while predicting noise.
- Optional negative prompts describe features to avoid.
- Other conditioning can include image, mask, depth, pose, edge map, style, or reference subject.

## Classifier-free guidance

Classifier-free guidance compares two denoising predictions:

| Prediction | Meaning |
|---|---|
| Conditional | what the model predicts given the prompt |
| Unconditional | what the model predicts with no or empty prompt |
| Guided | push away from unconditional and toward prompt-conditioned direction |

Higher guidance can improve prompt adherence but may reduce realism, diversity, and
color balance.

## Prompt control levers

- Specific subject, medium, composition, lighting, and style.
- Negative prompt for recurring unwanted artifacts.
- Seed for reproducibility.
- Sampling steps and sampler choice.
- Guidance scale for adherence versus naturalness.
- Image size and aspect ratio.

## Pitfall

Prompting is only one control channel. Precise layout, pose, identity, and product
consistency usually need structural conditioning or fine-tuned adapters, not more
adjectives.

**Connects to:** [[ai/prompt-engineering/anatomy-of-a-prompt|prompt anatomy]] ·
[[ai/multimodal-and-generative/controlling-image-generation|controlling image generation]] ·
[[ai/llms/tokenization|tokenization]]
