"""Composable screenplay pipeline interface."""
from dataclasses import dataclass,field
from .format_check import analyze_script
from .harness import Artifact,ArtifactHarness,EvalDataset
@dataclass
class PipelineResult:
 prompt:str;script:str;report:dict;score:float|None=None;stages:dict=field(default_factory=dict)
class ScreenplayPipeline:
 def __init__(self,artifact:Artifact,harness:ArtifactHarness|None=None):
  self.harness=harness or ArtifactHarness("muse_screenplay_pipeline");self.artifact=artifact
 def run(self,prompt,score=True):
  r=self.harness.execute(self.artifact,{"prompt":prompt});script=str(r.value or "")
  result=PipelineResult(prompt,script,analyze_script(script).to_dict(),stages={"passed":r.passed,"duration_ms":round(r.duration_ms,2),"tests":{t.name:t.passed for t in r.test_results},"error":r.error})
  if score and r.passed:result.score=self.artifact.evaluator({"prompt":prompt},script,{"artifact":self.artifact.name})
  return result
 def evaluate(self,dataset:EvalDataset):return self.harness.evaluate(self.artifact,dataset)
def build_genre_conditioned_prompt(prompt,genre,tone=None):
 return f"[GENRE: {genre.upper()}]"+(f" [TONE: {tone.upper()}]" if tone else "")+"\n\n"+prompt
def build_screenplay_pipeline(model_key=None,*,genre=None,tone=None):
 from .harness_artifacts import build_script_artifact
 from .evaluators import composite_evaluator
 artifact=build_script_artifact(model_key)
 if genre:
  base=artifact.fn
  artifact.fn=lambda prompt="",**kw:base(prompt=build_genre_conditioned_prompt(prompt,genre,tone),**kw)
  artifact.evaluator=composite_evaluator(format=.35,length=.2,dialogue=.15,diversity=.15,repetition=.15)
  artifact.provenance={**artifact.provenance,"genre":genre,"tone":tone}
 return ScreenplayPipeline(artifact)
