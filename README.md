# OSINT Fusion Workbench — Multilingual Intelligence Analysis Agent

A reusable, evidence-grounded open-source intelligence analysis workbench built to process, connect, and verify information from multiple lawful, public, or authorized sources across Indian languages (Bengali, Hindi, Assamese, Tamil, Telugu, Marathi) and English.

Prioritizes **evidence provenance, explainability, uncertainty bounding, privacy, and human verification over automated conclusions**.

---

## 🌟 Key Capabilities

### 1. Multilingual Document & Speech Ingestion
- **Languages Supported:** Bengali (বাংলা), Hindi (हिन्दी), Assamese (অসমীয়া), Tamil (தமிழ்), Telugu (తెలుగు), Marathi (मराठी), and English.
- **Side-by-Side Preservation:** Maintains original-script verbatim text alongside English translations. Never discards original phrasing.
- **Code-Mixing Detection:** Identifies mixed-script content (e.g. Banglish, Hinglish, bilingual police records).
- **Audio Transcript Analysis:** Supports authorized broadcast transcripts with timecodes (`[00:45]`, `[01:23]`), flags uncertain tokens (`[uncertain: ...]`, `[inaudible]`), and enforces transparency on acoustic tool availability.

### 2. Conservative Entity Resolution
- **Strict Anti-Merge Protocol:** Forbids merging people or organizations merely because names match phonetically or orthographically.
- **Case Study (`ENT-001` vs `ENT-007`):** Apprehended driver *Subrata Mukherjee* (resident of Malda, son of B. Mukherjee) is strictly distinguished from civil land litigant *Subrata Mukherjee* (resident of Cooch Behar, son of Late N. Mukherjee).
- **Mention vs Verified Involvement:** Differentiates between mere co-mention in a source and verified participation in an incident.

### 3. Chronological Event Reconstruction
- **Bounded Temporal Precision:** Separates confirmed dates, reported dates, and estimated windows (`+/-` intervals).
- **Distinguishes Key Timestamps:** Explicitly decouples event occurrence dates from publication dates, reported dates, and historical precedents.

### 4. Cross-Lingual Knowledge Graph
- **Typed Provenance Edges:** Nodes connect entities, events, and sources via typed relationships (`mentions`, `affiliated_with`, `reports_event`, `corroborates`, `contradicts`, `transshipped_to`).
- **Direct vs Inferred Links:** Direct primary citations are visually and structurally distinguished from analytical hypotheses.
- **Multi-Format Exports:** One-click export to:
  - Node Table CSV (`data/exports/knowledge_graph_nodes.csv`)
  - Edge Table CSV (`data/exports/knowledge_graph_edges.csv`)
  - Neo4j / Memgraph Cypher statements
  - Mermaid markdown diagrams
  - Interactive Cytoscape.js canvas elements

### 5. Weak-Signal Detection & Heuristic Scoring
- **Distinct Dual Metrics:**
  - **Evidence Confidence:** Assesses primary source grounding, directness, corroboration, and consistency.
  - **Signal Strength:** Evaluates operational anomaly level (e.g. cross-border riverine-to-road conduit, intermediary broker shielding, aggregator echo-chambers).
- **Documented Heuristic Formula:**
  $$\text{Composite Score} = (0.35 \times \text{Reliability}) + (0.25 \times \text{Directness}) + (0.25 \times \text{Corroboration}) + (0.15 \times \text{Consistency})$$
- **Alternative Explanations & Counterevidence:** Every signal documents competing benign hypotheses and targeted follow-up verification actions.

### 6. Contradiction & Circular Reporting Analyzer
- **Factual Discrepancies Flagged:** Highlights date contradictions (Oct 8 vs Oct 7) and seizure volume variations (120 kg vs 200 kg) side-by-side.
- **Circular Copycat Detection:** Flags secondary syndication portals republishing single-source leaks without field reporting, preventing artificial corroboration inflation.

### 7. Human-in-the-Loop Analyst Review Queue & Audit Log
- **Analyst Control:** Machine hypotheses receive `needs_verification` status until approved, rejected, or amended by an authorized analyst.
- **Immutable Audit Trail:** Preserves the machine's initial assessment while logging human rationale, timestamp, and decision.

### 8. Standard 10-Section Intelligence Report
Automatically generates audit-grade reports with:
1. Executive Summary
2. Scope and Sources
3. Key Entities
4. Event Timeline
5. Knowledge Graph (with Mermaid syntax)
6. Weak Signals
7. Contradictions and Gaps
8. Analyst Review Queue
9. Recommended Verification Steps
10. Evidence Appendix (verbatim bilingual quotes & locators)

---

## 🚀 Quickstart

### 1. Start the Interactive Web Workbench
```bash
python run_server.py 8080
```
Open **[http://127.0.0.1:8080](http://127.0.0.1:8080)** in your browser.

### 2. Run Headless Pipeline via CLI
```bash
# Analyze benchmark corpus
python -m osint_fusion.cli analyze

# Export full 10-section intelligence report in Markdown
python -m osint_fusion.cli report --format markdown --output data/exports/intelligence_report.md

# Export knowledge graph to Mermaid or Cypher
python -m osint_fusion.cli export-graph --format mermaid
python -m osint_fusion.cli export-graph --format cypher

# Inspect human review queue
python -m osint_fusion.cli review

# Act on a review item as an analyst
python -m osint_fusion.cli review --decide REV-001 --action approve --rationale "Verified distinct identities via court docket."
```

### 3. Run Automated Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## 📁 Repository Layout

```
├── osint_fusion/
│   ├── models/            # Pydantic schemas (Source, Entity, Event, Graph, Signal, Review, Report)
│   ├── multilingual/      # Indic script detection, transliteration engine, translation manager, audio STT
│   ├── extraction/        # Entity extraction, conservative resolver, event timeline extractor
│   ├── reasoning/         # Knowledge graph builder, contradiction & circular detector, weak signals
│   ├── report/            # 10-section report generator and multi-format exporter
│   ├── corpus/            # Realistic benchmark corpus (Bengali, Hindi, Assamese, Tamil, English)
│   ├── engine.py          # Central stateful OSINT intelligence engine
│   ├── cli.py             # Command-line interface
│   └── api/app.py         # FastAPI REST service & static web host
├── web/
│   ├── index.html         # Analyst Workbench Single-Page Application
│   ├── css/styles.css     # Sleek dark-mode intelligence UI design system
│   └── js/
│       ├── app.js         # Workbench state management, REST integration, review modal
│       └── graph_view.js  # Cytoscape.js interactive knowledge graph canvas
├── tests/                 # 25 automated unit tests
├── run_server.py          # One-click launcher script
└── README.md              # System documentation
```

---

## ⚖️ Safety, Privacy & Compliance Certification

1. **Lawful Public Sourcing:** Operates exclusively on authorized public sources, official bulletins, court records, and public gazettes.
2. **No Guilt by Association:** Weak ties or corporate affiliations are never treated as proof of guilt or wrongdoing.
3. **PII Masking:** Integrated redaction shield masks personal telephone numbers, door addresses, and sensitive identifiers.
4. **Transparent AI Limitations:** Explicitly discloses speech engine availability, acoustic uncertainties, and machine translation badges.