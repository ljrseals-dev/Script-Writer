from muse_screenplay.governance import (
    DatasetProvenance, Provenance, sha256_bytes, sha256_value, verify_sha256,
)

def test_hash_is_deterministic_and_verifiable():
    digest = sha256_bytes(b"evidence")
    assert verify_sha256(b"evidence", digest)
    assert not verify_sha256(b"changed", digest)
    assert sha256_value({"b": 2, "a": 1}) == sha256_value({"a": 1, "b": 2})

def test_remote_offline_fallback_are_distinct():
    assert len({DatasetProvenance.REMOTE, DatasetProvenance.OFFLINE,
                DatasetProvenance.FALLBACK}) == 3
    assert Provenance("dataset", "remote").source == "dataset"
