"""Sarvam AI client wrapper for Indic translation, speech-to-text, and transliteration."""

import os
import json
import logging
from typing import Optional, Dict, Any, List
import requests

logger = logging.getLogger("osint_fusion.sarvam")

# Sarvam AI API endpoints
SARVAM_BASE_URL = os.getenv("SARVAM_BASE_URL", "https://api.sarvam.ai")

# Mapping internal LanguageCode to Sarvam locale codes
SARVAM_LOCALE_MAP = {
    "bn": "bn-IN",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "mr": "mr-IN",
    "as": "as-IN",
    "en": "en-IN",
}


def _load_dotenv_if_present():
    if "SARVAM_API_KEY" not in os.environ or not os.environ["SARVAM_API_KEY"].strip():
        cur = os.path.dirname(os.path.abspath(__file__))
        for _ in range(4):
            env_file = os.path.join(cur, ".env")
            if os.path.isfile(env_file):
                try:
                    with open(env_file, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith("#") and "=" in line:
                                k, v = line.split("=", 1)
                                if k.strip() == "SARVAM_API_KEY":
                                    os.environ["SARVAM_API_KEY"] = v.strip().strip("'\"")
                    break
                except Exception:
                    pass
            cur = os.path.dirname(cur)


class SarvamAIClient:
    """
    Client for invoking Sarvam AI's Indic models:
    - Translation (Mayura v1)
    - Speech-to-Text (Saaras v1)
    - Transliteration
    - Language Identification
    """

    def __init__(self, api_key: Optional[str] = None):
        _load_dotenv_if_present()
        self.api_key = api_key or os.getenv("SARVAM_API_KEY")

    def is_configured(self) -> bool:
        """Returns True if a Sarvam API key is available."""
        return bool(self.api_key and self.api_key.strip())

    def get_headers(self) -> Dict[str, str]:
        if not self.is_configured():
            raise ValueError(
                "Sarvam API key is missing. Set the SARVAM_API_KEY environment variable "
                "or pass api_key to SarvamAIClient."
            )
        return {
            "api-subscription-key": self.api_key.strip(),
            "Content-Type": "application/json",
        }

    def get_status(self) -> Dict[str, Any]:
        """Returns current configuration status of the Sarvam connector."""
        configured = self.is_configured()
        masked_key = (
            f"{self.api_key[:4]}...{self.api_key[-4:]}"
            if configured and len(self.api_key) > 8
            else ("CONFIGURED" if configured else "NOT_CONFIGURED")
        )
        return {
            "is_configured": configured,
            "masked_key": masked_key,
            "base_url": SARVAM_BASE_URL,
            "models_available": [
                {"name": "mayura:v1", "service": "Text Translation (Indic <-> English)"},
                {"name": "saaras:v1", "service": "Speech-to-Text & Spoken Translation"},
                {"name": "transliterate", "service": "Indic Script-to-Latin Transliteration"},
                {"name": "language-id", "service": "Indic Language Identification"},
            ],
            "supported_locales": list(SARVAM_LOCALE_MAP.values()),
        }

    def translate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "en",
        mode: str = "formal",
    ) -> Optional[Dict[str, Any]]:
        """
        Translates text using Sarvam Mayura translation API.
        Returns dict with translated_text and model metadata, or None if failed/unconfigured.
        """
        if not self.is_configured():
            return None

        src_locale = SARVAM_LOCALE_MAP.get(source_lang, f"{source_lang}-IN")
        tgt_locale = SARVAM_LOCALE_MAP.get(target_lang, "en-IN")

        url = f"{SARVAM_BASE_URL}/translate"
        payload = {
            "input": text,
            "source_language_code": src_locale,
            "target_language_code": tgt_locale,
            "speaker_gender": "Male",
            "mode": mode,
            "model": "mayura:v1",
            "enable_preprocessing": True,
        }

        try:
            resp = requests.post(url, json=payload, headers=self.get_headers(), timeout=30)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    "translated_text": data.get("translated_text", ""),
                    "source_language_code": src_locale,
                    "target_language_code": tgt_locale,
                    "engine": "Sarvam AI (mayura:v1)",
                    "raw_response": data,
                }
            else:
                logger.warning("Sarvam Translation API returned %s: %s", resp.status_code, resp.text)
                return None
        except Exception as exc:
            logger.error("Error calling Sarvam Translation API: %s", exc)
            return None

    def speech_to_text(
        self,
        audio_file_path: str,
        language_code: str = "unknown",
        with_timestamps: bool = True,
    ) -> Optional[Dict[str, Any]]:
        """
        Transcribes audio using Sarvam Saaras Speech-to-Text API.
        """
        if not self.is_configured():
            return None

        if not os.path.exists(audio_file_path):
            logger.error("Audio file not found: %s", audio_file_path)
            return None

        url = f"{SARVAM_BASE_URL}/speech-to-text"
        headers = {"api-subscription-key": self.api_key.strip()}
        lang_locale = SARVAM_LOCALE_MAP.get(language_code, language_code)

        try:
            with open(audio_file_path, "rb") as f:
                files = {"file": (os.path.basename(audio_file_path), f)}
                data = {
                    "model": "saaras:v1",
                    "language_code": lang_locale,
                    "with_timestamps": "true" if with_timestamps else "false",
                }
                resp = requests.post(url, files=files, data=data, headers=headers, timeout=60)
                if resp.status_code == 200:
                    res_json = resp.json()
                    return {
                        "transcript": res_json.get("transcript", ""),
                        "timestamps": res_json.get("timestamps", []),
                        "language_code": res_json.get("language_code", lang_locale),
                        "engine": "Sarvam AI (saaras:v1)",
                        "raw_response": res_json,
                    }
                else:
                    logger.warning("Sarvam Speech-to-Text API returned %s: %s", resp.status_code, resp.text)
                    return None
        except Exception as exc:
            logger.error("Error calling Sarvam Speech-to-Text API: %s", exc)
            return None

    def speech_to_text_translate(
        self,
        audio_file_path: str,
        prompt: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """
        Transcribes spoken Indic audio directly into English text using Sarvam Saaras.
        """
        if not self.is_configured():
            return None

        if not os.path.exists(audio_file_path):
            return None

        url = f"{SARVAM_BASE_URL}/speech-to-text-translate"
        headers = {"api-subscription-key": self.api_key.strip()}

        try:
            with open(audio_file_path, "rb") as f:
                files = {"file": (os.path.basename(audio_file_path), f)}
                data = {"model": "saaras:v1"}
                if prompt:
                    data["prompt"] = prompt
                resp = requests.post(url, files=files, data=data, headers=headers, timeout=60)
                if resp.status_code == 200:
                    res_json = resp.json()
                    return {
                        "english_transcript": res_json.get("transcript", ""),
                        "engine": "Sarvam AI (saaras:v1 - translate)",
                        "raw_response": res_json,
                    }
                else:
                    logger.warning("Sarvam STT-Translate API returned %s: %s", resp.status_code, resp.text)
                    return None
        except Exception as exc:
            logger.error("Error calling Sarvam STT-Translate API: %s", exc)
            return None

    def transliterate(
        self,
        text: str,
        source_lang: str,
        target_lang: str = "en",
    ) -> Optional[str]:
        """
        Transliterates Indic script text into Roman or other Indic script using Sarvam API.
        """
        if not self.is_configured():
            return None

        url = f"{SARVAM_BASE_URL}/transliterate"
        payload = {
            "input": text,
            "source_language_code": SARVAM_LOCALE_MAP.get(source_lang, f"{source_lang}-IN"),
            "target_language_code": SARVAM_LOCALE_MAP.get(target_lang, "en-IN"),
        }

        try:
            resp = requests.post(url, json=payload, headers=self.get_headers(), timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("transliterated_text")
            return None
        except Exception as exc:
            logger.error("Error calling Sarvam Transliterate API: %s", exc)
            return None
