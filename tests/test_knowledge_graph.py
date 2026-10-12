"""Unit tests for knowledge graph assembly, edge provenance, and multi-format exports."""

import unittest
from osint_fusion.corpus.sample_corpus import get_default_benchmark_corpus
from osint_fusion.extraction.entity_extractor import EntityExtractor
from osint_fusion.extraction.entity_resolver import ConservativeEntityResolver
from osint_fusion.extraction.event_extractor import EventExtractor
from osint_fusion.reasoning.graph_builder import KnowledgeGraphBuilder


class TestKnowledgeGraph(unittest.TestCase):

    def setUp(self):
        self.sources = get_default_benchmark_corpus()
        raw_entities = []
        for s in self.sources:
            raw_entities.extend(EntityExtractor.extract_from_source(s))
        self.entities, _ = ConservativeEntityResolver.resolve_entities(raw_entities)
        self.events = EventExtractor.extract_events(self.sources)
        self.graph = KnowledgeGraphBuilder.build_graph(self.sources, self.entities, self.events)

    def test_graph_has_nodes_and_edges(self):
        self.assertGreater(len(self.graph.nodes), 10)
        self.assertGreater(len(self.graph.edges), 5)

    def test_direct_vs_inferred_edges_distinguished(self):
        direct_edges = [e for e in self.graph.edges if e.is_direct_evidence]
        inferred_edges = [e for e in self.graph.edges if not e.is_direct_evidence]
        self.assertTrue(len(direct_edges) > 0, "Should have direct evidence edges")
        self.assertTrue(len(inferred_edges) > 0, "Should have inferred analytical edges")

    def test_csv_node_export(self):
        csv_nodes = KnowledgeGraphBuilder.export_nodes_csv(self.graph)
        self.assertIn("NodeID,Label,NodeType", csv_nodes)
        self.assertIn("SRC-001", csv_nodes)
        self.assertIn("ENT-001", csv_nodes)

    def test_csv_edge_export(self):
        csv_edges = KnowledgeGraphBuilder.export_edges_csv(self.graph)
        self.assertIn("EdgeID,SourceNodeID,TargetNodeID", csv_edges)
        self.assertIn("EDG-001", csv_edges)

    def test_cypher_export(self):
        cypher = KnowledgeGraphBuilder.export_cypher(self.graph)
        self.assertIn("MERGE (n:", cypher)
        self.assertIn("MERGE (s)-[r:", cypher)

    def test_mermaid_export(self):
        mermaid = KnowledgeGraphBuilder.export_mermaid(self.graph)
        self.assertTrue(mermaid.startswith("graph TD"))
        self.assertIn("SRC-001", mermaid)


if __name__ == "__main__":
    unittest.main()
