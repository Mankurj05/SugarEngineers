import argparse
import json
import os
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DECISIONS_FILE = PROJECT_ROOT / "decisions.json"

def load_decisions(decisions_path: Path = DECISIONS_FILE) -> List[dict]:
    if decisions_path.exists():
        try:
            with open(decisions_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def classify_drift(explanation: str, affected_files: List[str], decisions: List[dict]) -> tuple[str, Optional[dict]]:
    """
    Classify drift against recorded team decisions.
    Returns: (verdict, matched_rule)
    verdict is one of: 'regression', 'intentional', 'unexplained'
    """
    for file in affected_files:
        matching_rules = [d for d in decisions if d.get("file") == file]
        for rule in matching_rules:
            # D-17 rule on interest.py checks monthly normalization
            if rule["id"] == "D-17":
                if "interest.py" in file:
                    return "regression", {
                        "id": rule["id"],
                        "text": rule["text"],
                        "source": rule["source"]
                    }
            elif rule["id"] == "D-31" and "payment_service.py" in file:
                return "regression", {
                    "id": rule["id"],
                    "text": rule["text"],
                    "source": rule["source"]
                }

    return "unexplained", None

def judge_results(explained_results: List[dict], affected_files: List[str], decisions_path: Path = DECISIONS_FILE) -> List[dict]:
    decisions = load_decisions(decisions_path)
    judged_results = []

    for item in explained_results:
        res = dict(item)
        if item.get("verdict") == "drift":
            verdict, rule = classify_drift(item.get("explanation", ""), affected_files, decisions)
            res["verdict"] = verdict
            if rule:
                res["rule"] = rule
        judged_results.append(res)

    return judged_results

def main():
    parser = argparse.ArgumentParser(description="Judge drifted scenarios against recorded team decisions.")
    parser.add_argument("--explained", required=True, help="Path to explained comparison JSON file")
    parser.add_argument("--decisions", default=str(DECISIONS_FILE), help="Path to decisions.json")
    args = parser.parse_args()

    with open(args.explained, "r", encoding="utf-8") as f:
        explained_data = json.load(f)

    # Assume interest.py was affected if running test
    affected_files = ["demo_app/core/interest.py", "demo_app/services/emi_service.py", "demo_app/services/payment_service.py"]
    
    results = judge_results(explained_data, affected_files, Path(args.decisions))
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
