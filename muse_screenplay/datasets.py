"""Offline-first screenplay datasets with explicit field, language, and provenance boundaries."""
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
    prompt_field: str | None
    expected_field: str | None = None
    split: str = "train"
    notes: str = ""
    languages: dict | None = None
    genre_fields: tuple[str, ...] = ()
    license_status: str = "unverified"\n    fallback: str | None = None


DATASETS = {
    "movies": DatasetSpec(
        "movies", "IsmaelMousa/movies", "Script",
        notes="1,172 English movie scripts; dataset card declares English and Apache-2.0.",
        languages={"declared": ["en"], "verified": [], "verification_method": None},
        license_status="apache-2.0 (dataset-card declared)",
    ),
    "moviesum": DatasetSpec(
        "moviesum", "rohitsaxena/MovieSum", "script", "summary",
        notes="2,200 XML-structured screenplays and summaries; train/val/test splits; CC BY-NC 4.0.",
        languages={"declared": ["unverified"], "verified": [], "verification_method": None},
        license_status="cc-by-nc-4.0",
    ),
    "imsdb": DatasetSpec(
        "imsdb", "aneeshas/imsdb-genre-movie-scripts", None,
        notes="150 rows arranged in five genre-specific columns; card says more information needed.",
        languages={"declared": ["en"], "verified": [], "verification_method": None},
        genre_fields=("Action", "Horror", "Sci-Fi", "Comedy", "Drama"),
        license_status="unverified",
    ),
}
ALIASES = {"sample": "offline", "movie": "movies", "sum": "moviesum", "genre": "imsdb"}


def _offline_dataset(limit, prompt_words, target_language, *, fallback_reason=None):
    rows = []
    selected = OFFLINE_CASES[:limit if limit is not None else len(OFFLINE_CASES)]
    for case in selected:
        prompt = case["prompt"]
        if prompt_words is not None:
            prompt = " ".join(prompt.split()[:prompt_words])
        rows.append({
            "prompt": prompt,
            "metadata": {**case["metadata"], "target_language": target_language},
        })
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
    if not isinstance(target_language, str) or not target_language.strip():
        raise ValueError("target_language is required for every screenplay evaluation/generation run")
    key = ALIASES.get(name.strip().lower(), name.strip().lower())
    if key == "offline":
        return _offline_dataset(limit, prompt_words, target_language)
    if key not in DATASETS:
        raise KeyError(f"Unknown dataset {name!r}")
    spec = DATASETS[key]
    try:
        from datasets import load_dataset
    except ImportError as exc:
        return _offline_dataset(limit, prompt_words, target_language, fallback_reason=exc)
    try:
        dataset = load_dataset(spec.hf_id, split=spec.split)
        if limit is not None:
            dataset = dataset.select(range(min(limit, len(dataset))))
        rows = []
        for row in dataset:
            candidates = []
            if spec.prompt_field:
                candidates.append((None, row.get(spec.prompt_field)))
            for genre in spec.genre_fields:
                candidates.append((genre, row.get(genre)))
            for genre, raw_prompt in candidates:
                prompt = str(raw_prompt or "").strip()
                if not prompt:
                    continue
                if prompt_words is not None:
                    prompt = " ".join(prompt.split()[:prompt_words])
                if prompt_chars is not None:
                    prompt = prompt[:prompt_chars]
                expected = (
                    str(row.get(spec.expected_field, "") or "")[:2000] or None
                    if spec.expected_field else None
                )
                metadata = {
                    field: row[field]
                    for field in ("genre", "genres", "title", "movie_name", "Name")
                    if field in row and row[field] is not None
                }
                if genre:
                    metadata["genre"] = genre
                rows.append({
                    "prompt": prompt,
                    "expected": expected,
                    "metadata": {**metadata, "target_language": target_language},
                })
        if not rows:
            raise ValueError("No non-empty screenplay rows matched the declared dataset field mapping")
        boundary = EvalBoundary(
            dataset_source=DatasetProvenance.REMOTE,
            dataset_id=spec.hf_id,
            disclaimer="Loaded from the configured remote Hugging Face dataset.",
        )
        return EvalDataset(key, rows, boundary=boundary)
    except Exception as exc:
        return _offline_dataset(limit, prompt_words, target_language, fallback_reason=exc)


def dataset_catalog():
    return {
        "offline": {"hf_id": None, "notes": f"{len(OFFLINE_CASES)} built-in prompt seeds."},
        **{
            key: {
                "hf_id": spec.hf_id,
                "notes": spec.notes,
                "languages": spec.languages,
                "field_mapping_verified": bool(spec.prompt_field or spec.genre_fields),
                "license_status": spec.license_status,\n                "fallback": spec.fallback,
            }
            for key, spec in DATASETS.items()
        },
    }
