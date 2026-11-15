from muse_screenplay.format_check import *
def test_headings():
 assert is_scene_heading("INT. COFFEE SHOP - DAY")
 assert is_scene_heading("EXT. ROOFTOP - DAWN")
 assert is_scene_heading("INT./EXT. CAR - CONTINUOUS")
 assert not is_scene_heading("The barista smiles.")
def test_transitions():
 assert is_transition("CUT TO:") and is_transition("FADE OUT.")
 assert not is_transition("He cuts to the left.")
def test_cues():
 assert is_character_cue("SCREENWRITER") and is_parenthetical("(to herself)")
 assert not is_character_cue("Just start with the coffee.")
def test_sample(sample_scene):
 r=analyze_script(sample_scene)
 assert r.scene_headings>=2 and r.character_cues>=2 and r.dialogue_lines>=2
 assert r.transitions>=1 and 0<r.format_score<=1
def test_empty():assert analyze_script("").format_score==0
