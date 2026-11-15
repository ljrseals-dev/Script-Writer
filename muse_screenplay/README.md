# Muse Screenplay Module

A pluggable screenplay generation module for Muse, using Hugging Face Transformers and Datasets with a bundled Artifact Harness.

**Status:** experimental. Offline tests do not download models. Model generation requires the optional `models` extra.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

For generation: `pip install -e ".[models]"`. For remote datasets: `pip install -e ".[datasets]"`.

## CLI

```bash
muse-screenplay models
muse-screenplay datasets
muse-screenplay validate --file examples/sample_scene.txt
muse-screenplay evaluate --dataset offline --target-language en --limit 2
muse-screenplay optimize --dataset offline --limit 2 --rounds 1
muse-screenplay generate --model script-bart --target-language en --prompt "INT. COFFEE SHOP - DAY"
```

## Python

```python
from muse_screenplay.datasets import load_eval_dataset
from muse_screenplay.harness_artifacts import build_script_artifact
from muse_screenplay.harness import ArtifactHarness
artifact = build_script_artifact("script-bart")
harness = ArtifactHarness("muse")
result = harness.execute(artifact, {"prompt": "INT. COFFEE SHOP - DAY", "target_language": "en"})
run = harness.evaluate(artifact, load_eval_dataset("offline", limit=2, target_language="en"))
```

## Models and datasets

Models: `sahilnagaralu/movie-script-generator`, `AventIQ-AI/gpt-2-movie-script-writter`, `pranikz/SLM-Movie-Script`.
Datasets: `IsmaelMousa/movies` (1,172 rows; `Name`/`Script`; English; Apache-2.0), `rohitsaxena/MovieSum` (2,200 rows; `script`/`summary`; train/val/test; CC BY-NC 4.0), and `aneeshas/imsdb-genre-movie-scripts` (150 rows; five genre columns; license unverified). MovieSum language is unverified; IMSDb is source-implied English. Dataset-card declarations are not model-output evaluations.

Check each model and dataset card for license and usage restrictions. Screenplays may be copyrighted; generated content needs human review. Heuristic scores are not measures of artistic quality or legal clearance. Preserve model, dataset, prompt, parameter, and evaluation provenance. Optimization is parameter search, not model fine-tuning; promotion remains a human decision.

Lifecycle: `EXECUTE → CRITIQUE → MUTATE → COMPOSE → PROMOTE`.

MIT for this project; model and dataset terms remain with their authors.

## Governance and provenance

The screenplay module uses a separate governance layer for concept/implementation provenance,
evidence status, requested credits versus evidenced contributions, dataset boundaries,
criteria versioning, and mutation audit. See [GOVERNANCE.md](GOVERNANCE.md).

The hash-chained ledger defaults to `.muse/ledger.jsonl`; export snapshots are written to
`data/ledger/`. A ledger hash proves byte consistency, not authorship or ownership. Remote
dataset failures are explicitly marked as fallback evaluations and must not be presented as
remote results.

Run the focused governance gate:

```bash
pytest tests/test_governance_schema.py tests/test_governance_integration.py -q
python scripts/integration_check.py
```

## Model-loading security contract

The loader applies two independent controls: (A) explicit PyTorch deserialization uses `torch.load(..., map_location="cpu", weights_only=True)`; (B) Transformers uses `trust_remote_code=False` and rejects remote `auto_map` architectures. Safetensors is preferred with `use_safetensors=True`. A legacy `.bin` fallback is explicit and must pass through `torch_load_safe()`; there is no unsafe fallback. A model requiring remote code is not loaded.

These controls do not validate tensor correctness, source authenticity, output quality, licensing, bias, or copyright. SHA-256 checks byte identity only.

## Language contract

The model and dataset catalog declares language coverage without assuming multilingual behavior. Unverified entries remain `unverified`; English expectations are not evaluation results. Every generation and model-backed evaluation requires `target_language`; omission is an error. Inputs are not automatically translated. Language mismatches are recorded. Output provenance includes `requested` and `generated_in` (or `unverified` if detection is unavailable). Muse's internal nine-stage keys remain canonical English; symbol registers are locale/culture-specific.

## Attribution

Requested weights-integration innovation attribution to **Angela Seals** is preserved in [CITATION.cff](../CITATION.cff), the provenance ledger header, and the demo footer. Localized documentation must retain the original English attribution alongside any translation.

## Upstream resources

- Models: [sahilnagaralu/movie-script-generator](https://huggingface.co/sahilnagaralu/movie-script-generator), [AventIQ-AI/gpt-2-movie-script-writter](https://huggingface.co/AventIQ-AI/gpt-2-movie-script-writter), [pranikz/SLM-Movie-Script](https://huggingface.co/pranikz/SLM-Movie-Script).
- Datasets: [IsmaelMousa/movies](https://huggingface.co/datasets/IsmaelMousa/movies), [rohitsaxena/MovieSum](https://huggingface.co/datasets/rohitsaxena/MovieSum), [aneeshas/imsdb-genre-movie-scripts](https://huggingface.co/datasets/aneeshas/imsdb-genre-movie-scripts).
