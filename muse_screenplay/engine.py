"""Deterministic Muse prompt compiler and optional Hugging Face generation adapter."""
from __future__ import annotations
import hashlib
import json
import random
from dataclasses import dataclass
from pathlib import Path
from .models import get_model

STAGES = ("ordinary_world", "inciting_incident", "rising_action", "first_climax",
          "fall", "dark_night", "second_climax", "falling_action", "resolution")

@dataclass(frozen=True)
class ScriptBrief:
    title: str
    premise: str
    genre: str = "historical crime drama"
    period: str = "unspecified"
    location: str = "unspecified"
    language: str = "en"
    characters: str = ""
    research_notes: str = ""
    constraints: str = ""

def _muse_consult(stage: str) -> dict:
    try:
        from muse_core.muse_bridge import consult
        return consult(stage, "en")
    except (ImportError, FileNotFoundError):
        return {"stage": {"stage": stage, "language": "en", "prompts": []},
                "symbolic_readings": [], "core_modified": False}

def compile_prompt(brief: ScriptBrief) -> str:
    """Compile a stable nine-stage prompt; the genre layer cannot rewrite Muse semantics."""
    if not brief.title.strip() or not brief.premise.strip():
        raise ValueError("title and premise are required")
    sections = [
        "ROLE: Draft screenplay material under the deterministic Muse narrative structure.",
        "ENGINE: Muse by Rihanna. Preserve the fixed nine-stage order; do not merge or omit stages.",
        "GENRE LENS: Gangster Manga / Brute Genius is a sidecar, not a source of historical facts.",
        "HISTORICAL RULE: Use supplied source-backed research only. Never invent dates, laws, quotations, or events.",
        "Mark unsupported factual details [RESEARCH NEEDED]. Separate fact, disputed claim, interpretation, and fiction.",
        f"TITLE: {brief.title.strip()}", f"PREMISE: {brief.premise.strip()}",
        f"GENRE: {brief.genre}", f"PERIOD: {brief.period}", f"LOCATION: {brief.location}",
        f"CHARACTERS: {brief.characters or 'Develop from the supplied premise and research.'}",
        f"RESEARCH NOTES: {brief.research_notes or 'No verified research supplied.'}",
        f"CONSTRAINTS: {brief.constraints or 'Maintain causal continuity and avoid stereotypes.'}",
        f"FINAL OUTPUT LANGUAGE: {brief.language}",
        "OUTPUT: First provide a beat sheet under all nine headings, then a screenplay draft.",
        "For each scene include INT./EXT., location, time, action, and dialogue.",
        "English is canonical for model prompts and reasoning; honor the requested final output language.",
    ]
    for stage in STAGES:
        prompts = _muse_consult(stage).get("stage", {}).get("prompts", [])
        if isinstance(prompts, str):
            prompts = [prompts]
        sections.append("\nMUSE STAGE — " + stage.upper().replace("_", " "))
        sections.extend("- " + str(item) for item in prompts)
        sections.append("Track the character decision, consequence, and change in power or knowledge.")
    return "\n".join(sections)

def prompt_digest(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

def _seed_everything(seed: int) -> None:
    random.seed(seed)
    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass
    try:
        import torch
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)
        torch.use_deterministic_algorithms(True, warn_only=True)
        if hasattr(torch.backends, "cudnn"):
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

def load_generator(model_key: str, *, download: bool = False, revision: str = "main"):
    """Load from local cache by default. Network access requires explicit download=True."""
    try:
        from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
    except ImportError as exc:
        raise RuntimeError("Install optional dependencies: pip install -e '.[models]'") from exc
    spec = get_model(model_key)
    common = {"revision": revision, "trust_remote_code": False, "local_files_only": not download}
    tokenizer = AutoTokenizer.from_pretrained(spec.repo_id, **common)
    model_cls = AutoModelForSeq2SeqLM if spec.architecture == "seq2seq" else AutoModelForCausalLM
    model = model_cls.from_pretrained(spec.repo_id, **common)
    return pipeline(spec.task, model=model, tokenizer=tokenizer)

def generate(brief: ScriptBrief, *, model_key: str, seed: int = 17,
             max_new_tokens: int = 1200, download: bool = False, revision: str = "main") -> dict:
    if not 1 <= max_new_tokens <= 8192:
        raise ValueError("max_new_tokens must be between 1 and 8192")
    prompt = compile_prompt(brief)
    _seed_everything(seed)
    generator = load_generator(model_key, download=download, revision=revision)
    result = generator(prompt, do_sample=False, num_beams=1,
                       max_new_tokens=max_new_tokens, truncation=True)
    generated = result[0].get("generated_text") or result[0].get("summary_text") or ""
    if generated.startswith(prompt):
        generated = generated[len(prompt):].lstrip()
    if not generated.strip():
        raise RuntimeError("The selected model returned empty text")
    spec = get_model(model_key)
    return {
        "title": brief.title, "engine": "Muse by Rihanna",
        "genre_layer": "Gangster Manga / Brute Genius",
        "model": spec.repo_id, "revision": revision, "seed": seed,
        "decoding": {"do_sample": False, "num_beams": 1, "max_new_tokens": max_new_tokens},
        "prompt_sha256": prompt_digest(prompt), "prompt": prompt, "script": generated,
        "determinism_note": "Greedy decoding and a seed improve repeatability; bit-identical output across hardware and library versions is not guaranteed.",
    }

def write_result(result: dict, output: str | Path) -> Path:
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return target
