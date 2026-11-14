import unittest
from muse_core.muse_bridge import consult, symbolic_reading, theme_prompt

class MuseBridgeTests(unittest.TestCase):
    def test_nine_stage_prompts_exist(self):
        keys = ["ordinary_world", "inciting_incident", "rising_action", "first_climax", "fall", "dark_night", "second_climax", "falling_action", "resolution"]
        for key in keys:
            self.assertTrue(theme_prompt(key, "en")["prompts"])
    def test_multilingual_prompt_and_fallback(self):
        self.assertEqual(theme_prompt("ordinary_world", "zh-Hans")["language"], "zh-Hans")
        self.assertEqual(theme_prompt("ordinary_world", "xx")["language"], "en")
    def test_symbol_mapping_preserves_base_meaning(self):
        value = symbolic_reading("symbols", "crown")
        self.assertIn("authority", value["muse_default"])
        self.assertIn("boss", value["gangster_manga"])
    def test_consult_is_sidecar(self):
        result = consult("fall", "es", [("symbols", "wound")])
        self.assertFalse(result["core_modified"])
        self.assertEqual(result["stage"]["language"], "es")
        self.assertEqual(len(result["symbolic_readings"]), 1)

if __name__ == "__main__":
    unittest.main()
