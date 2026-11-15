# Repository layout and hygiene

This note distinguishes maintained code from retained historical material so contributors do not accidentally run or package an obsolete snapshot.

## Active code

- `muse_core/` contains the Muse narrative core.
- `muse_gm/` is the maintained MUSE-GM engine and local writing-room application.
- `tests/` contains the current automated tests.
- `results/baseline/` contains the checked-in baseline used by the current test suite.

## Retained historical material

- `Muse_GM/` is a legacy snapshot, not an installable package. Its former configuration directory is absent, so its standalone engine is not the supported entry point. See [`Muse_GM/README.md`](../Muse_GM/README.md).
- `prototype/muse_surface_v0.py` is retained as the original prototype source. A byte-identical duplicate formerly stored under `Muse_GM/` was removed.
- `results/prototype/surface_v0.json` is a historical prototype output, not a current baseline or validated empirical result.
- `logs/vintage-harness/` contains dry-run audit records from the separate Vintage Compressor Reference harness. They are preserved as provenance and explicitly record that no hardware measurements or submission occurred.
- `IMPORT_SNAPSHOT_SHA256SUMS` preserves the imported archive's checksum inventory. Its `repo/...` paths describe the imported snapshot namespace; it is not a checksum manifest for the current working tree and must not be used to validate current `main` files.

## Generated files and local environments

Runtime output belongs under `runs/` (or the directory selected with `MUSE_RUNS`). Python bytecode, virtual environments, common test/lint caches, coverage output, editor swap files, and OS metadata are ignored by `.gitignore`. Intentionally checked-in baseline and audit artifacts remain tracked.

## Contributor checks

Run from the repository root:

```bash
python -m unittest discover -v tests
python -m muse_gm check
```

GitHub Actions additionally compiles the active Python modules across the supported Python matrix. The legacy `Muse_GM/` snapshot is not part of the active test or packaging path.

## Cleanup policy

Historical material is retained when it carries provenance or explains an earlier implementation. Remove a duplicate only after confirming byte identity and preserving the canonical copy. Do not delete checked-in baseline outputs, audit records, or import provenance merely because they are not part of the active runtime.
