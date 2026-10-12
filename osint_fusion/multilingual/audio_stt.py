"""Audio transcription and speech analysis interface with timestamping and limitation disclosures."""

import re
from typing import Dict, List, Any, Optional
from ..models.source import AudioMetadata


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
        return {
            "speech_recognition_tool_available": False,
            "external_whisper_configured": False,
            "status_message": (
                "Native acoustic audio decoding and automated speech-to-text API (e.g. Whisper / Sarvam Audio API) "
                "is currently not configured with live hardware microphones or direct cloud STT API credentials. "
                "Transcripts must be imported with analyst certification and timestamp metadata."
            ),
            "next_practical_steps": [
                "1. Provide verified broadcast audio transcript in text format with [MM:SS] timestamps.",
                "2. Mark uncertain or inaudible words explicitly as [uncertain: 'word'] or [inaudible].",
                "3. Configure an authorized Speech API key (e.g. Sarvam AI / OpenAI / Whisper local) in osint_fusion.config.",
                "4. Maintain chain-of-custody recording log for lawful radio interception."
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
