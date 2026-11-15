"""Command-line entry point."""
import argparse,json,sys
from pathlib import Path
from .config import settings
from .datasets import dataset_catalog,load_eval_dataset
from .format_check import analyze_script
from .models import CANDIDATES, MODELS
def _print(data):print(json.dumps(data,indent=2,ensure_ascii=False,default=str))
def cmd_models(a):_print({"generators":{k:v.to_dict() for k,v in MODELS.items()},"candidates":CANDIDATES});return 0
def cmd_datasets(a):_print(dataset_catalog());return 0
def cmd_validate(a):
 text=Path(a.file).read_text(encoding="utf-8") if a.file else sys.stdin.read()
 report=analyze_script(text).to_dict();_print(report);return 0 if report["format_score"]>=a.threshold else 1
def _artifact(a):
 from .harness_artifacts import build_script_artifact
 return build_script_artifact(a.model,max_length=getattr(a,"max_length",None),temperature=getattr(a,"temperature",None),top_p=getattr(a,"top_p",None))
def cmd_generate(a):
 from .harness import ArtifactHarness
 art=_artifact(a);r=ArtifactHarness("muse_cli").execute(art,{"prompt":a.prompt,"target_language":a.target_language})
 if a.json:_print({"artifact":art.to_dict(),"passed":r.passed,"duration_ms":r.duration_ms,"output":r.value,"language_provenance":getattr(art.fn,"_last_language_provenance",None),"error":r.error,"tests":[{"name":t.name,"passed":t.passed,"message":t.message} for t in r.test_results]})
 elif r.error:print(r.error,file=sys.stderr)
 else:print(r.value)
 return 0 if r.passed else 1
def cmd_evaluate(a):
 from .harness import ArtifactHarness
 art=_artifact(a);ds=load_eval_dataset(a.dataset,a.limit,target_language=a.target_language);run=ArtifactHarness("muse_cli").evaluate(art,ds)
 if a.json:_print({"artifact":art.to_dict(),"dataset":ds.name,"mean_score":run.mean_score,"pass_rate":run.pass_rate,"rows":[{"prompt":x.prompt[:120],"score":x.score,"passed":x.passed,"error":x.error,"output":str(x.output)[:400]} for x in run.rows]})
 else:print(f"dataset={ds.name} cases={len(ds)} mean={run.mean_score:.4f} pass_rate={run.pass_rate:.2%}")
 return 0 if run.pass_rate>=a.min_pass_rate else 1
def cmd_optimize(a):
 from .harness import ArtifactHarness
 art=_artifact(a);ds=load_eval_dataset(a.dataset,a.limit,target_language=a.target_language);h=ArtifactHarness("muse_cli");best,run=h.optimize(art,ds,rounds=a.rounds)
 if a.json:_print({"baseline":art.to_dict(),"best":best.to_dict(),"mean_score":run.mean_score,"pass_rate":run.pass_rate,"log":h.log})
 else:print(f"best version={best.version} score={run.mean_score:.4f} pass_rate={run.pass_rate:.2%}")
 return 0
def build_parser():
 p=argparse.ArgumentParser(prog="muse-screenplay");s=p.add_subparsers(dest="command",required=True)
 for name,fn in (("models",cmd_models),("datasets",cmd_datasets)):
  q=s.add_parser(name);q.set_defaults(func=fn)
 q=s.add_parser("validate");q.add_argument("--file");q.add_argument("--stdin",action="store_true");q.add_argument("--threshold",type=float,default=.5);q.set_defaults(func=cmd_validate)
 q=s.add_parser("generate");q.add_argument("--model",default=settings.default_model);q.add_argument("--prompt",required=True);q.add_argument("--target-language",required=True,help="Required BCP-47-style output language tag");q.add_argument("--max-length",type=int,default=settings.max_length);q.add_argument("--temperature",type=float,default=settings.temperature);q.add_argument("--top-p",type=float,default=settings.top_p);q.add_argument("--json",action="store_true");q.set_defaults(func=cmd_generate)
 for name,fn in (("evaluate",cmd_evaluate),("optimize",cmd_optimize)):
  q=s.add_parser(name);q.add_argument("--model",default=settings.default_model);q.add_argument("--dataset",default=settings.default_dataset);q.add_argument("--limit",type=int,default=settings.dataset_limit);q.add_argument("--target-language",required=True,help="Required BCP-47-style target language");q.add_argument("--json",action="store_true")
  if name=="evaluate":q.add_argument("--min-pass-rate",type=float,default=0.0)
  else:q.add_argument("--rounds",type=int,default=3)
  q.set_defaults(func=fn)
 return p
def main(argv=None):
 a=build_parser().parse_args(argv);settings.apply_environment()
 try:return int(a.func(a))
 except (RuntimeError,KeyError,ValueError) as exc:print(f"error: {exc}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
