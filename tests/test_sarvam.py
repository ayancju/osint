"""Unit tests for Sarvam AI client wrapper and fallback behaviors."""

import os
import unittest
from osint_fusion.multilingual.sarvam_client import SarvamAIClient, SARVAM_LOCALE_MAP
from osint_fusion.multilingual.audio_stt import AudioSpeechProcessor


class TestSarvamAIClient(unittest.TestCase):

    def test_unconfigured_client_graceful_fallback(self):
        client = SarvamAIClient(api_key=None)
        # Should report not configured
        if "SARVAM_API_KEY" not in os.environ:
            self.assertFalse(client.is_configured())
            status = client.get_status()
            self.assertEqual(status["masked_key"], "NOT_CONFIGURED")
            self.assertIsNone(client.translate("নমস্কার", "bn"))
            self.assertIsNone(client.transliterate("নমস্কার", "bn"))

    def test_configured_client_status(self):
        client = SarvamAIClient(api_key="test-sarvam-key-1234567890")
        self.assertTrue(client.is_configured())
        status = client.get_status()
        self.assertTrue(status["is_configured"])
        self.assertIn("mayura:v1", [m["name"] for m in status["models_available"]])
        self.assertIn("saaras:v1", [m["name"] for m in status["models_available"]])

    def test_locale_mapping(self):
        self.assertEqual(SARVAM_LOCALE_MAP["bn"], "bn-IN")
        self.assertEqual(SARVAM_LOCALE_MAP["hi"], "hi-IN")
        self.assertEqual(SARVAM_LOCALE_MAP["ta"], "ta-IN")
        self.assertEqual(SARVAM_LOCALE_MAP["as"], "as-IN")

    def test_audio_speech_processor_dynamic_disclosure(self):
        # Without key
        orig_key = os.environ.get("SARVAM_API_KEY")
        if "SARVAM_API_KEY" in os.environ:
            del os.environ["SARVAM_API_KEY"]

        caps = AudioSpeechProcessor.inspect_audio_capabilities()
        self.assertFalse(caps["speech_recognition_tool_available"])
        self.assertIn("NOT active", caps["status_message"])

        # With mock key
        os.environ["SARVAM_API_KEY"] = "mock-key-123"
        caps_active = AudioSpeechProcessor.inspect_audio_capabilities()
        self.assertTrue(caps_active["speech_recognition_tool_available"])
        self.assertTrue(caps_active["sarvam_configured"])
        self.assertIn("ACTIVE", caps_active["status_message"])

        # Restore
        if orig_key:
            os.environ["SARVAM_API_KEY"] = orig_key
        else:
            del os.environ["SARVAM_API_KEY"]


if __name__ == "__main__":
    unittest.main()
