#!/usr/bin/env python3
"""Static integration check for the Muse Screenplay governance interfaces.

This checks importability and cross-module contracts. It is not a substitute for pytest
and does not claim that unrelated Muse packages are untouched or side-effect free.
"""
from __future__ import annotations

import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

def check_imports() -> None:
    from muse_screenplay.governance import (
        GovernanceLedger, LedgerIntegrityError, EvalBoundary, DatasetProvenance,
        assert_no_offline_disguise,
    )
    from muse_screenplay.harness import ArtifactHarness, criteria_fingerprint
    assert GovernanceLedger and LedgerIntegrityError and EvalBoundary
    assert DatasetProvenance.FALLBACK.value == "fallback"
    assert callable(assert_no_offline_disguise)
    assert callable(ArtifactHarness) and callable(criteria_fingerprint)

def check_boundary_contract() -> None:
    from muse_screenplay.governance import EvalBoundary, DatasetProvenance, assert_no_offline_disguise
    from muse_screenplay.harness import ArtifactHarness
    boundary = EvalBoundary(
        dataset_source=DatasetProvenance.FALLBACK,
        fallback_reason="network unavailable",
        disclaimer="Using local fixture data; not a remote evaluation.",
    )
    assert_no_offline_disguise(boundary)
    observed = {}
    artifact = ArtifactHarness().create_code_artifact(
        "boundary-check", lambda prompt="", **kwargs: observed.update(kwargs) or prompt,
    )
    result = ArtifactHarness().execute(
        artifact, {"prompt": "fixture", "_boundary": boundary},
    )
    assert result.passed
    assert observed == {}, "boundary metadata leaked into artifact inputs"
    assert result.context["_boundary"] is boundary

def check_criteria_contract() -> None:
    from muse_screenplay.harness import ArtifactHarness
    harness = ArtifactHarness()
    original = harness.create_code_artifact(
        "criteria-check", lambda prompt="": prompt,
        evaluator=lambda inputs, output, context: 1.0,
        criteria_spec={"rubric": "v1"},
    )
    revised = original.with_criteria(criteria_spec={"rubric": "v2"})
    assert revised.config == original.config
    assert revised.criteria_version == original.criteria_version + 1
    assert revised.criteria_digest != original.criteria_digest

def check_ledger_contract() -> None:
    from muse_screenplay.governance import GovernanceLedger, LedgerIntegrityError
    with tempfile.TemporaryDirectory(prefix="muse-governance-") as directory:
        ledger = GovernanceLedger(Path(directory) / "ledger.jsonl")
        ledger.append("created", "artifact", datetime.now(timezone.utc).isoformat(), {"x": 1})
        ledger.append("evaluated", "artifact", datetime.now(timezone.utc).isoformat(), {"score": 0.5})
        assert ledger.verify()
        ledger._entries[0].payload["x"] = 999
        try:
            ledger.append("mutated", "artifact", datetime.now(timezone.utc).isoformat(), {})
        except LedgerIntegrityError:
            return
        raise AssertionError("append() extended a broken chain instead of raising")

def main() -> int:
    checks = (
        check_imports,
        check_boundary_contract,
        check_criteria_contract,
        check_ledger_contract,
    )
    for check in checks:
        check()
        print(f"PASS {check.__name__}")
    print("PASS governance interface integration (behavioral pytest suite still required)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
