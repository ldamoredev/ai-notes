---
title: "Audio and speech"
description: Audio AI covers speech recognition, text-to-speech, voice conversion, speech translation, music generation, and audio understanding.
tags: [audio, speech, tts, asr]
order: 9
updated: 2026-06-07
---
# Audio and speech

Audio models handle time-varying signals: speech, music, environmental sound, and
generated voice. The same generative and representation ideas appear, but evaluation is
tied to intelligibility, timing, speaker identity, and listening quality.

## Main task families

| Task | Input | Output |
|---|---|---|
| ASR | speech audio | transcript |
| TTS | text | speech waveform |
| Speech translation | speech in one language | text or speech in another |
| Voice conversion | source voice and target style | transformed speech |
| Music generation | prompt, melody, or audio | music clip |
| Audio understanding | sound clip | labels, events, captions |

## Model ingredients

- Acoustic features or learned audio tokens.
- Sequence models for long temporal structure.
- Diffusion, autoregressive, or codec-based generators.
- Speaker embeddings for voice identity.
- Alignment mechanisms for text, phonemes, and timing.

## Evaluation signals

- Word error rate for ASR.
- Naturalness, intelligibility, and speaker similarity for TTS.
- Latency for streaming voice interfaces.
- Robustness to noise, accents, domain vocabulary, and code-switching.
- Consent, likeness, watermarking, and abuse risk for generated voices.

## Pitfall

Voice quality demos can hide operational weakness. Production voice systems must handle
noise, interruptions, turn-taking, latency, accents, and safety boundaries.

**Connects to:** [[ai/llms/tokenization|tokenization]] ·
[[ai/ai-product-engineering/streaming-and-perceived-latency|streaming latency]] ·
[[ai/multimodal-and-generative/deepfakes-provenance-and-watermarking|voice provenance]]
