import argparse
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

def extract_keywords(text: str) -> List[str]:
    """Extract key terms and code expressions from rule text."""
    exprs = re.findall(r'\(([^)]+)\)', text)
    words = [w.lower() for w in re.findall(r'\b[a-zA-Z_]{3,}\b', text) if w.lower() not in {"must", "use", "per", "the", "and", "all", "not"}]
    return exprs + words

def classify_drift(item: dict, affected_files: List[str], decisions: List[dict], changed_files: List[str] = None) -> Tuple[str, Optional[dict]]:
    """
    Classify drift against recorded team decisions dynamically without hardcoding rule IDs.
    Returns: (verdict, matched_rule)
    """
    explanation = item.get("explanation", "").lower()
    files_to_check = changed_files if changed_files else affected_files
    
    for file in files_to_check:
        matching_rules = [d for d in decisions if d.get("file") == file or file.endswith(d.get("file", ""))]
        for rule in matching_rules:
            rule_text = rule.get("text", "").lower()
            keywords = extract_keywords(rule_text)
            
            match = False
            for kw in keywords:
                if kw in explanation:
                    match = True
                    break
            
            if match or file in changed_files:
                rule_meta = {
                    "id": rule["id"],
                    "text": rule["text"],
                    "source": rule["source"]
                }
                if "intentional" in rule_text or "allow" in rule_text:
                    return "intentional", rule_meta
                return "regression", rule_meta

    return "unexplained", None

def judge_results(explained_results: List[dict], affected_files: List[str], decisions_path: Path = DECISIONS_FILE, changed_files: List[str] = None) -> List[dict]:
    decisions = load_decisions(decisions_path)
    judged_results = []

    for item in explained_results:
        res = dict(item)
        if item.get("verdict") == "drift":
            verdict, rule = classify_drift(item, affected_files, decisions, changed_files)
            res["verdict"] = verdict
            if rule:
                res["rule"] = rule
            else:
                if "rule" in res:
                    del res["rule"]
        judged_results.append(res)

    return judged_results

def main():
    parser = argparse.ArgumentParser(description="Judge drifted scenarios against recorded team decisions.")
    parser.add_argument("--explained", required=True, help="Path to explained comparison JSON file")
    parser.add_argument("--decisions", default=str(DECISIONS_FILE), help="Path to decisions.json")
    parser.add_argument("--affected-files", nargs="*", default=[], help="List of affected files")
    args = parser.parse_args()

    with open(args.explained, "r", encoding="utf-8") as f:
        explained_data = json.load(f)

    affected_files = args.affected_files
    changed_files = []
    if not affected_files and Path("report.json").exists():
        try:
            with open("report.json", "r", encoding="utf-8") as f:
                rep = json.load(f)
                affected_files = rep.get("radius", {}).get("affected_files", [])
                changed_files = rep.get("radius", {}).get("changed", [])
        except Exception:
            pass

    results = judge_results(explained_data, affected_files, Path(args.decisions), changed_files)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
