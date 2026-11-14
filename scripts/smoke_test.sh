#!/usr/bin/env bash
set -euo pipefail
muse-screenplay models
muse-screenplay datasets
muse-screenplay validate --file examples/sample_scene.txt
echo "Smoke test complete. Generation requires optional model dependencies."
