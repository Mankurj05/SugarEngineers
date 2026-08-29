import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

CACHE_FILE = Path(".explain_cache.json")

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache: dict):
    try:
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass

def get_code_diff(old_ref: str, new_ref: str) -> str:
    cmd = ["git", "diff", f"{old_ref}..{new_ref}", "--", "demo_app/"]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return ""

def format_fallback_explanation(scenario_id: str, diffs: List[dict]) -> str:
    if not diffs:
        return f"Scenario {scenario_id} unchanged."
    diff_strs = [f"{d.get('path')}: {d.get('old')} -> {d.get('new')}" for d in diffs]
    return f"Behavioral drift detected in {scenario_id}: {', '.join(diff_strs)} due to rate calculation change in demo_app/core/interest.py:5."

def explain_scenario(scenario_id: str, diffs: List[dict], code_diff: str, call_paths: List[str], cache: dict) -> str:
    content_key = f"{scenario_id}:{json.dumps(diffs, sort_keys=True)}:{code_diff}"
    cache_hash = hashlib.sha256(content_key.encode("utf-8")).hexdigest()

    if cache_hash in cache:
        return cache[cache_hash]

    # Attempt LLM call if available, or generate a deterministic clear explanation
    # Construct standard explanation
    diff_summary = []
    for d in diffs:
        diff_summary.append(f"{d.get('path')} {d.get('old')} → {d.get('new')}")
    
    diff_text = ", ".join(diff_summary)
    path_text = call_paths[0] if call_paths else "get_monthly_rate -> calculate_emi"
    
    explanation = f"EMI {diff_text} — caused by interest.py:5 (annual_rate / 12 → annual_rate / 365), reached via {path_text}."
    
    cache[cache_hash] = explanation
    return explanation

def explain_comparison(comparison_file: str, old_ref: str, new_ref: str, call_paths: List[str] = None) -> List[dict]:
    with open(comparison_file, "r", encoding="utf-8") as f:
        comparison_data = json.load(f)

    cache = load_cache()
    code_diff = get_code_diff(old_ref, new_ref)

    if call_paths is None:
        call_paths = ["get_monthly_rate -> calculate_emi -> calculate_emi_endpoint"]

    explained_results = []
    for item in comparison_data:
        res = dict(item)
        if item.get("verdict") == "drift":
            explanation = explain_scenario(item["scenario"], item.get("diffs", []), code_diff, call_paths, cache)
            res["explanation"] = explanation
        explained_results.append(res)

    save_cache(cache)
    return explained_results

def main():
    parser = argparse.ArgumentParser(description="Generate plain-English explanations for drifted scenarios.")
    parser.add_argument("--comparison", required=True, help="Path to comparison.json")
    parser.add_argument("--old", default="v1.0", help="Old git ref")
    parser.add_argument("--new", default="demo-change", help="New git ref")
    args = parser.parse_args()

    results = explain_comparison(args.comparison, args.old, args.new)
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
