"""FastAPI web application exposing REST endpoints and serving the workbench UI."""

import os
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse, PlainTextResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ..engine import OSINTFusionEngine
from ..models.source import SourceType
from ..models.review import ReviewAction
from ..reasoning.graph_builder import KnowledgeGraphBuilder
from ..report.export import ReportExporter


app = FastAPI(
    title="OSINT Fusion Workbench API",
    description="Multilingual Intelligence Analysis Agent & Analyst Workbench API",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global engine singleton initialized with benchmark corpus
engine = OSINTFusionEngine(analyst_id="analyst_lead")
engine.load_benchmark_corpus()


class IngestSourceRequest(BaseModel):
    title: str
    source_org: str
    text: str
    source_type: Optional[str] = "news_article"
    original_url: Optional[str] = None
    publication_date: Optional[str] = None
    page_numbers: Optional[str] = None
    is_primary: bool = True


class AnalystReviewDecisionRequest(BaseModel):
    decision: str  # approve, reject, amend, mark_needs_verification, mark_corroborated, mark_contradicted
    rationale: str
    amended_values: Optional[Dict[str, Any]] = None


@app.get("/api/dashboard")
def get_dashboard():
    """Returns top-level workbench metrics and health status."""
    return engine.get_dashboard_summary()


@app.get("/api/sources")
def get_sources():
    """Returns all ingested sources with original texts, translations, and metadata."""
    return [s.model_dump() for s in engine.sources]


@app.post("/api/sources")
def ingest_source(payload: IngestSourceRequest):
    """Ingests a new multilingual document or text snippet."""
    try:
        stype = SourceType(payload.source_type)
    except ValueError:
        stype = SourceType.NEWS_ARTICLE

    src = engine.add_custom_source(
        title=payload.title,
        source_org=payload.source_org,
        text=payload.text,
        source_type=stype,
        original_url=payload.original_url,
        publication_date=payload.publication_date,
        page_numbers=payload.page_numbers,
        is_primary=payload.is_primary,
    )
    return {"status": "success", "source": src.model_dump()}


@app.get("/api/entities")
def get_entities():
    """Returns extracted entities and conservative resolution ambiguities."""
    return {
        "entities": [e.model_dump() for e in engine.entities],
        "unresolved_ambiguities": engine.unresolved_ambiguities,
    }


@app.get("/api/timeline")
def get_timeline():
    """Returns chronological event reconstruction."""
    return [ev.model_dump() for ev in engine.events]


@app.get("/api/graph/cytoscape")
def get_cytoscape_graph():
    """Returns Knowledge Graph elements formatted for Cytoscape.js visual canvas."""
    return {
        "elements": engine.get_cytoscape_elements(),
        "unresolved_matches": engine.graph.unresolved_matches if engine.graph else [],
        "unsupported_relationships": engine.graph.unsupported_relationships if engine.graph else [],
    }


@app.get("/api/graph/export/csv/nodes")
def export_nodes_csv():
    """Exports node table as downloadable CSV."""
    if not engine.graph:
        raise HTTPException(status_code=404, detail="Graph not built")
    csv_content = KnowledgeGraphBuilder.export_nodes_csv(engine.graph)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=knowledge_graph_nodes.csv"}
    )


@app.get("/api/graph/export/csv/edges")
def export_edges_csv():
    """Exports edge table as downloadable CSV."""
    if not engine.graph:
        raise HTTPException(status_code=404, detail="Graph not built")
    csv_content = KnowledgeGraphBuilder.export_edges_csv(engine.graph)
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=knowledge_graph_edges.csv"}
    )


@app.get("/api/graph/export/cypher")
def export_cypher():
    """Exports graph as Neo4j / Memgraph Cypher statements."""
    if not engine.graph:
        raise HTTPException(status_code=404, detail="Graph not built")
    cypher_text = KnowledgeGraphBuilder.export_cypher(engine.graph)
    return PlainTextResponse(cypher_text)


@app.get("/api/graph/export/mermaid")
def export_mermaid():
    """Exports graph in Mermaid syntax."""
    if not engine.graph:
        raise HTTPException(status_code=404, detail="Graph not built")
    return PlainTextResponse(KnowledgeGraphBuilder.export_mermaid(engine.graph))


@app.get("/api/weak-signals")
def get_weak_signals():
    """Returns detected candidate patterns and heuristic confidence assessments."""
    return [s.model_dump() for s in engine.signals]


@app.get("/api/contradictions")
def get_contradictions():
    """Returns cross-source contradiction matrix and circular reporting alerts."""
    return {
        "contradictions": engine.contradictions,
        "circular_reporting": engine.circular_reporting,
    }


@app.get("/api/review-queue")
def get_review_queue():
    """Returns human-in-the-loop analyst review items."""
    return [q.model_dump() for q in engine.review_queue]


@app.post("/api/review-queue/{review_id}/action")
def record_review_action(review_id: str, payload: AnalystReviewDecisionRequest):
    """Records an analyst's decision (approve, reject, amend) with rationale."""
    try:
        action = ReviewAction(payload.decision)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid action: {payload.decision}")

    success = engine.record_analyst_decision(
        review_id=review_id,
        decision=action,
        rationale=payload.rationale,
        amended_values=payload.amended_values,
    )
    if not success:
        raise HTTPException(status_code=404, detail="Review item not found")

    return {
        "status": "success",
        "message": f"Review item {review_id} updated with action {action.value}",
        "dashboard": engine.get_dashboard_summary(),
    }


@app.get("/api/audit-log")
def get_audit_log():
    """Returns the immutable log of intelligence operations and analyst overrides."""
    return [entry.model_dump() for entry in engine.audit_log]


@app.get("/api/report")
def get_report():
    """Returns the complete standard 10-section intelligence report in JSON."""
    if not engine.latest_report:
        engine.run_full_analysis()
    return engine.latest_report.model_dump()


@app.get("/api/report/markdown")
def get_report_markdown():
    """Returns the full 10-section report rendered in GitHub-flavored Markdown."""
    if not engine.latest_report:
        engine.run_full_analysis()
    md = ReportExporter.to_markdown(engine.latest_report)
    return PlainTextResponse(md)


@app.get("/api/audio/capabilities")
def get_audio_capabilities():
    """Returns explicit disclosures regarding speech-to-text tools and practical next steps."""
    return engine.get_dashboard_summary()["audio_capabilities"]


@app.post("/api/reset-corpus")
def reset_to_benchmark():
    """Resets the workbench state to the default benchmark test corpus."""
    engine.load_benchmark_corpus()
    return {"status": "success", "message": "Workbench reloaded with benchmark corpus"}


# Mount web directory if it exists
web_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "web"))
if os.path.isdir(web_dir):
    app.mount("/static", StaticFiles(directory=web_dir), name="static")

    @app.get("/", response_class=FileResponse)
    def serve_index():
        return FileResponse(os.path.join(web_dir, "index.html"))
