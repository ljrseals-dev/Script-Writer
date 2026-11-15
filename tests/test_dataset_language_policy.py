import pytest

from muse_screenplay.datasets import load_eval_dataset


def test_target_language_is_required_for_every_dataset():
    with pytest.raises(ValueError, match="target_language is required"):
        load_eval_dataset("offline")


def test_offline_dataset_carries_requested_language():
    dataset = load_eval_dataset("offline", limit=1, target_language="fr")
    assert dataset.cases[0].metadata["target_language"] == "fr"


def test_unverified_movie_dataset_field_mapping_fails_to_explicit_fallback():
    dataset = load_eval_dataset("movies", limit=1, target_language="en")
    assert dataset.name == "offline-fallback"
    assert dataset.boundary.dataset_id == "builtin:offline"
    assert "field mapping is unverified" in dataset.boundary.fallback_reason
