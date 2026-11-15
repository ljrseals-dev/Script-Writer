<div align="center">

# Script Writer powered by Muse by Rhianna

![HBO Styled Gangster Scene](images/gangster1.jpg)


### A deterministic story-development and screenplay-writing workspace

**4,445,280 origins. One instrument. No dice.**

[![tests](https://github.com/ljrseals-dev/bang/actions/workflows/ci.yml/badge.svg)](https://github.com/ljrseals-dev/bang/actions/workflows/ci.yml)
![python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![evidence](https://img.shields.io/badge/evidence-rubric%20judgments%2C%20not%20measurements-orange)

*Project attribution: Lewis James Seals Jr., Liliabet Diana Windsor, Laila Star Seals, and Lawrence James Seals.*

</div>

---

Fourteen diaspora nodes. Eight eras. Nine economies. Seven pressures. Five media frames. Six family systems. Seven archetypes. Three effects.
Multiply them. That is the whole space of origins, and it is finite.

Script Writer uses the MUSE-GM decision-surface engine; it does not sample the story space. It **walks** it. Every combination is scored, ranked, hashed and exported to SPSS. Two weight profiles ship with it, sensitivity analysis is built in, and every run leaves a manifest you can reproduce to the sixth decimal.

![Historical Street Scene](images/gangster2.jpg)

> **Stratagem №1: don't sample the story. Exhaust it.**
> Every screenwriter guesses. This one enumerates. Zero of the 4,445,280 possible origins are left to chance.

**Read the paper:** [Using Brute Force: Deterministic Genesis of the Origins of Gangsters](docs/paper/using-brute-force-deterministic-genesis.md) · [Addendum: baseline results](docs/paper/ADDENDUM-baseline-results.md) · [The mathematics](docs/MATH.md)

## Contents
[What it is](#what-it-is) · [Credits & agreement](#credits--chicken-or-egg-agreement) · [Baseline results](#baseline-results) · [Quick start](#quick-start) · [Usage](#usage) · [The chat app](#the-chat-app) · [How it works](#how-it-works) · [Evidence and limits](#evidence-and-limits) · [Integrity and reproducibility](#integrity-and-reproducibility) · [Repository layout](#repository-layout) · [Roadmap](#roadmap) · [Cite](#cite) · [Brute Genius addendum](#brute-genius-addendum) · [License](#license)

## What it is
- **An engine.** A full-factorial enumeration of eight nominal variables (a story world declared like an SPSS Variable View), scored by six components built from 24 rubric tables.
- **An instrument, not an oracle.** The rubric is human judgment, stated plainly, versioned and hashed. Every manifest says so in machine-readable text: `rubric_encoded_judgments_not_measured_data`.
- **A workflow.** A local chat app that uses the engine to walk a writer through ranking, human approval, causal spine, audit, characters, tonal sheet and script, with the gates enforced in code.

## Baseline results
Rank-1 premises under the `master` profile (rubric SHA-256 `04c2bcf7dff0051f…`). Full lists: [`results/baseline/`](results/baseline/).

| Target | Rank-1 premise (node · era · economy · pressure · media · family · archetype) | Score |
|---|---|---|
| Humanized | Harlem · 1940s-50s numbers/labor · policy/numbers · police surveillance · Black press counter-narrative · matriarch-led · ethical rebel loner | 0.9157 |
| Dreaded | Kingston JA · 1980s Yardie/garrison · drug corridor · political garrison patronage · state intelligence file · estranged-return · enforcer | 0.9160 |
| Pivot | Harlem · 1940s-50s numbers/labor · policy/numbers · police surveillance · state intelligence file · matriarch-led · heir | 0.8981 |

**Read these with care.** Under 0.05 weight shifts the exact rank-1 premise changes in 1 of 12 variants (humanized), 4 of 12 (dreaded) and 6 of 12 (pivot). The stable finding is the neighborhood (Harlem 1940s policy; Kingston 1980s drug corridor), not a single cell. See the [addendum](docs/paper/ADDENDUM-baseline-results.md).

## Muse by Rhianna foundation + Gangster Manga theme

This repository now includes the extracted Muse narrative core from
[stunning-happiness](https://github.com/ljrseals-dev/stunning-happiness), preserved
under `muse_core/` and presented as the foundation of Script Writer. It tracks the nine-stage double-climax pyramid and the four
symbolic registers (colors, lights, thoughts, symbols). The existing MUSE-GM
factorial decision-surface engine remains separate and unchanged.

The `gangster_manga` theme is a sidecar: it interprets Muse symbols through
territory, hierarchy, loyalty, debt, complicity, succession, and the cost of power.
It does not alter Muse's base symbol meanings or force a story outcome.

English is the canonical model/prompt language. The theme includes localized
writer-facing prompts for English, Simplified Chinese, Spanish, Japanese, and
French; unsupported locales fall back to English. Model weights are not bundled
or downloaded implicitly. See [the integration contract](docs/MUSE_RIHANNA_GANGSTER_MANGA.md).

Quick theme consultation:

```bash
python -m muse_core --stage ordinary_world --language en --symbol colors:black --symbol symbols:crown
python -m unittest tests.test_muse_bridge -v
```

## Quick start
```bash
git clone https://github.com/ljrseals-dev/bang && cd bang
pip install -e .            # engine only (needs numpy)
pip install -e ".[app]"     # plus the chat app (needs the anthropic package)
python -m unittest discover -v tests
```
Without installing, run `python -m muse_gm ...` from the repository root.

## Usage
```bash
muse-gm variables --values                                  # the Variable View with value labels
muse-gm check                                               # validate config, size, hashes
muse-gm run --top 5                                         # all 4,445,280 cases, top 5 per target
muse-gm run --effect pivot --distinct node,era,economy      # best premise per core, not near-duplicates
muse-gm run --select node=Harlem --select era=3 --out runs/001
muse-gm sensitivity                                         # master vs equal, plus 12 weight shifts
```
`--out` writes `results.jsonl`, `manifest.json`, a numeric-coded CSV, a labeled CSV and an SPSS `.sps` file. `--select` restricts the space (exhaustive inside it). Edit [`muse_gm/data/variables.json`](muse_gm/data/variables.json) and [`rubric.json`](muse_gm/data/rubric.json) to change the world; the code does not move.

## The chat app
```bash
export ANTHROPIC_API_KEY=...        # your key, billed to you, never written to disk
muse-gm-app                         # http://127.0.0.1:8484
```
- Approval of a configuration is a **button you click**. The model has no approve tool.
- `save_artifact` refuses a script until the spine, audit, characters and tonal sheet are saved.
- Rankings come only from the engine. The server binds to 127.0.0.1 and never echoes your key.
- **Status:** the tool loop, gates and HTTP layer are tested against a fake client. The live Claude API path has not been run.

## How it works
```
 variables.json ─┐                       ┌─> ranked lists (per effect target)
                 ├─> 4,445,280 cases ──> 6 components ──> weighted score ──┤
 rubric.json  ───┘   (full factorial)    (24 tables)       (profile)        └─> manifest + hashes + CSV/SPSS
```
Tables are broadcast onto one 8-D array, so there is no row-per-case table in memory. Linear and geometric combinations are defined in the rubric; weights must sum to 1; non-finite or out-of-range values stop the run. The full derivation, with a worked example, is in [`docs/MATH.md`](docs/MATH.md).

## Evidence and limits
- **Judgments, not data.** Every table entry is an editorial judgment. The mathematics is exact; the inputs are not measurements.
- **Fragile at the margin.** Exact winners move under small weight shifts (above). Use `--distinct` and `sensitivity`.
- **Documented-anchor bias.** Less-saturated nodes (Salvador, Accra, Marseille, Lagos) score lower mostly on documented-anchor plausibility. Revisit them with sourced research.
- **Untested paths.** The SPSS export has not been run in SPSS; the chat app has not been run against the live API; CI covers Linux only.
- **Not an audience model.** It does not know whether a script will be good.

## Integrity and reproducibility
- Every run records the SHA-256 of both config files, the command, profile, weights, selection, and versions.
- `tests/test_baseline.py` re-runs the engine and compares the top five per target with `results/baseline/` on every CI run.
- A release zip ships with `SHA256SUMS`; `sha256sum -c SHA256SUMS` detects truncated or altered files.

## Repository layout
```
muse_gm/            engine.py (scoring + CLI), app.py (chat server), data/ (variables + rubric), prompts/, static/
tests/              27 tests: engine, app gates, baseline reproducibility
docs/paper/         the paper and the baseline-results addendum
docs/               MATH.md, ARCHITECTURE.md, ROADMAP.md, source/ (original Master Prompt export)
results/            baseline/ (current run), prototype/ (first-draft output)
logs/               run records, incl. the Vintage harness dry-run audit (see logs/README.md)
prototype/          first-draft scoring script, kept for provenance
.github/workflows/  CI on Python 3.10-3.12
```

## Roadmap
Penalty terms, the guilt/forgiveness/containment dimensions, staged search for spaces beyond 10⁹, and machine-checkable refusal conditions. Open decisions are listed in [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Cite
See [`CITATION.cff`](CITATION.cff). Lewis James Seals Jr. and Laila Star Seals, *MUSE-GM: Deterministic Genesis of the Origins of Gangsters*, 2026.

## License
MIT. See [`LICENSE`](LICENSE).

---
*Brute force, applied to the entire space at once, is craft made legible.*


## Realm of Quant audio codec (optional)

The local chatbot now has a `/codec` page with user-initiated links to the upstream
FP16 ONNX encoder and decoder researched in
[Realm of Quant](https://github.com/ljrseals-dev/realm-quant). These are 24 kHz
audio-codec components, not text tokenizers or language-model encoders. The current
integration exposes downloads and research context; it does **not** yet execute
ONNX inference or process audio. See
[the integration and evidence notes](docs/REALM_QUANT_CHATBOT_INTEGRATION.md).

**Research credit:** Realm of Quant preprint author: Lewis James Seals Jr.
Requested research acknowledgement: Adonna Seals. Her specific role is
not independently detailed in the preprint's current author-contributions section;
the acknowledgement is included at the project maintainer's request and is not a
claim of preprint co-authorship.


## Credits & Chicken-or-Egg Agreement

Project credits and the provenance agreement are recorded in
[docs/CREDITS_AND_CHICKEN_EGG_AGREEMENT.md](docs/CREDITS_AND_CHICKEN_EGG_AGREEMENT.md).
The agreement treats concept and implementation as potentially reciprocal, relies on
preserved evidence for attribution, and does not assume legal consent or assign
unsupported individual roles.


## Forensic credits and Chicken-or-Egg agreement

The project carries forward the requested credits for **Lewis James Seals Jr., Liliabet Diana Windsor, Laila Star Seals, and Lawrence James Seals**. The forensic governance prompt and working agreement are documented in [docs/FORENSIC_CHICKEN_OR_EGG_SYSTEM_PROMPT.md](docs/FORENSIC_CHICKEN_OR_EGG_SYSTEM_PROMPT.md) and [docs/CREDITS_AND_CHICKEN_EGG_AGREEMENT.md](docs/CREDITS_AND_CHICKEN_EGG_AGREEMENT.md). They require evidence-led attribution, reciprocal concept/implementation provenance, preservation of originals, and clear limits on MIT and third-party institutional attribution. They do not imply Microsoft Research endorsement or a signed legal agreement.


## Brute Genius addendum

A production-context draft of the [Brute Genius Software License — Hold Harmless, Limited Warranty, and Production Risk Addendum](docs/BRUTE_GENIUS_HOLD_HARMLESS_WARRANTY_ADDENDUM.md) is available for legal review. It is a template, not an executed agreement or legal advice; bracketed business and jurisdiction terms must be completed before signature.

## Muse Screenplay module

An experimental, offline-first screenplay-generation module with a bundled Artifact Harness,
evaluation and optimization workflows, dataset provenance controls, and a hash-chained
governance ledger. It is maintained as a separate package under `muse_screenplay/`; the
existing `muse_core/` and `muse_gm/` foundations remain in place.

See the [module guide](muse_screenplay/README.md) for installation, CLI, model and dataset
options, and usage. The module's governance rules are in [GOVERNANCE.md](GOVERNANCE.md).
