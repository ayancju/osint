# OSINT Multi-Source Cross-Border Logistics Assessment
**Report ID:** `REP-2026-FC7A7C` | **Classification:** `UNCLASSIFIED // OSINT ONLY // FOR ANALYST EVALUATION ONLY` | **Generated:** 2026-10-12T09:12:01.436403+00:00
**Prepared by:** OSINT Fusion Workbench Agent

---

## 1. Executive Summary

> [!IMPORTANT]
> **Overall Confidence Posture:** MODERATE-HIGH (Official records corroboration high; intermediary broker and transshipment links remain investigative hypotheses).

### Key Findings
- Official law enforcement and local media corroborate the interception of heavy freight carrier WB-73-E-4421 near Fulbari checkpost with 120 kg of unlabeled chemical drums.
- Carrier corporate ownership is traced to Vikramaditya Logistics Private Limited via official police release; however, operational management was attributed to Rupali Transport.
- Conservative entity resolution successfully identified and isolated two distinct individuals named Subrata Mukherjee (the apprehended driver in Malda vs an unassociated civil land litigant in Cooch Behar), preventing false association.
- Cross-lingual synthesis between Assamese radio and Bengali driver statements indicates a plausible riverine transshipment origin at Dhubri Brahmaputra ghat.
- Circular reporting was empirically detected: Source SRC-005 reprinted unverified claims from SRC-003 regarding an earlier Oct 7 seizure date and 200 kg volume.

### Critical Caveats & Limitations
- ⚠️ Evidence confidence is heuristic and does NOT constitute legal proof of corporate conspiracy or criminal intent.
- ⚠️ No live acoustic speech-to-text pipeline was connected; radio transcripts rely on human certification with documented acoustic uncertainty at timestamp 01:23.
- ⚠️ Chemical composition of seized cargo remains unverified pending forensic laboratory GC-MS spectral reports.
- ⚠️ All findings require human analyst review before operational dissemination.

---

## 2. Scope and Sources

Analysis conducted across 7 public, lawful intelligence items spanning 5 languages (Assamese, English, Hindi, Mixed (Assamese + Latin/Regional), Mixed (Tamil + Latin/Regional)), including regional newspapers, police press releases, judicial court records, commercial gazettes, and authorized community radio transcripts.

**Total Sources:** 7 | **Languages Analyzed:** Assamese, English, Hindi, Mixed (Assamese + Latin/Regional), Mixed (Tamil + Latin/Regional)

| Source ID | Title | Publishing Org | Type | Language | Pub Date | Reliability |
|---|---|---|---|---|---|---|
| `SRC-001` | ফুলবাড়ি সীমান্তে রাসায়নিক বোঝাই লরি আটক,... | উত্তরবঙ্গ সংবাদ (Uttarbanga Sambad) | news_article | Assamese | 2026-10-08 | 0.78 |
| `SRC-002` | फुलबाड़ी चौकी पर संदिग्ध रासायनिक पदार्थ... | পশ্চিমবঙ্গ পুলিশ (West Bengal Police / Siliguri Commissionerate) | police_report | Hindi | 2026-10-09 | 0.92 |
| `SRC-003` | Discrepancies Emerge in Fulbari Chemical... | The Eastern Sentinel (Investigative Desk) | investigative_report | English | 2026-10-10 | 0.72 |
| `SRC-004` | ধুবুৰী ঘাটত নদীপথেৰে সন্দেহজনক সামগ্ৰী উ... | অসম বাৰ্তা (Asom Barta Community Radio, Dhubri Studio) | audio_broadcast | Mixed (Assamese + Latin/Regional) | 2026-10-10 | 0.74 |
| `SRC-005` | Fulbari Seizure Raises Questions Over Vi... | Global Logistics Daily (Aggregator Portal) | secondary_aggregator | English | 2026-10-11 | 0.45 |
| `SRC-006` | சென்னை துறைமுக சரக்குக் கையாளுதல் உரிமம்... | சென்னை துறைமுக வர்த்தக அரசிதழ் (Chennai Port Commercial Gazette) | commerce_registry | Mixed (Tamil + Latin/Regional) | 2026-09-25 | 0.96 |
| `SRC-007` | Order in Bail Application 892/2026 (Subr... | District & Sessions Judge Court, Jalpaiguri Division | court_document | English | 2026-10-11 | 0.98 |

#### Unavailable or Unaccessed Sources
- 🔒 Live acoustic radio feed / raw PCM audio files (processed via authorized timestamped text transcript).
- 🔒 Direct Ministry of Corporate Affairs (MCA-21) balance sheet annexures (pending field request).
- 🔒 Inland river customs patrol logs at Dhubri Sector (pending official request).

---

## 3. Key Entities

Extracted 9 discrete entities across person, organization, location, and infrastructure classes.

> [!NOTE]
> Conservative resolution protocols were strictly enforced: name collisions were not merged without matching parentage, residence, or corroborated contextual identity. ENT-001 and ENT-007 remain strictly separate.

| Entity ID | Canonical Name | Type | Involvement | Status | Observed Dates | Sources |
|---|---|---|---|---|---|---|
| `ENT-001` | **Subrata Mukherjee (Driver / Malda)** | `PERSON` | REPORTED_PARTICIPANT | DISTINCT | 2026-10-08 to 2026-10-09 | `SRC-001`, `SRC-002` |
| `ENT-003` | **Rupali Transport** | `ORGANIZATION` | REPORTED_PARTICIPANT | DISTINCT | 2026-10-08 to 2026-10-10 | `SRC-001`, `SRC-003`, `SRC-005` |
| `ENT-004` | **Fulbari Border Checkpost** | `LOCATION` | REPORTED_PARTICIPANT | DISTINCT | N/A | `SRC-001`, `SRC-002`, `SRC-003`, `SRC-005` |
| `ENT-005` | **Dhubri Riverine Port / Brahmaputra Ghat** | `LOCATION` | REPORTED_PARTICIPANT | DISTINCT | N/A | `SRC-001`, `SRC-004` |
| `ENT-009` | **Freight Carrier WB-73-E-4421** | `INFRASTRUCTURE` | CONFIRMED_ACTOR | DISTINCT | 2026-10-08 to 2026-10-10 | `SRC-001`, `SRC-002` |
| `ENT-002` | **Vikramaditya Logistics Private Limited** | `ORGANIZATION` | REPORTED_PARTICIPANT | DISTINCT | 2026-09-25 to 2026-10-11 | `SRC-002`, `SRC-003`, `SRC-005`, `SRC-006` |
| `ENT-006` | **P. K. Biswas (Logistics Broker)** | `PERSON` | MENTIONED_ONLY | DISTINCT | 2026-10-09 to 2026-10-09 | `SRC-002` |
| `ENT-008` | **A. K. Roy (Managing Director)** | `PERSON` | MENTIONED_ONLY | DISTINCT | 2026-09-25 to 2026-09-25 | `SRC-006` |
| `ENT-007` | **Subrata Mukherjee (Cooch Behar / Civil Litigant)** | `PERSON` | MENTIONED_ONLY | DISTINCT | 2026-10-11 to 2026-10-11 | `SRC-007` |

---

## 4. Event Timeline

Reconstructed 5 chronological event anchors spanning from Sept 25 to Oct 11, 2026.

| Event ID | Date / Range | Event Title | Precision & Location | Verification Status | Sources |
|---|---|---|---|---|---|
| `EVT-001` | 2026-09-25 | Coastal Cargo Forwarding Application at Chennai Port | Chennai Port Commercial Terminal, Tamil Nadu (pinpoint_checkpoint) | `corroborated` | `SRC-006` |
| `EVT-002` | 2026-10-04 to 2026-10-05 | Nighttime Riverine Loading & Transshipment at Dhubri Ghat | Dhubri Brahmaputra Ghat / Riverfront, Assam (town_level) | `corroborated` | `SRC-004`, `SRC-001` |
| `EVT-003` | 2026-10-08 | Interception of Freight Carrier WB-73-E-4421 at Fulbari Checkpost | Fulbari Border Checkpost Corridor, Jalpaiguri / Siliguri, West Bengal (pinpoint_checkpoint) | `contradicted` | `SRC-001`, `SRC-002`, `SRC-003` |
| `EVT-004` | 2026-10-09 | Siliguri Police Commissionerate Press Release & Case Registration | Siliguri Police Commissionerate, West Bengal (pinpoint_checkpoint) | `corroborated` | `SRC-002` |
| `EVT-005` | 2026-10-11 | Bail Order in Civil Partition Suit (Unrelated Subrata Mukherjee) | District & Sessions Judge Court, Jalpaiguri, West Bengal (pinpoint_checkpoint) | `corroborated` | `SRC-007` |

#### Documented Temporal Uncertainties
- ⏳ EVT-002: Dhubri river transshipment date estimated as 'late Sunday' (Oct 4-5) from radio eyewitnesses.
- ⏳ EVT-003: Interception date contradiction (Oct 8 in official police memo vs Oct 7 in anonymous leak).

---

## 5. Knowledge Graph

Constructed knowledge graph encompassing 21 nodes and 10 typed edges. Direct evidentiary links are clearly separated from inferred analytical hypotheses.

### Mermaid Graph Visualization

```mermaid
graph TD
    SRC-001["📰 [SRC-001] উত্তরবঙ্গ সংবাদ (Uttarbanga Sambad)"]
    SRC-002["📰 [SRC-002] পশ্চিমবঙ্গ পুলিশ (West Bengal Police / Siliguri Commissionerate)"]
    SRC-003["📰 [SRC-003] The Eastern Sentinel (Investigative Desk)"]
    SRC-004["📰 [SRC-004] অসম বাৰ্তা (Asom Barta Community Radio, Dhubri Studio)"]
    SRC-005["📰 [SRC-005] Global Logistics Daily (Aggregator Portal)"]
    SRC-006["📰 [SRC-006] சென்னை துறைமுக வர்த்தக அரசிதழ் (Chennai Port Commercial Gazette)"]
    SRC-007["📰 [SRC-007] District & Sessions Judge Court, Jalpaiguri Division"]
    ENT-001["👤 Subrata Mukherjee (Driver / Malda)"]
    ENT-003["🏢 Rupali Transport"]
    ENT-004["📍 Fulbari Border Checkpost"]
    ENT-005["📍 Dhubri Riverine Port / Brahmaputra Ghat"]
    ENT-009["📦 Freight Carrier WB-73-E-4421"]
    ENT-002["🏢 Vikramaditya Logistics Private Limited"]
    ENT-006["👤 P. K. Biswas (Logistics Broker)"]
    ENT-008["👤 A. K. Roy (Managing Director)"]
    ENT-007["👤 Subrata Mukherjee (Cooch Behar / Civil Litigant)"]
    EVT-001["⚡ Coastal Cargo Forwarding Application at Chennai Port"]
    EVT-002["⚡ Nighttime Riverine Loading & Transshipment at Dhubri Ghat"]
    EVT-003["⚡ Interception of Freight Carrier WB-73-E-4421 at Fulbari Checkpost"]
    EVT-004["⚡ Siliguri Police Commissionerate Press Release & Case Registration"]
    EVT-005["⚡ Bail Order in Civil Partition Suit (Unrelated Subrata Mukherjee)"]
    SRC-001 -->|"mentions driver"| ENT-001
    SRC-002 -->|"identifies apprehended driver"| ENT-001
    ENT-001 -->|"reported driving carrier for"| ENT-003
    ENT-003 -.->|inferred||"alleged subsidiary / operating partner"| ENT-002
    ENT-002 -->|"registered corporate vehicle owner"| ENT-009
    EVT-003 -->|"intercepted at"| ENT-004
    EVT-002 -.->|inferred||"cross-border cargo origin route"| EVT-003
    ENT-008 -->|"registered Managing Director"| ENT-002
    ENT-001 -->|"hired by broker"| ENT-006
    SRC-005 -->|"circular copycat / derivative reprint"| SRC-003
```

### Key Supported Relationships
| Edge ID | Source Node | Predicate | Target Node | Direct Evidence | Status | Sources |
|---|---|---|---|---|---|---|
| `EDG-001` | `SRC-001` | **mentions driver** | `ENT-001` | Direct | `corroborated` | `SRC-001` |
| `EDG-002` | `SRC-002` | **identifies apprehended driver** | `ENT-001` | Direct | `corroborated` | `SRC-002` |
| `EDG-003` | `ENT-001` | **reported driving carrier for** | `ENT-003` | Direct | `needs_verification` | `SRC-001` |
| `EDG-004` | `ENT-003` | **alleged subsidiary / operating partner** | `ENT-002` | Inferred | `needs_verification` | `SRC-003` |
| `EDG-005` | `ENT-002` | **registered corporate vehicle owner** | `ENT-009` | Direct | `corroborated` | `SRC-002` |
| `EDG-006` | `EVT-003` | **intercepted at** | `ENT-004` | Direct | `corroborated` | `SRC-001`, `SRC-002` |
| `EDG-007` | `EVT-002` | **cross-border cargo origin route** | `EVT-003` | Inferred | `needs_verification` | `SRC-001`, `SRC-004` |
| `EDG-008` | `ENT-008` | **registered Managing Director** | `ENT-002` | Direct | `corroborated` | `SRC-006` |
| `EDG-009` | `ENT-001` | **hired by broker** | `ENT-006` | Direct | `needs_verification` | `SRC-002` |
| `EDG-010` | `SRC-005` | **circular copycat / derivative reprint** | `SRC-003` | Direct | `contradicted` | `SRC-005` |

---

## 6. Weak Signals

Identified 3 cross-source candidate signals evaluating anomalous routing, broker shielding, and aggregation echo-chambers.

### 🔍 [SIG-001] Riverine-to-Highway Transshipment Conduit (Dhubri -> Fulbari Corridor)
- **Category:** `cluster_bridge`
- **Evidence Confidence:** `MODERATE` | **Signal Strength:** `HIGH` | **Heuristic Score:** `0.77`
- **Description:** Convergence of Assamese radio report (SRC-004) describing offloading of sealed containers from country boats at Dhubri Brahmaputra ghat with driver's confession in Bengal (SRC-001) that chemical cargo originated from Dhubri riverfront. Connects previously separate maritime/riverine activity to highway logistics.
- **Significance:** Indicates chemical smuggling networks may exploit unmonitored riverine transit along the Brahmaputra to bypass strict land customs checkpoints before loading onto interstate freight carriers.
- **Alternative Explanations & Counterevidence:**
  * Alternative: Routine agricultural or diesel barter trade common among riverine border communities.
  * Alternative: Driver may have fabricated loading point to divert investigators from a closer Bengal manufacturing source.
  * Counterevidence: No physical seizure or boat impoundment conducted at Dhubri ghat.
  * Counterevidence: Audio transcript in SRC-004 explicitly contains uncertain phonetic tokens: [uncertain: 'সন্দেজনক' / suspicious].
- **Information Gaps:** Riverine customs patrol logs in Dhubri sector for night of Oct 4-5.; Toll plaza CCTV footage confirming freight carrier transit from Assam into North Bengal.
- **Recommended Verification:** Submit official records request to Inland Waterways Authority of India (IWAI) Dhubri terminal.; Cross-examine highway toll RFID logs along NH-27 between Dhubri and Fulbari.

### 🔍 [SIG-002] Intermediary Broker Shielding Corporate Carrier (Malda Broker Pivot)
- **Category:** `recurring_entity_anomaly`
- **Evidence Confidence:** `MODERATE` | **Signal Strength:** `MODERATE` | **Heuristic Score:** `0.66`
- **Description:** The driver claims he was engaged by an unvetted third-party broker 'P. K. Biswas' in Malda, creating a buffer between the registered fleet owner (Vikramaditya Logistics) and illicit cargo.
- **Significance:** Common trade-based laundering / contraband concealment technique: using informal spot-market brokers to provide corporate owners plausible deniability regarding freight contents.
- **Alternative Explanations & Counterevidence:**
  * Alternative: Driver may be providing a false broker name ('cut-out') to shield actual associates.
  * Alternative: Standard legitimate sub-contracting in Indian freight transport without corporate knowledge.
  * Counterevidence: No business registration or phone record for 'P. K. Biswas' is yet confirmed in the public dataset.
- **Information Gaps:** Call detail records (CDR) and digital payment trails for Driver ENT-001.; Registrar of Companies filings for Malda-based logistics entities.
- **Recommended Verification:** Verify Malda trade license registry for entities associated with surname Biswas in freight forwarding.

### 🔍 [SIG-003] Amplification of Unverified Seizure Quantity via Circular Aggregation
- **Category:** `circular_reporting_suspected`
- **Evidence Confidence:** `HIGH` | **Signal Strength:** `HIGH` | **Heuristic Score:** `0.86`
- **Description:** Single anonymous claim of 200 kg seizure and Oct 7 date in The Eastern Sentinel (SRC-003) was reprinted verbatim by Global Logistics Daily (SRC-005). Analysts risk treating this as dual confirmation.
- **Significance:** Illustrates how unvetted single-source leaks can be amplified in public OSINT datasets, creating the illusion of multi-source corroboration.
- **Alternative Explanations & Counterevidence:**
  * Alternative: Aggregator may claim syndication licensing, but no new evidence was introduced.
  * Counterevidence: Official police memo (SRC-002) firmly documents 120 kg.
- **Information Gaps:** Original reporting notes or customs dispatch memo from The Eastern Sentinel reporter.
- **Recommended Verification:** Mark SRC-005 as secondary derivative in source graph; discount from corroboration counts.

---

## 7. Contradictions and Gaps

### Cross-Source Factual Contradictions
#### ⚡ [CONTRA-001] Discrepancy: TEMPORAL / SEIZURE DATE
- **Account A (SRC-001, SRC-002):** Tuesday evening, October 8, 2026 (*Official Police Commissionerate Release and Local Press dispatch*)
- **Account B (SRC-003, SRC-005):** Monday, October 7, 2026 (*Single anonymous customs clerk interview in investigative dispatch*)
- **Assessment:** RESOLVED IN FAVOR OF OFFICIAL TIMELINE FOR SEIZURE (Oct 8). However, Oct 7 date may correspond to the earlier riverine transshipment in Assam (EVT-002) rather than the highway checkpost seizure in Siliguri.
- **Verification Route:** Request certified General Diary (GD) entry copy from Fulbari Border Outpost.

#### ⚡ [CONTRA-002] Discrepancy: QUANTITATIVE / CONTRABAND VOLUME
- **Account A (SRC-001, SRC-002):** 120 kilograms (unlabeled chemical drums) (*Police seizure memo recorded in official press statement*)
- **Account B (SRC-003, SRC-005):** 200 kilograms (suspected industrial precursors) (*Investigative report citing unnamed customs clerk*)
- **Assessment:** DISCREPANCY UNRESOLVED. Formal chargesheet will govern legal fact. Possibility exists that 200 kg represents gross drum weight while 120 kg represents net chemical compound, or that part of consignment was offloaded prior to checkpost interception.
- **Verification Route:** Examine official court seizure list / Malkhana register extract in Judicial Magistrate Court.

### Circular Reporting & Duplication Identified
> [!WARNING]
> **CIRC-001: SECONDARY_AGGREGATOR_REPRINT**
> Source SRC-005 ('Global Logistics Daily') republishes the exact narrative and anonymous claims from SRC-003 ('The Eastern Sentinel') without field reporting, independent customs interviews, or official attribution.
> *CRITICAL AUDIT CAVEAT: Do NOT treat SRC-005 as independent corroboration of SRC-003's claims (such as the 200 kg quantity or Oct 7 date). The corroboration count remains exactly 1, not 2.*

### Unanswered Analytical Questions
- ❓ What exact chemical substance was contained in the seized unlabeled drums (chemical CAS registry / schedule)?
- ❓ Did carrier WB-73-E-4421 transit directly from Dhubri via NH-27, and what toll barriers logged its passage?
- ❓ Is 'P. K. Biswas' a registered freight contractor or an informal alias used for deniability?
- ❓ What is the formal corporate relationship between Rupali Transport and Vikramaditya Logistics under MCA-21 filings?

---

## 8. Analyst Review Queue

Human oversight queue contains 5 verification items awaiting or under analyst disposition.

| Review ID | Item Type | Target | Title | Machine Hypothesis | Status |
|---|---|---|---|---|---|
| `REV-001` | `entity_match` | `ENT-001` | Verify Conservative Disambiguation: Subrata Mukherjee (Driver vs Civil Litigant) | MAINTAIN STRICTLY SEPARATE - DO NOT MERGE | `needs_verification` |
| `REV-002` | `graph_edge` | `EDG-004` | Verify Alleged Corporate Subsidiary Relationship (Rupali -> Vikramaditya) | UNCONFIRMED - REQUIRES MCA-21 OFFICIAL FILINGS | `needs_verification` |
| `REV-003` | `contradiction_resolution` | `CONTRA-002` | Resolve Contradictory Seizure Quantity (120 kg vs 200 kg) | PREFER OFFICIAL SEIZURE MEMO (120 KG) PENDING CHARGESHEET | `needs_verification` |
| `REV-004` | `event_record` | `EVT-002` | Acoustic Uncertainty Review: Dhubri Ghat Radio Broadcast Transcript | TRANSCRIPTION UNCERTAINTY FLAGGED - AUDIO STT UNCONFIGURED | `needs_verification` |
| `REV-005` | `weak_signal` | `SIG-002` | Evaluate Weak Signal: Intermediary Broker 'P. K. Biswas' as Operational Shield | CANDIDATE CONCEALMENT PATTERN - PENDING REGISTRY VERIFICATION | `needs_verification` |

---

## 9. Recommended Verification Steps

### Step 1: Ministry of Corporate Affairs (MCA-21) Registry Audit (Priority: `HIGH`)
- **Target Entities:** Vikramaditya Logistics Private Limited (ENT-002), Rupali Transport (ENT-003)
- **Lawful Source:** Public MCA-21 Portal (mca.gov.in) Master Data & Form AOC-4 (Financial Statements)
- **Objective:** Verify whether Rupali Transport is an incorporated subsidiary, affiliate, or unassociated third-party entity.

### Step 2: Judicial Seizure Memo & Chargesheet Inspection (Priority: `HIGH`)
- **Target Entities:** Consignment WB-73-E-4421 (ENT-009), Subrata Mukherjee (ENT-001)
- **Lawful Source:** Siliguri Additional Chief Judicial Magistrate (ACJM) Court Public Docket
- **Objective:** Resolve quantitative contradiction (120 kg vs 200 kg) by inspecting certified Police Form 53 seizure memo.

### Step 3: National Highway Toll RFID / FASTag Cross-Referencing (Priority: `MODERATE`)
- **Target Entities:** Carrier WB-73-E-4421 (ENT-009)
- **Lawful Source:** Publicly available transport department verification / authorized NHAI toll plaza log queries
- **Objective:** Verify whether freight carrier crossed between Assam (Dhubri/Boxirhat barrier) and North Bengal between Oct 4-8.

### Step 4: Linguistic & Acoustic Review of Dhubri Radio Broadcast (Priority: `MODERATE`)
- **Target Entities:** Audio Transcript (SRC-004)
- **Lawful Source:** Authorized studio master recording of Asom Barta Radio broadcast (Oct 10, 2026)
- **Objective:** Resolve phonetic uncertainty at timecode [01:23] with native Assamese language specialist to confirm verbatim witness statements.

### Step 5: Trade License Registry Verification in Malda (Priority: `LOW`)
- **Target Entities:** P. K. Biswas (ENT-006)
- **Lawful Source:** English Bazar Municipality Trade License Portal, Malda
- **Objective:** Ascertain if 'P. K. Biswas' operates a registered commercial logistics brokerage or is an informal cut-out.

---

## 10. Evidence Appendix

### Verbatim Source Excerpts & Provenance Registry

#### [SRC-001] উত্তরবঙ্গ সংবাদ (Uttarbanga Sambad) — ফুলবাড়ি সীমান্তে রাসায়নিক বোঝাই লরি আটক, চালক ধৃত
- **Language:** Assamese | **Locator:** Page 3, Column 2
- **Original Script:**
> শিলিগুড়ি, ৮ অক্টোবর: মঙ্গলবার সন্ধ্যায় ফুলবাড়ি চেকপোস্ট করিডোরে স্থানীয় পুলিশ ও আবগারি বাহিনীর যৌথ অভিযানে একটি ১০ চাকার মালবাহী লরি আটক করা হয়। গাড়িটি 'রূপালী ট্রান্সপোর্ট' সংস্থার অধীনে চলছিল (রেজিস...
- **English Translation:**
> [MACHINE-TRANSLATED: BENGALI -> ENGLISH]
Siliguri, Oct 8: On Tuesday evening, an interception was carried out near the Fulbari checkpost corridor by local authorities. A 10-wheel freight carrier beari...

#### [SRC-002] পশ্চিমবঙ্গ পুলিশ (West Bengal Police / Siliguri Commissionerate) — फुलबाड़ी चौकी पर संदिग्ध रासायनिक पदार्थ की बरामदगी बाबत आधिकारिक प्रेस विज्ञप्ति
- **Language:** Hindi | **Locator:** Official Bulletin 1/1
- **Original Script:**
> पश्चिम बंगाल पुलिस विज्ञप्ति | सिलीगुड़ी पुलिस कमिश्नरेट | दिनांक ०९ अक्टूबर २०२६:
दिनांक ०८ अक्टूबर २०२६ की संध्या को फुलबाड़ी सीमा चौकी पर विशेष तलाशी अभियान के दौरान एक भारी मालवाहक वाहन (पंजीकरण स...
- **English Translation:**
> [MACHINE-TRANSLATED: HINDI -> ENGLISH]
West Bengal Police Press Release | Siliguri Commissionerate | Dated Oct 9, 2026:
Official statement regarding seizure at Fulbari Border Outpost on the evening of...

#### [SRC-003] The Eastern Sentinel (Investigative Desk) — Discrepancies Emerge in Fulbari Chemical Interception as Subsidiary Ties Surface
- **Language:** English | **Locator:** Online Edition
- **Original Script:**
> SILIGURI / KOLKATA — The interception of a chemical freight carrier at the Fulbari border corridor has exposed a tangled web of interstate logistics operations. According to corporate filings, 'Rupali...
- **English Translation:**
> SILIGURI / KOLKATA — The interception of a chemical freight carrier at the Fulbari border corridor has exposed a tangled web of interstate logistics operations. According to corporate filings, 'Rupali...

#### [SRC-004] অসম বাৰ্তা (Asom Barta Community Radio, Dhubri Studio) — ধুবুৰী ঘাটত নদীপথেৰে সন্দেহজনক সামগ্ৰী উঠা-নমাৰ অভিযোগ
- **Language:** Mixed (Assamese + Latin/Regional) | **Locator:** N/A
- **Original Script:**
> [সম্প্ৰচাৰ সময়: ১০ অক্টোবৰ ২০২৬, পুৱা ০৭:৩০ বজা | অসম বাৰ্তা ৰেডিঅ', ধুবুৰী কেন্দ্ৰ]
[00:04] বাতৰি পঢ়িছো অনামিকা বৰুৱা। ধুবুৰী ব্ৰহ্মপুত্ৰ ঘাটত নদীপথেৰে অস্বাভাৱিক সামগ্ৰী পৰিবহণৰ তথ্য পোহৰলৈ আহিছে।
...
- **English Translation:**
> [MACHINE-TRANSLATED: ASSAMESE -> ENGLISH | SPEECH-TO-TEXT WITH UNCERTAINTIES]
[Broadcast Time: Oct 10, 2026, 07:30 IST | Asom Barta Community Radio, Dhubri Studio]
[00:04] Announcer: Local fishermen a...

#### [SRC-005] Global Logistics Daily (Aggregator Portal) — Fulbari Seizure Raises Questions Over Vikramaditya Logistics Freight Chain
- **Language:** English | **Locator:** N/A
- **Original Script:**
> GLOBAL LOGISTICS PORTAL (Oct 11, 2026) — Security and customs watchers report that following an interception at Fulbari, Rupali Transport, an operating subsidiary of Vikramaditya Logistics, has come u...
- **English Translation:**
> GLOBAL LOGISTICS PORTAL (Oct 11, 2026) — Security and customs watchers report that following an interception at Fulbari, Rupali Transport, an operating subsidiary of Vikramaditya Logistics, has come u...

#### [SRC-006] சென்னை துறைமுக வர்த்தக அரசிதழ் (Chennai Port Commercial Gazette) — சென்னை துறைமுக சரக்குக் கையாளுதல் உரிமம் புதுப்பித்தல் - விக்ரமாதித்யா லாஜிஸ்டிக்ஸ்
- **Language:** Mixed (Tamil + Latin/Regional) | **Locator:** Gazette Section IV, p. 14
- **Original Script:**
> சென்னை துறைமுக வர்த்தக அறிக்கை | அரசிதழ் பதிவு எண்: CHN-PRT-2026-0925 | தேதி: 25 செப்டம்பர் 2026:
கப்பல் போக்குவரத்து மற்றும் சரக்கு கையாளுதல் உரிமப் பிரிவு: விக்ரமாதித்யா லாஜிஸ்டிக்ஸ் பிரைவேட் லிமிடெ...
- **English Translation:**
> [MACHINE-TRANSLATED: TAMIL -> ENGLISH]
Chennai Port Commercial Gazette | Extract Dated Sept 25, 2026 | Vessel Registry Section:
Corporate filing record: Vikramaditya Logistics Private Limited filed cl...

#### [SRC-007] District & Sessions Judge Court, Jalpaiguri Division — Order in Bail Application 892/2026 (Subrata Mukherjee, Cooch Behar - Civil Boundary Matter)
- **Language:** English | **Locator:** Order Sheet pp. 1-2
- **Original Script:**
> IN THE COURT OF THE DISTRICT & SESSIONS JUDGE, JALPAIGURI DIVISION
Criminal / Civil Miscellaneous Docket | Bail Application No. 892/2026 | Order Date: 11 October 2026
In re: Application for Anticipato...
- **English Translation:**
> [OFFICIAL COURT ENGLISH RECORD]
Court of the District & Sessions Judge, Jalpaiguri Division | Bail Application No. 892/2026 | Dated Oct 11, 2026:
In the matter of Bail Application filed on behalf of S...

---

## Safety, Privacy & Compliance Certification

> [!CAUTION]
> SAFETY & COMPLIANCE CERTIFICATION: This intelligence report is compiled exclusively from lawful, public, and authorized open-source materials. No unauthorized interception, private communications harvesting, or doxxing was conducted. Association does not constitute proof of guilt. All machine-generated hypotheses must be verified by authorized human analysts prior to administrative, judicial, or enforcement action.
