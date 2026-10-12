"""Central OSINT Fusion Workbench Engine orchestrating multilingual processing,
knowledge graph synthesis, contradiction analysis, weak signals, and analyst oversight.
"""

import uuid
import datetime
from typing import List, Dict, Any, Optional, Tuple
from .models.source import Source, SourceType, LanguageCode
from .models.entity import Entity, EntityResolutionStatus
from .models.event import EventRecord, VerificationStatus
from .models.graph import KnowledgeGraph
from .models.signal import WeakSignal
from .models.review import ReviewQueueItem, ReviewAction, AuditLogEntry
from .models.report import IntelligenceReport
from .multilingual.detector import LanguageDetector
from .multilingual.translation import TranslationManager
from .multilingual.audio_stt import AudioSpeechProcessor
from .extraction.entity_extractor import EntityExtractor
from .extraction.entity_resolver import ConservativeEntityResolver
from .extraction.event_extractor import EventExtractor
from .reasoning.graph_builder import KnowledgeGraphBuilder
from .reasoning.contradiction import ContradictionAnalyzer
from .reasoning.weak_signals import WeakSignalDetector
from .reasoning.verification import VerificationManager
from .report.generator import ReportGenerator
from .report.export import ReportExporter
from .corpus.sample_corpus import get_default_benchmark_corpus


class OSINTFusionEngine:
    """The central stateful intelligence engine for OSINT Fusion Workbench."""

    def __init__(self, analyst_id: str = "analyst_primary"):
        self.analyst_id = analyst_id
        self.sources: List[Source] = []
        self.entities: List[Entity] = []
        self.unresolved_ambiguities: List[Dict[str, Any]] = []
        self.events: List[EventRecord] = []
        self.graph: Optional[KnowledgeGraph] = None
        self.signals: List[WeakSignal] = []
        self.contradictions: List[Dict[str, Any]] = []
        self.circular_reporting: List[Dict[str, Any]] = []
        self.review_queue: List[ReviewQueueItem] = []
        self.audit_log: List[AuditLogEntry] = []
        self.latest_report: Optional[IntelligenceReport] = None
        self.pii_redaction_enabled: bool = False

    def load_benchmark_corpus(self) -> None:
        """Loads and ingests the default multilingual benchmark corpus."""
        benchmark_sources = get_default_benchmark_corpus()
        self.sources = benchmark_sources
        self.run_full_analysis()

    def add_custom_source(
        self,
        title: str,
        source_org: str,
        text: str,
        source_type: SourceType = SourceType.NEWS_ARTICLE,
        original_url: Optional[str] = None,
        publication_date: Optional[str] = None,
        page_numbers: Optional[str] = None,
        is_primary: bool = True,
    ) -> Source:
        """Ingests a new user-provided source and executes multilingual analysis."""
        sid = f"SRC-{len(self.sources) + 1:03d}"
        
        # Analyze language and script
        lang_res = LanguageDetector.analyze_text(text)
        trans_text, trans_status = TranslationManager.get_translation_with_badges(
            sid, text, lang_res["primary_language"]
        )

        src = Source(
            id=sid,
            title=title,
            source_org=source_org,
            source_type=source_type,
            original_url=original_url,
            publication_date=publication_date,
            original_language=lang_res["primary_language"],
            original_language_name=lang_res["language_name"],
            is_mixed_language=lang_res["is_mixed"],
            languages_detected=lang_res["detected_languages"],
            original_text=text,
            english_translation=trans_text,
            translation_status=trans_status,
            page_numbers=page_numbers,
            is_primary_source=is_primary,
        )

        self.sources.append(src)
        self.log_audit("INGEST_SOURCE", sid, "SOURCE", {}, src.model_dump(), f"Ingested source {sid}: {title}")
        self.run_full_analysis()
        return src

    def run_full_analysis(self) -> None:
        """Executes the complete cross-lingual extraction, resolution, graph, and signal pipeline."""
        # 1. Entity Extraction across all sources
        raw_entities = []
        for src in self.sources:
            extracted = EntityExtractor.extract_from_source(src)
            raw_entities.extend(extracted)

        # 2. Conservative Entity Resolution
        self.entities, self.unresolved_ambiguities = ConservativeEntityResolver.resolve_entities(raw_entities)

        # 3. Event Extraction and Timeline Ordering
        self.events = EventExtractor.extract_events(self.sources)

        # 4. Cross-Lingual Knowledge Graph Assembly
        self.graph = KnowledgeGraphBuilder.build_graph(self.sources, self.entities, self.events)

        # 5. Contradiction and Circular Reporting Analysis
        self.contradictions, self.circular_reporting = ContradictionAnalyzer.analyze_contradictions(self.sources)

        # 6. Weak-Signal Detection & Heuristic Confidence Scoring
        self.signals = WeakSignalDetector.detect_signals(self.sources, self.entities, self.events)

        # 7. Populate Analyst Review Queue
        self.review_queue = VerificationManager.generate_review_queue(
            self.entities, self.events, self.signals, self.contradictions
        )

        # 8. Generate Latest 10-Section Intelligence Report
        steps = VerificationManager.get_recommended_verification_steps()
        self.latest_report = ReportGenerator.generate_report(
            report_id=f"REP-2026-{uuid.uuid4().hex[:6].upper()}",
            title="OSINT Multi-Source Cross-Border Logistics Assessment",
            sources=self.sources,
            entities=self.entities,
            events=self.events,
            graph=self.graph,
            signals=self.signals,
            contradictions=self.contradictions,
            circular_reporting=self.circular_reporting,
            review_queue=self.review_queue,
            verification_steps=steps,
        )

    def record_analyst_decision(
        self,
        review_id: str,
        decision: ReviewAction,
        rationale: str,
        amended_values: Optional[Dict[str, Any]] = None,
    ) -> bool:
        """
        Records human analyst verification or override with an immutable audit log entry.
        Never overwrites original raw evidence.
        """
        for item in self.review_queue:
            if item.id == review_id:
                prev_state = item.model_dump()
                item.analyst_decision = decision
                item.analyst_rationale = rationale
                item.analyst_id = self.analyst_id
                item.reviewed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
                if amended_values:
                    item.amended_values = amended_values

                # Update item verification status
                if decision == ReviewAction.APPROVE:
                    item.current_status = VerificationStatus.ANALYST_APPROVED
                elif decision == ReviewAction.REJECT:
                    item.current_status = VerificationStatus.REJECTED
                elif decision == ReviewAction.AMEND:
                    item.current_status = VerificationStatus.ANALYST_APPROVED
                elif decision == ReviewAction.MARK_NEEDS_VERIFICATION:
                    item.current_status = VerificationStatus.NEEDS_VERIFICATION
                elif decision == ReviewAction.MARK_CORROBORATED:
                    item.current_status = VerificationStatus.CORROBORATED
                elif decision == ReviewAction.MARK_CONTRADICTED:
                    item.current_status = VerificationStatus.CONTRADICTED

                # If this is a graph edge or entity, update target status without deleting machine hypothesis
                if item.item_type.value == "graph_edge" and self.graph:
                    for edge in self.graph.edges:
                        if edge.id == item.target_id:
                            edge.verification_status = item.current_status
                            edge.analyst_notes = rationale
                elif item.item_type.value == "entity_match":
                    for ent in self.entities:
                        if ent.id == item.target_id:
                            ent.disambiguation_notes = rationale

                self.log_audit(
                    f"ANALYST_DECISION_{decision.value.upper()}",
                    review_id,
                    item.item_type.value,
                    prev_state,
                    item.model_dump(),
                    rationale,
                )
                return True
        return False

    def log_audit(
        self,
        action: str,
        target_id: str,
        target_type: str,
        prev_state: Dict[str, Any],
        new_state: Dict[str, Any],
        rationale: str,
    ) -> None:
        """Appends an immutable audit log entry."""
        entry = AuditLogEntry(
            id=f"AUD-{len(self.audit_log) + 1:04d}",
            analyst_id=self.analyst_id,
            action=action,
            target_id=target_id,
            target_type=target_type,
            previous_state=prev_state,
            new_state=new_state,
            rationale=rationale,
        )
        self.audit_log.append(entry)

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Returns consolidated intelligence dashboard statistics."""
        return {
            "total_sources": len(self.sources),
            "primary_sources_count": sum(1 for s in self.sources if s.is_primary_source),
            "total_entities": len(self.entities),
            "total_events": len(self.events),
            "total_graph_nodes": len(self.graph.nodes) if self.graph else 0,
            "total_graph_edges": len(self.graph.edges) if self.graph else 0,
            "total_weak_signals": len(self.signals),
            "contradictions_count": len(self.contradictions),
            "circular_reporting_count": len(self.circular_reporting),
            "review_queue_pending": sum(1 for q in self.review_queue if q.current_status == VerificationStatus.NEEDS_VERIFICATION or q.current_status == VerificationStatus.UNREVIEWED),
            "review_queue_decided": sum(1 for q in self.review_queue if q.analyst_decision is not None),
            "audit_log_entries": len(self.audit_log),
            "audio_capabilities": AudioSpeechProcessor.inspect_audio_capabilities(),
        }

    def get_cytoscape_elements(self) -> List[Dict[str, Any]]:
        """Transforms the Knowledge Graph into Cytoscape.js format."""
        if not self.graph:
            return []
        elements = []
        for n in self.graph.nodes:
            elements.append({
                "data": {
                    "id": n.id,
                    "label": n.label,
                    "type": n.node_type,
                    "confidence": n.confidence,
                    "status": n.verification_status.value,
                    "properties": n.properties,
                }
            })
        for e in self.graph.edges:
            elements.append({
                "data": {
                    "id": e.id,
                    "source": e.source_node_id,
                    "target": e.target_node_id,
                    "label": e.label,
                    "rel_type": e.relationship_type.value,
                    "direct": e.is_direct_evidence,
                    "confidence": e.confidence,
                    "status": e.verification_status.value,
                    "flags": e.flags,
                }
            })
        return elements
