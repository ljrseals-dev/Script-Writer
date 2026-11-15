"""Run a theme consultation: python -m muse_core --stage ordinary_world --language en."""
import argparse, json
from .muse_bridge import consult
p=argparse.ArgumentParser()
p.add_argument("--stage", required=True)
p.add_argument("--language", default="en")
p.add_argument("--symbol", action="append", default=[], help="register:symbol; repeatable")
a=p.parse_args()
pairs=[]
for item in a.symbol:
    if ":" not in item: p.error("--symbol must be register:symbol")
    pairs.append(tuple(item.split(":",1)))
print(json.dumps(consult(a.stage,a.language,pairs),ensure_ascii=False,indent=2))
