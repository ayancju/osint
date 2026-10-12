"""Unit tests for multilingual processing, language detection, and transliteration."""

import unittest
from osint_fusion.multilingual.detector import LanguageDetector
from osint_fusion.multilingual.transliteration import (
    TransliterationEngine,
    indic_to_roman,
    phonetic_key,
    string_similarity,
)
from osint_fusion.models.source import LanguageCode


class TestMultilingualProcessing(unittest.TestCase):

    def test_bengali_detection(self):
        text = "শিলিগুড়ি ফুলবাড়ি চেকপোস্ট করিডোরে লরি আটক করা হয়।"
        res = LanguageDetector.analyze_text(text)
        self.assertEqual(res["primary_language"], LanguageCode.BENGALI)
        self.assertIn("Bengali (বাংলা)", res["detected_languages"])

    def test_hindi_detection(self):
        text = "पश्चिम बंगाल पुलिस विज्ञप्ति दिनांक ०८ अक्टूबर २०२६।"
        res = LanguageDetector.analyze_text(text)
        self.assertEqual(res["primary_language"], LanguageCode.HINDI)
        self.assertIn("Hindi (हिन्दी)", res["detected_languages"])

    def test_assamese_unique_character_detection(self):
        # Assamese uniquely has 'ৰ' (U+09F0) and 'ৱ' (U+09F1)
        text = "ধুবুৰী ব্ৰহ্মপুত্ৰ ঘাটত নদীপথেৰে অস্বাভাৱিক সামগ্ৰী পৰিবহণৰ তথ্য।"
        res = LanguageDetector.analyze_text(text)
        self.assertEqual(res["primary_language"], LanguageCode.ASSAMESE)
        self.assertIn("Assamese (অসমীয়া)", res["detected_languages"])

    def test_tamil_detection(self):
        text = "சென்னை துறைமுக வர்த்தக அறிக்கை மற்றும் சரக்கு கையாளுதல்."
        res = LanguageDetector.analyze_text(text)
        self.assertEqual(res["primary_language"], LanguageCode.TAMIL)

    def test_code_mixed_detection(self):
        text = "FIR filed at Siliguri PS regarding তল্লাশি অভিযান near ফুলবাড়ি border checkpost."
        res = LanguageDetector.analyze_text(text)
        self.assertTrue(res["is_mixed"])
        self.assertIn("Bengali (বাংলা)", res["detected_languages"])
        self.assertIn("English (Latin Script)", res["detected_languages"])

    def test_transliteration_match_subrata_mukherjee(self):
        match, score, reason = TransliterationEngine.match_entity_name(
            "সুব্রত মুখার্জী", "Subrata Mukherjee"
        )
        self.assertTrue(match)
        self.assertGreaterEqual(score, 0.8)

    def test_transliteration_match_hindi_subroto(self):
        match, score, reason = TransliterationEngine.match_entity_name(
            "सुब्रतो मुखर्जी", "Subrata Mukherjee"
        )
        self.assertTrue(match)
        self.assertGreaterEqual(score, 0.8)

    def test_phonetic_key_consistency(self):
        k1 = phonetic_key("Subrata")
        k2 = phonetic_key("Subroto")
        # Both share root s-b-r-t
        self.assertEqual(k1, k2)


if __name__ == "__main__":
    unittest.main()
