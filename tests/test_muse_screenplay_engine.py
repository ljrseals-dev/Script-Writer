import unittest
from muse_screenplay.engine import ScriptBrief, STAGES, compile_prompt, prompt_digest

class MuseScreenplayEngineTests(unittest.TestCase):
    def test_all_nine_stages_are_in_fixed_order(self):
        prompt = compile_prompt(ScriptBrief(title="Test", premise="A family faces a choice."))
        positions = [prompt.index(stage.upper().replace("_", " ")) for stage in STAGES]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(len(STAGES), 9)

    def test_prompt_and_digest_are_stable(self):
        brief = ScriptBrief(title="Test", premise="A family faces a choice.")
        first, second = compile_prompt(brief), compile_prompt(brief)
        self.assertEqual(first, second)
        self.assertEqual(prompt_digest(first), prompt_digest(second))

    def test_missing_brief_fails_closed(self):
        with self.assertRaises(ValueError):
            compile_prompt(ScriptBrief(title="", premise=""))

if __name__ == "__main__":
    unittest.main()
