"""Unit tests for standard 10-section intelligence report generation and export."""

import unittest
from osint_fusion.engine import OSINTFusionEngine
from osint_fusion.report.export import ReportExporter


class TestReportGeneration(unittest.TestCase):

    def setUp(self):
        self.engine = OSINTFusionEngine(analyst_id="test_analyst")
        self.engine.load_benchmark_corpus()

    def test_report_contains_all_10_sections(self):
        rep = self.engine.latest_report
        self.assertIsNotNone(rep)
        self.assertEqual(rep.section1_executive_summary.title, "1. Executive Summary")
        self.assertEqual(rep.section2_scope_and_sources.title, "2. Scope and Sources")
        self.assertEqual(rep.section3_key_entities.title, "3. Key Entities")
        self.assertEqual(rep.section4_event_timeline.title, "4. Event Timeline")
        self.assertEqual(rep.section5_knowledge_graph.title, "5. Knowledge Graph")
        self.assertEqual(rep.section6_weak_signals.title, "6. Weak Signals")
        self.assertEqual(rep.section7_contradictions_and_gaps.title, "7. Contradictions and Gaps")
        self.assertEqual(rep.section8_analyst_review_queue.title, "8. Analyst Review Queue")
        self.assertEqual(rep.section9_recommended_verification_steps.title, "9. Recommended Verification Steps")
        self.assertEqual(rep.section10_evidence_appendix.title, "10. Evidence Appendix")

    def test_markdown_export(self):
        md = ReportExporter.to_markdown(self.engine.latest_report)
        self.assertIn("# OSINT Multi-Source Cross-Border Logistics Assessment", md)
        self.assertIn("## 1. Executive Summary", md)
        self.assertIn("## 5. Knowledge Graph", md)
        self.assertIn("```mermaid", md)
        self.assertIn("## 10. Evidence Appendix", md)
        self.assertIn("Safety, Privacy & Compliance Certification", md)

    def test_json_export(self):
        json_str = ReportExporter.to_json(self.engine.latest_report)
        self.assertIn("section1_executive_summary", json_str)
        self.assertIn("compliance_statement", json_str)


if __name__ == "__main__":
    unittest.main()
