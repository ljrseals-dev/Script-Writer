"""Deterministic heuristic evaluators."""
import math
from .format_check import analyze_script
def _text(x): return x if isinstance(x,str) else str(x or "")
def _clamp(x): return max(0.0,min(1.0,float(x)))
def length_score(inputs,out,trace):
 n=len(_text(out).split());lo=inputs.get("min_words",40);hi=inputs.get("max_words",600)
 if n<=0:return 0.0
 if lo<=n<=hi:return 1.0
 return _clamp(n/lo if n<lo else 1-(n-hi)/(hi*2))
def format_score(inputs,out,trace):return analyze_script(_text(out)).format_score
def dialogue_score(inputs,out,trace):return _clamp(1-abs(analyze_script(_text(out)).dialogue_ratio-.5)*2)
def diversity_score(inputs,out,trace):
 t=_text(out).lower().split();return 0.0 if len(t)<10 else _clamp(len(set(t))/len(t)/.75)
def prompt_overlap_score(inputs,out,trace):
 stop={"the","and","for","with","that","this","from","into","int","ext","day","night"}
 w={x.strip(".,:;!?").lower() for x in str(inputs.get("prompt","")).split()};w={x for x in w if len(x)>3 and x not in stop}
 return .5 if not w else _clamp(sum(x in _text(out).lower() for x in w)/len(w))
def repetition_penalty_score(inputs,out,trace):
 t=_text(out).lower().split()
 if len(t)<10:return 0.0
 g=[tuple(t[i:i+5]) for i in range(len(t)-4)]
 return _clamp(1-(len(g)-len(set(g)))/len(g))
def composite_evaluator(*parts,**named_weights):
 named={"length":length_score,"format":format_score,"dialogue":dialogue_score,"diversity":diversity_score,"overlap":prompt_overlap_score,"repetition":repetition_penalty_score}
 weights=list(parts)
 for name,w in named_weights.items():
  if name not in named:raise KeyError(name)
  weights.append((w,named[name]))
 total=sum(w for w,_ in weights) or 1
 return lambda i,o,t:_clamp(sum(w*f(i,o,t) for w,f in weights)/total)
def default_evaluator(i,o,t):return composite_evaluator(format=.30,length=.20,dialogue=.15,diversity=.15,repetition=.10,overlap=.10)(i,o,t)
def mean(values):
 v=list(values);return sum(v)/len(v) if v else 0.0
def geometric_mean(values):
 v=list(values);return 0.0 if not v else math.exp(sum(math.log(max(x,1e-9)) for x in v)/len(v))
