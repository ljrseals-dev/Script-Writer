import pytest
from muse_screenplay.datasets import load_eval_dataset
from muse_screenplay.governance import (
    DatasetProvenance, EvalBoundary, assert_no_offline_disguise,
)
from muse_screenplay.harness import ArtifactHarness

def test_explicit_offline_dataset_is_labelled():
    dataset = load_eval_dataset("offline", limit=1)
    assert dataset.boundary.dataset_source is DatasetProvenance.OFFLINE

def test_fallback_requires_reason_and_disclaimer():
    with pytest.raises(ValueError):
        assert_no_offline_disguise(EvalBoundary(dataset_source=DatasetProvenance.FALLBACK))

def test_evaluator_rejects_disguised_fallback():
    dataset = load_eval_dataset("offline", limit=1)
    dataset.boundary = EvalBoundary(dataset_source=DatasetProvenance.FALLBACK)
    artifact = ArtifactHarness().create_code_artifact("x", lambda prompt="": prompt)
    with pytest.raises(ValueError):
        ArtifactHarness().evaluate(artifact, dataset)
