"""Command-line interface (CLI) for OSINT Fusion Workbench."""

import argparse
import sys
import json
import uvicorn
from .engine import OSINTFusionEngine
from .report.export import ReportExporter
from .reasoning.graph_builder import KnowledgeGraphBuilder


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="osint-fusion",
        description="OSINT Fusion Workbench — Multilingual Intelligence Analysis Agent CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Workbench sub-commands")

    # Command: analyze
    p_analyze = subparsers.add_parser("analyze", help="Execute complete analysis on benchmark or ingested corpus")
    p_analyze.add_argument("--json", action="store_true", help="Output summary in JSON format")

    # Command: report
    p_report = subparsers.add_parser("report", help="Generate 10-section standard intelligence report")
    p_report.add_argument("--format", choices=["markdown", "json"], default="markdown", help="Output format")
    p_report.add_argument("--output", "-o", type=str, help="Output destination file path")

    # Command: export-graph
    p_graph = subparsers.add_parser("export-graph", help="Export knowledge graph in CSV, Cypher, or Mermaid")
    p_graph.add_argument("--format", choices=["mermaid", "cypher", "csv-nodes", "csv-edges"], default="mermaid")
    p_graph.add_argument("--output", "-o", type=str, help="Output destination file path")

    # Command: review
    p_review = subparsers.add_parser("review", help="List or inspect analyst review queue items")
    p_review.add_argument("--decide", type=str, help="Review Item ID to act upon (e.g. REV-001)")
    p_review.add_argument("--action", choices=["approve", "reject", "amend", "mark_needs_verification"], help="Analyst decision")
    p_review.add_argument("--rationale", type=str, default="CLI manual analyst review", help="Analyst rationale note")

    # Command: serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive workbench web application")
    p_serve.add_argument("--host", default="127.0.0.1", help="Server host IP")
    p_serve.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    p_serve.add_argument("--reload", action="store_true", help="Auto-reload on code change")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    engine = OSINTFusionEngine(analyst_id="cli_analyst")
    engine.load_benchmark_corpus()

    if args.command == "analyze":
        summary = engine.get_dashboard_summary()
        if args.json:
            print(json.dumps(summary, indent=2))
        else:
            print("=================================================================")
            print("       OSINT FUSION WORKBENCH — INTELLIGENCE PIPELINE SUMMARY     ")
            print("=================================================================")
            print(f"Sources Ingested:        {summary['total_sources']} (Primary: {summary['primary_sources_count']})")
            print(f"Entities Extracted:      {summary['total_entities']}")
            print(f"Chronological Events:    {summary['total_events']}")
            print(f"Knowledge Graph Nodes:   {summary['total_graph_nodes']}")
            print(f"Knowledge Graph Edges:   {summary['total_graph_edges']}")
            print(f"Candidate Weak Signals:  {summary['total_weak_signals']}")
            print(f"Contradictions Flagged:  {summary['contradictions_count']}")
            print(f"Circular Reporting Risk: {summary['circular_reporting_count']}")
            print(f"Review Queue Pending:    {summary['review_queue_pending']}")
            print("=================================================================")
            print("\n[!] Top Weak Signals:")
            for s in engine.signals:
                print(f"  • [{s.id}] {s.title}")
                print(f"    Confidence: {s.evidence_confidence} | Strength: {s.signal_strength} | Heuristic Score: {s.confidence_breakdown.composite_heuristic_score if s.confidence_breakdown else 'N/A'}")
            print("\n[!] Key Cross-Source Contradictions:")
            for c in engine.contradictions:
                print(f"  • [{c['id']}] {c['dimension']}: {c['claim_a']['value']} vs {c['claim_b']['value']}")

    elif args.command == "report":
        if not engine.latest_report:
            engine.run_full_analysis()
        if args.format == "json":
            out_str = ReportExporter.to_json(engine.latest_report)
        else:
            out_str = ReportExporter.to_markdown(engine.latest_report)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out_str)
            print(f"[+] Successfully wrote intelligence report ({args.format}) to {args.output}")
        else:
            print(out_str)

    elif args.command == "export-graph":
        if not engine.graph:
            engine.run_full_analysis()
        
        if args.format == "mermaid":
            content = KnowledgeGraphBuilder.export_mermaid(engine.graph)
        elif args.format == "cypher":
            content = KnowledgeGraphBuilder.export_cypher(engine.graph)
        elif args.format == "csv-nodes":
            content = KnowledgeGraphBuilder.export_nodes_csv(engine.graph)
        elif args.format == "csv-edges":
            content = KnowledgeGraphBuilder.export_edges_csv(engine.graph)

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"[+] Exported graph ({args.format}) to {args.output}")
        else:
            print(content)

    elif args.command == "review":
        if args.decide and args.action:
            from .models.review import ReviewAction
            act = ReviewAction(args.action)
            res = engine.record_analyst_decision(args.decide, act, args.rationale)
            if res:
                print(f"[+] Recorded analyst decision '{act.value}' for item {args.decide}.")
            else:
                print(f"[-] Review item {args.decide} not found.", file=sys.stderr)
        else:
            print(f"--- Analyst Review Queue ({len(engine.review_queue)} items) ---")
            for item in engine.review_queue:
                status_icon = "⏳" if item.current_status.value == "needs_verification" else "✓"
                print(f"{status_icon} [{item.id}] ({item.item_type.value}) {item.title}")
                print(f"    Machine Hypothesis: {item.machine_hypothesis}")
                print(f"    Current Status:     {item.current_status.value}")

    elif args.command == "serve":
        print(f"[+] Starting OSINT Fusion Workbench Web Server on http://{args.host}:{args.port}")
        uvicorn.run("osint_fusion.api.app:app", host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
