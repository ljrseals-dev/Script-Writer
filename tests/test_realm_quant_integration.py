import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class RealmQuantChatbotIntegrationTests(unittest.TestCase):
    def test_download_page_has_pinned_fp16_models(self):
        page = (ROOT / "muse_gm" / "static" / "realm_quant_models.html").read_text()
        self.assertIn("encoder_model_fp16.onnx", page)
        self.assertIn("decoder_model_fp16.onnx", page)
        self.assertIn("4b180296388b0cebdca8191db999e87b03cd7a95", page)
        self.assertIn("Adonna Seals", page)
        self.assertIn("does not run ONNX inference", page)

    def test_chatbot_route_and_prompt_reference_codec(self):
        app = (ROOT / "muse_gm" / "app.py").read_text()
        prompt = (ROOT / "muse_gm" / "prompts" / "chatbot_system_prompt.md").read_text()
        self.assertIn('if u.path == "/codec":', app)
        self.assertIn("audio codec", prompt.lower())
        self.assertIn("not a text tokenizer", prompt.lower())
        self.assertIn("Adonna Seals", prompt)

    def test_weights_are_not_auto_downloaded_or_bundled(self):
        page = (ROOT / "muse_gm" / "static" / "realm_quant_models.html").read_text()
        docs = (ROOT / "docs" / "REALM_QUANT_CHATBOT_INTEGRATION.md").read_text()
        self.assertIn("never fetches model weights automatically", page)
        self.assertIn("not copied into this repository", docs)


if __name__ == "__main__":
    unittest.main()
