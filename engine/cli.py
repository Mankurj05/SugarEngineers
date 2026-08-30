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
    
    affected_endpoints = impact.get("endpoints", [])
    print(f"      Affected endpoints: {affected_endpoints}")

    # Map endpoints to tags
    tags = []
    for ep in affected_endpoints:
        if 'cart' in ep: tags.append('cart')
        if 'product' in ep: tags.append('product')
        if 'order' in ep or 'checkout' in ep: tags.append('order')

    # If no endpoints detected (like when we don't have tags), default to "all" to run everything
    tags_str = ",".join(set(tags)) if tags else "all"

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
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Replay failed with exit code {e.returncode}. Generating report with impact data only.", file=sys.stderr)
        # Generate minimal report with impact data even if replay fails
        minimal_report = {
            "summary": {
                "total": 0,
                "identical": 0,
                "intentional": 0,
                "regression": 0,
                "unexplained": 0
            },
            "radius": impact,
            "results": []
        }
        
        with open("report.json", "w", encoding="utf-8") as f:
            json.dump(minimal_report, f, indent=2)

        ui_dir = PROJECT_ROOT / "ui"
        ui_dir.mkdir(exist_ok=True)
        ui_report_data_file = ui_dir / "report-data.js"
        with open(ui_report_data_file, "w", encoding="utf-8") as f:
            f.write(f"window.BLASTPROOF_REPORT = {json.dumps(minimal_report, indent=2)};")

        print(f"Generated minimal report.json with impact data (replay failed).")
        return minimal_report

    # Step 3: Compare
    print("[3/6] Comparing results...")
    with open(results_file, "r", encoding="utf-8") as f:
        results_data = json.load(f)

    compared_data = compare_results(results_data)

    if no_llm:
        print("[4/6] Skipping explain (--no-llm mode)")
        print("[5/6] Skipping judge (--no-llm mode)")
        # In no_llm mode, map drift -> unexplained to maintain 4-key report contract
        final_results = []
        for r in compared_data:
            res = dict(r)
            if res.get("verdict") == "drift":
                res["verdict"] = "unexplained"
            final_results.append(res)
    else:
        # Step 4: Explain
        print("[4/6] Generating explanations for drifted scenarios...")
        temp_comp = "comparison_temp.json"
        with open(temp_comp, "w", encoding="utf-8") as f:
            json.dump(compared_data, f, indent=2)

        explained_data = explain_comparison(temp_comp, old_ref, new_ref, impact.get("call_paths", []))
        if Path(temp_comp).exists():
            Path(temp_comp).unlink()

        # Step 5: Judge
        print("[5/6] Judging findings against team decisions...")
        final_results = judge_results(explained_data, impact.get("affected_files", []), changed_files=impact.get("changed", []))

    # Step 6: Assemble final report.json
    print("[6/6] Assembling report.json...")
    
    counts = {
        "total": len(final_results),
        "identical": sum(1 for r in final_results if r.get("verdict") == "identical"),
        "intentional": sum(1 for r in final_results if r.get("verdict") == "intentional"),
        "regression": sum(1 for r in final_results if r.get("verdict") == "regression"),
        "unexplained": sum(1 for r in final_results if r.get("verdict") == "unexplained")
    }

    report = {
        "summary": counts,
        "radius": impact,
        "results": final_results
    }

    with open("report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    ui_dir = PROJECT_ROOT / "ui"
    ui_dir.mkdir(exist_ok=True)
    ui_report_data_file = ui_dir / "report-data.js"
    with open(ui_report_data_file, "w", encoding="utf-8") as f:
        f.write(f"window.BLASTPROOF_REPORT = {json.dumps(report, indent=2)};")

    print("Pipeline complete! Wrote report.json and ui/report-data.js")
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
