"""Run the critique/mutate/evaluate loop."""
import argparse
from muse_screenplay.datasets import load_eval_dataset
from muse_screenplay.harness import ArtifactHarness
from muse_screenplay.harness_artifacts import build_script_artifact
def main():
 p=argparse.ArgumentParser();p.add_argument("--model",default="script-bart");p.add_argument("--dataset",default="offline");p.add_argument("--limit",type=int,default=4);p.add_argument("--rounds",type=int,default=3);a=p.parse_args()
 h=ArtifactHarness("example");best,run=h.optimize(build_script_artifact(a.model),load_eval_dataset(a.dataset,a.limit),rounds=a.rounds);print(best.to_dict());print(run.mean_score,run.pass_rate);return 0
if __name__=="__main__":raise SystemExit(main())
