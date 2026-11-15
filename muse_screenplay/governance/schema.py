from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any

class Relationship(str, Enum):
    IMPLEMENTS = "implements"
    CHALLENGES = "challenges"
    CONSTRAINS = "constrains"
    INSPIRES = "inspires"
    UNKNOWN = "unknown"

@dataclass(frozen=True)
class Contribution:
    person: str
    description: str
    status: str = "Unknown"
    evidence_ids: tuple[str, ...] = ()

@dataclass(frozen=True)
class ArtifactRecord:
    artifact_id: str
    artifact_type: str
    sha256: str | None = None
    source: str | None = None
    relationship: Relationship = Relationship.UNKNOWN
    status: str = "Unknown"
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class CreditRecord:
    requested_credits: tuple[str, ...] = ()
    evidenced_contributions: tuple[Contribution, ...] = ()

@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    description: str
    status: str = "Unknown"
    artifact_sha256: str | None = None
    source: str | None = None
    limitations: tuple[str, ...] = ()

@dataclass(frozen=True)
class MutationRecord:
    artifact_id: str
    rationale: str
    before_evaluation: dict[str, Any]
    after_evaluation: dict[str, Any]
    criteria_before: str | None = None
    criteria_after: str | None = None
    status: str = "Incomplete"

def to_dict(record: Any) -> dict[str, Any]:
    value = asdict(record)
    for key, item in tuple(value.items()):
        if isinstance(item, Enum):
            value[key] = item.value
    return value
