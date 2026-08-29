import argparse
import json
import subprocess
import sys
from pathlib import Path

from engine.impact import compute_impact
from engine.compare import compare_results
from engine.explain import explain_comparison
from engine.judge import judge_results

PROJECT_ROOT = Path(__file__).resolve().parent.parent

def run_pipeline(old_ref: str, new_ref: str, app: str, use_local: bool = False, no_llm: bool = False) -> dict:
    # Step 1: Impact / Blast Radius
    print(f"[1/6] Computing impact between {old_ref} and {new_ref}...")
    impact = compute_impact(old_ref, new_ref, use_local=use_local)
    
    affected_endpoints = impact.get("affected_endpoints", [])
    print(f"      Affected endpoints: {affected_endpoints}")

    # Map endpoints to tags (e.g. /api/emi -> emi, /api/payment -> payment)
    tags = []
    for ep in affected_endpoints:
        clean_ep = ep.strip("/").split("/")[1] if len(ep.strip("/").split("/")) > 1 else ep.strip("/")
        tags.append(clean_ep)

    tags_str = ",".join(set(tags)) if tags else "nosuchtag"

    # Step 2: Replay
    print(f"[2/6] Replaying scenarios for tags: '{tags_str}'...")
    results_file = "results.json"
    replay_cmd = [
        sys.executable, "-m", "engine.replay",
        "--old", old_ref,
        "--new", new_ref,
        "--tags", tags_str,
        "--app", app
    ]
    
    try:
        subprocess.run(replay_cmd, cwd=str(PROJECT_ROOT), check=True)
    except subprocess.CalledProcessError:
        print("      No scenarios matched or replay failed.")
        results_data = []
        with open(results_file, "w", encoding="utf-8") as f:
            json.dump(results_data, f)

    # Step 3: Compare
    print("[3/6] Comparing results...")
    with open(results_file, "r", encoding="utf-8") as f:
        results_data = json.load(f)

    compared_data = compare_results(results_data)

    if no_llm:
        print("[4/6] Skipping explain (--no-llm mode)")
        print("[5/6] Skipping judge (--no-llm mode)")
        final_results = compared_data
    else:
        # Step 4: Explain
        print("[4/6] Generating explanations for drifted scenarios...")
        # Write comparison temporarily to compare_temp.json
        temp_comp = "comparison_temp.json"
        with open(temp_comp, "w", encoding="utf-8") as f:
            json.dump(compared_data, f, indent=2)

        explained_data = explain_comparison(temp_comp, old_ref, new_ref, impact.get("call_paths", []))
        if Path(temp_comp).exists():
            Path(temp_comp).unlink()

        # Step 5: Judge
        print("[5/6] Judging findings against team decisions...")
        final_results = judge_results(explained_data, impact.get("affected_files", []))

    # Step 6: Assemble final report.json
    print("[6/6] Assembling report.json...")
    
    counts = {
        "total": len(final_results),
        "identical": sum(1 for r in final_results if r.get("verdict") == "identical"),
        "intentional": sum(1 for r in final_results if r.get("verdict") == "intentional"),
        "regression": sum(1 for r in final_results if r.get("verdict") == "regression"),
        "unexplained": sum(1 for r in final_results if r.get("verdict") == "unexplained")
    }
    
    # If no_llm was passed, counts will be identical and drift
    if no_llm:
        counts["drift"] = sum(1 for r in final_results if r.get("verdict") == "drift")

    report = {
        "summary": counts,
        "radius": impact,
        "results": final_results
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("Pipeline complete! Wrote report.json")
    return report

def main():
    parser = argparse.ArgumentParser(description="BlastProof One-Command Pipeline")
    parser.add_argument("--old", required=True, help="Old git ref")
    parser.add_argument("--new", required=True, help="New git ref")
    parser.add_argument("--app", default="demo_app.main:app", help="App module import path")
    parser.add_argument("--local", action="store_true", help="Force local impact engine")
    parser.add_argument("--no-llm", action="store_true", help="Skip LLM explain and judge steps")
    args = parser.parse_args()

    run_pipeline(args.old, args.new, args.app, use_local=args.local, no_llm=args.no_llm)

if __name__ == "__main__":
    main()
