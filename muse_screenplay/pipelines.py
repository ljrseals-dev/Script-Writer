"""Composable screenplay pipeline interface with mandatory target language."""
from dataclasses import dataclass, field

from .format_check import analyze_script
from .harness import Artifact, ArtifactHarness, EvalDataset


@dataclass
class PipelineResult:
    prompt: str
    script: str
    report: dict
    score: float | None = None
    stages: dict = field(default_factory=dict)
    language_provenance: dict = field(default_factory=dict)


class ScreenplayPipeline:
    def __init__(self, artifact: Artifact, harness: ArtifactHarness | None = None):
        self.harness = harness or ArtifactHarness("muse_screenplay_pipeline")
        self.artifact = artifact

    def run(self, prompt, *, target_language, score=True):
        if not isinstance(target_language, str) or not target_language.strip():
            raise ValueError("target_language is required")
        result = self.harness.execute(
            self.artifact, {"prompt": prompt, "target_language": target_language}
        )
        script = str(result.value or "")
        language = getattr(self.artifact.fn, "_last_language_provenance", None) or {
            "requested": target_language, "generated_in": "unverified",
            "language_mismatch": False,
        }
        output = PipelineResult(
            prompt, script, analyze_script(script).to_dict(),
            stages={
                "passed": result.passed,
                "duration_ms": round(result.duration_ms, 2),
                "tests": {test.name: test.passed for test in result.test_results},
                "error": result.error,
            },
            language_provenance=language,
        )
        if score and result.passed:
            output.score = self.artifact.evaluator(
                result.inputs, script, {"artifact": self.artifact.name}
            )
        return output

    def evaluate(self, dataset: EvalDataset):
        for case in dataset.cases:
            if not case.metadata.get("target_language"):
                raise ValueError("every evaluation case must declare metadata.target_language")
        return self.harness.evaluate(self.artifact, dataset)


def build_genre_conditioned_prompt(prompt, genre, tone=None):
    return (
        f"[GENRE: {genre.upper()}]"
        + (f" [TONE: {tone.upper()}]" if tone else "")
        + "\n\n"
        + prompt
    )


def build_screenplay_pipeline(model_key=None, *, genre=None, tone=None):
    from .harness_artifacts import build_script_artifact
    from .evaluators import composite_evaluator

    artifact = build_script_artifact(model_key)
    if genre:
        base = artifact.fn

        def genre_wrapper(prompt="", **kwargs):
            output = base(prompt=build_genre_conditioned_prompt(prompt, genre, tone), **kwargs)\n            genre_wrapper._last_language_provenance = getattr(base, "_last_language_provenance", None)\n            return output

        artifact.fn = genre_wrapper
        artifact.evaluator = composite_evaluator(
            format=.35, length=.2, dialogue=.15, diversity=.15, repetition=.15
        )
        artifact.provenance = {**artifact.provenance, "genre": genre, "tone": tone}
    return ScreenplayPipeline(artifact)
