from muse_screenplay.datasets import load_eval_dataset
from muse_screenplay.governance import DatasetProvenance
from muse_screenplay.harness import ArtifactHarness, criteria_fingerprint

def test_boundary_metadata_never_reaches_artifact_function():
    seen = {}
    def fn(prompt="", **kwargs):
        seen.update(kwargs)
        return prompt
    harness = ArtifactHarness()
    artifact = harness.create_code_artifact("echo", fn)
    result = harness.execute(
        artifact, {"prompt": "hello", "_boundary": "internal", "_boundary_trace": "trace"}
    )
    assert result.passed
    assert seen == {}
    assert result.context["_boundary"] == "internal"

def test_evaluator_exception_is_incomplete_not_a_pass():
    harness = ArtifactHarness()
    artifact = harness.create_code_artifact(
        "echo", lambda prompt="": prompt,
        evaluator=lambda inputs, output, context: 1 / 0,
    )
    run = harness.evaluate(artifact, load_eval_dataset("offline", limit=1))
    assert run.rows[0].status == "Incomplete"
    assert not run.rows[0].passed

def test_criteria_only_mutation_is_detected():
    harness = ArtifactHarness()
    first = lambda inputs, output, context: 1.0
    second = lambda inputs, output, context: 0.5
    artifact = harness.create_code_artifact("echo", lambda prompt="": prompt, evaluator=first)
    changed = artifact.with_criteria(evaluator=second)
    assert changed.config == artifact.config
    assert criteria_fingerprint(changed.evaluator, changed.tests, changed.criteria_spec) != artifact.criteria_digest
    assert changed.criteria_version == artifact.criteria_version + 1

def test_remote_failure_metadata_is_explicit(monkeypatch):
    import datasets
    def fail(*args, **kwargs):
        raise OSError("network unavailable")
    monkeypatch.setattr(datasets, "load_dataset", fail)
    dataset = load_eval_dataset("movies", limit=1)
    assert dataset.boundary.dataset_source is DatasetProvenance.FALLBACK
    assert "network unavailable" in dataset.boundary.fallback_reason
    assert dataset.boundary.disclaimer
