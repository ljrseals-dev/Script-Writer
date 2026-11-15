from muse_screenplay.governance import (
    ArtifactRecord, Contribution, CreditRecord, MutationRecord, Relationship,
    GovernanceStatus,
)

def test_relationship_and_status_vocabularies_are_explicit():
    assert Relationship.IMPLEMENTS.value == "implements"
    assert Relationship.CHALLENGES.value == "challenges"
    assert GovernanceStatus.INCOMPLETE.value == "Incomplete"

def test_requested_credits_are_separate_from_evidenced_contributions():
    record = CreditRecord(
        requested_credits=("A",),
        evidenced_contributions=(Contribution("B", "implemented test harness", "Inferred"),),
    )
    assert record.requested_credits == ("A",)
    assert record.evidenced_contributions[0].person == "B"

def test_artifact_relationship_is_not_assumed():
    record = ArtifactRecord("x", "concept")
    assert record.relationship is Relationship.UNKNOWN
