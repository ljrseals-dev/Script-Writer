from muse_screenplay.evaluators import *
def test_length():
 assert length_score({},"one two",{})<1
 assert length_score({}," ".join(["word"]*100),{})==1
def test_scores(sample_scene):
 assert format_score({},sample_scene,{})>.5
 assert 0<=default_evaluator({"prompt":"INT. COFFEE SHOP - DAY"},sample_scene,{})<=1
def test_diversity():
 assert diversity_score({},"short",{})==0
 assert diversity_score({}," ".join(f"word{i}" for i in range(100)),{})>.9
def test_composite():
 assert 0<=composite_evaluator(format=.5,length=.5)({},"INT. ROOM - DAY "+("word "*30),{})<=1
