from muse_screenplay.governance import (
    AuditEvent, CRITERIA_FINGERPRINT_LIMITATIONS,
)
from muse_screenplay.harness import ArtifactHarness

def test_criteria_only_change_increments_criteria_version():
    harness = ArtifactHarness()
    artifact = harness.create_code_artifact(
        "a", lambda prompt="": prompt,
        evaluator=lambda inputs, output, context: 1.0,
        criteria_spec={"rubric": "v1"},
    )
    changed = artifact.with_criteria(criteria_spec={"rubric": "v2"})
    assert changed.config == artifact.config
    assert changed.criteria_version == artifact.criteria_version + 1
    assert changed.criteria_digest != artifact.criteria_digest
    assert changed.mutation_audit

def test_callable_fingerprint_limitations_are_disclosed():
    assert "closure values" in CRITERIA_FINGERPRINT_LIMITATIONS
    event = AuditEvent("mutation", "a", "criteria changed")
    assert event.limitations
