import pytest

from muse_screenplay.datasets import load_eval_dataset


def test_dataset_inspection_does_not_require_generation_language():
    dataset = load_eval_dataset("offline", limit=1)
    assert len(dataset) == 1
    assert "target_language" not in dataset.cases[0].metadata


def test_offline_dataset_carries_requested_language():
    dataset = load_eval_dataset("offline", limit=1, target_language="fr")
    assert dataset.cases[0].metadata["target_language"] == "fr"


def test_movies_dataset_language_and_field_metadata_are_explicit():
    from muse_screenplay.datasets import dataset_catalog
    entry = dataset_catalog()["movies"]
    assert entry["languages"]["declared"] == ["en"]
    assert entry["field_mapping_verified"] is True
    assert "apache-2.0" in entry["license_status"]
