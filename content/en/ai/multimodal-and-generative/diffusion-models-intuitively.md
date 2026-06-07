---
title: "Diffusion models, intuitively"
description: Diffusion models learn to generate data by reversing a gradual noising process through repeated denoising steps.
tags: [diffusion, generative-models, denoising]
order: 2
updated: 2026-06-07
---
# Diffusion models, intuitively

Diffusion models generate by learning how to reverse noise. During training, clean data
is gradually corrupted; the model learns to predict and remove the noise at each step.

## The training idea

1. Start with a real image, audio clip, or latent representation.
2. Add a small amount of noise.
3. Repeat until the sample is nearly pure noise.
4. Train a neural network to predict the noise or the clean sample at a given timestep.
5. At generation time, start from noise and denoise step by step.

The model does not memorize a lookup table of images. It learns a denoising direction
that moves noisy samples toward the data distribution.

## Key components

| Component | Role |
|---|---|
| Noise schedule | controls how quickly signal is destroyed |
| Denoising network | predicts noise, clean sample, or velocity |
| Timestep embedding | tells the model how noisy the sample is |
| Sampler | chooses the reverse denoising trajectory |
| Conditioning | injects text, image, class, audio, or layout guidance |

## Why diffusion became dominant

- Stable training compared with older adversarial approaches.
- High sample quality and diversity.
- Flexible conditioning for text, image, masks, depth, pose, and more.
- Editing workflows such as inpainting and image-to-image.

## Pitfall

Diffusion quality depends heavily on sampling settings. More denoising steps can help
but also increase latency and cost, so product systems need quality-speed tradeoffs.

**Connects to:** [[ai/deep-learning/training-dynamics|training dynamics]] ·
[[ai/multimodal-and-generative/latent-diffusion-and-stable-diffusion|latent diffusion]] ·
[[ai/inference-and-optimization/index|inference optimization]]
