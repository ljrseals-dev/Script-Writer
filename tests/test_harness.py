import pytest
from muse_screenplay.harness import *
def test_execute():
 h=ArtifactHarness();a=h.create_code_artifact("echo",lambda prompt="":prompt.upper());r=h.execute(a,{"prompt":"hi"})
 assert r.passed and r.value=="HI" and r.duration_ms>=0
def test_error():
 h=ArtifactHarness();a=h.create_code_artifact("bad",lambda:1/0);assert not h.execute(a).passed
def test_constraints():
 h=ArtifactHarness();a=h.create_code_artifact("warn",lambda:"x",tests=[TestCase("w",lambda x:False,ConstraintLevel.WARN)])
 assert h.execute(a).passed
 b=h.create_code_artifact("assert",lambda:"x",tests=[TestCase("a",lambda x:False)]);assert not h.execute(b).passed
def test_dataset_and_critique():
 h=ArtifactHarness();a=h.create_code_artifact("echo",lambda prompt="":prompt,evaluator=lambda i,o,t:1.0)
 run=h.evaluate(a,EvalDataset("d",[{"prompt":"a"},{"prompt":"b"}]));assert run.mean_score==pytest.approx(1)
 assert h.critique(run)["pass_rate"]==1
def test_optimize_and_compose():
 h=ArtifactHarness()
 a=h.create_code_artifact("opt",lambda prompt="",temperature=.1:"good "*int(temperature*100),evaluator=lambda i,o,t:min(1,len(o.split())/50),config={"temperature":.1})
 best,run=h.optimize(a,EvalDataset("d",[{"prompt":"a"}]),mutator=lambda x,c:x.with_config(temperature=x.config["temperature"]+.2),rounds=3)
 assert best.version>1
 b=h.create_code_artifact("b",lambda prompt="":prompt+"B");pipe=h.compose([b]);assert h.execute(pipe,{"prompt":"x"}).value=="xB"
