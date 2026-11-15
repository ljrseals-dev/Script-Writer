from dataclasses import dataclass, field
from .integrity import sha256_value

@dataclass(frozen=True)
class Evidence:
    evidence_id: str
    description: str
    payload: dict = field(default_factory=dict)
    status: str = "Unknown"
    limitations: tuple[str, ...] = ()

    @property
    def digest(self) -> str:
        # A digest establishes byte consistency, not authorship or ownership.
        return sha256_value({"id": self.evidence_id, "description": self.description,
                             "payload": self.payload, "status": self.status,
                             "limitations": self.limitations})
