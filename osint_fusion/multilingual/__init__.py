"""Multilingual processing package for OSINT Fusion Workbench."""

from .detector import LanguageDetector
from .transliteration import TransliterationEngine, indic_to_roman, phonetic_key, string_similarity
from .translation import TranslationManager
from .audio_stt import AudioSpeechProcessor
from .sarvam_client import SarvamAIClient

__all__ = [
    "LanguageDetector",
    "TransliterationEngine",
    "indic_to_roman",
    "phonetic_key",
    "string_similarity",
    "TranslationManager",
    "AudioSpeechProcessor",
    "SarvamAIClient",
]
