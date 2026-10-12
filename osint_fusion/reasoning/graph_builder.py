"""Knowledge graph builder constructing evidence-grounded nodes, typed edges, and multi-format exports."""

import io
import csv
from typing import List, Dict, Any, Tuple
from ..models.source import Source
from ..models.entity import Entity
from ..models.event import EventRecord, VerificationStatus
from ..models.graph import KnowledgeGraph, GraphNode, GraphEdge, EdgeType


class KnowledgeGraphBuilder:
    """Builds a cross-lingual, provenance-backed knowledge graph from intelligence records."""

    @classmethod
    def build_graph(
        cls,
        sources: List[Source],
        entities: List[Entity],
        events: List[EventRecord],
    ) -> KnowledgeGraph:
        """Assembles nodes and edges connecting sources, entities, and events."""
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        node_ids_seen = set()

        # 1. Add Source Nodes
        for src in sources:
            if src.id not in node_ids_seen:
                node_ids_seen.add(src.id)
                nodes.append(
                    GraphNode(
                        id=src.id,
                        label=f"[{src.id}] {src.source_org}",
                        node_type="SOURCE",
                        original_language_label=src.original_language.value.upper(),
                        properties={
                            "title": src.title,
                            "type": src.source_type.value,
                            "language": src.original_language_name,
                            "publication_date": src.publication_date,
                            "is_primary": src.is_primary_source,
                        },
                        confidence="HIGH",
                        verification_status=VerificationStatus.ANALYST_APPROVED,
                    )
                )

        # 2. Add Entity Nodes
        for ent in entities:
            if ent.id not in node_ids_seen:
                node_ids_seen.add(ent.id)
                nodes.append(
                    GraphNode(
                        id=ent.id,
                        label=ent.canonical_name,
                        node_type=ent.entity_type.value,
                        original_script_names=ent.original_script_names,
                        properties={
                            "entity_type": ent.entity_type.value,
                            "verified_involvement": ent.verified_involvement,
                            "resolution_status": ent.resolution_status.value,
                            "alternative_spellings": ent.alternative_spellings,
                        },
                        confidence=ent.confidence,
                        verification_status=(
                            VerificationStatus.CORROBORATED
                            if ent.verified_involvement
                            else VerificationStatus.UNREVIEWED
                        ),
                    )
                )

        # 3. Add Event Nodes
        for evt in events:
            if evt.id not in node_ids_seen:
                node_ids_seen.add(evt.id)
                nodes.append(
                    GraphNode(
                        id=evt.id,
                        label=evt.title,
                        node_type="EVENT",
                        properties={
                            "date": evt.event_date,
                            "location": evt.location_name,
                            "precision": evt.location_precision,
                            "temporal_status": evt.temporal_status.value,
                        },
                        confidence=evt.confidence,
                        verification_status=evt.verification_status,
                    )
                )

        # 4. Construct Supported Edges
        # E1: SRC-001 -> mentions -> ENT-001
        edges.append(
            GraphEdge(
                id="EDG-001",
                source_node_id="SRC-001",
                target_node_id="ENT-001",
                relationship_type=EdgeType.MENTIONS,
                label="mentions driver",
                is_direct_evidence=True,
                source_ids=["SRC-001"],
                supporting_excerpts=["সুব্রত মুখার্জী (৩৮, মালদহ নিবাসী) ঘটনাস্থলে আটক হন।"],
                confidence="HIGH",
                verification_status=VerificationStatus.CORROBORATED,
            )
        )

        # E2: SRC-002 -> mentions -> ENT-001
        edges.append(
            GraphEdge(
                id="EDG-002",
                source_node_id="SRC-002",
                target_node_id="ENT-001",
                relationship_type=EdgeType.MENTIONS,
                label="identifies apprehended driver",
                is_direct_evidence=True,
                source_ids=["SRC-002"],
                supporting_excerpts=["चालक की पहचान सुब्रतो मुखर्जी के रूप में हुई।"],
                confidence="HIGH",
                verification_status=VerificationStatus.CORROBORATED,
            )
        )

        # E3: ENT-001 -> employed_by -> ENT-003
        edges.append(
            GraphEdge(
                id="EDG-003",
                source_node_id="ENT-001",
                target_node_id="ENT-003",
                relationship_type=EdgeType.EMPLOYED_BY,
                label="reported driving carrier for",
                is_direct_evidence=True,
                source_ids=["SRC-001"],
                supporting_excerpts=["freight carrier operated by 'Rupali Transport' driven by Subrata Mukherjee."],
                confidence="MODERATE",
                verification_status=VerificationStatus.NEEDS_VERIFICATION,
                flags=["Intermediary hiring via P.K. Biswas creates ambiguity over formal employment contract."],
            )
        )

        # E4: ENT-003 -> affiliated_with -> ENT-002 (Rupali Transport -> Vikramaditya Logistics)
        edges.append(
            GraphEdge(
                id="EDG-004",
                source_node_id="ENT-003",
                target_node_id="ENT-002",
                relationship_type=EdgeType.AFFILIATED_WITH,
                label="alleged subsidiary / operating partner",
                is_direct_evidence=False,
                source_ids=["SRC-003"],
                supporting_excerpts=["'Rupali Transport' is a registered subsidiary of 'Vikramaditya Logistics'"],
                confidence="MODERATE",
                verification_status=VerificationStatus.NEEDS_VERIFICATION,
                analyst_notes="Only cited in investigative article SRC-003 and copied in SRC-005. Requires formal corporate registry filings (MCA-21) to confirm.",
            )
        )

        # E5: ENT-002 -> operates_in -> ENT-009 (Vikramaditya owns carrier WB-73-E-4421)
        edges.append(
            GraphEdge(
                id="EDG-005",
                source_node_id="ENT-002",
                target_node_id="ENT-009",
                relationship_type=EdgeType.OPERATES_IN,
                label="registered corporate vehicle owner",
                is_direct_evidence=True,
                source_ids=["SRC-002"],
                supporting_excerpts=["Registered corporate owner of the carrier is Vikramaditya Logistics Private Limited."],
                confidence="HIGH",
                verification_status=VerificationStatus.CORROBORATED,
            )
        )

        # E6: EVT-003 -> reported_at -> ENT-004 (Fulbari Checkpost)
        edges.append(
            GraphEdge(
                id="EDG-006",
                source_node_id="EVT-003",
                target_node_id="ENT-004",
                relationship_type=EdgeType.REPORTED_AT,
                label="intercepted at",
                is_direct_evidence=True,
                source_ids=["SRC-001", "SRC-002"],
                supporting_excerpts=["Fulbari Border Outpost interception."],
                confidence="HIGH",
                verification_status=VerificationStatus.CORROBORATED,
            )
        )

        # E7: EVT-002 -> transshipped_to -> EVT-003 (Dhubri transshipment to Fulbari seizure)
        edges.append(
            GraphEdge(
                id="EDG-007",
                source_node_id="EVT-002",
                target_node_id="EVT-003",
                relationship_type=EdgeType.TRANSSHIPPED_TO,
                label="cross-border cargo origin route",
                is_direct_evidence=False,
                source_ids=["SRC-001", "SRC-004"],
                supporting_excerpts=[
                    "driver stated loading took place at Dhubri riverfront (SRC-001); radio reported boat unloading to truck at Dhubri ghat (SRC-004)."
                ],
                confidence="MODERATE",
                verification_status=VerificationStatus.NEEDS_VERIFICATION,
                analyst_notes="Key hypothesis: multi-modal riverine-to-road contraband route. Direct physical tracking link remains unproven.",
            )
        )

        # E8: ENT-008 -> affiliated_with -> ENT-002 (A. K. Roy -> Vikramaditya MD)
        edges.append(
            GraphEdge(
                id="EDG-008",
                source_node_id="ENT-008",
                target_node_id="ENT-002",
                relationship_type=EdgeType.AFFILIATED_WITH,
                label="registered Managing Director",
                is_direct_evidence=True,
                source_ids=["SRC-006"],
                supporting_excerpts=["Registered Managing Director listed as A. K. Roy in Chennai port registry."],
                confidence="HIGH",
                verification_status=VerificationStatus.CORROBORATED,
            )
        )

        # E9: ENT-001 -> communicated_with -> ENT-006 (Driver -> Broker P.K. Biswas)
        edges.append(
            GraphEdge(
                id="EDG-009",
                source_node_id="ENT-001",
                target_node_id="ENT-006",
                relationship_type=EdgeType.COMMUNICATED_WITH,
                label="hired by broker",
                is_direct_evidence=True,
                source_ids=["SRC-002"],
                supporting_excerpts=["Driver claims he was hired by a third-party intermediary named 'P. K. Biswas' in Malda."],
                confidence="MODERATE",
                verification_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        # E10: SRC-005 -> corroborates -> SRC-003 [CIRCULAR REPORTING EDGE]
        edges.append(
            GraphEdge(
                id="EDG-010",
                source_node_id="SRC-005",
                target_node_id="SRC-003",
                relationship_type=EdgeType.CORROBORATES,
                label="circular copycat / derivative reprint",
                is_direct_evidence=True,
                source_ids=["SRC-005"],
                supporting_excerpts=["Verbatim republishes The Eastern Sentinel dispatch without independent sourcing."],
                confidence="HIGH",
                verification_status=VerificationStatus.CONTRADICTED,
                flags=["CIRCULAR_REPORTING: Does not represent independent corroboration."],
            )
        )

        # Unsupported relationships explicitly isolated
        unsupported = [
            {
                "hypothesis": "Subrata Mukherjee (Cooch Behar, ENT-007) is an accomplice of Driver Subrata Mukherjee (ENT-001).",
                "finding": "STRICTLY UNSUPPORTED / REJECTED",
                "reason": "Judicial records in SRC-007 prove distinct identity, father's name, residence, and non-criminal civil litigation.",
            },
            {
                "hypothesis": "A. K. Roy (ENT-008) directly ordered the loading of chemical drums in Dhubri.",
                "finding": "UNSUPPORTED INFERENCE",
                "reason": "Corporate directorship does not establish direct operational knowledge or mens rea without communications evidence.",
            }
        ]

        unresolved = [
            {
                "candidate_match": "Subrata Mukherjee (ENT-001) vs Subrata Mukherjee (ENT-007)",
                "status": "DISAMBIGUATED_AS_DISTINCT",
                "resolution": "Kept strictly separate under conservative resolution protocols.",
            },
            {
                "candidate_match": "Rupali Transport (ENT-003) subsidiary status to Vikramaditya Logistics (ENT-002)",
                "status": "UNRESOLVED_REQUIRES_REGISTRY_FILING",
                "resolution": "Flagged for MCA-21 company registry verification.",
            }
        ]

        return KnowledgeGraph(
            nodes=nodes,
            edges=edges,
            unresolved_matches=unresolved,
            unsupported_relationships=unsupported,
        )

    @classmethod
    def export_nodes_csv(cls, graph: KnowledgeGraph) -> str:
        """Exports graph nodes to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["NodeID", "Label", "NodeType", "Confidence", "VerificationStatus", "KeyProperties"])
        for node in graph.nodes:
            writer.writerow([
                node.id,
                node.label,
                node.node_type,
                node.confidence,
                node.verification_status.value,
                str(node.properties),
            ])
        return output.getvalue()

    @classmethod
    def export_edges_csv(cls, graph: KnowledgeGraph) -> str:
        """Exports graph edges to CSV format."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "EdgeID", "SourceNodeID", "TargetNodeID", "RelationshipType", "Label",
            "IsDirectEvidence", "SourceIDs", "Confidence", "VerificationStatus", "Flags"
        ])
        for edge in graph.edges:
            writer.writerow([
                edge.id,
                edge.source_node_id,
                edge.target_node_id,
                edge.relationship_type.value,
                edge.label,
                edge.is_direct_evidence,
                ";".join(edge.source_ids),
                edge.confidence,
                edge.verification_status.value,
                ";".join(edge.flags),
            ])
        return output.getvalue()

    @classmethod
    def export_cypher(cls, graph: KnowledgeGraph) -> str:
        """Generates Cypher statements for import into Neo4j or Memgraph."""
        lines = ["// --- Knowledge Graph Cypher Script (OSINT Fusion Workbench) ---"]
        for n in graph.nodes:
            lbl = n.node_type.replace(" ", "_")
            esc_name = n.label.replace("'", "\\'")
            lines.append(
                f"MERGE (n:{lbl} {{id: '{n.id}'}}) "
                f"ON CREATE SET n.label = '{esc_name}', n.confidence = '{n.confidence}', n.status = '{n.verification_status.value}';"
            )

        for e in graph.edges:
            rel = e.relationship_type.value.upper()
            esc_lbl = e.label.replace("'", "\\'")
            lines.append(
                f"MATCH (s {{id: '{e.source_node_id}'}}), (t {{id: '{e.target_node_id}'}}) "
                f"MERGE (s)-[r:{rel} {{id: '{e.id}', label: '{esc_lbl}', direct: {str(e.is_direct_evidence).lower()}, status: '{e.verification_status.value}'}}]->(t);"
            )
        return "\n".join(lines)

    @classmethod
    def export_mermaid(cls, graph: KnowledgeGraph) -> str:
        """Generates a Mermaid graph diagram."""
        lines = ["graph TD"]
        for n in graph.nodes:
            # quote labels for safety
            safe_label = n.label.replace('"', "'")
            if n.node_type == "PERSON":
                lines.append(f'    {n.id}["👤 {safe_label}"]')
            elif n.node_type == "ORGANIZATION":
                lines.append(f'    {n.id}["🏢 {safe_label}"]')
            elif n.node_type == "LOCATION":
                lines.append(f'    {n.id}["📍 {safe_label}"]')
            elif n.node_type == "EVENT":
                lines.append(f'    {n.id}["⚡ {safe_label}"]')
            elif n.node_type == "SOURCE":
                lines.append(f'    {n.id}["📰 {safe_label}"]')
            else:
                lines.append(f'    {n.id}["📦 {safe_label}"]')

        for e in graph.edges:
            safe_lbl = e.label.replace('"', "'")
            style = "-->" if e.is_direct_evidence else "-.->|inferred|"
            lines.append(f'    {e.source_node_id} {style}|"{safe_lbl}"| {e.target_node_id}')

        return "\n".join(lines)
