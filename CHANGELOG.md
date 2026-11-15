# Changelog

## Unreleased
- Repository hygiene: clarified the active lowercase `muse_gm/` package versus the retained `Muse_GM/` snapshot.
- Corrected stale README references to a screenplay adapter that is not present in this revision.
- Moved Vintage Compressor Reference dry-run records under `logs/vintage-harness/` and expanded ignores for local Python/tooling artifacts.
- Removed a byte-identical duplicate prototype file and obsolete legacy packaging metadata; the original prototype and historical result remain preserved.

## 0.1.0
- Engine: exhaustive enumeration of 4,445,280 combinations (8 variables), six scored components, `master` and `equal` profiles.
- Config-driven variables (value labels) and rubric tables, with fail-closed validation.
- CLI: `variables`, `check`, `run` (`--select`, `--distinct`, `--out`), `sensitivity`; CSV, JSONL, manifest and SPSS syntax export.
- Chat app: local web UI, Claude tool loop, human-click approval gate, artifact gate.
- 26 tests (engine and app, fake Claude client).
