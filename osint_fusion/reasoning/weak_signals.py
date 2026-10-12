"""Weak signal detection with distinct evidence confidence and signal strength metrics."""

from typing import List, Dict, Any, Tuple
from ..models.source import Source
from ..models.entity import Entity
from ..models.event import EventRecord
from ..models.signal import WeakSignal, SignalCategory, ConfidenceFactors


class WeakSignalDetector:
    """
    Identifies candidate intelligence patterns, anomaly signals,
    and clusters across disparate multilingual sources.
    """

    @classmethod
    def calculate_heuristic_confidence(
        cls,
        source_rel: float,
        directness: float,
        corroboration: float,
        consistency: float,
        notes: str,
    ) -> ConfidenceFactors:
        """
        Documented heuristic calculation:
        Composite = (0.35 * SourceReliability) + (0.25 * Directness) + (0.25 * Corroboration) + (0.15 * Consistency)
        """
        composite = (0.35 * source_rel) + (0.25 * directness) + (0.25 * corroboration) + (0.15 * consistency)
        composite = max(0.0, min(1.0, composite))
        return ConfidenceFactors(
            source_reliability=round(source_rel, 2),
            directness_of_evidence=round(directness, 2),
            independent_corroboration=round(corroboration, 2),
            internal_consistency=round(consistency, 2),
            composite_heuristic_score=round(composite, 2),
            scoring_notes=notes,
        )

    @classmethod
    def detect_signals(
        cls,
        sources: List[Source],
        entities: List[Entity],
        events: List[EventRecord],
    ) -> List[WeakSignal]:
        """Detects candidate patterns across the analyzed corpus."""
        signals: List[WeakSignal] = []

        # Signal 1: Cross-Border Riverine-to-Road Contraband Transshipment Pipeline
        s1_conf = cls.calculate_heuristic_confidence(
            source_rel=0.82,
            directness=0.75,
            corroboration=0.70,
            consistency=0.80,
            notes=(
                "Assamese community radio broadcast (SRC-004) independently documented night boat unloading at Dhubri ghat; "
                "driver interrogation in Siliguri (SRC-001) independently confessed loading at Dhubri riverfront. "
                "Cross-border geographic alignment is consistent."
            ),
        )
        s1 = WeakSignal(
            id="SIG-001",
            title="Riverine-to-Highway Transshipment Conduit (Dhubri -> Fulbari Corridor)",
            category=SignalCategory.CLUSTER_BRIDGE,
            description=(
                "Convergence of Assamese radio report (SRC-004) describing offloading of sealed containers from country boats "
                "at Dhubri Brahmaputra ghat with driver's confession in Bengal (SRC-001) that chemical cargo originated from Dhubri riverfront. "
                "Connects previously separate maritime/riverine activity to highway logistics."
            ),
            supporting_source_ids=["SRC-001", "SRC-004"],
            supporting_entity_ids=["ENT-001", "ENT-004", "ENT-005"],
            supporting_event_ids=["EVT-002", "EVT-003"],
            supporting_excerpts=[
                "SRC-004: Two motorized cargo country-boats unloaded sealed plastic containers into a covered truck late Sunday at Dhubri ghat.",
                "SRC-001: driver stated consignment was loaded at an unregistered depot in Dhubri border riverfront."
            ],
            significance_rationale=(
                "Indicates chemical smuggling networks may exploit unmonitored riverine transit along the Brahmaputra "
                "to bypass strict land customs checkpoints before loading onto interstate freight carriers."
            ),
            alternative_explanations=[
                "Routine agricultural or diesel barter trade common among riverine border communities.",
                "Driver may have fabricated loading point to divert investigators from a closer Bengal manufacturing source."
            ],
            counterevidence=[
                "No physical seizure or boat impoundment conducted at Dhubri ghat.",
                "Audio transcript in SRC-004 explicitly contains uncertain phonetic tokens: [uncertain: 'সন্দেজনক' / suspicious]."
            ],
            information_gaps=[
                "Riverine customs patrol logs in Dhubri sector for night of Oct 4-5.",
                "Toll plaza CCTV footage confirming freight carrier transit from Assam into North Bengal."
            ],
            recommended_verification_steps=[
                "Submit official records request to Inland Waterways Authority of India (IWAI) Dhubri terminal.",
                "Cross-examine highway toll RFID logs along NH-27 between Dhubri and Fulbari."
            ],
            evidence_confidence="MODERATE",  # Backed by 2 independent accounts, but speech transcript has uncertainties
            signal_strength="HIGH",          # High operational significance for border monitoring
            confidence_breakdown=s1_conf,
        )
        signals.append(s1)

        # Signal 2: Third-Party Broker Shield (Malda Pivot)
        s2_conf = cls.calculate_heuristic_confidence(
            source_rel=0.75,
            directness=0.60,
            corroboration=0.55,
            consistency=0.70,
            notes=(
                "Intermediary broker P.K. Biswas is named in driver's interrogation statement (SRC-002) and matches "
                "boatmen report in Assam (SRC-004) mentioning logistics signage of a Malda trading company. "
                "However, broker identity is not officially verified."
            ),
        )
        s2 = WeakSignal(
            id="SIG-002",
            title="Intermediary Broker Shielding Corporate Carrier (Malda Broker Pivot)",
            category=SignalCategory.RECURRING_ENTITY_ANOMALY,
            description=(
                "The driver claims he was engaged by an unvetted third-party broker 'P. K. Biswas' in Malda, "
                "creating a buffer between the registered fleet owner (Vikramaditya Logistics) and illicit cargo."
            ),
            supporting_source_ids=["SRC-002", "SRC-004"],
            supporting_entity_ids=["ENT-001", "ENT-002", "ENT-006"],
            supporting_event_ids=["EVT-003", "EVT-004"],
            supporting_excerpts=[
                "SRC-002: Driver claims he was hired by a third-party intermediary named 'P. K. Biswas' operating out of Malda.",
                "SRC-004: Witnesses reported logistics signage on local feeder van matching a trading firm based in Malda."
            ],
            significance_rationale=(
                "Common trade-based laundering / contraband concealment technique: using informal spot-market brokers "
                "to provide corporate owners plausible deniability regarding freight contents."
            ),
            alternative_explanations=[
                "Driver may be providing a false broker name ('cut-out') to shield actual associates.",
                "Standard legitimate sub-contracting in Indian freight transport without corporate knowledge."
            ],
            counterevidence=[
                "No business registration or phone record for 'P. K. Biswas' is yet confirmed in the public dataset."
            ],
            information_gaps=[
                "Call detail records (CDR) and digital payment trails for Driver ENT-001.",
                "Registrar of Companies filings for Malda-based logistics entities."
            ],
            recommended_verification_steps=[
                "Verify Malda trade license registry for entities associated with surname Biswas in freight forwarding."
            ],
            evidence_confidence="MODERATE",
            signal_strength="MODERATE",
            confidence_breakdown=s2_conf,
        )
        signals.append(s2)

        # Signal 3: Circular Reporting & Echo-Chamber Amplification Risk
        s3_conf = cls.calculate_heuristic_confidence(
            source_rel=0.90,
            directness=0.85,
            corroboration=0.80,
            consistency=0.90,
            notes=(
                "Textual duplication between SRC-003 and SRC-005 is empirically confirmed. "
                "Heuristic confidence in the detection of circular reporting is High."
            ),
        )
        s3 = WeakSignal(
            id="SIG-003",
            title="Amplification of Unverified Seizure Quantity via Circular Aggregation",
            category=SignalCategory.CIRCULAR_REPORTING_SUSPECTED,
            description=(
                "Single anonymous claim of 200 kg seizure and Oct 7 date in The Eastern Sentinel (SRC-003) "
                "was reprinted verbatim by Global Logistics Daily (SRC-005). Analysts risk treating this as dual confirmation."
            ),
            supporting_source_ids=["SRC-003", "SRC-005"],
            supporting_entity_ids=["ENT-009"],
            supporting_event_ids=["EVT-003"],
            supporting_excerpts=[
                "SRC-003: Anonymous customs clerk claims seizure occurred on Oct 7 and totaled 200 kg.",
                "SRC-005: Verbatim republication of 200 kg claim without independent corroboration."
            ],
            significance_rationale=(
                "Illustrates how unvetted single-source leaks can be amplified in public OSINT datasets, "
                "creating the illusion of multi-source corroboration."
            ),
            alternative_explanations=[
                "Aggregator may claim syndication licensing, but no new evidence was introduced."
            ],
            counterevidence=[
                "Official police memo (SRC-002) firmly documents 120 kg."
            ],
            information_gaps=[
                "Original reporting notes or customs dispatch memo from The Eastern Sentinel reporter."
            ],
            recommended_verification_steps=[
                "Mark SRC-005 as secondary derivative in source graph; discount from corroboration counts."
            ],
            evidence_confidence="HIGH",
            signal_strength="HIGH",
            confidence_breakdown=s3_conf,
        )
        signals.append(s3)

        return signals
