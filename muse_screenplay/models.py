"""Hugging Face model registry."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ModelSpec:
    key: str
    hf_id: str
    task: str
    family: str
    notes: str = ""
MODELS = {
    "script-bart": ModelSpec("script-bart", "sahilnagaralu/movie-script-generator", "text2text-generation", "bart"),
    "gpt2-screenplay": ModelSpec("gpt2-screenplay", "AventIQ-AI/gpt-2-movie-script-writter", "text-generation", "gpt2"),
    "mini-gpt-script": ModelSpec("mini-gpt-script", "pranikz/SLM-Movie-Script", "text-generation", "minigpt"),
}
ALIASES = {"bart":"script-bart", "default":"script-bart", "gpt2":"gpt2-screenplay", "mini":"mini-gpt-script"}
def get_model(key):
    key=key.strip()
    if key in MODELS:return MODELS[key]
    if key in ALIASES:return MODELS[ALIASES[key]]
    for spec in MODELS.values():
        if spec.hf_id==key:return spec
    raise KeyError(f"Unknown model {key!r}; known: {', '.join(MODELS)}")
def resolve_model(key):
    try:return get_model(key)
    except KeyError:return ModelSpec(key,key,"text-generation","custom")
