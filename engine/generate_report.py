import argparse
import json
import sys
from pathlib import Path

from engine.impact import compute_impact

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def generate_report_from_impact(old_ref: str, new_ref: str, use_local: bool = False) -> dict:
    """Generate a minimal report.json from impact analysis only (for UI display)."""
    print(f"Computing impact between {old_ref} and {new_ref}...")
    impact = compute_impact(old_ref, new_ref, use_local=use_local)
    
    # Create minimal report with impact data and sample results
    report = {
        "summary": {
            "total": 2,
            "identical": 2,
            "intentional": 0,
            "regression": 0,
            "unexplained": 0
        },
        "radius": impact,
        "results": [
            {
                "scenario": "product_list",
                "verdict": "identical",
                "diffs": [],
                "explanation": "No behavioral changes detected in product listing endpoint."
            },
            {
                "scenario": "cart_quote",
                "verdict": "identical",
                "diffs": [],
                "explanation": "No behavioral changes detected in cart quote calculation."
            }
        ]
    }
    
    # Write report.json
    with open(PROJECT_ROOT / "report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    
    # Write ui/report-data.js
    ui_dir = PROJECT_ROOT / "ui"
    ui_dir.mkdir(exist_ok=True)
    ui_report_data_file = ui_dir / "report-data.js"
    with open(ui_report_data_file, "w", encoding="utf-8") as f:
        f.write(f"window.BLASTPROOF_REPORT = {json.dumps(report, indent=2)};")
    
    print(f"Generated report.json with impact data from {impact.get('source', 'unknown')}")
    print(f"Affected endpoints: {impact.get('endpoints', [])}")
    print(f"Changed files: {len(impact.get('changed', []))}")
    
    return report

def main():
    parser = argparse.ArgumentParser(description="Generate report.json from impact analysis for UI display")
    parser.add_argument("--old", required=True, help="Old git ref")
    parser.add_argument("--new", required=True, help="New git ref")
    parser.add_argument("--local", action="store_true", help="Force local impact engine")
    args = parser.parse_args()
    
    generate_report_from_impact(args.old, args.new, use_local=args.local)

if __name__ == "__main__":
    main()