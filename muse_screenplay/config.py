"""Environment-driven settings."""
import os
from dataclasses import dataclass, field
from pathlib import Path

def _int(name, default):
    try: return int(os.getenv(name, default))
    except (TypeError, ValueError): return default
def _float(name, default):
    try: return float(os.getenv(name, default))
    except (TypeError, ValueError): return default
@dataclass
class Settings:
    hf_token: str | None = field(default_factory=lambda: os.getenv("HF_TOKEN") or None)
    hf_home: Path = field(default_factory=lambda: Path(os.getenv("HF_HOME", "./data/hf")).expanduser())
    default_model: str = field(default_factory=lambda: os.getenv("MUSE_MODEL", "script-bart"))
    device: str = field(default_factory=lambda: os.getenv("MUSE_DEVICE", "auto"))
    max_length: int = field(default_factory=lambda: _int("MUSE_MAX_LENGTH", 256))
    temperature: float = field(default_factory=lambda: _float("MUSE_TEMPERATURE", .9))
    top_p: float = field(default_factory=lambda: _float("MUSE_TOP_P", .95))
    default_dataset: str = field(default_factory=lambda: os.getenv("MUSE_DATASET", "offline"))
    dataset_limit: int = field(default_factory=lambda: _int("MUSE_DATASET_LIMIT", 5))
    def apply_environment(self):
        self.hf_home.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("HF_HOME", str(self.hf_home))
        if self.hf_token: os.environ.setdefault("HF_TOKEN", self.hf_token)
    def resolve_device(self):
        if self.device == "cpu": return -1
        if self.device.startswith("cuda"):
            _, _, idx = self.device.partition(":")
            return int(idx or 0)
        if self.device == "auto":
            try:
                import torch
                return 0 if torch.cuda.is_available() else -1
            except ImportError: return -1
        return -1
settings = Settings()
