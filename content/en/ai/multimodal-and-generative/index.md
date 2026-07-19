---
title: Multimodal & Generative
description: Beyond text - diffusion models, image/audio/video generation, vision transformers, and the vision-language models that fuse modalities.
tags: [multimodal, generative, diffusion, vision-language]
order: 0
updated: 2026-06-07
---
# Multimodal & Generative

The rest of the atlas is text-centric; this branch covers everything else AI now
generates and understands: images, audio, video, and the models that combine
modalities. The same [[ai/deep-learning/index|deep-learning]] machinery reappears here
in new shapes.

## Mental model

Multimodal systems translate different observation spaces into representations that can be aligned, fused, generated, or acted upon. The architecture and objective must respect each modality's structure while evaluation covers semantic quality, temporal or spatial consistency, provenance, and human impact.

## Roadmap: landscape and core models

- [[ai/multimodal-and-generative/multimodal-landscape|The multimodal landscape]] maps text, image, audio, video, and action spaces.
- [[ai/multimodal-and-generative/diffusion-models-intuitively|Diffusion models, intuitively]] explains iterative denoising.
- [[ai/multimodal-and-generative/latent-diffusion-and-stable-diffusion|Latent diffusion and Stable Diffusion]] explains why generation often happens in compressed latent space.
- [[ai/multimodal-and-generative/text-to-image-conditioning-and-cfg|Text-to-image conditioning and CFG]] covers prompt conditioning and classifier-free guidance.

## Vision and shared representations

- [[ai/multimodal-and-generative/clip-and-shared-embedding-spaces|CLIP and shared embedding spaces]] links text and images through contrastive learning.
- [[ai/multimodal-and-generative/vision-transformers|Vision Transformers]] explains images as patches and tokens.
- [[ai/multimodal-and-generative/vision-language-models|Vision-language models and multimodal LLMs]] covers image inputs, captions, OCR, grounding, and visual reasoning.
- [[ai/multimodal-and-generative/controlling-image-generation|Controlling image generation]] covers ControlNet, inpainting, adapters, and image LoRAs.

## Media, evaluation, and risk

- [[ai/multimodal-and-generative/audio-and-speech|Audio and speech]] covers ASR, TTS, voice conversion, and music generation.
- [[ai/multimodal-and-generative/video-generation|Video generation]] explains temporal consistency, motion, editing, and cost.
- [[ai/multimodal-and-generative/evaluating-generative-media|Evaluating generative media]] covers FID, CLIPScore, human eval, task success, and safety review.
- [[ai/multimodal-and-generative/deepfakes-provenance-and-watermarking|Deepfakes, provenance, and watermarking]] covers media risk, C2PA, and disclosure.

**Connects to:** [[ai/model-architectures/index|Model Architectures]] · [[ai/data-for-ai/index|Data for AI]] · [[ai/ai-ethics-and-governance/index|AI Ethics and Governance]]

## Core sources

- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) — foundational diffusion objective and sampling process.
- [High-Resolution Image Synthesis with Latent Diffusion Models](https://arxiv.org/abs/2112.10752) — generation in compressed latent space with cross-attention conditioning.
- [Learning Transferable Visual Models From Natural Language Supervision](https://arxiv.org/abs/2103.00020) — CLIP's contrastive text-image representation learning.
- [An Image is Worth 16x16 Words](https://arxiv.org/abs/2010.11929) — Vision Transformer architecture and scale behavior.
- [C2PA specification](https://c2pa.org/specifications/specifications/2.2/index.html) — interoperable media provenance and authenticity metadata.
