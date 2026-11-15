import pytest
from muse_screenplay.generators import GenerationConfig,Generator
from muse_screenplay.models import get_model,resolve_model
def test_registry():
 assert get_model("bart").key=="script-bart"
 assert get_model("gpt2-screenplay").task=="text-generation"
 assert resolve_model("org/custom").hf_id=="org/custom"
def test_config():
 kw=GenerationConfig(max_new_tokens=64).to_kwargs()
 assert "max_new_tokens" in kw and "max_length" not in kw and "repetition_penalty" not in kw
def test_missing_transformers(monkeypatch):
 import builtins
 original=builtins.__import__
 def fake(name,*a,**kw):
  if name=="transformers":raise ImportError("mock")
  return original(name,*a,**kw)
 monkeypatch.setattr(builtins,"__import__",fake)
 with pytest.raises(RuntimeError,match="transformers is not installed"):_=Generator().pipeline
