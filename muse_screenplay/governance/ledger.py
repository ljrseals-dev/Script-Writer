import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from .integrity import sha256_value

LEDGER_FORMAT_VERSION = 1
GENESIS = "0" * 64

class LedgerIntegrityError(RuntimeError):
    pass

@dataclass(frozen=True)
class LedgerEntry:
    sequence: int
    event_type: str
    artifact_id: str
    timestamp: str
    payload: dict[str, Any]
    previous_digest: str
    digest: str
    format_version: int = LEDGER_FORMAT_VERSION

class GovernanceLedger:
    """Append-only, hash-chained ledger; tamper-evident, not externally anchored."""
    def __init__(self, path: str | Path = ".muse/ledger.jsonl"):
        self.path = Path(path)
        self._entries: list[LedgerEntry] = []
        if self.path.exists():
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    self._entries.append(LedgerEntry(**json.loads(line)))
            if not self.verify():
                raise LedgerIntegrityError("Persisted governance ledger failed verification")

    def _entry_body(self, sequence, event_type, artifact_id, timestamp, payload, previous_digest):
        return {"format_version": LEDGER_FORMAT_VERSION, "sequence": sequence,
                "event_type": event_type, "artifact_id": artifact_id,
                "timestamp": timestamp, "payload": payload,
                "previous_digest": previous_digest}

    def verify(self) -> bool:
        previous = GENESIS
        for index, entry in enumerate(self._entries, 1):
            if entry.format_version != LEDGER_FORMAT_VERSION or entry.sequence != index:
                return False
            if entry.previous_digest != previous:
                return False
            expected = sha256_value(self._entry_body(
                entry.sequence, entry.event_type, entry.artifact_id,
                entry.timestamp, entry.payload, entry.previous_digest))
            if entry.digest != expected:
                return False
            previous = entry.digest
        return True

    def _persist(self, entry: LedgerEntry) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        existing = self.path.read_text(encoding="utf-8") if self.path.exists() else ""
        line = json.dumps(entry.__dict__, sort_keys=True, ensure_ascii=False) + "\n"
        fd, temporary = tempfile.mkstemp(prefix=self.path.name + ".", dir=str(self.path.parent))
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as stream:
                stream.write(existing)
                stream.write(line)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, self.path)
        except Exception:
            try:
                os.unlink(temporary)
            except FileNotFoundError:
                pass
            raise

    def append(self, event_type: str, artifact_id: str, timestamp: str,
               payload: dict[str, Any] | None = None) -> LedgerEntry:
        if not self.verify():
            raise LedgerIntegrityError("Refusing to append to a broken governance ledger")
        data = dict(payload or {})
        previous = self._entries[-1].digest if self._entries else GENESIS
        sequence = len(self._entries) + 1
        body = self._entry_body(sequence, event_type, artifact_id, timestamp, data, previous)
        entry = LedgerEntry(**body, digest=sha256_value(body))
        self._persist(entry)
        self._entries.append(entry)
        return entry

    @property
    def entries(self) -> tuple[LedgerEntry, ...]:
        return tuple(self._entries)

    def export(self, directory: str | Path = "data/ledger") -> Path:
        target = Path(directory)
        target.mkdir(parents=True, exist_ok=True)
        output = target / "ledger.jsonl"
        output.write_text("".join(json.dumps(e.__dict__, sort_keys=True, ensure_ascii=False) + "\n"
                                   for e in self._entries), encoding="utf-8")
        return output
