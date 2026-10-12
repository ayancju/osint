"""Unit tests for conservative entity resolution and ambiguity logging."""

import unittest
from osint_fusion.corpus.sample_corpus import get_default_benchmark_corpus
from osint_fusion.extraction.entity_extractor import EntityExtractor
from osint_fusion.extraction.entity_resolver import ConservativeEntityResolver
from osint_fusion.models.entity import EntityResolutionStatus, InvolvementType


class TestConservativeEntityResolution(unittest.TestCase):

    def setUp(self):
        self.sources = get_default_benchmark_corpus()
        self.raw_entities = []
        for s in self.sources:
            self.raw_entities.extend(EntityExtractor.extract_from_source(s))
        self.resolved, self.ambiguities = ConservativeEntityResolver.resolve_entities(self.raw_entities)

    def test_conservative_isolation_of_subrata_mukherjee(self):
        """Driver Subrata Mukherjee must NOT be merged with Civil Litigant Subrata Mukherjee."""
        driver_candidates = [e for e in self.resolved if e.id == "ENT-001"]
        litigant_candidates = [e for e in self.resolved if e.id == "ENT-007"]

        self.assertEqual(len(driver_candidates), 1, "Driver entity ENT-001 should exist as distinct")
        self.assertEqual(len(litigant_candidates), 1, "Litigant entity ENT-007 should exist as distinct")

        driver = driver_candidates[0]
        litigant = litigant_candidates[0]

        # Ensure they are distinct records
        self.assertNotEqual(driver.id, litigant.id)
        self.assertEqual(driver.resolution_status, EntityResolutionStatus.DISTINCT)
        self.assertEqual(litigant.resolution_status, EntityResolutionStatus.DISTINCT)

        # Ensure verified involvement is differentiated
        self.assertTrue(driver.verified_involvement)
        self.assertFalse(litigant.verified_involvement)

    def test_ambiguity_log_contains_clashing_justification(self):
        """Ambiguity log must explicitly document clashing parentage and civil litigation context."""
        found = False
        for amb in self.ambiguities:
            if "ENT-001" in [amb["entity_1_id"], amb["entity_2_id"]] and "ENT-007" in [amb["entity_1_id"], amb["entity_2_id"]]:
                found = True
                self.assertIn("CONSERVATIVE RESOLUTION APPLIED", amb["justification"])
                self.assertIn("Late N. Mukherjee vs B. Mukherjee", amb["justification"])
                self.assertEqual(amb["resolution_action"], "REJECTED_MERGE_KEPT_DISTINCT")
        self.assertTrue(found, "Ambiguity record between ENT-001 and ENT-007 should be logged")

    def test_corporate_entities_resolved_correctly(self):
        """Vikramaditya Logistics and Rupali Transport should be extracted and separated."""
        vik = [e for e in self.resolved if e.id == "ENT-002"]
        rup = [e for e in self.resolved if e.id == "ENT-003"]
        self.assertEqual(len(vik), 1)
        self.assertEqual(len(rup), 1)
        self.assertIn("vikramaditya", vik[0].canonical_name.lower())
        self.assertIn("rupali", rup[0].canonical_name.lower())


if __name__ == "__main__":
    unittest.main()
