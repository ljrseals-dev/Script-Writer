"""Evaluation dataset containers and provenance boundary."""
from dataclasses import dataclass, field

@dataclass
class EvalCase:
    prompt: str
    expected: str | None = None
    metadata: dict = field(default_factory=dict)

    @classmethod
    def coerce(cls, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            return cls(value)
        data = dict(value)
        prompt = data.pop("prompt", "")
        expected = data.pop("expected", None)
        metadata = data.pop("metadata", None)
        return cls(prompt, expected, data if metadata is None else metadata)

class EvalDataset:
    def __init__(self, name, cases, boundary=None):
        self.name = name
        self.cases = [EvalCase.coerce(case) for case in cases]
        self.boundary = boundary

    def __len__(self):
        return len(self.cases)

    def __iter__(self):
        return iter(self.cases)

    def __getitem__(self, index):
        return self.cases[index]

    def __repr__(self):
        return f"EvalDataset(name={self.name!r}, cases={len(self.cases)})"
