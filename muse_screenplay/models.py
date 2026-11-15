"""Auditable Hugging Face registry; language coverage is never inferred as multilingual."""
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True)
class ModelSpec:
    key: str
    hf_id: str
    task: str
    family: str
    notes: str = ""
    languages: dict = field(default_factory=lambda: {
        "declared": ["unverified"], "verified": [], "verification_method": None
    })
    tokenizer_languages: str = "unverified"
    fallback: str | None = None
    revision: str | None = None
    expected_sha256: dict = field(default_factory=dict)

    def to_dict(self):
        return asdict(self)


MODELS = {
    "summary-distilbart": ModelSpec(
        "summary-distilbart", "sshleifer/distilbart-cnn-12-6",
        "summarization", "bart",
        notes="Summarization model; language coverage is unverified.",
        languages={"declared": ["unverified"], "verified": [], "verification_method": None},
    ),
    "script-bart": ModelSpec(
        "script-bart", "sahilnagaralu/movie-script-generator",
        "text2text-generation", "bart",
        notes="BART-base fine-tune; model-card language declaration requires verification.",
        languages={"declared": ["unverified"], "verified": [], "verification_method": None},
    ),
    "gpt2-screenplay": ModelSpec(
        "gpt2-screenplay", "AventIQ-AI/gpt-2-movie-script-writter",
        "text-generation", "gpt2",
        notes="GPT-2 English is expected from the model description; not independently evaluated.",
        languages={"declared": ["en"], "verified": [], "verification_method": None},
    ),
    "mini-gpt-script": ModelSpec(
        "mini-gpt-script", "pranikz/SLM-Movie-Script",
        "text-generation", "minigpt",
        notes="Small Transformer trained on IsmaelMousa/movies; source dataset declares English, model output not independently evaluated.",
        languages={"declared": ["en"], "verified": [], "verification_method": None},
    ),
}

ALIASES = {
    "bart": "script-bart",
    "default": "script-bart",
    "gpt2": "gpt2-screenplay",
    "mini": "mini-gpt-script",
}

# Non-default candidates require separate language, architecture, and license review.
CANDIDATES = []


def get_model(key):
    key = key.strip()
    if key in MODELS:
        return MODELS[key]
    if key in ALIASES:
        return MODELS[ALIASES[key]]
    for spec in MODELS.values():
        if spec.hf_id == key:
            return spec
    raise KeyError(f"Unknown model {key!r}; known: {', '.join(MODELS)}")


def resolve_model(key):
    try:
        return get_model(key)
    except KeyError:
        return ModelSpec(key, key, "text-generation", "custom")
