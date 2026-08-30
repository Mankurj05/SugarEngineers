import sys
import os
import subprocess
import shutil
import json

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def check_diagnostics():
    print("========================================")
    print("   BLASTPROOF MCP DIAGNOSTIC SUITE    ")
    print("========================================")
    
    # 1. Check CLI Installation
    lgraph_path = shutil.which("lgraph")
    if lgraph_path:
        try:
            res = subprocess.run(["lgraph.cmd", "--version"], capture_output=True, text=True, shell=True, encoding="utf-8", errors="ignore")
            print(f"[OK] 1. LatentGraph CLI Installed: Version {res.stdout.strip()}")
        except Exception as e:
            print(f"[FAIL] 1. LatentGraph CLI Installed: Error checking version ({e})")
    else:
        print("[FAIL] 1. LatentGraph CLI Installed: NOT FOUND")

    # 2. Check Project Configuration
    try:
        with open(".lgraph/config.json", "r") as f:
            cfg = json.load(f)
            print(f"[OK] 2. Project Configuration: Found (.lgraph/config.json)")
    except FileNotFoundError:
        print("[FAIL] 2. Project Configuration: Not found (.lgraph/config.json missing)")

    # 3. Check Authentication & Status
    try:
        res = subprocess.run(["lgraph.cmd", "status"], capture_output=True, text=True, shell=True, encoding="utf-8", errors="ignore")
        if res.stdout and "API Key:" in res.stdout and "Not configured" not in res.stdout:
            print("[OK] 3. API Authentication: Available")
        else:
            print("[FAIL] 3. API Authentication: Not configured")
    except Exception as e:
        print(f"[FAIL] 3. API Authentication: Status check failed ({e})")

    # 4. Check Local Fallback Compatibility
    try:
        import engine.impact_local
        print("[OK] 4. Local AST Fallback Engine: Ready")
    except ImportError as e:
        print(f"[FAIL] 4. Local AST Fallback Engine: Failed to import ({e})")

    print("\n========================================")
    print("Required MCP Tools Specification:")
    print(" - get_file")
    print(" - get_dependencies")
    print(" - get_call_chain")
    print(" - get_pr_insights")
    print(" - update_graph")
    print("========================================")

if __name__ == "__main__":
    check_diagnostics()