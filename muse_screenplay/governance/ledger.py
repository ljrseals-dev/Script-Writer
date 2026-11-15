import json
import os
import tempfile
from contextlib import contextmanager
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


@contextmanager
def _exclusive_file_lock(path: Path):
    """Serialize cooperating writers across processes on POSIX and Windows."""
    lock_path = path.with_name(path.name + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as stream:
        if os.name == "nt":
            import msvcrt

            stream.seek(0)
            if stream.read(1) == b"":
                stream.seek(0)
                stream.write(b"\0")
                stream.flush()
            stream.seek(0)
            msvcrt.locking(stream.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                stream.seek(0)
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)


class GovernanceLedger:
    """Append-only, hash-chained ledger; tamper-evident, not externally anchored."""

    def __init__(self, path: str | Path = ".muse/ledger.jsonl"):
        self.path = Path(path)
        self._entries: list[LedgerEntry] = self._read_disk_entries()
        if not self._verify_entries(self._entries):
            raise LedgerIntegrityError("Persisted governance ledger failed verification")

    def _entry_body(self, sequence, event_type, artifact_id, timestamp, payload, previous_digest):
        return {
            "format_version": LEDGER_FORMAT_VERSION,
            "sequence": sequence,
            "event_type": event_type,
            "artifact_id": artifact_id,
            "timestamp": timestamp,
            "payload": payload,
            "previous_digest": previous_digest,
        }

    def _read_disk_entries(self) -> list[LedgerEntry]:
        if not self.path.exists():
            return []
        entries = []
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    entries.append(LedgerEntry(**json.loads(line)))
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, KeyError) as exc:
            raise LedgerIntegrityError("Persisted governance ledger cannot be parsed") from exc
        return entries

    def _verify_entries(self, entries: list[LedgerEntry]) -> bool:
        previous = GENESIS
        for index, entry in enumerate(entries, 1):
            if entry.format_version != LEDGER_FORMAT_VERSION or entry.sequence != index:
                return False
            if entry.previous_digest != previous:
                return False
            expected = sha256_value(
                self._entry_body(
                    entry.sequence,
                    entry.event_type,
                    entry.artifact_id,
                    entry.timestamp,
                    entry.payload,
                    entry.previous_digest,
                )
            )
            if entry.digest != expected:
                return False
            previous = entry.digest
        return True

    def verify(self) -> bool:
        return self._verify_entries(self._entries)

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

    def append(
        self,
        event_type: str,
        artifact_id: str,
        timestamp: str,
        payload: dict[str, Any] | None = None,
    ) -> LedgerEntry:
        # The advisory lock coordinates independent GovernanceLedger writers.
        # Re-read under that lock so stale instances and out-of-process edits
        # cannot silently be overwritten by this append.
        with _exclusive_file_lock(self.path):
            if not self.verify():
                raise LedgerIntegrityError("Refusing to append to a broken in-memory ledger")

            disk_entries = self._read_disk_entries()
            if not self._verify_entries(disk_entries):
                raise LedgerIntegrityError("Refusing to append to a broken on-disk ledger")
            if disk_entries != self._entries:
                raise LedgerIntegrityError(
                    "On-disk governance ledger changed since this instance was loaded"
                )

            data = dict(payload or {})
            previous = self._entries[-1].digest if self._entries else GENESIS
            sequence = len(self._entries) + 1
            body = self._entry_body(
                sequence, event_type, artifact_id, timestamp, data, previous
            )
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
        output.write_text(
            "".join(
                json.dumps(e.__dict__, sort_keys=True, ensure_ascii=False) + "\n"
                for e in self._entries
            ),
            encoding="utf-8",
        )
        return output
