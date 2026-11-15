from dataclasses import dataclass
from typing import Any,Callable
from .constraints import ConstraintLevel
@dataclass
class TestCase:
 name:str
 predicate:Callable[[Any],bool]
 level:ConstraintLevel=ConstraintLevel.ASSERT
 message:str=""
 def run(self,value):
  try:
   passed=bool(self.predicate(value));msg="" if passed else (self.message or f"{self.name} failed")
  except Exception as exc:passed=False;msg=f"predicate raised: {exc}"
  return TestResult(self.name,passed,self.level,msg)
@dataclass
class TestResult:
 name:str
 passed:bool
 level:ConstraintLevel
 message:str=""
