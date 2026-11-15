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
muse-screenplay evaluate --dataset offline --limit 2
muse-screenplay optimize --dataset offline --limit 2 --rounds 1
muse-screenplay generate --model script-bart --prompt "INT. COFFEE SHOP - DAY"
```

## Python

```python
from muse_screenplay.datasets import load_eval_dataset
from muse_screenplay.harness_artifacts import build_script_artifact
from muse_screenplay.harness import ArtifactHarness
artifact = build_script_artifact("script-bart")
harness = ArtifactHarness("muse")
result = harness.execute(artifact, {"prompt": "INT. COFFEE SHOP - DAY"})
run = harness.evaluate(artifact, load_eval_dataset("offline", limit=2))
```

## Models and datasets

Models: `sahilnagaralu/movie-script-generator`, `AventIQ-AI/gpt-2-movie-script-writter`, `pranikz/SLM-Movie-Script`.
Datasets: `IsmaelMousa/movies`, `rohitsaxena/MovieSum`, `aneeshas/imsdb-genre-movie-scripts`.

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
