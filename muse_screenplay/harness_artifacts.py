"""Build generation artifacts with explicit provenance and attribution boundaries."""
from functools import lru_cache

from .config import settings
from .evaluators import default_evaluator
from .format_check import analyze_script
from .generators import GenerationConfig, Generator
from .harness import ConstraintLevel, TestCase, load_harness
from .harness import criteria_fingerprint

def _normalize_attribution(attribution):
    if attribution is None:
        return {
            "status": "Unknown",
            "requested_credits": [],
            "evidenced_contributions": [],
            "note": "No attribution statement supplied at artifact build time.",
        }
    if not isinstance(attribution, dict):
        raise TypeError("attribution must be a mapping with separate requested_credits and evidenced_contributions")
    requested = attribution.get("requested_credits", [])
    evidenced = attribution.get("evidenced_contributions", [])
    if not isinstance(requested, (list, tuple)) or not isinstance(evidenced, (list, tuple)):
        raise TypeError("requested_credits and evidenced_contributions must be lists or tuples")
    if any(not isinstance(name, str) or not name.strip() for name in requested):
        raise ValueError("requested_credits entries must be non-empty strings")
    if any(not isinstance(item, dict) for item in evidenced):
        raise ValueError("evidenced_contributions entries must be mappings")
    return {
        "status": attribution.get("status", "Unknown"),
        "requested_credits": list(requested),
        "evidenced_contributions": list(evidenced),
        "limitations": list(attribution.get("limitations", [])),
    }

@lru_cache(maxsize=8)
def _generator(key, length, temp, top_p):
    return Generator(key, generation=GenerationConfig(
        max_length=length, temperature=temp, top_p=top_p,
    ))

def script_tests():
    return [
        TestCase("non_empty_output", lambda value: isinstance(value, str) and bool(value.strip()),
                 ConstraintLevel.ASSERT, "empty output"),
        TestCase("min_words", lambda value: len(str(value).split()) >= 15,
                 ConstraintLevel.WARN, "output shorter than 15 words"),
        TestCase("screenplay_structure", lambda value: bool(
            analyze_script(str(value)).scene_headings or analyze_script(str(value)).dialogue_lines
        ), ConstraintLevel.WARN, "no scene heading or dialogue"),
    ]

def build_script_artifact(model_key=None, *, max_length=None, temperature=None, top_p=None,
                          name=None, attribution=None, criteria_spec=None):
    key = model_key or settings.default_model
    length = settings.max_length if max_length is None else max_length
    temp = settings.temperature if temperature is None else temperature
    probability = settings.top_p if top_p is None else top_p
    attribution_record = _normalize_attribution(attribution)

    def generate(prompt="", **kwargs):
        generator = _generator(key, length, temp, probability)
        target_language = kwargs.pop("target_language", None)
        if not target_language:
            raise ValueError("target_language is required; generation is never defaulted to English")
        overrides = {
            key: value for key, value in kwargs.items()
            if key in GenerationConfig.__dataclass_fields__
        }
        output = generator.generate(prompt, target_language=target_language, **overrides)\n        generate._last_language_provenance = generator._last_language_provenance\n        return output

    generator = _generator(key, length, temp, probability)
    tests = script_tests()
    spec = criteria_spec or {
        "evaluator": "default_evaluator",
        "tests": [{"name": test.name, "level": test.level.value} for test in tests],
        "generation_contract": "prompt-to-screenplay",
    }
    provenance = {
        **generator.provenance(),
        "attribution": attribution_record,
        "criteria_fingerprint": criteria_fingerprint(default_evaluator, tests, spec),
        "attribution_policy": (
            "Requested credits and evidenced contributions are stored separately; "
            "missing attribution is Unknown, never inferred."
        ),
    }
    return load_harness().create_code_artifact(
        name or f"script_generator[{key}]",
        generate,
        "prompt: str -> script: str",
        default_evaluator,
        tests,
        {"temperature": temp, "top_p": probability, "max_length": length},
        provenance,
        criteria_spec=spec,
    )

def build_summary_artifact(model_id="sshleifer/distilbart-cnn-12-6", *, attribution=None):
    attribution_record = _normalize_attribution(attribution)

    if model_id != "sshleifer/distilbart-cnn-12-6":
        raise ValueError("Only the registered built-in DistilBART summarizer is allowed")
    def summarize(prompt="", target_language=None, max_length=130, min_length=30):
        if not target_language:
            raise ValueError("target_language is required; summarization is never defaulted to English")
        generator = Generator("summary-distilbart", generation=GenerationConfig(
            max_new_tokens=max_length, do_sample=False,
        ))
        output = generator.generate(prompt[:3000], target_language=target_language, min_length=min_length)\n        summarize._last_language_provenance = generator._last_language_provenance\n        return output

    return load_harness().create_code_artifact(
        "script_summarizer", summarize, "prompt -> summary",
        tests=[TestCase("non_empty_summary", lambda value: len(str(value).split()) >= 5)],
        provenance={
            "hf_id": model_id, "task": "summarization",
            "pytorch_weights_only": True, "remote_code_policy": "disabled",
            "trust_remote_code": False, "use_safetensors": True,
            "attribution": attribution_record,
        },
        criteria_spec={"task": "summarization", "minimum_words": 5},
    )

def build_default_pipeline(model_key=None, *, attribution=None):
    harness = load_harness()
    generator = build_script_artifact(model_key, attribution=attribution)
    gate = harness.create_code_artifact(
        "format_gate", lambda prompt, **kwargs: prompt, "script -> script",
        tests=[TestCase(
            "scene_heading", lambda value: analyze_script(str(value)).scene_headings > 0,
            ConstraintLevel.WARN,
        )],
        provenance={"attribution": _normalize_attribution(attribution)},
        criteria_spec={"test": "scene_heading", "level": "warn"},
    )
    return harness.compose([generator, gate], name="default_pipeline")
