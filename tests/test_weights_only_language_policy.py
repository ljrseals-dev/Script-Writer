import sys
import types

import pytest

from muse_screenplay.generators import Generator, _validate_language, torch_load_safe
from muse_screenplay.models import MODELS
from muse_screenplay.symbol_registers import (
    SymbolRegister, get_symbol_register, register_symbol_context,
)


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


def test_torch_load_safe_passes_explicit_weights_only(monkeypatch):
    calls = {}
    fake_torch = types.SimpleNamespace(
        load=lambda path, **kwargs: calls.update({"path": path, **kwargs}) or "weights"
    )
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    assert torch_load_safe("weights.bin") == "weights"
    assert calls == {
        "path": "weights.bin", "map_location": "cpu", "weights_only": True
    }


def test_torch_load_safe_refuses_unsupported_safe_mode(monkeypatch):
    def old_torch_load(path, map_location=None):
        return None
    monkeypatch.setitem(sys.modules, "torch", types.SimpleNamespace(load=old_torch_load))
    with pytest.raises(RuntimeError, match="refusing unsafe .bin loading"):
        torch_load_safe("weights.bin")


def test_model_auto_map_is_rejected_without_remote_code(monkeypatch):
    fake_torch = types.ModuleType("torch")
    fake_transformers = types.ModuleType("transformers")

    class FakeConfig:
        auto_map = {"AutoModel": "modeling_custom.CustomModel"}

    class FakeAutoConfig:
        @staticmethod
        def from_pretrained(*args, **kwargs):
            assert kwargs["trust_remote_code"] is False
            return FakeConfig()

    fake_transformers.AutoConfig = FakeAutoConfig
    fake_transformers.AutoModelForCausalLM = object
    fake_transformers.AutoModelForSeq2SeqLM = object
    fake_transformers.AutoTokenizer = object
    monkeypatch.setitem(sys.modules, "torch", fake_torch)
    monkeypatch.setitem(sys.modules, "transformers", fake_transformers)

    generator = Generator()
    monkeypatch.setattr(generator, "_record_remote_code_rejection", lambda source: None)
    with pytest.raises(RuntimeError, match="requires-remote-code"):
        generator._load()


def test_symbol_register_has_no_cross_cultural_fallback():
    register = SymbolRegister(language="en", cultural_context="test-context", version="1")
    register_symbol_context(register)
    assert get_symbol_register("en", "test-context") is register
    with pytest.raises(LookupError):
        get_symbol_register("fr", "test-context")
