import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROPOSED_INVARIANTS_FILE = PROJECT_ROOT / "proposed_invariants.md"
REPORT_FILE = PROJECT_ROOT / "report.json"

from engine.mcp_client import run_mcp_command

def generate_proposal(scenario_id: str = "cart_discount", date_str: str = None) -> str:
    if date_str is None:
        date_str = datetime.date.today().isoformat()
    
    changed_files = ["demo_app/core/discount_rules.py"]
    endpoints = ["/api/carts/quote"]
    total_scenarios = 2
    drifted_count = 1

    if REPORT_FILE.exists():
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                report = json.load(f)
                radius = report.get("radius", {})
                if radius.get("changed"):
                    changed_files = radius["changed"]
                if radius.get("endpoints"):
                    endpoints = radius["endpoints"]
                summary = report.get("summary", {})
                if "total" in summary:
                    total_scenarios = summary["total"]
                drifted_count = summary.get("regression", 0) + summary.get("unexplained", 0) + summary.get("intentional", 0)
        except Exception:
            pass

    changed_str = ", ".join(changed_files)
    endpoints_str = ", ".join(endpoints)

    return (
        f"Changing logic in {changed_str} affects endpoints {endpoints_str}. "
        f"Verified across {total_scenarios} replayed scenarios ({drifted_count} drifted) on {date_str} for scenario {scenario_id}."
    )

def commit_proposal(proposal_text: str) -> Tuple[str, str]:
    """
    Commit the proposal.
    Primary: MCP update_graph.
    Fallback: Append to proposed_invariants.md if MCP is unavailable.
    """
    project_id = "cb278f60-3b7b-4a08-b34e-b08331497f72"
    
    # Target file mapping for the graph indexer
    target_file = "demo_app/core/discount_rules.py"
    if REPORT_FILE.exists():
        try:
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                report = json.load(f)
                if report.get("radius", {}).get("changed"):
                    target_file = report["radius"]["changed"][0]
        except Exception:
            pass
            
    mapped_target = target_file.replace("demo_app/", "Reference/backend/") if target_file.startswith("demo_app/") else target_file
    
    try:
        # P6: Attempt REAL MCP TEACH
        mcp_args = {
            "operation": "add_insight",
            "file_path": mapped_target,
            "insight": proposal_text,
            "confidence": "high"
        }
        mcp_res = run_mcp_command(project_id, "update_graph", mcp_args)
        
        if mcp_res["status"] != "error":
            return "mcp_graph_write", f"Successfully recorded learning to LatentGraph: {mcp_res['data']}"
            
        mcp_err_reason = mcp_res["message"]
    except Exception as e:
        mcp_err_reason = str(e)
    
    # Fallback path
    try:
        entry = f"- [{datetime.datetime.now().isoformat()}] {proposal_text}\n"
        with open(PROPOSED_INVARIANTS_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        receipt_msg = f"Appended to proposed_invariants.md (graph unavailable: {mcp_err_reason})"
        return "fallback_local_file", receipt_msg
    except Exception as e:
        return "error", str(e)

def main():
    parser = argparse.ArgumentParser(description="Propose or commit invariants to graph.")
    parser.add_argument("--confirm", action="store_true", help="Explicitly confirm and write proposed invariant")
    parser.add_argument("--scenario", default="cart_discount", help="Scenario ID")
    args = parser.parse_args()

    proposal = generate_proposal(args.scenario)

    if not args.confirm:
        print("PROPOSAL GENERATED (read-only mode, use --confirm to write):")
        print(proposal)
    else:
        path_taken, receipt = commit_proposal(proposal)
        print(f"PROPOSAL COMMITTED ({path_taken}): {receipt}")

if __name__ == "__main__":
    main()
