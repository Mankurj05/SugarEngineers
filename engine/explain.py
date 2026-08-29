import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional

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

def parse_git_diff(code_diff: str) -> List[dict]:
    """Parse unified git diff into structured list of file changes."""
    changes = []
    current_file = None
    current_line = None

    lines = code_diff.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("+++ b/"):
            current_file = line[6:].strip()
            i += 1
            continue
        
        # Hunk header: @@ -old_line,len +new_line,len @@
        hunk_match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk_match:
            hunk_start = int(hunk_match.group(1))
            i += 1
            old_lines = []
            new_lines = []
            curr_offset = 0
            changed_line = None

            while i < len(lines) and not lines[i].startswith("diff --git") and not lines[i].startswith("@@"):
                dl = lines[i]
                if dl.startswith("-") and not dl.startswith("---"):
                    old_lines.append(dl[1:].strip())
                    if changed_line is None:
                        changed_line = hunk_start + curr_offset
                elif dl.startswith("+") and not dl.startswith("+++"):
                    new_lines.append(dl[1:].strip())
                    if changed_line is None:
                        changed_line = hunk_start + curr_offset
                elif dl.startswith(" "):
                    curr_offset += 1
                i += 1

            if current_file and (old_lines or new_lines):
                changes.append({
                    "file": current_file,
                    "line": changed_line if changed_line is not None else hunk_start,
                    "old_code": " ".join(old_lines),
                    "new_code": " ".join(new_lines)
                })
            continue

        i += 1

    return changes

def explain_scenario(scenario_id: str, diffs: List[dict], code_diff: str, call_paths: List[str], cache: dict) -> str:
    content_key = f"{scenario_id}:{json.dumps(diffs, sort_keys=True)}:{code_diff}"
    cache_hash = hashlib.sha256(content_key.encode("utf-8")).hexdigest()

    if cache_hash in cache:
        return cache[cache_hash]

    parsed_changes = parse_git_diff(code_diff)
    
    diff_summary = []
    for d in diffs:
        diff_summary.append(f"{d.get('path')} {d.get('old')} → {d.get('new')}")
    diff_text = ", ".join(diff_summary) if diff_summary else "behavioral drift"

    path_text = call_paths[0] if call_paths else "direct call"

    if parsed_changes:
        primary = parsed_changes[0]
        file_loc = f"{primary['file']}:{primary['line']}"
        code_change = f"({primary['old_code']} → {primary['new_code']})" if primary['old_code'] or primary['new_code'] else ""
        explanation = f"Scenario {scenario_id} ({diff_text}) — caused by change in {file_loc} {code_change}, reached via {path_text}."
    else:
        explanation = f"Scenario {scenario_id} ({diff_text}) — reached via {path_text}."

    cache[cache_hash] = explanation
    return explanation

def explain_comparison(comparison_file: str, old_ref: str, new_ref: str, call_paths: List[str] = None) -> List[dict]:
    with open(comparison_file, "r", encoding="utf-8") as f:
        comparison_data = json.load(f)

    cache = load_cache()
    code_diff = get_code_diff(old_ref, new_ref)

    if call_paths is None:
        call_paths = []

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
