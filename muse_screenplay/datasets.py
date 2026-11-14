"""Offline-first prompt datasets with optional Hugging Face loading."""
from dataclasses import dataclass
from .harness.dataset import EvalDataset
OFFLINE_CASES=[
 {"prompt":"INT. DINER - NIGHT\n\nA tired waitress wipes the counter. MARCUS stares at a napkin.\n\nMARCUS:","metadata":{"genre":"drama"}},
 {"prompt":"EXT. ROOFTOP - DAWN\n\nTwo strangers sit above the city.\n\nJUNE:","metadata":{"genre":"romance"}},
 {"prompt":"INT. SPACESHIP COCKPIT - CONTINUOUS\n\nAlarms blink red. HAYES grips the yoke.\n\nHAYES:","metadata":{"genre":"sci-fi"}},
 {"prompt":"INT. INTERROGATION ROOM - DAY\n\nA bulb swings. ROSS slides a photograph across the table.\n\nROSS:","metadata":{"genre":"thriller"}},
 {"prompt":"INT. RECORD STORE - AFTERNOON\n\nELI flips through vinyl.\n\nELI:","metadata":{"genre":"comedy"}}]
@dataclass(frozen=True)
class DatasetSpec:
 key:str;hf_id:str;prompt_field:str;expected_field:str|None=None;split:str="train";notes:str=""
DATASETS={"movies":DatasetSpec("movies","IsmaelMousa/movies","Script",notes="Full movie scripts."),
 "moviesum":DatasetSpec("moviesum","rohitsaxena/MovieSum","screenplay","summary",notes="Screenplays and summaries."),
 "imsdb":DatasetSpec("imsdb","aneeshas/imsdb-genre-movie-scripts","script",notes="Genre-labelled scripts.")}
ALIASES={"sample":"offline","movie":"movies","sum":"moviesum","genre":"imsdb"}
def _offline(limit,prompt_words):
 rows=[]
 for c in OFFLINE_CASES[:limit if limit is not None else len(OFFLINE_CASES)]:
  p=c["prompt"];p=" ".join(p.split()[:prompt_words]) if prompt_words else p;rows.append({"prompt":p,"metadata":c["metadata"]})
 return EvalDataset("offline",rows)
def load_eval_dataset(name="offline",limit=5,prompt_chars=1200,prompt_words=None):
 key=ALIASES.get(name.strip().lower(),name.strip().lower())
 if key=="offline":return _offline(limit,prompt_words)
 if key not in DATASETS:raise KeyError(f"Unknown dataset {name!r}")
 try:from datasets import load_dataset
 except ImportError:return _offline(limit,prompt_words)
 spec=DATASETS[key]
 try:
  ds=load_dataset(spec.hf_id,split=spec.split)
  if limit is not None:ds=ds.select(range(min(limit,len(ds))))
  rows=[]
  for row in ds:
   p=str(row.get(spec.prompt_field,"") or "")
   if prompt_words:p=" ".join(p.split()[:prompt_words])
   if prompt_chars:p=p[:prompt_chars]
   expected=(str(row.get(spec.expected_field,"") or "")[:2000] or None) if spec.expected_field else None
   meta={k:row[k] for k in ("genre","genres","title","movie_name") if k in row and row[k] is not None}
   rows.append({"prompt":p,"expected":expected,"metadata":meta})
  return EvalDataset(key,rows)
 except Exception:return _offline(limit,prompt_words)
def dataset_catalog():return {"offline":{"hf_id":None,"notes":f"{len(OFFLINE_CASES)} built-in prompt seeds."},**{k:{"hf_id":v.hf_id,"notes":v.notes} for k,v in DATASETS.items()}}
