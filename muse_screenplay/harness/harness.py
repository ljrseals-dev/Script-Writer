"""Self-contained Artifact Harness: execution, tests, evaluation and mutation."""
import time,traceback
from dataclasses import dataclass,field,replace
from typing import Any,Callable
from .constraints import ConstraintLevel
from .tests import TestCase,TestResult
def _identity(i,o,t):return 1.0 if o not in (None,"") else 0.0
@dataclass
class ExecutionResult:
 artifact:str;version:int;inputs:dict;outputs:dict;value:Any
 test_results:list[TestResult]=field(default_factory=list);duration_ms:float=0.0;error:str|None=None
 @property
 def passed(self):return self.error is None and all(x.passed for x in self.test_results if x.level is ConstraintLevel.ASSERT)
@dataclass
class EvalRow:
 prompt:str;output:Any;score:float;passed:bool;error:str|None=None
@dataclass
class EvalRun:
 artifact:str;version:int;dataset:str;rows:list[EvalRow]=field(default_factory=list)
 @property
 def scores(self):return [r.score for r in self.rows]
 @property
 def mean_score(self):return sum(self.scores)/len(self.rows) if self.rows else 0.0
 @property
 def pass_rate(self):return sum(r.passed for r in self.rows)/len(self.rows) if self.rows else 0.0
@dataclass
class Artifact:
 name:str;fn:Callable[...,Any];interface:str="kwargs -> value";evaluator:Callable=_identity
 tests:list[TestCase]=field(default_factory=list);config:dict=field(default_factory=dict);provenance:dict=field(default_factory=dict)
 version:int=1;history:list[dict]=field(default_factory=list)
 def with_config(self,**kw):return replace(self,config={**self.config,**kw},version=self.version+1,history=[*self.history,{"config":dict(self.config)}])
 def to_dict(self):return {"name":self.name,"interface":self.interface,"version":self.version,"config":self.config,"provenance":self.provenance,"tests":[{"name":t.name,"level":t.level.value,"message":t.message} for t in self.tests]}
class ArtifactHarness:
 def __init__(self,name="harness"):self.name=name;self.log=[]
 def create_code_artifact(self,name,fn,interface="kwargs -> value",evaluator=None,tests=None,config=None,provenance=None):
  return Artifact(name,fn,interface,evaluator or _identity,list(tests or []),dict(config or {}),dict(provenance or {}))
 def execute(self,artifact,inputs=None):
  merged={**artifact.config,**(inputs or {})};start=time.perf_counter();value=None;error=None
  try:value=artifact.fn(**merged)
  except Exception:error=traceback.format_exc(limit=3)
  ms=(time.perf_counter()-start)*1000;tests=[t.run(value) for t in artifact.tests] if error is None else []
  result=ExecutionResult(artifact.name,artifact.version,merged,{"output":value},value,tests,ms,error)
  self.log.append({"event":"execute","artifact":artifact.name,"version":artifact.version,"passed":result.passed,"duration_ms":round(ms,2)})
  return result
 def evaluate(self,artifact,dataset,max_samples=None):
  from .dataset import EvalDataset
  run=EvalRun(artifact.name,artifact.version,dataset.name);cases=dataset.cases if max_samples is None else dataset.cases[:max_samples]
  for c in cases:
   r=self.execute(artifact,{"prompt":c.prompt,**c.metadata})
   if r.error or not r.passed:run.rows.append(EvalRow(c.prompt,r.value,0.0,False,(r.error or "test failure").strip().splitlines()[-1]));continue
   try:s=max(0.0,min(1.0,float(artifact.evaluator(r.inputs,r.value,{"duration_ms":r.duration_ms,"config":artifact.config}))))
   except Exception as exc:run.rows.append(EvalRow(c.prompt,r.value,0.0,False,str(exc)));continue
   run.rows.append(EvalRow(c.prompt,r.value,s,True))
  self.log.append({"event":"evaluate","artifact":artifact.name,"dataset":dataset.name,"mean_score":run.mean_score,"pass_rate":run.pass_rate})
  return run
 def critique(self,run,samples=3):
  bad=[r for r in run.rows if not r.passed];rank=sorted(run.rows,key=lambda r:r.score)
  return {"artifact":run.artifact,"version":run.version,"dataset":run.dataset,"mean_score":run.mean_score,"pass_rate":run.pass_rate,"failure_count":len(bad),"failure_reasons":sorted({r.error or "unknown" for r in bad}),"weakest_samples":[{"prompt":r.prompt,"score":r.score,"output":str(r.output)[:400]} for r in rank[:samples]]}
 def default_mutator(self,artifact,critique):
  c=dict(artifact.config);low=critique.get("mean_score",0)<.6
  c["temperature"]=round(min(1.2,c.get("temperature",.9)+(.05 if low else -.05)),3)
  c["top_p"]=round(min(.99,max(.7,c.get("top_p",.95)+(.02 if low else -.02))),3)
  if low:c["max_length"]=int(c.get("max_length",256)*1.25)
  return artifact.with_config(**c)
 def optimize(self,artifact,train_data,mutator=None,rounds=3,validation_data=None):
  mutate=mutator or self.default_mutator;val=validation_data or train_data;best=artifact;best_run=self.evaluate(artifact,val);current=artifact
  for i in range(rounds):
   candidate=mutate(current,self.critique(self.evaluate(current,train_data)))
   if candidate is current or candidate.config==current.config:break
   trial=self.evaluate(candidate,val);self.log.append({"event":"optimize_round","round":i,"candidate":candidate.version,"candidate_score":trial.mean_score})
   if trial.mean_score>best_run.mean_score:best,best_run,current=candidate,trial,candidate
   else:break
  return best,best_run
 def compose(self,artifacts,name=None,evaluator=None,tests=None):
  stages=list(artifacts)
  if not stages:raise ValueError("compose() requires at least one artifact")
  def run(prompt="",**kw):
   value=prompt
   for stage in stages:
    r=self.execute(stage,{"prompt":value,**kw})
    if not r.passed:raise RuntimeError(f"stage {stage.name!r} failed: {r.error or r.test_results}")
    value=r.value
   return str(value)
  return self.create_code_artifact(name or "pipeline_"+"_".join(x.name for x in stages),run,"prompt -> script",evaluator or stages[-1].evaluator,tests,provenance={"stages":[x.name for x in stages]})
