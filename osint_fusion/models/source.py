"""Source data models for OSINT Fusion Workbench.
Preserves complete provenance, original script/text, translation, and metadata.
"""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import datetime


class SourceType(str, Enum):
    NEWS_ARTICLE = "news_article"
    OFFICIAL_STATEMENT = "official_statement"
    POLICE_REPORT = "police_report"
    COURT_DOCUMENT = "court_document"
    AUDIO_BROADCAST = "audio_broadcast"
    INVESTIGATIVE_REPORT = "investigative_report"
    COMMERCE_REGISTRY = "commerce_registry"
    SECONDARY_AGGREGATOR = "secondary_aggregator"
    ANALYST_REPORT = "analyst_report"


class LanguageCode(str, Enum):
    BENGALI = "bn"
    HINDI = "hi"
    ASSAMESE = "as"
    TAMIL = "ta"
    TELUGU = "te"
    MARATHI = "mr"
    ENGLISH = "en"
    MIXED = "mixed"
    UNKNOWN = "und"


class AudioMetadata(BaseModel):
    is_audio: bool = False
    duration_seconds: Optional[float] = None
    sample_rate_hz: Optional[int] = None
    channel_info: Optional[str] = None
    has_timestamps: bool = True
    transcription_engine: Optional[str] = None
    uncertain_segments_count: int = 0
    analyst_authorization_ref: Optional[str] = None


class Source(BaseModel):
    id: str = Field(..., description="Unique Source ID, e.g. SRC-001")
    title: str = Field(..., description="Headline or document title")
    source_org: str = Field(..., description="Publishing organization, agency, or outlet")
    source_type: SourceType = Field(default=SourceType.NEWS_ARTICLE)
    original_url: Optional[str] = None
    filename: Optional[str] = None
    publication_date: Optional[str] = Field(None, description="ISO date YYYY-MM-DD or unconfirmed date string")
    ingestion_date: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    original_language: LanguageCode = LanguageCode.ENGLISH
    original_language_name: str = "English"
    is_mixed_language: bool = False
    languages_detected: List[str] = Field(default_factory=list)
    
    # Text preservation
    original_text: str = Field(..., description="Full original verbatim text or transcript")
    english_translation: Optional[str] = Field(None, description="English translation for cross-source comparison")
    translation_status: str = Field(default="ORIGINAL_OR_NOT_REQUIRED", description="e.g. MACHINE_TRANSLATED, HUMAN_VERIFIED")
    
    # Provenance details
    page_numbers: Optional[str] = None
    paragraph_reference: Optional[str] = None
    audio_timestamps: Optional[List[Dict[str, Any]]] = None
    audio_metadata: Optional[AudioMetadata] = None
    
    # Integrity and metadata flags
    is_primary_source: bool = True
    derived_from_source_id: Optional[str] = None
    missing_metadata_flags: List[str] = Field(default_factory=list)
    incomplete_document_flag: bool = False
    transcription_uncertainty_flag: bool = False
    possible_duplicate_flag: bool = False
    
    # Reliability assessment
    source_reliability_score: float = Field(default=0.8, ge=0.0, le=1.0, description="Heuristic reliability [0.0 - 1.0]")
    reliability_notes: Optional[str] = None
