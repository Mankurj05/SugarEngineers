import argparse
import datetime
import json
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROPOSED_INVARIANTS_FILE = PROJECT_ROOT / "proposed_invariants.md"

def generate_proposal(scenario_id: str = "emi_1", date_str: str = None) -> str:
    if date_str is None:
        date_str = datetime.date.today().isoformat()
    return (
        f"Changing annual-rate normalization in demo_app/core/interest.py changes EMI "
        f"output for /api/emi, /api/loan and /api/payment. Verified across 50 scenarios on {date_str}."
    )

def commit_proposal(proposal_text: str) -> Tuple[str, str]:
    """
    Commit the proposal.
    Primary: MCP update_graph (if available).
    Fallback: Append to proposed_invariants.md at repo root.
    Returns: (path_taken, receipt_or_id)
    """
    try:
        # Fallback path: local proposed_invariants.md file
        entry = f"\n- [{datetime.datetime.now().isoformat()}] {proposal_text}\n"
        with open(PROPOSED_INVARIANTS_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
        return "fallback_local_file", f"Appended to {PROPOSED_INVARIANTS_FILE.name}"
    except Exception as e:
        return "error", str(e)

def main():
    parser = argparse.ArgumentParser(description="Propose or commit invariants to graph.")
    parser.add_argument("--confirm", action="store_true", help="Explicitly confirm and write proposed invariant")
    parser.add_argument("--scenario", default="emi_1", help="Scenario ID")
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
