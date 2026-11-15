import pytest

from muse_screenplay.generators import Generator, _validate_language
from muse_screenplay.models import MODELS
from muse_screenplay.symbol_registers import SymbolRegister, get_symbol_register, register_symbol_context


def test_registry_never_claims_multilingual_without_evidence():
    for spec in MODELS.values():
        assert spec.languages["verified"] == []
        assert "multilingual" not in spec.languages["declared"]


def test_target_language_is_mandatory_and_validated():
    with pytest.raises(ValueError):
        _validate_language(None)
    with pytest.raises(ValueError):
        _validate_language("")
    assert _validate_language("en") == "en"
    assert _validate_language("zh-Hans") == "zh-Hans"


def test_generator_requires_target_language_before_model_loading():
    generator = Generator()
    with pytest.raises(ValueError, match="target_language is required"):
        generator.generate("INT. ROOM - DAY")


def test_remote_code_policy_is_separate_from_pytorch_safe_load_policy():
    provenance = Generator().provenance()
    assert provenance["pytorch_weights_only"] is True
    assert provenance["trust_remote_code"] is False
    assert provenance["remote_code_policy"] == "disabled"
    assert provenance["use_safetensors"] is True


def test_symbol_register_has_no_cross_cultural_fallback():
    register = SymbolRegister(language="en", cultural_context="test-context", version="1")
    register_symbol_context(register)
    assert get_symbol_register("en", "test-context") is register
    with pytest.raises(LookupError):
        get_symbol_register("fr", "test-context")
