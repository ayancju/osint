"""Analyst review queue and audit log models for human-in-the-loop oversight."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import datetime
from .event import VerificationStatus


class ReviewItemType(str, Enum):
    ENTITY_MATCH = "entity_match"
    GRAPH_EDGE = "graph_edge"
    EVENT_RECORD = "event_record"
    WEAK_SIGNAL = "weak_signal"
    CONTRADICTION_RESOLUTION = "contradiction_resolution"


class ReviewAction(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    AMEND = "amend"
    MARK_NEEDS_VERIFICATION = "mark_needs_verification"
    MARK_CORROBORATED = "mark_corroborated"
    MARK_CONTRADICTED = "mark_contradicted"


class ReviewQueueItem(BaseModel):
    id: str = Field(..., description="Unique review task ID, e.g. REV-001")
    item_type: ReviewItemType
    target_id: str = Field(..., description="ID of entity, edge, event, or signal under review")
    title: str = Field(..., description="Title of the review item")
    description: str = Field(..., description="Context and machine-generated hypothesis")
    
    # Original machine hypothesis (never overwritten!)
    machine_hypothesis: str
    machine_confidence: str
    supporting_source_ids: List[str] = Field(default_factory=list)
    supporting_excerpts: List[str] = Field(default_factory=list)
    
    # Human Review State
    current_status: VerificationStatus = VerificationStatus.UNREVIEWED
    analyst_decision: Optional[ReviewAction] = None
    analyst_rationale: Optional[str] = None
    analyst_id: Optional[str] = None
    reviewed_at: Optional[str] = None
    amended_values: Dict[str, Any] = Field(default_factory=dict)


class AuditLogEntry(BaseModel):
    id: str = Field(..., description="Log entry ID, e.g. AUD-001")
    timestamp: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    analyst_id: str = "analyst_primary"
    action: str
    target_id: str
    target_type: str
    previous_state: Dict[str, Any]
    new_state: Dict[str, Any]
    rationale: str
