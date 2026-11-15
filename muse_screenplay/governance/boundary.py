from dataclasses import dataclass
from .provenance import DatasetProvenance

@dataclass(frozen=True)
class EvalBoundary:
    dataset_source: DatasetProvenance = DatasetProvenance.UNKNOWN
    fallback_reason: str | None = None
    disclaimer: str | None = None
    dataset_id: str | None = None

def assert_no_offline_disguise(boundary: EvalBoundary | None) -> None:
    if boundary is None:
        return
    if boundary.dataset_source is DatasetProvenance.FALLBACK:
        if not boundary.fallback_reason or not boundary.disclaimer:
            raise ValueError("Fallback evaluation must disclose fallback_reason and disclaimer")
