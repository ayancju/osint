"""Audio transcription and speech analysis interface with timestamping and limitation disclosures."""

import re
from typing import Dict, List, Any, Optional
from ..models.source import AudioMetadata
from .sarvam_client import SarvamAIClient


TIMESTAMP_PATTERN = re.compile(r'\[(\d{2}:\d{2})\]\s*(.*)')
UNCERTAIN_PATTERN = re.compile(r'\[uncertain:\s*([^\]]+)\]')


class AudioSpeechProcessor:
    """
    Processes speech transcripts, preserves timestamped segments,
    and enforces strict transparency about speech engine availability.
    """

    @staticmethod
    def inspect_audio_capabilities() -> Dict[str, Any]:
        """Returns disclosure of available acoustic and speech-to-text processing engines."""
        sarvam = SarvamAIClient()
        sarvam_active = sarvam.is_configured()

        if sarvam_active:
            return {
                "speech_recognition_tool_available": True,
                "sarvam_configured": True,
                "active_engine": "Sarvam AI Saaras:v1 Indic Speech-to-Text",
                "status_message": (
                    "Sarvam AI Saaras:v1 Speech-to-Text connector is ACTIVE and configured with live API credentials. "
                    "Supports acoustic decoding and direct spoken Indic translation with timestamp tracking."
                ),
                "next_practical_steps": [
                    "1. Upload or pass raw WAV/MP3 broadcast recordings to /api/audio/transcribe.",
                    "2. Audio will be processed through Sarvam Saaras:v1 speech-to-text pipeline.",
                    "3. Timestamps and transcription confidence scores are automatically retained.",
                    "4. Chain-of-custody recording log maintained for lawful radio monitoring."
                ]
            }

        return {
            "speech_recognition_tool_available": False,
            "sarvam_configured": False,
            "active_engine": "Simulated Benchmark Certified Transcripts",
            "status_message": (
                "Native acoustic audio decoding API (Sarvam AI Saaras:v1 / Whisper) is currently NOT active "
                "(SARVAM_API_KEY environment variable is not set). "
                "Transcripts are currently imported via analyst-certified text with timestamp metadata."
            ),
            "next_practical_steps": [
                "1. To activate live acoustic transcription, set the environment variable: export SARVAM_API_KEY='your-key'.",
                "2. Transcripts currently provide verified broadcast text with [MM:SS] timestamps.",
                "3. Uncertain or inaudible words are explicitly tagged as [uncertain: 'word'] or [inaudible].",
                "4. Maintain chain-of-custody recording logs for authorized radio interception."
            ]
        }

    @staticmethod
    def parse_timestamped_transcript(transcript_text: str) -> List[Dict[str, Any]]:
        """Parses [MM:SS] markers from an authorized radio broadcast transcript."""
        segments = []
        lines = transcript_text.splitlines()
        for idx, line in enumerate(lines):
            line_str = line.strip()
            if not line_str:
                continue
            match = TIMESTAMP_PATTERN.match(line_str)
            if match:
                timecode, content = match.groups()
                # Check for uncertain markers
                uncertainties = UNCERTAIN_PATTERN.findall(content)
                segments.append({
                    "segment_index": len(segments) + 1,
                    "timestamp": timecode,
                    "text": content,
                    "uncertain_words": uncertainties,
                    "has_uncertainty": len(uncertainties) > 0,
                    "has_ambient_noise": "[ambient" in content.lower()
                })
            else:
                # Sub-segment or headline
                if "[uncertain:" in line_str:
                    uncertainties = UNCERTAIN_PATTERN.findall(line_str)
                    segments.append({
                        "segment_index": len(segments) + 1,
                        "timestamp": "N/A",
                        "text": line_str,
                        "uncertain_words": uncertainties,
                        "has_uncertainty": True,
                        "has_ambient_noise": False
                    })
        return segments

    @staticmethod
    def extract_uncertainty_count(transcript_text: str) -> int:
        """Counts explicitly tagged uncertain words or inaudible sections."""
        uncertain_matches = UNCERTAIN_PATTERN.findall(transcript_text)
        inaudible_count = transcript_text.lower().count("[inaudible]")
        return len(uncertain_matches) + inaudible_count
