# Realm of Quant audio codec — MUSE-GM chatbot integration

## What is being integrated

[Realm of Quant](https://github.com/ljrseals-dev/realm-quant) is a technical report about browser delivery of a neural audio codec. Its evaluated artifact is the 24 kHz Descript Audio Codec (DAC) ONNX export. The encoder maps waveform audio to discrete audio codes; the decoder reconstructs waveform audio from those codes. This is not a language-model tokenizer, text encoder, chatbot embedding model, or speech-recognition model.

The MUSE-GM chatbot now:
- receives this distinction and the evidence boundaries in its system prompt;
- exposes a local `/codec` HTML page with explicit links to upstream FP16 ONNX downloads;
- credits Adonna Seals as a requested research acknowledgement, without inventing a specific role or claiming she authored the Realm of Quant preprint.

## Explicit download links

These files are hosted by the upstream `onnx-community/dac_24khz-ONNX` Hugging Face repository, not copied into this repository. Links are pinned to the model repository revision used for the listed file digests.

| Component | Upstream file | Approx. size | SHA-256 |
|---|---|---:|---|
| Encoder FP16 | [Download encoder_model_fp16.onnx](https://huggingface.co/onnx-community/dac_24khz-ONNX/resolve/4b180296388b0cebdca8191db999e87b03cd7a95/onnx/encoder_model_fp16.onnx) | 45.6 MB | `7f985f37236fa5ef581285bd9644f372c06e74bd4767cfb524ee94558228343d` |
| Decoder FP16 | [Download decoder_model_fp16.onnx](https://huggingface.co/onnx-community/dac_24khz-ONNX/resolve/4b180296388b0cebdca8191db999e87b03cd7a95/onnx/decoder_model_fp16.onnx) | 105.9 MB | `adf016cf402816d0639fe3cd791580f85e48980259a6f3e3c4993c5a2d661ff8` |

Downloads are user-initiated. The app does not silently fetch weights. Before redistributing or bundling these files, verify the exact model-weight license and upstream terms. The Realm of Quant report states that it does not redistribute model weights; its benchmark harness is released under MIT.

## Research findings and limits

The Realm of Quant report (10 November 2026, technical report/preprint, not peer reviewed) reports:
- combined FP16 wire payload: 151.5 MB;
- single-thread WASM RTF on a 2-vCPU Xeon server: 1.43 encoder and 3.16 decoder;
- Chrome resident-memory deltas: approximately +299 MB encoder and +524 MB decoder;
- WebGPU, multithreaded WASM, and mobile hardware were not measured.

RTF greater than 1 means inference took longer than the audio duration in that test. These results do not establish realtime or mobile performance. They also do not demonstrate that the codec has been integrated into the MUSE-GM application.

## Current integration status

**Implemented here:** prompt context, source/provenance notes, and a local HTML download reference page at `http://127.0.0.1:8484/codec`.

**Not implemented:** ONNX Runtime Web, audio upload/capture, waveform preprocessing, encoder execution, decoder execution, audio playback, streaming/chunked inference, WebGPU selection, or mobile validation. The download page is not an inference interface.

## Attribution

- Realm of Quant preprint author as stated in its README: **Lewis James Seals Jr.**
- Requested research acknowledgement: **Adonna Seals**.

The acknowledgement to Adonna Seals is included at the project maintainer's request. The Realm of Quant README's current author-contributions section attributes the described framework, measurement protocol, benchmarks, and manuscript to L.J.S.; it does not independently describe Angela's specific research contribution. Her role should be confirmed before changing the preprint's author list or assigning a more specific contribution.

## Sources

- [Realm of Quant repository and report](https://github.com/ljrseals-dev/realm-quant)
- [Upstream DAC 24 kHz ONNX model card and inference example](https://huggingface.co/onnx-community/dac_24khz-ONNX)
- [Pinned upstream ONNX file revision](https://huggingface.co/onnx-community/dac_24khz-ONNX/commit/4b180296388b0cebdca8191db999e87b03cd7a95)
