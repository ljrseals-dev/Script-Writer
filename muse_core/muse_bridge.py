"""Theme bridge: enriches Muse by Rihanna consultations without changing core semantics."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEME = ROOT / "themes" / "gangster_manga"


def _load(name):
    with (THEME / name).open(encoding="utf-8") as stream:
        return json.load(stream)


def theme_prompt(stage_key: str, language: str = "en") -> dict:
    """Return localized genre prompts; unknown languages safely fall back to English."""
    data = _load("stage_prompts.json")
    for stage in data["stages"]:
        if stage["key"] == stage_key:
            prompts = stage["prompts"]
            chosen = language if language in prompts else "en"
            return {"stage": stage_key, "language": chosen, "prompts": prompts[chosen]}
    raise KeyError(f"unknown Muse narrative stage: {stage_key}")


def symbolic_reading(register: str, symbol: str) -> dict | None:
    """Return the genre lens for one symbol; never changes Muse's base definition."""
    palette = _load("palette_mapping.json")
    group = palette.get(register, {})
    item = group.get(symbol)
    if item is None:
        return None
    return {"register": register, "symbol": symbol,
            "muse_default": item["muse_default"],
            "gangster_manga": item["gangster_manga"]}


def consult(stage_key: str, language: str = "en", symbols: list[tuple[str, str]] | None = None) -> dict:
    """A sidecar consultation. Call the original Muse core separately for base prompts."""
    readings = [reading for pair in (symbols or [])
                if (reading := symbolic_reading(pair[0], pair[1])) is not None]
    return {"engine": "Muse by Rihanna", "theme": "gangster_manga",
            "core_modified": False, "stage": theme_prompt(stage_key, language),
            "symbolic_readings": readings}
