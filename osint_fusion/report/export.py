"""Report exporter generating GitHub-flavored Markdown, HTML, and JSON."""

import json
from ..models.report import IntelligenceReport


class ReportExporter:
    """Exports IntelligenceReport to Markdown, HTML, and JSON formats."""

    @classmethod
    def to_markdown(cls, report: IntelligenceReport) -> str:
        """Renders the complete 10-section intelligence report in GitHub-flavored Markdown."""
        lines = []
        lines.append(f"# {report.report_title}")
        lines.append(f"**Report ID:** `{report.report_id}` | **Classification:** `{report.classification_level}` | **Generated:** {report.generated_at}")
        lines.append(f"**Prepared by:** {report.prepared_by}\n")
        lines.append("---\n")

        # 1. Executive Summary
        s1 = report.section1_executive_summary
        lines.append(f"## {s1.title}\n")
        lines.append(f"> [!IMPORTANT]\n> **Overall Confidence Posture:** {s1.overall_confidence_posture}\n")
        lines.append("### Key Findings")
        for f in s1.key_findings:
            lines.append(f"- {f}")
        lines.append("\n### Critical Caveats & Limitations")
        for c in s1.critical_caveats_and_limitations:
            lines.append(f"- ⚠️ {c}")
        lines.append("\n---\n")

        # 2. Scope and Sources
        s2 = report.section2_scope_and_sources
        lines.append(f"## {s2.title}\n")
        lines.append(f"{s2.corpus_summary}\n")
        lines.append(f"**Total Sources:** {s2.total_sources_ingested} | **Languages Analyzed:** {', '.join(s2.languages_analyzed)}\n")
        lines.append("| Source ID | Title | Publishing Org | Type | Language | Pub Date | Reliability |")
        lines.append("|---|---|---|---|---|---|---|")
        for s in s2.source_breakdown:
            lines.append(f"| `{s['source_id']}` | {s['title'][:40]}... | {s['source_org']} | {s['type']} | {s['language']} | {s['pub_date']} | {s['reliability']} |")
        lines.append("\n#### Unavailable or Unaccessed Sources")
        for u in s2.unavailable_or_unaccessed_sources:
            lines.append(f"- 🔒 {u}")
        lines.append("\n---\n")

        # 3. Key Entities
        s3 = report.section3_key_entities
        lines.append(f"## {s3.title}\n")
        lines.append(f"{s3.entities_summary}\n")
        lines.append(f"> [!NOTE]\n> {s3.conservative_resolution_notes}\n")
        lines.append("| Entity ID | Canonical Name | Type | Involvement | Status | Observed Dates | Sources |")
        lines.append("|---|---|---|---|---|---|---|")
        for e in s3.entities:
            sids = ", ".join(f"`{sid}`" for sid in e['sources'])
            d_span = f"{e['first_date']} to {e['last_date']}" if e['first_date'] else "N/A"
            lines.append(f"| `{e['entity_id']}` | **{e['canonical_name']}** | `{e['type']}` | {e['involvement']} | {e['resolution_status']} | {d_span} | {sids} |")
        lines.append("\n---\n")

        # 4. Event Timeline
        s4 = report.section4_event_timeline
        lines.append(f"## {s4.title}\n")
        lines.append(f"{s4.chronology_summary}\n")
        lines.append("| Event ID | Date / Range | Event Title | Precision & Location | Verification Status | Sources |")
        lines.append("|---|---|---|---|---|---|")
        for ev in s4.events:
            sids = ", ".join(f"`{s}`" for s in ev['sources'])
            d_str = ev['date'] or "Unconfirmed"
            if ev['date_end']:
                d_str += f" to {ev['date_end']}"
            lines.append(f"| `{ev['event_id']}` | {d_str} | {ev['title']} | {ev['location']} ({ev['precision']}) | `{ev['verification_status']}` | {sids} |")
        lines.append("\n#### Documented Temporal Uncertainties")
        for tu in s4.temporal_uncertainties:
            lines.append(f"- ⏳ {tu}")
        lines.append("\n---\n")

        # 5. Knowledge Graph
        s5 = report.section5_knowledge_graph
        lines.append(f"## {s5.title}\n")
        lines.append(f"{s5.graph_narrative}\n")
        lines.append("### Mermaid Graph Visualization\n")
        lines.append("```mermaid")
        lines.append(s5.mermaid_diagram)
        lines.append("```\n")
        lines.append("### Key Supported Relationships")
        lines.append("| Edge ID | Source Node | Predicate | Target Node | Direct Evidence | Status | Sources |")
        lines.append("|---|---|---|---|---|---|---|")
        for r in s5.key_supported_relationships:
            sids = ", ".join(f"`{s}`" for s in r['sources'])
            direct = "Direct" if r['direct_evidence'] else "Inferred"
            lines.append(f"| `{r['edge_id']}` | `{r['source']}` | **{r['label']}** | `{r['target']}` | {direct} | `{r['status']}` | {sids} |")
        lines.append("\n---\n")

        # 6. Weak Signals
        s6 = report.section6_weak_signals
        lines.append(f"## {s6.title}\n")
        lines.append(f"{s6.overview}\n")
        for sig in s6.signals:
            lines.append(f"### 🔍 [{sig['signal_id']}] {sig['title']}")
            lines.append(f"- **Category:** `{sig['category']}`")
            lines.append(f"- **Evidence Confidence:** `{sig['evidence_confidence']}` | **Signal Strength:** `{sig['signal_strength']}` | **Heuristic Score:** `{sig['heuristic_score']}`")
            lines.append(f"- **Description:** {sig['description']}")
            lines.append(f"- **Significance:** {sig['significance']}")
            lines.append("- **Alternative Explanations & Counterevidence:**")
            for alt in sig['alternative_explanations']:
                lines.append(f"  * Alternative: {alt}")
            for ce in sig['counterevidence']:
                lines.append(f"  * Counterevidence: {ce}")
            lines.append("- **Information Gaps:** " + "; ".join(sig['information_gaps']))
            lines.append("- **Recommended Verification:** " + "; ".join(sig['recommended_verification']))
            lines.append("")
        lines.append("---\n")

        # 7. Contradictions and Gaps
        s7 = report.section7_contradictions_and_gaps
        lines.append(f"## {s7.title}\n")
        lines.append("### Cross-Source Factual Contradictions")
        for con in s7.cross_source_conflicts:
            lines.append(f"#### ⚡ [{con['id']}] Discrepancy: {con['dimension']}")
            lines.append(f"- **Account A ({', '.join(con['claim_a']['source_ids'])}):** {con['claim_a']['value']} (*{con['claim_a']['provenance']}*)")
            lines.append(f"- **Account B ({', '.join(con['claim_b']['source_ids'])}):** {con['claim_b']['value']} (*{con['claim_b']['provenance']}*)")
            lines.append(f"- **Assessment:** {con['analytical_assessment']}")
            lines.append(f"- **Verification Route:** {con['recommended_verification']}\n")

        lines.append("### Circular Reporting & Duplication Identified")
        for circ in s7.circular_reporting_identified:
            lines.append(f"> [!WARNING]\n> **{circ['id']}: {circ['detection_type']}**\n> {circ['similarity_rationale']}\n> *{circ['analytical_impact']}*\n")

        lines.append("### Unanswered Analytical Questions")
        for q in s7.unanswered_questions:
            lines.append(f"- ❓ {q}")
        lines.append("\n---\n")

        # 8. Analyst Review Queue
        s8 = report.section8_analyst_review_queue
        lines.append(f"## {s8.title}\n")
        lines.append(f"{s8.queue_summary}\n")
        lines.append("| Review ID | Item Type | Target | Title | Machine Hypothesis | Status |")
        lines.append("|---|---|---|---|---|---|")
        for it in s8.pending_items:
            lines.append(f"| `{it['review_id']}` | `{it['type']}` | `{it['target_id']}` | {it['title']} | {it['hypothesis']} | `{it['status']}` |")
        lines.append("\n---\n")

        # 9. Recommended Verification Steps
        s9 = report.section9_recommended_verification_steps
        lines.append(f"## {s9.title}\n")
        for st in s9.recommended_steps:
            lines.append(f"### Step {st['step_number']}: {st['title']} (Priority: `{st['priority']}`)")
            lines.append(f"- **Target Entities:** {', '.join(st['target_entities'])}")
            lines.append(f"- **Lawful Source:** {st['lawful_source']}")
            lines.append(f"- **Objective:** {st['objective']}\n")
        lines.append("---\n")

        # 10. Evidence Appendix
        s10 = report.section10_evidence_appendix
        lines.append(f"## {s10.title}\n")
        lines.append("### Verbatim Source Excerpts & Provenance Registry\n")
        for ev in s10.evidence_items:
            lines.append(f"#### [{ev['source_id']}] {ev['source_org']} — {ev['title']}")
            lines.append(f"- **Language:** {ev['language']} | **Locator:** {ev['page_or_timestamp']}")
            lines.append(f"- **Original Script:**\n> {ev['original_excerpt']}")
            if ev['english_translation']:
                lines.append(f"- **English Translation:**\n> {ev['english_translation']}")
            lines.append("")

        lines.append("---\n")
        lines.append("## Safety, Privacy & Compliance Certification\n")
        lines.append(f"> [!CAUTION]\n> {report.compliance_statement}\n")

        return "\n".join(lines)

    @classmethod
    def to_json(cls, report: IntelligenceReport) -> str:
        """Serializes IntelligenceReport to structured JSON."""
        return report.model_dump_json(indent=2)
