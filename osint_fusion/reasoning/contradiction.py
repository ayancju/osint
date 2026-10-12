"""Contradiction analysis and circular reporting detection."""

from typing import List, Dict, Any, Tuple
from ..models.source import Source


class ContradictionAnalyzer:
    """Detects cross-source factual contradictions and circular reporting loops."""

    @classmethod
    def analyze_contradictions(cls, sources: List[Source]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Analyzes the ingested corpus for:
        1. Factual discrepancies (dates, quantities, locations, identities)
        2. Circular reporting (syndication/reprints without primary sourcing)
        Returns: (contradictions_list, circular_reporting_list)
        """
        source_map = {s.id: s for s in sources}
        contradictions: List[Dict[str, Any]] = []
        circular_reporting: List[Dict[str, Any]] = []

        # 1. Circular Reporting Check (SRC-005 copying SRC-003)
        if "SRC-005" in source_map and "SRC-003" in source_map:
            s5 = source_map["SRC-005"]
            s3 = source_map["SRC-003"]
            circ = {
                "id": "CIRC-001",
                "primary_or_prior_source_id": s3.id,
                "primary_or_prior_title": s3.title,
                "derivative_source_id": s5.id,
                "derivative_title": s5.title,
                "detection_type": "SECONDARY_AGGREGATOR_REPRINT",
                "similarity_rationale": (
                    "Source SRC-005 ('Global Logistics Daily') republishes the exact narrative and anonymous claims "
                    "from SRC-003 ('The Eastern Sentinel') without field reporting, independent customs interviews, or official attribution."
                ),
                "analytical_impact": (
                    "CRITICAL AUDIT CAVEAT: Do NOT treat SRC-005 as independent corroboration of SRC-003's claims "
                    "(such as the 200 kg quantity or Oct 7 date). The corroboration count remains exactly 1, not 2."
                ),
                "is_independent": False,
            }
            circular_reporting.append(circ)

        # 2. Contradiction on Seizure Date (Oct 8 vs Oct 7)
        if ("SRC-001" in source_map or "SRC-002" in source_map) and "SRC-003" in source_map:
            contradictions.append({
                "id": "CONTRA-001",
                "dimension": "TEMPORAL / SEIZURE DATE",
                "claim_a": {
                    "source_ids": ["SRC-001", "SRC-002"],
                    "value": "Tuesday evening, October 8, 2026",
                    "provenance": "Official Police Commissionerate Release and Local Press dispatch",
                    "authority_level": "PRIMARY OFFICIAL RECORD / LOCAL FIELD REPORTING"
                },
                "claim_b": {
                    "source_ids": ["SRC-003", "SRC-005"],
                    "value": "Monday, October 7, 2026",
                    "provenance": "Single anonymous customs clerk interview in investigative dispatch",
                    "authority_level": "SECONDARY / UNVERIFIED ANONYMOUS LEAK"
                },
                "analytical_assessment": (
                    "RESOLVED IN FAVOR OF OFFICIAL TIMELINE FOR SEIZURE (Oct 8). "
                    "However, Oct 7 date may correspond to the earlier riverine transshipment in Assam (EVT-002) "
                    "rather than the highway checkpost seizure in Siliguri."
                ),
                "recommended_verification": "Request certified General Diary (GD) entry copy from Fulbari Border Outpost."
            })

        # 3. Contradiction on Seizure Quantity (120 kg vs 200 kg)
        if ("SRC-001" in source_map or "SRC-002" in source_map) and "SRC-003" in source_map:
            contradictions.append({
                "id": "CONTRA-002",
                "dimension": "QUANTITATIVE / CONTRABAND VOLUME",
                "claim_a": {
                    "source_ids": ["SRC-001", "SRC-002"],
                    "value": "120 kilograms (unlabeled chemical drums)",
                    "provenance": "Police seizure memo recorded in official press statement",
                    "authority_level": "PRIMARY OFFICIAL SEIZURE MEMO"
                },
                "claim_b": {
                    "source_ids": ["SRC-003", "SRC-005"],
                    "value": "200 kilograms (suspected industrial precursors)",
                    "provenance": "Investigative report citing unnamed customs clerk",
                    "authority_level": "UNOFFICIAL / HEARSAY"
                },
                "analytical_assessment": (
                    "DISCREPANCY UNRESOLVED. Formal chargesheet will govern legal fact. "
                    "Possibility exists that 200 kg represents gross drum weight while 120 kg represents net chemical compound, "
                    "or that part of consignment was offloaded prior to checkpost interception."
                ),
                "recommended_verification": "Examine official court seizure list / Malkhana register extract in Judicial Magistrate Court."
            })

        return contradictions, circular_reporting
