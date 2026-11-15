# Muse Screenplay

A screenplay drafting layer for Muse by Rihanna, with a Hugging Face model adapter and the existing Gangster Manga / Brute Genius sidecar.

## Responsibilities

- Muse owns the fixed nine-stage narrative structure and symbolic framework.
- Gangster Manga supplies genre questions around territory, hierarchy, loyalty, debt, complicity, succession, and power.
- MUSE-GM remains a separate deterministic premise-ranking engine.
- A selected Hugging Face model writes draft prose; it does not decide narrative rules or certify historical accuracy.

## Install

From the repository root, install optional model dependencies:

    pip install -e ".[models]"

## Commands

    muse-screenplay models
    muse-screenplay generate --title "The Long Return" --premise "An estranged heir returns to a changed neighborhood." --period "1980s" --location "Kingston, Jamaica" --model script-bart --seed 17 --out runs/draft.json

Model acquisition is explicit. The default is local-cache-only. Add --download to permit Hugging Face to download the selected model. No weights are bundled or fetched at import time.

## Supported models

| Key | Hugging Face repository | Architecture |
|---|---|---|
| script-bart | sahilnagaralu/movie-script-generator | Seq2seq |
| gpt2-screenplay | AventIQ-AI/gpt-2-movie-script-writter | Causal |
| mini-gpt-script | pranikz/SLM-Movie-Script | Causal |

Check each model card and license before use. Pin --revision to a commit hash for reproducible runs.

## Reproducibility

Each output records model ID, revision, seed, decoding settings, prompt SHA-256, compiled prompt, and generated draft. Greedy decoding plus a seed is repeatable under a fixed software/hardware stack; bit-identical output across hardware and library versions is not promised.

## Historical integrity

The engine marks missing research as needing review. Supply source-backed research notes; do not treat MUSE-GM rubric scores or genre conventions as historical evidence. Every screenplay requires human factual, rights, and editorial review.

## Tests

    python -m unittest tests.test_muse_screenplay_engine -v
