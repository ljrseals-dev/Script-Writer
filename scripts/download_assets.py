"""Pre-cache registered models and datasets."""
import argparse
from muse_screenplay.config import settings
from muse_screenplay.models import MODELS
from muse_screenplay.datasets import DATASETS
def main():
 p=argparse.ArgumentParser();p.add_argument("--models",nargs="*",default=[]);p.add_argument("--datasets",nargs="*",default=[]);a=p.parse_args();settings.apply_environment()
 if a.models:
  from transformers import pipeline
  for k in (list(MODELS) if a.models==["all"] else a.models):pipeline(MODELS[k].task,model=MODELS[k].hf_id)
 if a.datasets:
  from datasets import load_dataset
  for k in (list(DATASETS) if a.datasets==["all"] else a.datasets):load_dataset(DATASETS[k].hf_id,split=DATASETS[k].split)
 if not a.models and not a.datasets:p.print_help()
 return 0
if __name__=="__main__":raise SystemExit(main())
