from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from .integrity import sha256_bytes

class DatasetProvenance(str, Enum):
    REMOTE = "remote"
    OFFLINE = "offline"
    FALLBACK = "fallback"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class Provenance:
    source: str
    source_type: str = "unknown"
    revision: str | None = None
    sha256: str | None = None
    details: dict[str, Any] | None = None

def file_provenance(path: str | Path, source: str | None = None) -> Provenance:
    data = Path(path).read_bytes()
    return Provenance(source or str(path), "file", sha256=sha256_bytes(data))
