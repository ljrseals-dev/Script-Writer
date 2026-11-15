"""Explicit Hugging Face model registry; no import-time downloads."""
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelSpec:
    key: str
    repo_id: str
    task: str
    architecture: str
    description: str

MODELS = {
    "script-bart": ModelSpec("script-bart", "sahilnagaralu/movie-script-generator", "text2text-generation", "seq2seq", "BART screenplay generator"),
    "gpt2-screenplay": ModelSpec("gpt2-screenplay", "AventIQ-AI/gpt-2-movie-script-writter", "text-generation", "causal", "GPT-2 screenplay model"),
    "mini-gpt-script": ModelSpec("mini-gpt-script", "pranikz/SLM-Movie-Script", "text-generation", "causal", "Compact movie-script language model"),
}

def get_model(key: str) -> ModelSpec:
    if key in MODELS:
        return MODELS[key]
    for spec in MODELS.values():
        if spec.repo_id == key:
            return spec
    raise KeyError(f"Unknown model {key!r}; choose one of: {', '.join(MODELS)}")
