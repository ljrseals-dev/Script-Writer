"""Dependency-free heuristic screenplay format checks."""
import re
from dataclasses import dataclass,field
SCENE_HEADING=re.compile(r"^\\s*(?:INT\\.?/EXT\\.?|INT\\.?|EXT\\.?|I/E)\\b[ .]",re.I)
TRANSITION=re.compile(r"^\\s*(?:CUT TO:|SMASH CUT TO:|MATCH CUT TO:|DISSOLVE TO:|FADE IN:|FADE OUT\\.?|FADE TO BLACK\\.?|JUMP CUT TO:)",re.I)
PARENTHETICAL=re.compile(r"^\\s*\\(.+\\)\\s*$")
CHARACTER_CUE=re.compile(r"^\\s*([A-Z][A-Z0-9 .'-]{0,29})(?:\\s*\\(.*\\))?\\s*:?[ \\t]*$")
SHOT=re.compile(r"^\\s*(?:CLOSE ON|WIDE ON|ANGLE ON|POV|INSERT|AERIAL)\\b",re.I)
def split_lines(text):return [x.rstrip() for x in (text or "").splitlines()]
def is_scene_heading(line):return bool(SCENE_HEADING.match(line)) and any(c.isalpha() for c in line)
def is_transition(line):return bool(TRANSITION.match(line))
def is_parenthetical(line):return bool(PARENTHETICAL.match(line))
def is_character_cue(line):
 s=line.strip();return bool(s and len(s)<=40 and not is_scene_heading(s) and not is_transition(s) and CHARACTER_CUE.match(s))
@dataclass
class ScriptReport:
 line_count:int=0;word_count:int=0;scene_headings:int=0;transitions:int=0;parentheticals:int=0;character_cues:int=0;dialogue_lines:int=0;action_lines:int=0;shots:int=0;characters:list[str]=field(default_factory=list)
 @property
 def dialogue_ratio(self):
  n=self.dialogue_lines+self.action_lines;return self.dialogue_lines/n if n else 0.0
 @property
 def format_score(self):
  if self.word_count<20:return 0.0
  return min(1.0,.35*bool(self.scene_headings)+.25*bool(self.dialogue_lines)+.15*bool(self.character_cues)+.15*bool(self.action_lines)+.10*bool(self.transitions or self.parentheticals or self.shots))
 def to_dict(self):
  d={k:getattr(self,k) for k in ("line_count","word_count","scene_headings","transitions","parentheticals","character_cues","dialogue_lines","action_lines","shots")};d.update(dialogue_ratio=round(self.dialogue_ratio,3),format_score=round(self.format_score,3),characters=self.characters);return d
def analyze_script(text):
 lines=split_lines(text);r=ScriptReport(line_count=len(lines),word_count=len((text or "").split()));chars=set();after=False
 for raw in lines:
  s=raw.strip()
  if not s:after=False;continue
  if is_scene_heading(s):r.scene_headings+=1;after=False
  elif is_transition(s):r.transitions+=1;after=False
  elif is_parenthetical(s):r.parentheticals+=1;after=False
  elif is_character_cue(s):r.character_cues+=1;chars.add(CHARACTER_CUE.match(s).group(1).strip());after=True
  elif SHOT.match(s):r.shots+=1;r.action_lines+=1;after=False
  elif after:r.dialogue_lines+=1;after=False
  elif s.isupper() and len(s.split())<=6:r.shots+=1
  else:r.action_lines+=1;after=False
 r.characters=sorted(chars);return r
