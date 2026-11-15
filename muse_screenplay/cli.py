"""Command-line interface for Muse screenplay drafting."""
import argparse
import json
from .engine import ScriptBrief, generate, write_result
from .models import MODELS

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="muse-screenplay")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("models", help="list supported Hugging Face model IDs")
    draft = sub.add_parser("generate", help="draft a screenplay")
    draft.add_argument("--title", required=True)
    draft.add_argument("--premise", required=True)
    draft.add_argument("--genre", default="historical crime drama")
    draft.add_argument("--period", default="unspecified")
    draft.add_argument("--location", default="unspecified")
    draft.add_argument("--language", default="en")
    draft.add_argument("--characters", default="")
    draft.add_argument("--research-notes", default="")
    draft.add_argument("--constraints", default="")
    draft.add_argument("--model", default="script-bart", choices=tuple(MODELS))
    draft.add_argument("--revision", default="main")
    draft.add_argument("--seed", type=int, default=17)
    draft.add_argument("--max-new-tokens", type=int, default=1200)
    draft.add_argument("--download", action="store_true", help="allow Hugging Face downloads; default is cache-only")
    draft.add_argument("--out", default="runs/draft.json")
    args = parser.parse_args(argv)
    if args.command == "models":
        for key, spec in MODELS.items():
            print(f"{key}\t{spec.repo_id}\t{spec.description}")
        return 0
    brief = ScriptBrief(title=args.title, premise=args.premise, genre=args.genre,
        period=args.period, location=args.location, language=args.language,
        characters=args.characters, research_notes=args.research_notes, constraints=args.constraints)
    result = generate(brief, model_key=args.model, seed=args.seed,
        max_new_tokens=args.max_new_tokens, download=args.download, revision=args.revision)
    path = write_result(result, args.out)
    print(json.dumps({"output": str(path), "model": result["model"],
        "prompt_sha256": result["prompt_sha256"]}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
