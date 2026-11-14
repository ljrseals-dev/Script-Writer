"""Build generation artifacts with tests and model provenance."""
from functools import lru_cache
from .config import settings
from .evaluators import default_evaluator
from .format_check import analyze_script
from .generators import GenerationConfig,Generator
from .harness import ConstraintLevel,TestCase,load_harness
@lru_cache(maxsize=8)
def _generator(key,length,temp,top_p):
 return Generator(key,generation=GenerationConfig(max_length=length,temperature=temp,top_p=top_p))
def script_tests():
 return [TestCase("non_empty_output",lambda x:isinstance(x,str) and bool(x.strip()),ConstraintLevel.ASSERT,"empty output"),
 TestCase("min_words",lambda x:len(str(x).split())>=15,ConstraintLevel.WARN,"output shorter than 15 words"),
 TestCase("screenplay_structure",lambda x:bool(analyze_script(str(x)).scene_headings or analyze_script(str(x)).dialogue_lines),ConstraintLevel.WARN,"no scene heading or dialogue")]
def build_script_artifact(model_key=None,*,max_length=None,temperature=None,top_p=None,name=None):
 key=model_key or settings.default_model;length=max_length or settings.max_length
 temp=settings.temperature if temperature is None else temperature;p=settings.top_p if top_p is None else top_p
 def generate(prompt="",**kw):
  gen=_generator(key,length,temp,p);overrides={k:v for k,v in kw.items() if k in GenerationConfig.__dataclass_fields__}
  return gen.generate(prompt,**overrides)
 gen=_generator(key,length,temp,p)
 return load_harness().create_code_artifact(name or f"script_generator[{key}]",generate,"prompt: str -> script: str",
  default_evaluator,script_tests(),{"temperature":temp,"top_p":p,"max_length":length},gen.provenance())
def build_summary_artifact(model_id="sshleifer/distilbart-cnn-12-6"):
 def summarize(prompt="",max_length=130,min_length=30):
  from transformers import pipeline
  settings.apply_environment()
  pipe=pipeline("summarization",model=model_id,device=settings.resolve_device(),token=settings.hf_token)
  return str(pipe(prompt[:3000],max_length=max_length,min_length=min_length,do_sample=False)[0]["summary_text"]).strip()
 return load_harness().create_code_artifact("script_summarizer",summarize,"prompt -> summary",
  tests=[TestCase("non_empty_summary",lambda x:len(str(x).split())>=5)],provenance={"hf_id":model_id,"task":"summarization"})
def build_default_pipeline(model_key=None):
 h=load_harness();gen=build_script_artifact(model_key)
 gate=h.create_code_artifact("format_gate",lambda prompt:prompt,"script -> script",
  tests=[TestCase("scene_heading",lambda x:analyze_script(str(x)).scene_headings>0,ConstraintLevel.WARN)])
 return h.compose([gen,gate],name="default_pipeline")
