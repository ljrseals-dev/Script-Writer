# Legacy MUSE-GM snapshot (not the active package)

This directory is retained for historical reference only. It is **not** the current MUSE-GM implementation and is not an installable Python package.

The maintained implementation lives in the lowercase [`muse_gm/`](../muse_gm/) package. Use the repository-root instructions in [`README.md`](../README.md), and run its checks from the repository root:

```bash
python -m unittest discover -v tests
python -m muse_gm check
```

## Historical contents

- `muse_gm.py` — an earlier standalone engine snapshot. Its former `config/` directory is not present here, so this script is not expected to run from this directory.
- `surface.json` — a retained historical output; it is not a current baseline or a claim of independently verified story quality.
- `run.log.jsonl`, `failures.jsonl`, and `summary.json` were Vintage Compressor Reference dry-run records accidentally colocated with this legacy directory. They have been moved to [`logs/vintage-harness/`](../logs/vintage-harness/) so their provenance and project boundary are explicit.

The byte-identical duplicate of `prototype/muse_surface_v0.py` and the stale local `pyproject.toml` have been removed. The original prototype remains under `prototype/` for provenance.

Do not use this directory's historical code or output as evidence that the current engine has the same behavior. The active engine, current tests, and checked-in baseline are maintained separately.
