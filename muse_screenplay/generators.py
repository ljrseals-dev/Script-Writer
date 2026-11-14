"""Lazy Transformers-backed screenplay generators."""
from dataclasses import asdict,dataclass,field
from typing import Any
from .config import settings
from .models import resolve_model
@dataclass
class GenerationConfig:
    max_length:int=256
    max_new_tokens:int|None=None
    temperature:float=.9
    top_p:float=.95
    do_sample:bool=True
    num_return_sequences:int=1
    repetition_penalty:float|None=None
    def to_kwargs(self):
        d={k:v for k,v in asdict(self).items() if v is not None}
        if d.get("max_new_tokens") is not None:d.pop("max_length",None)
        return d
@dataclass
class Generator:
    model_key:str="script-bart"
    device:str|int="auto"
    generation:GenerationConfig=field(default_factory=GenerationConfig)
    _spec:Any=None
    _pipeline:Any=None
    def __post_init__(self):
        self._spec=resolve_model(self.model_key)
        if self._spec.family in {"gpt2","minigpt","custom"} and self.generation.max_new_tokens is None:self.generation.max_new_tokens=self.generation.max_length
    @property
    def spec(self):return self._spec
    @property
    def task(self):return self.spec.task
    @property
    def pipeline(self):
        if self._pipeline is None:
            try:from transformers import pipeline
            except ImportError as exc:raise RuntimeError('transformers is not installed; run pip install -e ".[models]"') from exc
            settings.apply_environment(); device=settings.resolve_device() if self.device=="auto" else self.device
            self._pipeline=pipeline(self.task,model=self.spec.hf_id,device=device,token=settings.hf_token)
        return self._pipeline
    def generate(self,prompt,**overrides):
        kw=self.generation.to_kwargs();kw.update({k:v for k,v in overrides.items() if v is not None})
        out=self.pipeline(prompt,**kw)
        if not out:return ""
        item=out[0]
        for key in ("generated_text","summary_text","translation_text"):
            if isinstance(item,dict) and key in item:
                text=str(item[key]).strip()
                if self.task=="text-generation" and text.startswith(prompt):return text[len(prompt):].strip() or text
                return text
        return str(item).strip()
    def provenance(self):return {"model_key":self.spec.key,"hf_id":self.spec.hf_id,"task":self.task,"family":self.spec.family,"generation":self.generation.to_kwargs()}
