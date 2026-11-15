import pytest

from muse_screenplay.datasets import load_eval_dataset


def test_target_language_is_required_for_every_dataset():
    with pytest.raises(ValueError, match="target_language is required"):
        load_eval_dataset("offline")


def test_offline_dataset_carries_requested_language():
    dataset = load_eval_dataset("offline", limit=1, target_language="fr")
    assert dataset.cases[0].metadata["target_language"] == "fr"


def test_movies_dataset_language_and_field_metadata_are_explicit():
    from muse_screenplay.datasets import dataset_catalog
    entry = dataset_catalog()["movies"]
    assert entry["languages"]["declared"] == ["en"]
    assert entry["field_mapping_verified"] is True
    assert "apache-2.0" in entry["license_status"]
