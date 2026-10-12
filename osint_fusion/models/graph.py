"""Knowledge graph models with edge-level provenance, verification status, and multi-format export."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .event import VerificationStatus


class EdgeType(str, Enum):
    AFFILIATED_WITH = "affiliated_with"
    EMPLOYED_BY = "employed_by"
    OPERATES_IN = "operates_in"
    ISSUED_STATEMENT_ABOUT = "issued_statement_about"
    REPORTED_AT = "reported_at"
    MENTIONS = "mentions"
    REPORTS_EVENT = "reports_event"
    CORROBORATES = "corroborates"
    CONTRADICTS = "contradicts"
    TRANSSHIPPED_TO = "transshipped_to"
    COMMUNICATED_WITH = "communicated_with"
    INFERRED_POSSIBLE_LINK = "inferred_possible_link"


class GraphNode(BaseModel):
    id: str = Field(..., description="Unique ID matching entity_id, event_id, or source_id")
    label: str = Field(..., description="Display label")
    node_type: str = Field(..., description="PERSON, ORGANIZATION, LOCATION, EVENT, SOURCE, INFRASTRUCTURE, OBJECT")
    original_language_label: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: str = "MODERATE"
    verification_status: VerificationStatus = VerificationStatus.UNREVIEWED


class GraphEdge(BaseModel):
    id: str = Field(..., description="Unique edge identifier, e.g. EDG-001")
    source_node_id: str
    target_node_id: str
    relationship_type: EdgeType
    label: str = Field(..., description="Human-readable edge predicate")
    
    # Evidence & Provenance
    is_direct_evidence: bool = Field(True, description="True if explicitly stated in source; False if inferred")
    source_ids: List[str] = Field(default_factory=list)
    supporting_excerpts: List[str] = Field(default_factory=list)
    
    # Confidence and Review
    confidence: str = Field(default="MODERATE", description="LOW, MODERATE, HIGH")
    verification_status: VerificationStatus = VerificationStatus.UNREVIEWED
    analyst_notes: Optional[str] = None
    flags: List[str] = Field(default_factory=list)


class KnowledgeGraph(BaseModel):
    nodes: List[GraphNode] = Field(default_factory=list)
    edges: List[GraphEdge] = Field(default_factory=list)
    unresolved_matches: List[Dict[str, Any]] = Field(default_factory=list)
    unsupported_relationships: List[Dict[str, Any]] = Field(default_factory=list)
