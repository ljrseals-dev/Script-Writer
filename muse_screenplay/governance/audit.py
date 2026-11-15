from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

CRITERIA_FINGERPRINT_LIMITATIONS = (
    "Structural callable fingerprints include name, qualified name, bytecode, constants, "
    "and defaults. They do not capture closure values, mutable globals, referenced objects, "
    "environment variables, files, remote services, or external configuration."
)

@dataclass
class AuditEvent:
    event_type: str
    artifact_id: str
    rationale: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    before: dict[str, Any] = field(default_factory=dict)
    after: dict[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = (CRITERIA_FINGERPRINT_LIMITATIONS,)
