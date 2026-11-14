"""Stable adapter for the bundled harness implementation."""
def load_harness(name="muse_screenplay_harness"):
 from .harness import ArtifactHarness
 return ArtifactHarness(name)
def load_symbols():
 from . import ArtifactHarness,ConstraintLevel,EvalDataset,TestCase
 return {"ArtifactHarness":ArtifactHarness,"ConstraintLevel":ConstraintLevel,"EvalDataset":EvalDataset,"TestCase":TestCase,"external":False}
