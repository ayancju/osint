"""Entity models with conservative resolution and evidence provenance."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class EntityType(str, Enum):
    PERSON = "PERSON"
    ORGANIZATION = "ORGANIZATION"
    LOCATION = "LOCATION"
    EVENT = "EVENT"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    OBJECT_CONSIGNMENT = "OBJECT_CONSIGNMENT"


class InvolvementType(str, Enum):
    MENTIONED_ONLY = "MENTIONED_ONLY"
    REPORTED_PARTICIPANT = "REPORTED_PARTICIPANT"
    CONFIRMED_ACTOR = "CONFIRMED_ACTOR"
    OFFICIAL_RESPONDENT = "OFFICIAL_RESPONDENT"
    WITNESS = "WITNESS"


class EntityQuoteReference(BaseModel):
    source_id: str
    quote_text: str
    quote_original_language: Optional[str] = None
    page_or_para: Optional[str] = None
    audio_timestamp: Optional[str] = None
    involvement: InvolvementType = InvolvementType.MENTIONED_ONLY


class EntityResolutionStatus(str, Enum):
    DISTINCT = "DISTINCT"
    CANDIDATE_MERGE = "CANDIDATE_MERGE"
    MERGED = "MERGED"
    AMBIGUOUS_UNRESOLVED = "AMBIGUOUS_UNRESOLVED"
    ANALYST_DISAMBIGUATED = "ANALYST_DISAMBIGUATED"


class Entity(BaseModel):
    id: str = Field(..., description="Unique Entity ID, e.g. ENT-001")
    canonical_name: str = Field(..., description="Standardized canonical name for indexing")
    entity_type: EntityType = Field(..., description="Entity classification")
    
    # Multilingual representations
    original_script_names: Dict[str, str] = Field(default_factory=dict, description="e.g. {'bn': 'সুব্রত মুখার্জী', 'hi': 'सुब्रतो मुखर्जी'}")
    alternative_spellings: List[str] = Field(default_factory=list, description="Transliterations, aliases, acronyms")
    
    # Temporal footprint
    first_observed_date: Optional[str] = None
    last_observed_date: Optional[str] = None
    
    # Provenance and citations
    references: List[EntityQuoteReference] = Field(default_factory=list)
    source_ids: List[str] = Field(default_factory=list)
    
    # Confidence and Resolution
    confidence: str = Field(default="MODERATE", description="LOW, MODERATE, HIGH")
    resolution_status: EntityResolutionStatus = Field(default=EntityResolutionStatus.DISTINCT)
    unresolved_ambiguities: List[str] = Field(default_factory=list)
    disambiguation_notes: Optional[str] = None
    
    # Distinguish mention vs verified involvement
    verified_involvement: bool = False
    involvement_roles: List[InvolvementType] = Field(default_factory=list)
