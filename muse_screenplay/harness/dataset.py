from dataclasses import dataclass,field
@dataclass
class EvalCase:
 prompt:str
 expected:str|None=None
 metadata:dict=field(default_factory=dict)
 @classmethod
 def coerce(cls,value):
  if isinstance(value,cls):return value
  if isinstance(value,str):return cls(value)
  d=dict(value);p=d.pop("prompt","");e=d.pop("expected",None);m=d.pop("metadata",{}) or d
  return cls(p,e,m)
class EvalDataset:
 def __init__(self,name,cases):self.name=name;self.cases=[EvalCase.coerce(x) for x in cases]
 def __len__(self):return len(self.cases)
 def __iter__(self):return iter(self.cases)
 def __getitem__(self,i):return self.cases[i]
 def __repr__(self):return f"EvalDataset(name={self.name!r}, cases={len(self.cases)})"
