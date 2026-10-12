"""Verification workflows, corroboration checks, and follow-up guidance."""

from typing import List, Dict, Any
from ..models.source import Source
from ..models.entity import Entity
from ..models.event import EventRecord, VerificationStatus
from ..models.review import ReviewQueueItem, ReviewItemType, ReviewAction
from ..models.signal import WeakSignal


class VerificationManager:
    """Manages corroboration pipelines, generates follow-up steps, and populates the review queue."""

    @classmethod
    def generate_review_queue(
        cls,
        entities: List[Entity],
        events: List[EventRecord],
        signals: List[WeakSignal],
        contradictions: List[Dict[str, Any]],
    ) -> List[ReviewQueueItem]:
        """Populates the human-in-the-loop analyst review queue."""
        queue: List[ReviewQueueItem] = []

        # Item 1: Disambiguation of ENT-001 vs ENT-007 (Subrata Mukherjee collision)
        queue.append(
            ReviewQueueItem(
                id="REV-001",
                item_type=ReviewItemType.ENTITY_MATCH,
                target_id="ENT-001",
                title="Verify Conservative Disambiguation: Subrata Mukherjee (Driver vs Civil Litigant)",
                description=(
                    "Two entities share the name 'Subrata Mukherjee'. ENT-001 is the freight driver in Malda/Fulbari, "
                    "while ENT-007 is a civil property litigant in Cooch Behar (SRC-007). Machine resolver separated them."
                ),
                machine_hypothesis="MAINTAIN STRICTLY SEPARATE - DO NOT MERGE",
                machine_confidence="HIGH",
                supporting_source_ids=["SRC-001", "SRC-002", "SRC-007"],
                supporting_excerpts=[
                    "SRC-002: Subroto Mukherjee, son of B. Mukherjee, resident of English Bazar, Malda.",
                    "SRC-007: Subrata Mukherjee, son of Late N. Mukherjee, resident of Dinhata Road, Cooch Behar (Title Suit 44/2024)."
                ],
                current_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        # Item 2: Subsidiary link between Rupali Transport & Vikramaditya Logistics
        queue.append(
            ReviewQueueItem(
                id="REV-002",
                item_type=ReviewItemType.GRAPH_EDGE,
                target_id="EDG-004",
                title="Verify Alleged Corporate Subsidiary Relationship (Rupali -> Vikramaditya)",
                description=(
                    "Single investigative report SRC-003 alleges Rupali Transport is a subsidiary of Vikramaditya Logistics. "
                    "Police release SRC-002 mentions vehicle ownership but does not confirm corporate subsidiary structure."
                ),
                machine_hypothesis="UNCONFIRMED - REQUIRES MCA-21 OFFICIAL FILINGS",
                machine_confidence="MODERATE",
                supporting_source_ids=["SRC-002", "SRC-003"],
                supporting_excerpts=[
                    "SRC-003: 'Rupali Transport' is a registered subsidiary of 'Vikramaditya Logistics'",
                    "SRC-002: Registered corporate owner of the carrier is Vikramaditya Logistics Private Limited."
                ],
                current_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        # Item 3: Contradiction in Seizure Weight (120 kg vs 200 kg)
        queue.append(
            ReviewQueueItem(
                id="REV-003",
                item_type=ReviewItemType.CONTRADICTION_RESOLUTION,
                target_id="CONTRA-002",
                title="Resolve Contradictory Seizure Quantity (120 kg vs 200 kg)",
                description=(
                    "Police press release states 120 kg; anonymous source in The Eastern Sentinel states 200 kg. "
                    "Derivative outlet Global Logistics Daily copied the 200 kg claim."
                ),
                machine_hypothesis="PREFER OFFICIAL SEIZURE MEMO (120 KG) PENDING CHARGESHEET",
                machine_confidence="HIGH",
                supporting_source_ids=["SRC-002", "SRC-003", "SRC-005"],
                supporting_excerpts=[
                    "SRC-002: Contraband consignment totaling 120 kilograms of suspected scheduled precursor chemicals seized.",
                    "SRC-003: customs clerk claims seizure ... totaled 200 kg."
                ],
                current_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        # Item 4: Audio Transcript Acoustic Uncertainty (Dhubri Boat Unloading)
        queue.append(
            ReviewQueueItem(
                id="REV-004",
                item_type=ReviewItemType.EVENT_RECORD,
                target_id="EVT-002",
                title="Acoustic Uncertainty Review: Dhubri Ghat Radio Broadcast Transcript",
                description=(
                    "Radio broadcast transcript (SRC-004) at timestamp [01:23] contains an explicitly uncertain phonetic token: "
                    "[uncertain: 'সন্দেজনক' / suspicious]. Human linguist verification required before drawing conclusions on cargo illegality."
                ),
                machine_hypothesis="TRANSCRIPTION UNCERTAINTY FLAGGED - AUDIO STT UNCONFIGURED",
                machine_confidence="MODERATE",
                supporting_source_ids=["SRC-004"],
                supporting_excerpts=[
                    "[01:23] [uncertain: 'সন্দেজনক' / suspicious cargo] Witnesses reported logistics signage..."
                ],
                current_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        # Item 5: Weak Signal Verification - Malda Broker Pivot
        queue.append(
            ReviewQueueItem(
                id="REV-005",
                item_type=ReviewItemType.WEAK_SIGNAL,
                target_id="SIG-002",
                title="Evaluate Weak Signal: Intermediary Broker 'P. K. Biswas' as Operational Shield",
                description=(
                    "Driver claims third-party broker hired him, potentially insulating fleet owners. "
                    "Analyst must decide whether to flag for priority field verification or classify as routine subcontracting."
                ),
                machine_hypothesis="CANDIDATE CONCEALMENT PATTERN - PENDING REGISTRY VERIFICATION",
                machine_confidence="MODERATE",
                supporting_source_ids=["SRC-002", "SRC-004"],
                supporting_excerpts=[
                    "Driver claims he was hired by a third-party intermediary named 'P. K. Biswas' operating out of Malda."
                ],
                current_status=VerificationStatus.NEEDS_VERIFICATION,
            )
        )

        return queue

    @classmethod
    def get_recommended_verification_steps(cls) -> List[Dict[str, Any]]:
        """Produces targeted, lawful follow-up recommendations."""
        return [
            {
                "step_number": 1,
                "title": "Ministry of Corporate Affairs (MCA-21) Registry Audit",
                "target_entities": ["Vikramaditya Logistics Private Limited (ENT-002)", "Rupali Transport (ENT-003)"],
                "lawful_source": "Public MCA-21 Portal (mca.gov.in) Master Data & Form AOC-4 (Financial Statements)",
                "objective": "Verify whether Rupali Transport is an incorporated subsidiary, affiliate, or unassociated third-party entity.",
                "priority": "HIGH",
            },
            {
                "step_number": 2,
                "title": "Judicial Seizure Memo & Chargesheet Inspection",
                "target_entities": ["Consignment WB-73-E-4421 (ENT-009)", "Subrata Mukherjee (ENT-001)"],
                "lawful_source": "Siliguri Additional Chief Judicial Magistrate (ACJM) Court Public Docket",
                "objective": "Resolve quantitative contradiction (120 kg vs 200 kg) by inspecting certified Police Form 53 seizure memo.",
                "priority": "HIGH",
            },
            {
                "step_number": 3,
                "title": "National Highway Toll RFID / FASTag Cross-Referencing",
                "target_entities": ["Carrier WB-73-E-4421 (ENT-009)"],
                "lawful_source": "Publicly available transport department verification / authorized NHAI toll plaza log queries",
                "objective": "Verify whether freight carrier crossed between Assam (Dhubri/Boxirhat barrier) and North Bengal between Oct 4-8.",
                "priority": "MODERATE",
            },
            {
                "step_number": 4,
                "title": "Linguistic & Acoustic Review of Dhubri Radio Broadcast",
                "target_entities": ["Audio Transcript (SRC-004)"],
                "lawful_source": "Authorized studio master recording of Asom Barta Radio broadcast (Oct 10, 2026)",
                "objective": "Resolve phonetic uncertainty at timecode [01:23] with native Assamese language specialist to confirm verbatim witness statements.",
                "priority": "MODERATE",
            },
            {
                "step_number": 5,
                "title": "Trade License Registry Verification in Malda",
                "target_entities": ["P. K. Biswas (ENT-006)"],
                "lawful_source": "English Bazar Municipality Trade License Portal, Malda",
                "objective": "Ascertain if 'P. K. Biswas' operates a registered commercial logistics brokerage or is an informal cut-out.",
                "priority": "LOW",
            },
        ]
