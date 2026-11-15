"""Generate a sample scene; requires optional model dependencies."""
import argparse
from muse_screenplay.harness import ArtifactHarness
from muse_screenplay.harness_artifacts import build_script_artifact
PROMPT="INT. COFFEE SHOP - DAY\n\nRain streaks the windows. A SCREENWRITER sits alone.\n\nSCREENWRITER:"
def main():
 p=argparse.ArgumentParser();p.add_argument("--model",default="script-bart");p.add_argument("--prompt",default=PROMPT);a=p.parse_args()
 art=build_script_artifact(a.model);r=ArtifactHarness("example").execute(art,{"prompt":a.prompt});print(r.value or r.error);return 0 if r.passed else 1
if __name__=="__main__":raise SystemExit(main())
