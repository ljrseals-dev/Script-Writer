from datetime import datetime, timezone

import pytest

from muse_screenplay.governance import GovernanceLedger, LedgerIntegrityError


def _ledger_verifies_before_append(tmp_path=None):
    path = tmp_path / "ledger.jsonl" if tmp_path else ":memory:"
    ledger = GovernanceLedger(path)
    ledger.append("a", "art", datetime.now(timezone.utc).isoformat(), {"x": 1})
    ledger.append("b", "art", datetime.now(timezone.utc).isoformat(), {"x": 2})
    assert ledger.verify()

    ledger._entries[0].payload["x"] = 999  # tamper

    with pytest.raises(LedgerIntegrityError):
        ledger.append("c", "art", datetime.now(timezone.utc).isoformat(), {"x": 3})


def test_ledger_verifies_before_append(tmp_path):
    _ledger_verifies_before_append(tmp_path)


def test_ledger_persists_and_reloads(tmp_path):
    path = tmp_path / ".muse" / "ledger.jsonl"
    ledger = GovernanceLedger(path)
    ledger.append("created", "artifact-1", "2026-11-14T00:00:00Z", {"ok": True})
    reloaded = GovernanceLedger(path)
    assert reloaded.verify()
    assert len(reloaded.entries) == 1


def test_ledger_rejects_external_disk_tampering(tmp_path):
    path = tmp_path / "ledger.jsonl"
    ledger = GovernanceLedger(path)
    ledger.append("created", "artifact-1", "now", {"ok": True})
    original = path.read_text(encoding="utf-8")

    path.write_text(original.replace('"artifact-1"', '"artifact-2"'), encoding="utf-8")

    with pytest.raises(LedgerIntegrityError, match="on-disk"):
        ledger.append("next", "artifact-1", "later", {})
    assert path.read_text(encoding="utf-8") != original


def test_ledger_rejects_stale_instance_before_append(tmp_path):
    path = tmp_path / "ledger.jsonl"
    first = GovernanceLedger(path)
    stale = GovernanceLedger(path)

    first.append("created", "artifact-1", "now", {})

    with pytest.raises(LedgerIntegrityError, match="changed since"):
        stale.append("created", "artifact-2", "later", {})

    reloaded = GovernanceLedger(path)
    assert len(reloaded.entries) == 1
    assert reloaded.entries[0].artifact_id == "artifact-1"


def test_ledger_export(tmp_path):
    ledger = GovernanceLedger(tmp_path / "source.jsonl")
    ledger.append("created", "artifact-1", "now", {})
    output = ledger.export(tmp_path / "data" / "ledger")
    assert output.exists()
    assert "artifact-1" in output.read_text(encoding="utf-8")
