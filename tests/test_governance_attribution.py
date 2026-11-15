from muse_screenplay.governance import separate_credits
from muse_screenplay.harness_artifacts import _normalize_attribution

def test_requested_and_evidenced_credits_remain_separate():
    result = separate_credits(["Requested"], [{"person": "Contributor", "work": "weights"}])
    value = result.as_dict()
    assert value["requested_credits"] == ["Requested"]
    assert value["evidenced_contributions"][0]["person"] == "Contributor"

def test_build_time_attribution_defaults_to_unknown_not_inference():
    value = _normalize_attribution(None)
    assert value["status"] == "Unknown"
    assert value["requested_credits"] == []
    assert value["evidenced_contributions"] == []

def test_invalid_attribution_shape_is_rejected():
    try:
        _normalize_attribution({"requested_credits": ["A"], "evidenced_contributions": ["B"]})
    except ValueError:
        return
    raise AssertionError("string contribution should be rejected")
