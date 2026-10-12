"""Standard 10-Section Intelligence Report data model."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
import datetime


class ReportSection1ExecutiveSummary(BaseModel):
    title: str = "1. Executive Summary"
    key_findings: List[str]
    critical_caveats_and_limitations: List[str]
    overall_confidence_posture: str


class ReportSection2ScopeAndSources(BaseModel):
    title: str = "2. Scope and Sources"
    corpus_summary: str
    total_sources_ingested: int
    languages_analyzed: List[str]
    source_breakdown: List[Dict[str, Any]]
    unavailable_or_unaccessed_sources: List[str]


class ReportSection3KeyEntities(BaseModel):
    title: str = "3. Key Entities"
    entities_summary: str
    entities: List[Dict[str, Any]]
    conservative_resolution_notes: str


class ReportSection4EventTimeline(BaseModel):
    title: str = "4. Event Timeline"
    chronology_summary: str
    events: List[Dict[str, Any]]
    temporal_uncertainties: List[str]


class ReportSection5KnowledgeGraph(BaseModel):
    title: str = "5. Knowledge Graph"
    graph_narrative: str
    key_supported_relationships: List[Dict[str, Any]]
    unsupported_or_rejected_relationships: List[Dict[str, Any]]
    mermaid_diagram: str


class ReportSection6WeakSignals(BaseModel):
    title: str = "6. Weak Signals"
    overview: str
    signals: List[Dict[str, Any]]


class ReportSection7ContradictionsAndGaps(BaseModel):
    title: str = "7. Contradictions and Gaps"
    cross_source_conflicts: List[Dict[str, Any]]
    circular_reporting_identified: List[Dict[str, Any]]
    unanswered_questions: List[str]


class ReportSection8AnalystReviewQueue(BaseModel):
    title: str = "8. Analyst Review Queue"
    queue_summary: str
    pending_items: List[Dict[str, Any]]
    analyst_decisions_recorded: List[Dict[str, Any]]


class ReportSection9RecommendedVerificationSteps(BaseModel):
    title: str = "9. Recommended Verification Steps"
    recommended_steps: List[Dict[str, Any]]


class ReportSection10EvidenceAppendix(BaseModel):
    title: str = "10. Evidence Appendix"
    evidence_items: List[Dict[str, Any]]
    provenance_registry: List[Dict[str, Any]]


class IntelligenceReport(BaseModel):
    report_id: str = Field(..., description="e.g. REP-2026-001")
    report_title: str
    classification_level: str = "UNCLASSIFIED // OSINT ONLY // FOR ANALYST EVALUATION ONLY"
    generated_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    prepared_by: str = "OSINT Fusion Workbench Agent"
    
    # 10 Standard Sections
    section1_executive_summary: ReportSection1ExecutiveSummary
    section2_scope_and_sources: ReportSection2ScopeAndSources
    section3_key_entities: ReportSection3KeyEntities
    section4_event_timeline: ReportSection4EventTimeline
    section5_knowledge_graph: ReportSection5KnowledgeGraph
    section6_weak_signals: ReportSection6WeakSignals
    section7_contradictions_and_gaps: ReportSection7ContradictionsAndGaps
    section8_analyst_review_queue: ReportSection8AnalystReviewQueue
    section9_recommended_verification_steps: ReportSection9RecommendedVerificationSteps
    section10_evidence_appendix: ReportSection10EvidenceAppendix
    
    # Responsible use & governance
    compliance_statement: str
