"""Weak signal detection and heuristic confidence scoring models."""

from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class SignalCategory(str, Enum):
    CLUSTER_BRIDGE = "cluster_bridge"
    RECURRING_ENTITY_ANOMALY = "recurring_entity_anomaly"
    CORROBORATED_CONVERGENCE = "corroborated_convergence"
    REPORTING_VELOCITY_ANOMALY = "reporting_velocity_anomaly"
    TEMPORAL_INCONSISTENCY = "temporal_inconsistency"
    GEO_SPATIAL_DISPERSION = "geo_spatial_dispersion"
    CIRCULAR_REPORTING_SUSPECTED = "circular_reporting_suspected"


class ConfidenceFactors(BaseModel):
    source_reliability: float = Field(..., ge=0.0, le=1.0, description="Heuristic score for publisher reliability")
    directness_of_evidence: float = Field(..., ge=0.0, le=1.0, description="Direct primary reporting vs hearsay/secondary")
    independent_corroboration: float = Field(..., ge=0.0, le=1.0, description="Number & diversity of non-derivative sources")
    internal_consistency: float = Field(..., ge=0.0, le=1.0, description="Lack of internal or cross-source contradictions")
    composite_heuristic_score: float = Field(..., ge=0.0, le=1.0, description="Product / weighted composite [0.0 - 1.0]")
    scoring_notes: str = Field(..., description="Documented explanation of scoring factors and limitations")


class WeakSignal(BaseModel):
    id: str = Field(..., description="Unique Signal ID, e.g. SIG-001")
    title: str = Field(..., description="Concise label of observed pattern")
    category: SignalCategory
    description: str = Field(..., description="Detailed description of the pattern")
    
    # Evidence Provenance
    supporting_source_ids: List[str] = Field(default_factory=list)
    supporting_entity_ids: List[str] = Field(default_factory=list)
    supporting_event_ids: List[str] = Field(default_factory=list)
    supporting_excerpts: List[str] = Field(default_factory=list)
    
    # Intelligence Analysis
    significance_rationale: str = Field(..., description="Why this pattern may be operationally or analytically significant")
    alternative_explanations: List[str] = Field(default_factory=list, description="Benign or competing explanations")
    counterevidence: List[str] = Field(default_factory=list, description="Contradicting observations")
    information_gaps: List[str] = Field(default_factory=list, description="Crucial missing pieces needed for evaluation")
    recommended_verification_steps: List[str] = Field(default_factory=list, description="Targeted, lawful follow-up actions")
    
    # Distinct Metrics
    evidence_confidence: str = Field(default="MODERATE", description="LOW, MODERATE, HIGH assessment of evidence backing")
    signal_strength: str = Field(default="MODERATE", description="LOW, MODERATE, HIGH operational anomaly level")
    confidence_breakdown: Optional[ConfidenceFactors] = None
    
    # Analyst Disposition
    analyst_disposition: str = Field(default="PENDING_REVIEW", description="PENDING_REVIEW, CONFIRMED_PATTERNING, DISMISSED_NOISE, FIELD_CHECK_QUEUED")
    analyst_comment: Optional[str] = None
