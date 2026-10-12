"""Event data models with precision-bounded geolocation and uncertainty handling."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class VerificationStatus(str, Enum):
    UNREVIEWED = "unreviewed"
    NEEDS_VERIFICATION = "needs_verification"
    CORROBORATED = "corroborated"
    CONTRADICTED = "contradicted"
    ANALYST_APPROVED = "analyst_approved"
    REJECTED = "rejected"


class TemporalStatus(str, Enum):
    CONFIRMED_DATE = "CONFIRMED_DATE"
    REPORTED_DATE = "REPORTED_DATE"
    ESTIMATED_RANGE = "ESTIMATED_RANGE"
    HISTORICAL_ANTECEDENT = "HISTORICAL_ANTECEDENT"
    UNCERTAIN = "UNCERTAIN"


class EventExcerpt(BaseModel):
    source_id: str
    excerpt_text: str
    original_language_excerpt: Optional[str] = None
    publication_date: Optional[str] = None
    page_or_timestamp: Optional[str] = None


class EventRecord(BaseModel):
    id: str = Field(..., description="Unique Event ID, e.g. EVT-001")
    title: str = Field(..., description="Short headline for timeline display")
    description: str = Field(..., description="Detailed description grounded strictly in evidence")
    
    # Temporal footprint
    event_date: Optional[str] = Field(None, description="ISO date or approximate date, e.g. 2026-10-08")
    event_time: Optional[str] = Field(None, description="Reported time if explicitly documented")
    date_end: Optional[str] = Field(None, description="End date if a range")
    temporal_status: TemporalStatus = TemporalStatus.REPORTED_DATE
    date_uncertainty: Optional[str] = Field(None, description="Explicit statement of temporal uncertainty or +/- window")
    
    # Location (bounded precision)
    location_name: str = Field(..., description="Location name as documented")
    location_precision: str = Field(default="district_level", description="country_level, state_level, district_level, town_level, pinpoint_checkpoint")
    location_notes: Optional[str] = None
    
    # Participants
    reported_participants: List[str] = Field(default_factory=list, description="Entity IDs or names of persons involved")
    reported_organizations: List[str] = Field(default_factory=list, description="Entity IDs or names of organizations")
    
    # Provenance
    source_ids: List[str] = Field(default_factory=list)
    supporting_excerpts: List[EventExcerpt] = Field(default_factory=list)
    
    # Inconsistencies and Status
    contradictory_accounts: List[str] = Field(default_factory=list, description="Documented disagreements between sources")
    missing_information: List[str] = Field(default_factory=list, description="Identified informational gaps")
    verification_status: VerificationStatus = VerificationStatus.UNREVIEWED
    confidence: str = Field(default="MODERATE", description="LOW, MODERATE, HIGH")
