"""Multilingual script and language detection engine for Indian languages and English."""

import re
from typing import Dict, List, Tuple
from ..models.source import LanguageCode


# Unicode ranges for Indic scripts (excluding shared punctuation \u0964\u0965)
SCRIPT_PATTERNS = {
    # Eastern Nagari letters & vowel signs (Bengali and Assamese)
    "bengali_assamese": re.compile(r'[\u0980-\u09E5\u09E8-\u09FF]'),
    # Devanagari letters & vowel signs (excluding \u0964 and \u0965 which are shared danda full-stops)
    "devanagari": re.compile(r'[\u0900-\u0963\u0966-\u097F]'),
    # Tamil
    "tamil": re.compile(r'[\u0B80-\u0BFF]'),
    # Telugu
    "telugu": re.compile(r'[\u0C00-\u0C7F]'),
    # Latin
    "latin": re.compile(r'[a-zA-Z]'),
}

# Distinguishing markers between Assamese and Bengali (both use Eastern Nagari script)
# Assamese uniquely uses 'ৰ' (U+09F0) and 'ৱ' (U+09F1)
ASSAMESE_UNIQUE_CHARS = re.compile(r'[\u09F0\u09F1]')

# Distinguishing markers for Marathi in Devanagari (e.g. ळ U+0933)
MARATHI_UNIQUE_CHARS = re.compile(r'[\u0933]')


class LanguageDetector:
    """Detects languages, scripts, and code-mixing in intelligence documents."""

    @staticmethod
    def analyze_text(text: str) -> Dict[str, any]:
        """Analyzes text to detect primary language, detected scripts, and code-mixing."""
        if not text or not text.strip():
            return {
                "primary_language": LanguageCode.UNKNOWN,
                "language_name": "Unknown",
                "is_mixed": False,
                "detected_languages": [],
                "script_distribution": {},
                "code_mixed_rationale": "Empty or whitespace text."
            }

        total_alpha = 0
        counts = {}
        for script_name, pattern in SCRIPT_PATTERNS.items():
            matches = len(pattern.findall(text))
            counts[script_name] = matches
            total_alpha += matches

        if total_alpha == 0:
            return {
                "primary_language": LanguageCode.UNKNOWN,
                "language_name": "Symbolic / Numeric",
                "is_mixed": False,
                "detected_languages": [],
                "script_distribution": counts,
                "code_mixed_rationale": "No alphabetic characters found."
            }

        distribution = {k: v / total_alpha for k, v in counts.items() if v > 0}
        
        detected_languages: List[str] = []
        is_mixed = False

        if counts["bengali_assamese"] > 0:
            bengali_ra_count = len(re.findall(r'[\u09B0]', text))
            assamese_ra_count = len(re.findall(r'[\u09F0\u09F1]', text))
            if assamese_ra_count > bengali_ra_count:
                detected_languages.append("Assamese (অসমীয়া)")
            else:
                detected_languages.append("Bengali (বাংলা)")
                if assamese_ra_count > 0:
                    detected_languages.append("Assamese (অসমীয়া) [Loan/Placename]")

        if counts["devanagari"] > 0:
            if MARATHI_UNIQUE_CHARS.search(text):
                detected_languages.append("Marathi (मराठी)")
            else:
                detected_languages.append("Hindi (हिन्दी)")

        if counts["tamil"] > 0:
            detected_languages.append("Tamil (தமிழ்)")

        if counts["telugu"] > 0:
            detected_languages.append("Telugu (తెలుగు)")

        if counts["latin"] > 0:
            detected_languages.append("English (Latin Script)")

        # Determine dominant script by maximum character count
        dominant_script = max(counts, key=counts.get)

        if dominant_script == "bengali_assamese":
            bengali_ra_count = len(re.findall(r'[\u09B0]', text))
            assamese_ra_count = len(re.findall(r'[\u09F0\u09F1]', text))
            if assamese_ra_count > bengali_ra_count:
                primary_lang = LanguageCode.ASSAMESE
                primary_name = "Assamese"
            else:
                primary_lang = LanguageCode.BENGALI
                primary_name = "Bengali"
        elif dominant_script == "devanagari":
            if MARATHI_UNIQUE_CHARS.search(text):
                primary_lang = LanguageCode.MARATHI
                primary_name = "Marathi"
            else:
                primary_lang = LanguageCode.HINDI
                primary_name = "Hindi"
        elif dominant_script == "tamil":
            primary_lang = LanguageCode.TAMIL
            primary_name = "Tamil"
        elif dominant_script == "telugu":
            primary_lang = LanguageCode.TELUGU
            primary_name = "Telugu"
        else:
            primary_lang = LanguageCode.ENGLISH
            primary_name = "English"

        # Determine code-mixing: if non-dominant script accounts for > 8% of characters
        active_scripts = [s for s, ratio in distribution.items() if ratio > 0.08]
        if len(active_scripts) > 1:
            is_mixed = True
            primary_name = f"Mixed ({primary_name} + Latin/Regional)"

        return {
            "primary_language": primary_lang,
            "language_name": primary_name,
            "is_mixed": is_mixed,
            "detected_languages": detected_languages,
            "script_distribution": distribution,
            "code_mixed_rationale": (
                f"Contains multi-script segments: {', '.join(detected_languages)}"
                if is_mixed
                else f"Predominantly single-script: {primary_name}"
            )
        }
