"""Unit tests for contradiction analysis and circular reporting detection."""

import unittest
from osint_fusion.corpus.sample_corpus import get_default_benchmark_corpus
from osint_fusion.reasoning.contradiction import ContradictionAnalyzer


class TestContradictionAnalysis(unittest.TestCase):

    def setUp(self):
        self.sources = get_default_benchmark_corpus()
        self.contradictions, self.circular = ContradictionAnalyzer.analyze_contradictions(self.sources)

    def test_circular_reporting_detected(self):
        self.assertGreater(len(self.circular), 0, "Should detect at least 1 circular reporting instance")
        circ = self.circular[0]
        self.assertEqual(circ["primary_or_prior_source_id"], "SRC-003")
        self.assertEqual(circ["derivative_source_id"], "SRC-005")
        self.assertIn("CRITICAL AUDIT CAVEAT", circ["analytical_impact"])

    def test_factual_contradictions_detected(self):
        self.assertGreaterEqual(len(self.contradictions), 2)
        dimensions = [c["dimension"] for c in self.contradictions]
        self.assertTrue(any("SEIZURE DATE" in d for d in dimensions))
        self.assertTrue(any("CONTRABAND VOLUME" in d for d in dimensions))


if __name__ == "__main__":
    unittest.main()
