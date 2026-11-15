"""Lazy, weights-only Transformers loader with explicit language provenance."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
import os
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
    """Best-effort detector; absence or uncertainty is explicit."""
    try:
        from langdetect import DetectorFactory, detect_langs
        DetectorFactory.seed = 0
        if not text.strip():
            return "unverified"
        guesses = detect_langs(text)
        if not guesses or guesses[0].prob < 0.85:
            return "unverified"
        return guesses[0].lang
    except Exception:
        return "unverified"


def _validate_language(target_language):
    if not isinstance(target_language, str) or not re.fullmatch(
        r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", target_language
    ):
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

    @staticmethod
    def _hash_weight_file(path):
        digest = hashlib.sha256()
        with open(path, "rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return {
            "filename": os.path.basename(path),
            "sha256": digest.hexdigest(),
            "bytes": os.path.getsize(path),
        }

    def _observed_safetensors_hashes(self):
        """Record observed bytes for the loaded Safetensors artifact(s), not source authenticity."""
        try:
            from huggingface_hub import hf_hub_download
            from huggingface_hub.errors import EntryNotFoundError
            try:
                path = hf_hub_download(
                    self.spec.hf_id, filename="model.safetensors",
                    revision=self.spec.revision,
                )
                return [self._hash_weight_file(path)]
            except EntryNotFoundError:
                index_path = hf_hub_download(
                    self.spec.hf_id, filename="model.safetensors.index.json",
                    revision=self.spec.revision,
                )
                with open(index_path, encoding="utf-8") as stream:
                    index = json.load(stream)
                shards = sorted(set(index.get("weight_map", {}).values()))
                return [
                    self._hash_weight_file(hf_hub_download(
                        self.spec.hf_id, filename=shard, revision=self.spec.revision
                    ))
                    for shard in shards
                ]
        except Exception as exc:
            return [{"hash_status": "unavailable", "reason": str(exc)}]

    def _record_remote_code_rejection(self, source):
        from .governance import GovernanceLedger
        ledger = GovernanceLedger(
            os.environ.get("MUSE_PROVENANCE_LEDGER", ".muse/ledger.jsonl")
        )
        ledger.append(
            "model_load_rejected_remote_code",
            self.spec.key,
            datetime.now(timezone.utc).isoformat(),
            {
                "architecture_status": "requires-remote-code",
                "load_status": "not-loaded",
                "remote_code_policy": "disabled",
                "trust_remote_code": False,
                "rejection_source": source,
            },
        )

    def _load(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import (
                AutoConfig, AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
            )
        except ImportError as exc:
            raise RuntimeError(
                'transformers is not installed or PyTorch is unavailable; run pip install -e ".[models]"'
            ) from exc

        settings.apply_environment()
        common = {
            "revision": self.spec.revision,
            "trust_remote_code": False,
            "local_files_only": False,
        }
        common = {key: value for key, value in common.items() if value is not None}
        config = AutoConfig.from_pretrained(self.spec.hf_id, **common)
        if getattr(config, "auto_map", None):
            self._record_remote_code_rejection("model_config.auto_map")
            raise RuntimeError(
                f"architecture: requires-remote-code — not loaded under weights-only policy ({self.spec.hf_id})"
            )
        # Tokenizer custom code is a separate execution surface from model architecture.
        try:
            from huggingface_hub import hf_hub_download
            from huggingface_hub.errors import EntryNotFoundError
            tokenizer_config_path = hf_hub_download(
                self.spec.hf_id, filename="tokenizer_config.json",
                revision=self.spec.revision,
            )
            with open(tokenizer_config_path, encoding="utf-8") as stream:
                tokenizer_config = json.load(stream)
        except EntryNotFoundError:
            tokenizer_config = {}
        if tokenizer_config.get("auto_map"):
            self._record_remote_code_rejection("tokenizer_config.auto_map")
            raise RuntimeError(
                f"architecture: requires-remote-code — tokenizer custom code not loaded ({self.spec.hf_id})"
            )
        self._tokenizer = AutoTokenizer.from_pretrained(
            self.spec.hf_id, trust_remote_code=False, **{
                key: value for key, value in common.items() if key != "trust_remote_code"
            }
        )
        model_cls = (
            AutoModelForSeq2SeqLM
            if self.task in {"text2text-generation", "summarization"}
            else AutoModelForCausalLM
        )
        try:
            self._model = model_cls.from_pretrained(
                self.spec.hf_id,
                config=config,
                use_safetensors=True,
                trust_remote_code=False,
                revision=self.spec.revision,
            )
            weight_format = "safetensors"
            self._weight_artifacts = self._observed_safetensors_hashes()
        except (OSError, ValueError) as safe_error:
            # No implicit Transformers pickle fallback: .bin is an explicit safe path.
            try:
                from huggingface_hub import hf_hub_download

                weight_path = hf_hub_download(
                    self.spec.hf_id,
                    filename="pytorch_model.bin",
                    revision=self.spec.revision,
                )
                state = torch_load_safe(weight_path)
                self._model = model_cls.from_config(config)
                if isinstance(state, dict) and isinstance(state.get("state_dict"), dict):
                    state = state["state_dict"]
                self._model.load_state_dict(state, strict=True)
                weight_format = "pytorch-bin-weights-only"
                self._weight_artifacts = [self._hash_weight_file(weight_path)]
            except Exception as safe_load_error:
                raise RuntimeError(
                    "No loadable safetensors artifact was available and the explicit "
                    f"weights_only=True .bin path failed: {safe_load_error}"
                ) from safe_error

        self._device = settings.resolve_device() if self.device == "auto" else self.device
        self._torch = torch
        self._model.to(self._device)
        self._model.eval()
        self._weight_format = weight_format

    @property
    def pipeline(self):
        """Compatibility property returning this safe generator, never an HF pipeline."""
        self._load()
        return self

    def generate(self, prompt, *, target_language=None, **overrides):
        target = _validate_language(target_language)
        self._load()
        input_language = _detect_language(prompt)
        language_mismatch = (
            None
            if input_language == "unverified"
            else input_language != target.split("-")[0].lower()
        )
        # A mismatch is diagnostic only; the original prompt is passed unchanged.
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self._device) for key, value in inputs.items()}
        kwargs = self.generation.to_kwargs()
        kwargs.update({key: value for key, value in overrides.items() if value is not None})
        if kwargs.get("max_new_tokens") is not None:
            kwargs.pop("max_length", None)
        with self._torch.inference_mode():
            output = self._model.generate(**inputs, **kwargs)
        generated_text = self._tokenizer.decode(output[0], skip_special_tokens=True).strip()
        if self.task == "text-generation" and generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip() or generated_text

        generated_in = _detect_language(generated_text)
        self._last_language_provenance = {
            "requested": target,
            "generated_in": generated_in,
            "input_language": input_language,
            "language_mismatch": language_mismatch,
        }
        # Persist each actual generation's language record; a broken ledger blocks silent runs.
        from .governance import GovernanceLedger

        ledger = GovernanceLedger(
            os.environ.get("MUSE_PROVENANCE_LEDGER", ".muse/ledger.jsonl")
        )
        ledger.append(
            "generation_language_provenance",
            self.spec.key,
            datetime.now(timezone.utc).isoformat(),
            {
                **self._last_language_provenance,
                "weight_artifacts": getattr(self, "_weight_artifacts", []),
                "requested_attribution": [
                    {"person": "Angela Seals", "contribution": "weights-integration innovation"}
                ],
            },
        )
        return generated_text

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
            "legacy_bin_policy": "explicit torch_load(map_location='cpu', weights_only=True) only",
            "architecture_policy": "built-in Transformers architecture only; auto_map rejected",
            "language_detection": "langdetect seeded; confidence >= 0.85 else unverified",
            "language": {
                "declared": self.spec.languages,
                "tokenizer_languages": self.spec.tokenizer_languages,
                "last_run": getattr(self, "_last_language_provenance", None),
            },
            "weight_format": getattr(self, "_weight_format", "not-loaded"),
            "weight_artifacts": getattr(self, "_weight_artifacts", []),
        }
