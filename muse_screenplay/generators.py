"""Lazy, weights-only Transformers loader with explicit language provenance."""
from dataclasses import asdict, dataclass, field
import re
from typing import Any

from .config import settings
from .models import resolve_model


def torch_load_safe(path: str):
    """The only permitted pickle-based weight load; requires PyTorch safe mode."""
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("PyTorch is required to load .bin weights") from exc
    try:
        return torch.load(path, map_location="cpu", weights_only=True)
    except TypeError as exc:
        raise RuntimeError(
            "Installed PyTorch lacks torch.load(weights_only=True); refusing unsafe .bin loading"
        ) from exc


def _detect_language(text: str) -> str:
    """Best-effort language detector; absence or uncertainty is explicit."""
    try:
        from langdetect import detect
        return detect(text) if text.strip() else "unverified"
    except Exception:
        return "unverified"


def _validate_language(target_language):
    if not isinstance(target_language, str) or not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", target_language):
        raise ValueError("target_language is required and must be a BCP-47-style language tag")
    return target_language


@dataclass
class GenerationConfig:
    max_length: int = 256
    max_new_tokens: int | None = None
    temperature: float = .9
    top_p: float = .95
    do_sample: bool = True
    num_return_sequences: int = 1
    repetition_penalty: float | None = None

    def to_kwargs(self):
        data = {key: value for key, value in asdict(self).items() if value is not None}
        if data.get("max_new_tokens") is not None:
            data.pop("max_length", None)
        return data


@dataclass
class Generator:
    model_key: str = "script-bart"
    device: str | int = "auto"
    generation: GenerationConfig = field(default_factory=GenerationConfig)
    _spec: Any = None
    _model: Any = None
    _tokenizer: Any = None
    _torch: Any = None

    def __post_init__(self):
        self._spec = resolve_model(self.model_key)
        if self._spec.family in {"gpt2", "minigpt", "custom"} and self.generation.max_new_tokens is None:
            self.generation.max_new_tokens = self.generation.max_length

    @property
    def spec(self):
        return self._spec

    @property
    def task(self):
        return self.spec.task

    def _load(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import (
                AutoConfig, AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
            )
        except ImportError as exc:
            raise RuntimeError('PyTorch and transformers are required; run pip install -e ".[models]"') from exc

        settings.apply_environment()
        common = {
            "revision": self.spec.revision,
            "trust_remote_code": False,
            "local_files_only": False,
        }
        common = {key: value for key, value in common.items() if value is not None}
        config = AutoConfig.from_pretrained(self.spec.hf_id, **common)
        auto_map = getattr(config, "auto_map", None)
        if auto_map:
            raise RuntimeError(
                f"architecture: requires-remote-code — not loaded under weights-only policy ({self.spec.hf_id})"
            )
        self._tokenizer = AutoTokenizer.from_pretrained(self.spec.hf_id, **common)
        model_cls = AutoModelForSeq2SeqLM if self.task in {"text2text-generation", "summarization"} else AutoModelForCausalLM
        try:
            self._model = model_cls.from_pretrained(
                self.spec.hf_id, config=config, use_safetensors=True,
                trust_remote_code=False, revision=self.spec.revision,
            )
            weight_format = "safetensors"
        except (OSError, ValueError) as safe_error:
            # Explicit legacy .bin path only. No implicit Transformers pickle fallback.
            try:
                from huggingface_hub import hf_hub_download
                import os
                weight_path = hf_hub_download(
                    self.spec.hf_id, filename="pytorch_model.bin",
                    revision=self.spec.revision,
                )
                state = torch_load_safe(weight_path)
                self._model = model_cls.from_config(config)
                if isinstance(state, dict) and "state_dict" in state and isinstance(state["state_dict"], dict):
                    state = state["state_dict"]
                self._model.load_state_dict(state, strict=True)
                weight_format = "pytorch-bin-weights-only"
            except Exception as unsafe_or_missing:
                raise RuntimeError(
                    "No loadable safetensors artifact was available and the explicit "
                    f"weights_only=True .bin path failed: {unsafe_or_missing}"
                ) from safe_error
        device = settings.resolve_device() if self.device == "auto" else self.device
        self._torch = torch
        self._model.to(device)
        self._model.eval()
        self._device = device
        self._weight_format = weight_format

    @property
    def pipeline(self):
        # Compatibility property: return this generator, not an unsafe HF pipeline.
        self._load()
        return self

    def generate(self, prompt, *, target_language=None, **overrides):
        target = _validate_language(target_language)
        self._load()
        input_language = _detect_language(prompt)
        language_mismatch = None if input_language == "unverified" else input_language != target.split("-")[0].lower()
        if language_mismatch:
            # Record only; never translate or rewrite the user's prompt.
            pass
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self._device) for key, value in inputs.items()}
        kwargs = self.generation.to_kwargs()
        kwargs.update({key: value for key, value in overrides.items() if value is not None})
        kwargs.pop("max_length", None) if kwargs.get("max_new_tokens") is not None else None
        with self._torch.inference_mode():
            output = self._model.generate(**inputs, **kwargs)
        text = self._tokenizer.decode(output[0], skip_special_tokens=True).strip()
        if self.task == "text-generation" and text.startswith(prompt):
            text = text[len(prompt):].strip() or text
        generated_in = _detect_language(text)
        self._last_language_provenance = {
            "requested": target,
            "generated_in": generated_in,
            "input_language": input_language,
            "language_mismatch": language_mismatch,
        }
        return text

    def provenance(self):
        return {
            "model_key": self.spec.key,
            "hf_id": self.spec.hf_id,
            "task": self.task,
            "family": self.spec.family,
            "generation": self.generation.to_kwargs(),
            "pytorch_weights_only": True,
            "remote_code_policy": "disabled",
            "trust_remote_code": False,
            "use_safetensors": True,
            "legacy_bin_policy": "explicit torch_load(weights_only=True) only",
            "language": {
                "declared": self.spec.languages,
                "tokenizer_languages": self.spec.tokenizer_languages,
                "last_run": getattr(self, "_last_language_provenance", None),
            },
            "weight_format": getattr(self, "_weight_format", "not-loaded"),
        }
