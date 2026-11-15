# Script-Writer master implementation contract

**Status:** reconstructed implementation contract based on the preserved Muse integration contract and the project owner's current direction. This is not represented as a verbatim export of an unavailable original prompt.

## Mission

Build a screenplay workspace in which a selected language model supplies draft prose while Muse by Rihanna supplies the deterministic narrative structure. Model generation must not become the source of story structure or historical truth.

## Engine boundaries

1. **Muse core:** canonical nine-stage order: Ordinary World, Inciting Incident, Rising Action, First Climax (False Victory), Fall, Dark Night, Second Climax (True Choice), Falling Action, Resolution. Preserve the four symbolic registers: colors, lights, thoughts, symbols.
2. **Gangster Manga / Brute Genius:** sidecar research and genre lens for territory, hierarchy, loyalty, debt, complicity, succession, and the cost of power. It may guide questions and interpretation; it must not overwrite Muse's base meanings or invent historical facts.
3. **MUSE-GM:** deterministic factorial premise ranking remains separate. Rubric values are encoded editorial judgments, not empirical measurements. A score is not a historical source.
4. **Hugging Face model layer:** selected model weights generate prose within the Muse structure. Model and dataset licenses remain with their publishers.

## Determinism and reproducibility

- English is canonical for prompt compilation, model IDs, reasoning, and evaluation.
- User-facing output may be localized.
- Record model repository, revision, seed, decoding settings, prompt SHA-256, and output.
- Default decoding is greedy: do_sample=false, num_beams=1.
- A seed improves repeatability but does not guarantee bit-identical output across hardware, CUDA kernels, or library versions.
- Do not describe the neural model as deterministic in the same sense as the Muse rules engine.

## Weight acquisition and privacy

- No weights are bundled and no network download occurs at import time.
- Default model loading is local-cache-only.
- Remote Hugging Face downloads require explicit user action through --download.
- Never enable trust_remote_code implicitly.
- Never place credentials in source, logs, prompts, or output manifests.

## Historical research standard

- Separate sourced facts, disputed claims, editorial interpretation, and fictional invention.
- Current code does not yet implement independent web or primary-source retrieval; users must supply research notes. Do not advertise the historical-search requirement as complete until a source-search adapter and source-capture tests exist.
- Capture source title, publisher/creator, URL or stable identifier, access date, page or passage, and confidence when research records are added.
- Mark missing support [RESEARCH NEEDED]; do not fabricate citations.
- Gangster Manga is a research workflow and genre lens, not an authority that makes unsourced material historically accurate.

## Workflow

BRIEF → MUSE STRUCTURE → RESEARCH REVIEW → MODEL DRAFT → HUMAN REVISION

A human remains responsible for historical review, rights clearance, production decisions, and final approval. Generation does not certify quality, originality, or legal clearance.

## Attribution

Preserve existing repository credits. The project owner requests role-specific credit for Lewis Seals and Angela Seals for browser-based Hugging Face weight-download work. This does not imply sole authorship of the whole application or ownership of third-party model weights. Verify preferred full names and contribution evidence before treating this requested credit as a legal authorship statement.
