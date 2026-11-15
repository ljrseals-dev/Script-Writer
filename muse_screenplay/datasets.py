"""Offline-first prompt datasets with explicit remote/offline/fallback provenance."""
from dataclasses import dataclass

from .harness.dataset import EvalDataset
from .governance import DatasetProvenance, EvalBoundary

OFFLINE_CASES = [
    {"prompt": "INT. DINER - NIGHT\n\nA tired waitress wipes the counter. MARCUS stares at a napkin.\n\nMARCUS:", "metadata": {"genre": "drama"}},
    {"prompt": "EXT. ROOFTOP - DAWN\n\nTwo strangers sit above the city.\n\nJUNE:", "metadata": {"genre": "romance"}},
    {"prompt": "INT. SPACESHIP COCKPIT - CONTINUOUS\n\nAlarms blink red. HAYES grips the yoke.\n\nHAYES:", "metadata": {"genre": "sci-fi"}},
    {"prompt": "INT. INTERROGATION ROOM - DAY\n\nA bulb swings. ROSS slides a photograph across the table.\n\nROSS:", "metadata": {"genre": "thriller"}},
    {"prompt": "INT. RECORD STORE - AFTERNOON\n\nELI flips through vinyl.\n\nELI:", "metadata": {"genre": "comedy"}},
]

@dataclass(frozen=True)
class DatasetSpec:
    key: str
    hf_id: str
    prompt_field: str
    expected_field: str | None = None
    split: str = "train"
    notes: str = ""
    languages: dict = None

DATASETS = {
    "movies": DatasetSpec("movies", "IsmaelMousa/movies", "Script", notes="Full movie scripts; language distribution unverified.", languages={"declared": ["unverified"], "verified": [], "verification_method": None}),
    "moviesum": DatasetSpec("moviesum", "rohitsaxena/MovieSum", "screenplay", "summary",
                            notes="Screenplays and summaries; language distribution unverified.", languages={"declared": ["unverified"], "verified": [], "verification_method": None}),
    "imsdb": DatasetSpec("imsdb", "aneeshas/imsdb-genre-movie-scripts", "script",
                         notes="IMSDb source-implied English; not independently audited.", languages={"declared": ["en"], "verified": [], "verification_method": None}),
}
ALIASES = {"sample": "offline", "movie": "movies", "sum": "moviesum", "genre": "imsdb"}

def _offline_dataset(limit, prompt_words, *, fallback_reason=None):
    rows = []
    selected = OFFLINE_CASES[:limit if limit is not None else len(OFFLINE_CASES)]
    for case in selected:
        prompt = case["prompt"]
        if prompt_words is not None:
            prompt = " ".join(prompt.split()[:prompt_words])
        rows.append({"prompt": prompt, "target_language": target_language, "metadata": case["metadata"]})
    if fallback_reason is None:
        boundary = EvalBoundary(
            dataset_source=DatasetProvenance.OFFLINE,
            dataset_id="builtin:offline",
            disclaimer="Built-in offline prompt seeds; no remote dataset was loaded.",
        )
        name = "offline"
    else:
        boundary = EvalBoundary(
            dataset_source=DatasetProvenance.FALLBACK,
            fallback_reason=str(fallback_reason),
            disclaimer=(
                "Remote dataset loading failed. This evaluation uses built-in offline "
                "prompt seeds and must not be represented as a remote-dataset evaluation."
            ),
            dataset_id="builtin:offline",
        )
        name = "offline-fallback"
    return EvalDataset(name, rows, boundary=boundary)

def load_eval_dataset(name="offline", limit=5, prompt_chars=1200, prompt_words=None, *, target_language=None):
    if not isinstance(target_language, str) or not target_language.strip():\n        raise ValueError("target_language is required for every screenplay evaluation/generation run")\n    key = ALIASES.get(name.strip().lower(), name.strip().lower())
    if key == "offline":
        return _offline_dataset(limit, prompt_words)
    if key not in DATASETS:
        raise KeyError(f"Unknown dataset {name!r}")
    spec = DATASETS[key]
    try:
        from datasets import load_dataset
    except ImportError as exc:
        return _offline_dataset(limit, prompt_words, fallback_reason=exc)
    try:
        dataset = load_dataset(spec.hf_id, split=spec.split)
        if limit is not None:
            dataset = dataset.select(range(min(limit, len(dataset))))
        rows = []
        for row in dataset:
            prompt = str(row.get(spec.prompt_field, "") or "")
            if prompt_words is not None:
                prompt = " ".join(prompt.split()[:prompt_words])
            if prompt_chars is not None:
                prompt = prompt[:prompt_chars]
            expected = (
                str(row.get(spec.expected_field, "") or "")[:2000] or None
                if spec.expected_field else None
            )
            metadata = {
                key: row[key] for key in ("genre", "genres", "title", "movie_name")
                if key in row and row[key] is not None
            }
            rows.append({"prompt": prompt, "expected": expected, "target_language": target_language, "metadata": metadata})
        boundary = EvalBoundary(
            dataset_source=DatasetProvenance.REMOTE,
            dataset_id=spec.hf_id,
            disclaimer="Loaded from the configured remote Hugging Face dataset.",
        )
        return EvalDataset(key, rows, boundary=boundary)
    except Exception as exc:
        return _offline_dataset(limit, prompt_words, fallback_reason=exc)

def dataset_catalog():
    return {
        "offline": {"hf_id": None, "notes": f"{len(OFFLINE_CASES)} built-in prompt seeds."},
        **{key: {"hf_id": spec.hf_id, "notes": spec.notes}
           for key, spec in DATASETS.items()},
    }
