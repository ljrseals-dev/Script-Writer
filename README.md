# Script-Writer
## A reproducible narrative-design and screenplay-development research environment

**Script-Writer** is a research-oriented workspace for constructing, comparing, and developing story premises. It brings together an explicit narrative framework, a finite factorial decision surface, and a human-governed writing workflow. Its purpose is not to replace authorship or historical scholarship. It is to make creative assumptions inspectable, premise exploration reproducible, and the transition from research to dramatic structure more disciplined.

The project combines two complementary foundations:

1. **Muse by Rihanna** — a nine-stage narrative architecture with symbolic registers.
2. **MUSE-GM / Brute Genius** — an exhaustive, rubric-scored enumeration of a configured story-origin space.

These systems have different epistemic roles. Muse supplies a narrative organization. MUSE-GM evaluates combinations under declared editorial criteria. Neither is a historical database, an empirical audience model, or an authority on the truth of a historical claim.

> **Research principle:** make the assumptions explicit, preserve the evidence trail, and keep human judgment accountable for the final work.

[![CI](https://github.com/ljrseals-dev/Script-Writer/actions/workflows/ci.yml/badge.svg)](https://github.com/ljrseals-dev/Script-Writer/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Evidence model](https://img.shields.io/badge/evidence-encoded%20editorial%20judgments-orange)

**Project attribution:** Lewis James Seals Jr., Liliabet Diana Windsor, Laila Star Seals, and Lawrence James Seals. See [CITATION.cff](CITATION.cff) and the project provenance documents for attribution context.

---

## 1. Scope and intended use

Script-Writer is intended for writers, directors, actors, researchers, and development teams who need a transparent way to explore story premises and examine the assumptions behind them. It is especially suited to historically and socially situated crime narratives, diaspora settings, family systems, political economies, and stories about power, obligation, complicity, and succession.

The software supports:

- exhaustive enumeration of a declared finite premise space;
- ranking against an explicit, versioned editorial rubric;
- sensitivity analysis under alternative weighting assumptions;
- reproducible export of results and run metadata;
- a Muse-based narrative-development framework;
- a local writing-room workflow with human approval gates.

It does **not** establish that a highly ranked premise is historically true, ethically sufficient, dramatically successful, or commercially viable. Those judgments require independent research, editorial scrutiny, and audience-facing evaluation.

## 2. System architecture

| Component | Function | What it does not establish |
|---|---|---|
| **Muse by Rihanna** | Organizes development through a nine-stage, double-climax narrative structure and symbolic registers for colors, lights, thoughts, and symbols. | It does not prove that a particular plot is historically accurate or artistically effective. |
| **MUSE-GM** | Enumerates the configured factorial premise space, applies rubric tables, ranks configurations, and exports reproducibility artifacts. | It does not retrieve primary sources or measure the real-world probability of a premise. |
| **Brute Genius** | Names the project's exhaustive-search approach: evaluate the declared configuration space rather than rely on an unrecorded sample. | It is not, in the current implementation, a general-purpose historical web-search or archival-retrieval service. |
| **Writing-room application** | Guides a user through premise review, approval, causal development, character work, tonal planning, and artifact capture. | A language-model response is not a substitute for the engine's recorded state or the user's approval. |
| **Optional screenplay/model adapters** | Where included in a checkout, the screenplay adapter compiles Muse's narrative structure into a stable prompt and can use external Hugging Face weights to draft prose. | Third-party weights do not define the narrative rules, certify facts, or become deterministic merely because a seed is supplied. |

### Muse's nine-stage sequence

1. Ordinary World
2. Inciting Incident
3. Rising Action
4. First Climax — False Victory
5. Fall
6. Dark Night
7. Second Climax — True Choice
8. Falling Action
9. Resolution

The Gangster Manga lens is a thematic sidecar. It may frame questions about territory, hierarchy, loyalty, debt, complicity, succession, and the cost of power. It must not silently redefine Muse's base symbolic meanings or predetermine a character's moral outcome.

The existing core also supports writer-facing prompts in multiple languages. English remains the canonical language for internal model prompts and technical identifiers; localization does not change the underlying narrative stages.

## 3. MUSE-GM: formal search space

The current configuration defines a full-factorial space of **4,445,280 possible origins**. Its dimensions represent declared categories such as diaspora node, era, economy, pressure, media frame, family system, and archetype, together with the project's other configured factors.

The engine evaluates the complete configured space. Its implementation broadcasts rubric tables over a multidimensional array, computes component scores, applies a selected weight profile, and ranks configurations with a deterministic tie-break. It supports restricted exhaustive runs through selection filters and distinct-result views for reducing near-duplicate premises.

The rubric contains **encoded editorial judgments**. The mathematics can be exact while the inputs remain interpretive. A score is therefore a statement about how a configuration performs under the currently declared rubric—not an objective measurement of historical plausibility.

The project ships with alternative weighting profiles and sensitivity analysis so that readers can inspect how rankings respond when editorial priorities change. Exact rank-one results should not be treated as stable if small weight changes reorder them.

For the mathematical specification and worked derivation, see [docs/MATH.md](docs/MATH.md). The research paper and baseline addendum are in [docs/paper/](docs/paper/).

## 4. Installation and quick start

The core engine targets Python 3.10–3.12. From a clone:

```bash
git clone https://github.com/ljrseals-dev/Script-Writer.git
cd Script-Writer

python3 -m venv .venv
. .venv/bin/activate

python -m pip install --upgrade pip
python -m pip install numpy

python -m unittest discover -v tests
python -m muse_gm check
```

This checkout does not currently define a repository-root `pyproject.toml` or installable package extras. Install dependencies explicitly. NumPy is sufficient for the core engine and test suite. To use the optional Anthropic-backed local writing-room app, install `anthropic` separately and provide `ANTHROPIC_API_KEY` in the server process environment; the key is not written to the repository.

### Core commands

```bash
python -m muse_gm variables --values
python -m muse_gm check
python -m muse_gm run --top 5
python -m muse_gm run --effect pivot --distinct node,era,economy
python -m muse_gm sensitivity
```

A selected run can be constrained without changing the underlying variable definitions:

```bash
python -m muse_gm run \
  --select node=Harlem \
  --select era=3 \
  --out runs/harlem-era3
```

Consult the CLI help for the exact options available in the checked-out revision:

```bash
python -m muse_gm --help
python -m muse_gm run --help
```

### Local writing-room application

```bash
python -m pip install anthropic
export ANTHROPIC_API_KEY='your-key'
python -m muse_gm.app --host 127.0.0.1 --port 8484
```

Open `http://127.0.0.1:8484` in your browser. Keep the server bound to localhost unless you have separately reviewed and configured an appropriate deployment boundary.

There is no `muse_screenplay/` package in this repository revision. The current writing-room application is `muse_gm/`; do not treat references to planned screenplay adapters as shipped functionality. Model weights are not bundled. Any future external model integration must require explicit user action and honor the model card and license.

## 5. Outputs and reproducibility

A run can emit ranked results, a machine-readable manifest, numeric-coded and labeled CSV files, and SPSS syntax. The manifest records the command, configuration hashes, weight profile, selection, software versions, and evidence-status metadata.

For reproducible research practice:

1. Preserve the exact input configuration and rubric used for a run.
2. Retain the manifest and generated outputs together.
3. Record any manual changes to the premise after ranking.
4. Report the weight profile and sensitivity results when presenting a selected premise.
5. Distinguish software reproducibility from the validity of the editorial assumptions.

The baseline tests compare current engine output with checked-in reference results. Such tests establish consistency with the recorded baseline; they do not independently validate the rubric's historical or artistic claims.

## 6. Historical research and evidence discipline

The project's intended use includes historically grounded storytelling. The current MUSE-GM factorial search is **not** an archival search engine and does not independently retrieve or authenticate historical sources. A ranked premise, model-generated passage, or thematic prompt must never be cited as evidence for a historical event.

A responsible research workflow should maintain separate records for:

- **Verified fact:** supported by an identifiable source and precise reference.
- **Disputed claim:** attributed to its source and presented with the disagreement intact.
- **Interpretation:** an argument drawn from evidence, not a fact in itself.
- **Fiction:** invented dialogue, composite characters, altered chronology, or constructed events.
- **Research gap:** a factual assertion that still requires verification.

For primary-source work, record the archive or publisher, collection or document identifier, creator, date, page or folio, stable URL or catalogue reference, access date, and any relevant rights or access restrictions. Seek corroboration for consequential claims. Where sources conflict, preserve the conflict rather than flattening it into a confident narrative.

Until a source-cited retrieval and provenance layer is implemented and validated, historical verification remains the responsibility of the research team.

## 7. Writing-room governance

The local writing-room application is designed around a simple governance distinction: a model may assist with language, but the application and the human operator retain authority over state transitions and approval. Approval is an explicit user action; it is not inferred from a model's conversational wording.

The project architecture documents the engine, application, session state, and approval gates in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). The live external language-model path and production deployment must be validated separately from tests that use a fake client or local fixtures.

### Yellow LED Writer's Room interface

The local MUSE-GM Writer's Room uses a warm yellow-LED palette on a near-black studio-console surface, with responsive layout, visible keyboard focus, and reduced-motion support. This is a presentation-only theme: it does not change ranking, evidence status, human approval authority, or server behavior. See [docs/UI_THEME_YELLOW_LED.md](docs/UI_THEME_YELLOW_LED.md) and [muse_gm/static/index.html](muse_gm/static/index.html).

## 8. Related projects in the Seals research and writing ecosystem

The following repositories are related projects with distinct audiences and scopes. They are linked here for discovery; they are **not** represented as dependencies or integrated subsystems of Script-Writer.

### [Muse Sermon — church](https://github.com/ljrseals-dev/church)

A sermon-preparation and study companion for preachers, with the King James Version as its default translation and a Mother Tammy conversational persona. Its engine records notes, tracks preparation stages, and prompts exegetical and pastoral reflection. Its stated design boundary is that it does not write the sermon. The repository describes a standard-library Python implementation with JSON session records and optional LLM-rendered replies.

**Positioning:** a preparation and reflection aid for sermon development—not an automated preacher and not a substitute for biblical scholarship, pastoral discernment, or denominational guidance.

### [Muse Sermon v2 — black-church](https://github.com/ljrseals-dev/black-church)

A focused study companion for the African American / Black church pulpit. Its documented prompts attend to the text's exigency, the hearers' concrete conditions, the cloud of witnesses, hope and denial, refrain, humor, the close, and stewardship. It leaves denominational distinctives for the user to specify and calls attention to checking archaic or shifted KJV wording against Hebrew and Greek.

**Positioning:** a tradition-aware sermon-preparation companion—not a replacement for the preacher's exegesis, community knowledge, or pastoral responsibility.

Both repositories have their own source, instructions, usage, and licensing context. Review each repository directly before adoption or deployment.

## 9. Limitations and validation status

The following boundaries are material to interpreting results:

- Rubric values are authored judgments, not measured observations.
- Sensitivity analysis can reveal ranking instability; it cannot remove subjectivity from the rubric.
- Less-documented regions or communities may be disadvantaged by the current anchor set. This is a research-design issue, not evidence of lower historical importance.
- SPSS syntax should be tested in the target SPSS environment before being treated as validated output.
- The writing-room live API path requires separate end-to-end testing; fake-client tests do not establish live-provider behavior.
- External model generation depends on model availability, tokenizer and runtime versions, hardware, and each model publisher's license.
- A fixed seed and greedy decoding improve repeatability but do not guarantee bit-identical results across hardware and software environments.
- Generated scripts require human editorial, historical, cultural, legal, and rights review.

Do not describe the project as guaranteeing historical accuracy, eliminating creative bias, predicting audience response, or producing production-ready scripts without further evidence.

## 10. Repository map

```text
muse_core/          Muse narrative core and symbolic bridge
muse_gm/            active factorial engine, rubric data, prompts, and local application
Muse_GM/            legacy snapshot and historical dry-run records; not the active package
tests/              engine, application, and baseline tests
docs/               architecture, mathematics, research, governance, and roadmap
IMPORT_SNAPSHOT_SHA256SUMS  checksum inventory for the imported archive, not current main
results/            checked-in baseline and prototype outputs
logs/               documented run records and audit material (including vintage-harness)
prototype/          retained early implementation source
.github/workflows/  continuous-integration configuration
```

The active package is the lowercase `muse_gm/` directory. `Muse_GM/` is retained for historical reference and is not an installable package. The earlier `prototype/` source is retained separately as provenance; see [docs/REPOSITORY_HYGIENE.md](docs/REPOSITORY_HYGIENE.md) for the directory boundaries.

## 11. Research citation and provenance

The repository includes [CITATION.cff](CITATION.cff). The research paper, baseline addendum, mathematics, and provenance documents provide additional context. Cite the version or commit actually used, rather than citing a moving branch as though it were a fixed research artifact.

Attribution and project-history statements should be read alongside the repository's provenance and credits documents. Third-party model weights, datasets, images, and other external materials remain subject to their respective authors' licenses and terms. Project attribution does not transfer ownership of those materials.

## 12. License

The project is distributed under the MIT License; see [LICENSE](LICENSE). The license for this repository does not override the terms attached to external models, datasets, archives, images, or other third-party resources.

---

*The objective is not to automate authorship. It is to make the structure, assumptions, evidence, and decisions behind authorship more legible.*
