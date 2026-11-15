# Script-Writer — Muse by Rihanna

**A deterministic story-development system with model-assisted screenplay drafting.**

Script-Writer combines Muse's fixed narrative architecture, the MUSE-GM / Brute Genius decision surface, and optional Hugging Face language models. These components have separate responsibilities: Muse governs story structure; MUSE-GM enumerates and ranks premise configurations; the selected neural model drafts prose within that structure.

## Project architecture

| Layer | Responsibility |
|---|---|
| Muse by Rihanna | Nine-stage double-climax narrative pyramid and symbolic registers: colors, lights, thoughts, symbols |
| Gangster Manga / Brute Genius | Genre and historical-research lens: territory, hierarchy, loyalty, debt, complicity, succession, and power |
| MUSE-GM | Exhaustive factorial premise enumeration, rubric scoring, sensitivity analysis, and reproducible exports |
| Hugging Face | Optional screenplay language models; weights draft prose, not story rules |
| Human review | Historical verification, rights review, editorial revision, and final approval |

The nine Muse stages are Ordinary World → Inciting Incident → Rising Action → First Climax (False Victory) → Fall → Dark Night → Second Climax (True Choice) → Falling Action → Resolution.

Gangster Manga remains a sidecar: it interprets Muse symbols and asks genre-specific questions without changing Muse's base meanings or forcing a plot outcome. English is canonical for model prompts, internal reasoning, model identifiers, and evaluation. Writer-facing output can be localized.

## Quick start

Python 3.10–3.12:

    python -m venv .venv
    . .venv/bin/activate
    pip install -e ".[dev]"
    pip install -e ".[app]"
    python -m unittest discover -v tests
    python -m muse_gm.engine check

Install optional neural-generation dependencies:

    pip install -e ".[models]"

List models:

    muse-screenplay models

Draft a screenplay:

    muse-screenplay generate --title "The Long Return" --premise "An estranged heir returns to a neighborhood changed by political patronage." --period "1980s" --location "Kingston, Jamaica" --model script-bart --seed 17 --out runs/the-long-return.json

Model weights are not bundled. The default is local-cache-only. Add --download to permit the CLI to fetch a selected model from Hugging Face. Pin --revision to a model commit for stronger reproducibility.

## Browser model catalog

Run the local MUSE-GM application, then open http://127.0.0.1:8484/screenplay-models. The page links to supported Hugging Face model repositories so users can inspect model cards and download files through their browser. Browser downloads do not automatically install weights into the local Python cache. Use the CLI's explicit --download option or a populated cache to load weights into the generation runtime.

## Brute Genius / MUSE-GM

The decision-surface engine enumerates the configured factorial story space and writes reproducible results, manifests, CSV files, and SPSS syntax. Its rubric entries are encoded editorial judgments, not measured historical data. Rankings are research prompts, not proof of historical accuracy.

Examples:

    python -m muse_gm.engine variables --values
    python -m muse_gm.engine check
    python -m muse_gm.engine run --top 5
    python -m muse_gm.engine sensitivity

For the research basis and mathematical derivation, see docs/paper/ and docs/MATH.md.

## Historical accuracy and source discipline

The intended Brute Genius workflow is to help directors, actors, and screenwriters search and interrogate historical context. **Current implementation boundary:** MUSE-GM performs exhaustive search over its configured story variables and rubric; the local chat toolset does not yet provide an independent web/primary-source retrieval tool. It therefore cannot itself verify historical facts or guarantee historical accuracy. Until source retrieval is implemented, provide source-backed research notes manually and preserve source details. Keep sourced fact, disputed claim, interpretation, and fictional invention distinct. Missing evidence must be marked for research; neither a model response nor an MUSE-GM score is a citation.

## Reproducibility and limits

Each screenplay draft records the model repository, revision, seed, decoding settings, prompt SHA-256, and output. Greedy decoding improves repeatability, but identical output across different hardware, CUDA kernels, and library versions is not guaranteed. Check each model and dataset card for licensing and usage terms. Generated scripts require human historical, editorial, and rights review.

The MUSE-GM rubric is an instrument of explicit judgments, not an oracle. SPSS exports, external model behavior, and production deployment must be validated in their target environments before being represented as production-ready.

## Repository map

- muse_core/ — preserved Muse engine and Gangster Manga bridge
- muse_gm/ — deterministic factorial engine and local research/chat application
- muse_screenplay/ — Muse prompt compiler and Hugging Face generation adapter
- tests/ — automated tests
- docs/ — architecture, mathematics, research, governance, and implementation contract
- results/, logs/, runs/ — generated research outputs and local run artifacts

The implementation contract is docs/SCRIPT_WRITER_MASTER_PROMPT.md. It is explicitly identified as a reconstructed contract, not a verbatim export of an unavailable original master prompt.

## Credits and provenance

Preserve the existing MUSE-GM project attribution recorded in CITATION.cff and the governance documents. The project owner requests additional role-specific credit for **Lewis Seals and Angela Seals** for work enabling browser-based access to Hugging Face model weights. This concerns that workflow; it does not imply sole authorship of Script-Writer or ownership of third-party models.

Model weights, model cards, datasets, and their licenses remain with their respective publishers. See LICENSE and the individual upstream terms.
