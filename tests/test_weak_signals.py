"""Unit tests for weak signal detection and heuristic confidence scoring."""

import unittest
from osint_fusion.corpus.sample_corpus import get_default_benchmark_corpus
from osint_fusion.extraction.entity_extractor import EntityExtractor
from osint_fusion.extraction.entity_resolver import ConservativeEntityResolver
from osint_fusion.extraction.event_extractor import EventExtractor
from osint_fusion.reasoning.weak_signals import WeakSignalDetector


class TestWeakSignals(unittest.TestCase):

    def setUp(self):
        self.sources = get_default_benchmark_corpus()
        raw_entities = []
        for s in self.sources:
            raw_entities.extend(EntityExtractor.extract_from_source(s))
        self.entities, _ = ConservativeEntityResolver.resolve_entities(raw_entities)
        self.events = EventExtractor.extract_events(self.sources)
        self.signals = WeakSignalDetector.detect_signals(self.sources, self.entities, self.events)

    def test_signals_detected(self):
        self.assertGreaterEqual(len(self.signals), 2)

    def test_evidence_confidence_and_signal_strength_distinct(self):
        for sig in self.signals:
            self.assertIn(sig.evidence_confidence, ["LOW", "MODERATE", "HIGH"])
            self.assertIn(sig.signal_strength, ["LOW", "MODERATE", "HIGH"])
            self.assertIsNotNone(sig.confidence_breakdown)
            # Heuristic composite score must be bounded [0.0, 1.0]
            score = sig.confidence_breakdown.composite_heuristic_score
            self.assertGreaterEqual(score, 0.0)
            self.assertLessEqual(score, 1.0)

    def test_counterevidence_and_alternatives_present(self):
        for sig in self.signals:
            self.assertGreater(len(sig.alternative_explanations), 0, f"Signal {sig.id} must have alternative explanations")
            self.assertGreater(len(sig.counterevidence), 0, f"Signal {sig.id} must have counterevidence")
            self.assertGreater(len(sig.recommended_verification_steps), 0, f"Signal {sig.id} must recommend verification steps")


if __name__ == "__main__":
    unittest.main()
