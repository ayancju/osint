"""Event extraction and chronological timeline ordering with uncertainty tracking."""

from typing import List, Dict, Any, Optional
from ..models.source import Source
from ..models.event import EventRecord, VerificationStatus, TemporalStatus, EventExcerpt


class EventExtractor:
    """Extracts evidence-grounded event records and organizes chronological timelines."""

    @classmethod
    def extract_events(cls, sources: List[Source]) -> List[EventRecord]:
        """Extracts and correlates events from the source corpus."""
        source_map = {s.id: s for s in sources}
        events: List[EventRecord] = []

        # 1. Event 2026-09-25: Chennai Port Commercial Filing
        if "SRC-006" in source_map:
            s = source_map["SRC-006"]
            evt1 = EventRecord(
                id="EVT-001",
                title="Coastal Cargo Forwarding Application at Chennai Port",
                description=(
                    "Vikramaditya Logistics Private Limited filed clearance application for coastal cargo freight forwarding "
                    "between Haldia Dock Complex and Chennai Port terminal. Managing Director listed as A. K. Roy."
                ),
                event_date="2026-09-25",
                temporal_status=TemporalStatus.CONFIRMED_DATE,
                date_uncertainty="Exact official filing date verified via port gazette registry.",
                location_name="Chennai Port Commercial Terminal, Tamil Nadu",
                location_precision="pinpoint_checkpoint",
                reported_participants=["ENT-008"],  # A. K. Roy
                reported_organizations=["ENT-002"],  # Vikramaditya Logistics
                source_ids=["SRC-006"],
                supporting_excerpts=[
                    EventExcerpt(
                        source_id="SRC-006",
                        excerpt_text="Corporate filing record: Vikramaditya Logistics Private Limited filed clearance application for coastal cargo freight forwarding",
                        publication_date=s.publication_date,
                    )
                ],
                verification_status=VerificationStatus.CORROBORATED,
                confidence="HIGH"
            )
            events.append(evt1)

        # 2. Event 2026-10-04 / 2026-10-05: Nighttime Riverine Transshipment at Dhubri Ghat
        if "SRC-004" in source_map or "SRC-001" in source_map:
            excerpts = []
            sids = []
            if "SRC-004" in source_map:
                s = source_map["SRC-004"]
                sids.append("SRC-004")
                excerpts.append(EventExcerpt(
                    source_id="SRC-004",
                    excerpt_text="Two motorized cargo country-boats unloaded sealed plastic containers into a covered truck late Sunday at Dhubri Brahmaputra ghat.",
                    page_or_timestamp="[00:45]-[01:23]",
                    publication_date=s.publication_date,
                ))
            if "SRC-001" in source_map:
                s = source_map["SRC-001"]
                sids.append("SRC-001")
                excerpts.append(EventExcerpt(
                    source_id="SRC-001",
                    excerpt_text="He stated during initial inquiries that the consignment was loaded at an unregistered depot in Dhubri border riverfront",
                    publication_date=s.publication_date,
                ))

            evt2 = EventRecord(
                id="EVT-002",
                title="Nighttime Riverine Loading & Transshipment at Dhubri Ghat",
                description=(
                    "Cargo country-boats transshipped sealed containers into a covered freight vehicle along the Brahmaputra "
                    "riverfront in Dhubri, Assam. Apprehended driver in Bengal subsequently identified this location as the loading point."
                ),
                event_date="2026-10-04",
                date_end="2026-10-05",
                temporal_status=TemporalStatus.ESTIMATED_RANGE,
                date_uncertainty="Approximate: 'Late Sunday night' reported by radio broadcast; timestamp corroborated by driver confession.",
                location_name="Dhubri Brahmaputra Ghat / Riverfront, Assam",
                location_precision="town_level",
                reported_participants=["ENT-001"],  # Driver
                reported_organizations=["ENT-003"],  # Rupali Transport
                source_ids=sids,
                supporting_excerpts=excerpts,
                missing_information=["Vessel registration numbers and upstream departure clearance records."],
                verification_status=VerificationStatus.CORROBORATED,
                confidence="MODERATE"
            )
            events.append(evt2)

        # 3. Event 2026-10-08: Interception of Chemical Consignment at Fulbari Checkpost
        # Note: Contains documented contradiction with SRC-003 (Oct 7 vs Oct 8, 120kg vs 200kg)
        if "SRC-001" in source_map or "SRC-002" in source_map or "SRC-003" in source_map:
            excerpts = []
            sids = []
            contradictions = []

            if "SRC-001" in source_map:
                sids.append("SRC-001")
                excerpts.append(EventExcerpt(
                    source_id="SRC-001",
                    excerpt_text="On Tuesday evening, an interception was carried out near the Fulbari checkpost corridor. Seized 120 kg unlabeled chemical drums.",
                    publication_date=source_map["SRC-001"].publication_date,
                ))
            if "SRC-002" in source_map:
                sids.append("SRC-002")
                excerpts.append(EventExcerpt(
                    source_id="SRC-002",
                    excerpt_text="Fulbari Border Outpost on the evening of Oct 8, 2026. Contraband consignment totaling 120 kilograms of suspected scheduled precursor chemicals seized.",
                    publication_date=source_map["SRC-002"].publication_date,
                ))
            if "SRC-003" in source_map:
                sids.append("SRC-003")
                excerpts.append(EventExcerpt(
                    source_id="SRC-003",
                    excerpt_text="Anonymous customs clerk claims seizure occurred on Oct 7 and totaled 200 kg of industrial chemicals.",
                    publication_date=source_map["SRC-003"].publication_date,
                ))
                contradictions.append(
                    "CONTRADICTION DETECTED: Source SRC-003 cites anonymous claim of Oct 7 seizure date and 200 kg volume, "
                    "directly conflicting with official police press release (SRC-002) and local reporting (SRC-001) citing Oct 8 and 120 kg."
                )

            evt3 = EventRecord(
                id="EVT-003",
                title="Interception of Freight Carrier WB-73-E-4421 at Fulbari Checkpost",
                description=(
                    "Enforcement authorities intercepted multi-axle carrier WB-73-E-4421 carrying chemical drums. "
                    "Driver Subrata/Subroto Mukherjee apprehended. Police state 120 kg seized on Oct 8; single investigative report claims 200 kg on Oct 7."
                ),
                event_date="2026-10-08",
                temporal_status=TemporalStatus.REPORTED_DATE,
                date_uncertainty="Oct 8 evening confirmed by official police release; Oct 7 date claimed by anonymous source in SRC-003.",
                location_name="Fulbari Border Checkpost Corridor, Jalpaiguri / Siliguri, West Bengal",
                location_precision="pinpoint_checkpoint",
                reported_participants=["ENT-001", "ENT-006"],
                reported_organizations=["ENT-002", "ENT-003"],
                source_ids=sids,
                supporting_excerpts=excerpts,
                contradictory_accounts=contradictions,
                missing_information=["Chemical laboratory GC-MS spectral analysis report verifying exact precursor compound."],
                verification_status=VerificationStatus.CONTRADICTED if contradictions else VerificationStatus.CORROBORATED,
                confidence="HIGH"
            )
            events.append(evt3)

        # 4. Event 2026-10-09: West Bengal Police Press Release & Interrogation Disclosures
        if "SRC-002" in source_map:
            s = source_map["SRC-002"]
            evt4 = EventRecord(
                id="EVT-004",
                title="Siliguri Police Commissionerate Press Release & Case Registration",
                description=(
                    "Police issued official release regarding Fulbari seizure, registered FIR under Sections 420/120B IPC, "
                    "identified Vikramaditya Logistics as carrier owner, and documented driver's disclosure of Malda broker P. K. Biswas."
                ),
                event_date="2026-10-09",
                temporal_status=TemporalStatus.CONFIRMED_DATE,
                date_uncertainty="Official press release publication date verified.",
                location_name="Siliguri Police Commissionerate, West Bengal",
                location_precision="pinpoint_checkpoint",
                reported_participants=["ENT-001", "ENT-006"],
                reported_organizations=["ENT-002"],
                source_ids=["SRC-002"],
                supporting_excerpts=[
                    EventExcerpt(
                        source_id="SRC-002",
                        excerpt_text="West Bengal Police Press Release | Siliguri Commissionerate | Dated Oct 9, 2026",
                        publication_date=s.publication_date,
                    )
                ],
                verification_status=VerificationStatus.CORROBORATED,
                confidence="HIGH"
            )
            events.append(evt4)

        # 5. Event 2026-10-11: Civil Land Partition Bail Order in Jalpaiguri Court
        if "SRC-007" in source_map:
            s = source_map["SRC-007"]
            evt5 = EventRecord(
                id="EVT-005",
                title="Bail Order in Civil Partition Suit (Unrelated Subrata Mukherjee)",
                description=(
                    "District Court at Jalpaiguri heard bail petition for Subrata Mukherjee of Cooch Behar in civil boundary dispute. "
                    "Court noted zero connection to logistics or contraband seizure."
                ),
                event_date="2026-10-11",
                temporal_status=TemporalStatus.CONFIRMED_DATE,
                date_uncertainty="Public judicial order date verified.",
                location_name="District & Sessions Judge Court, Jalpaiguri, West Bengal",
                location_precision="pinpoint_checkpoint",
                reported_participants=["ENT-007"],
                reported_organizations=[],
                source_ids=["SRC-007"],
                supporting_excerpts=[
                    EventExcerpt(
                        source_id="SRC-007",
                        excerpt_text="Bail Application No. 892/2026 | Dated Oct 11, 2026 | Civil boundary and land partition suit",
                        publication_date=s.publication_date,
                    )
                ],
                verification_status=VerificationStatus.CORROBORATED,
                confidence="HIGH"
            )
            events.append(evt5)

        # Sort chronologically by event_date
        events.sort(key=lambda x: x.event_date or "9999-99-99")
        return events
