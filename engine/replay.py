import argparse
import subprocess
import time
import json
import os
import sys
from pathlib import Path
import httpx
import signal
import shutil
import tempfile

def create_worktree(tag: str, target_dir: str) -> None:
    # Use git worktree add to check out the tag in target_dir
    print(f"Creating worktree for '{tag}' at {target_dir}...")
    subprocess.run(["git", "worktree", "add", "--detach", target_dir, tag], check=True, capture_output=True)

def remove_worktree(target_dir: str) -> None:
    print(f"Removing worktree at {target_dir}...")
    subprocess.run(["git", "worktree", "remove", "--force", target_dir], check=False, capture_output=True)

def start_server(app_path: str, port: int, cwd: str) -> subprocess.Popen:
    print(f"Starting server {app_path} on port {port} in {cwd}...")
    # Using python -m uvicorn instead of uvicorn directly to ensure we use the current python env
    # Windows requires shell=True for some python commands, but we'll try without first
    env = os.environ.copy()
    env["PYTHONPATH"] = cwd # Make sure it can import the app
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", app_path, "--port", str(port)],
        cwd=cwd,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return process

def wait_for_health(port: int, timeout: int = 10) -> bool:
    print(f"Waiting for health check on port {port}...")
    start_time = time.time()
    url = f"http://127.0.0.1:{port}/api/health"
    
    with httpx.Client() as client:
        while time.time() - start_time < timeout:
            try:
                resp = client.get(url, timeout=1.0)
                if resp.status_code == 200:
                    return True
            except httpx.RequestError:
                pass
            time.sleep(0.5)
            
    return False

def get_scenarios(tags: list[str]) -> list[dict]:
    scenarios_dir = Path("scenarios")
    if not scenarios_dir.exists():
        print(f"Warning: scenarios directory not found at {scenarios_dir.absolute()}")
        return []
        
    matched = []
    for filepath in scenarios_dir.glob("*.json"):
        try:
            with open(filepath, "r") as f:
                scenario = json.load(f)
                
            scenario_tags = set(scenario.get("tags", []))
            if not tags or any(tag in scenario_tags for tag in tags):
                matched.append(scenario)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            
    # Sort by ID for determinism
    return sorted(matched, key=lambda x: x.get("id", ""))

def run_scenario(client: httpx.Client, base_url: str, scenario: dict) -> dict:
    url = f"{base_url}{scenario.get('path', '')}"
    method = scenario.get("method", "GET").upper()
    
    kwargs = {}
    if "body" in scenario:
        kwargs["json"] = scenario["body"]
        
    try:
        resp = client.request(method, url, timeout=5.0, **kwargs)
        try:
            body = resp.json()
        except ValueError:
            body = resp.text
            
        return {
            "status": resp.status_code,
            "json": body
        }
    except Exception as e:
        return {
            "status": 500,
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Replay scenarios against old and new code")
    parser.add_argument("--old", required=True, help="Git tag or commit for old version")
    parser.add_argument("--new", required=True, help="Git tag, commit, or HEAD for new version")
    parser.add_argument("--tags", help="Comma-separated list of scenario tags to run")
    parser.add_argument("--app", default="stub.app:app", help="Path to ASGI app (e.g., demo_app.main:app)")
    args = parser.parse_args()

    tags_list = args.tags.split(",") if args.tags else []
    
    scenarios = get_scenarios(tags_list)
    print(f"Found {len(scenarios)} matching scenarios.")
    
    if not scenarios:
        print(f"ERROR: No matching scenarios found in 'scenarios' directory for tags: {args.tags}")
        sys.exit(1)
    
    old_port = 8001
    new_port = 8002
    
    current_dir = os.getcwd()
    old_worktree_dir = None
    new_worktree_dir = None
    
    old_proc = None
    new_proc = None
    
    results = []

    try:
        # Setup OLD version
        old_worktree_dir = tempfile.mkdtemp(prefix="blastproof_old_")
        create_worktree(args.old, old_worktree_dir)
        old_proc = start_server(args.app, old_port, old_worktree_dir)
        
        # Setup NEW version
        if args.new.upper() == "HEAD":
            # Just use current directory
            new_worktree_dir = current_dir
            new_proc = start_server(args.app, new_port, new_worktree_dir)
        else:
            new_worktree_dir = tempfile.mkdtemp(prefix="blastproof_new_")
            create_worktree(args.new, new_worktree_dir)
            new_proc = start_server(args.app, new_port, new_worktree_dir)

        # Wait for health
        if not wait_for_health(old_port):
            print("ERROR: Old version failed health check")
            sys.exit(1)
            
        if not wait_for_health(new_port):
            print("ERROR: New version failed health check")
            sys.exit(1)
            
        print("Both servers healthy. Running scenarios...")
        
        # Replay
        with httpx.Client() as client:
            for scenario in scenarios:
                scenario_id = scenario.get("id", "unknown")
                print(f"Running scenario {scenario_id}...")
                
                old_res = run_scenario(client, f"http://127.0.0.1:{old_port}", scenario)
                new_res = run_scenario(client, f"http://127.0.0.1:{new_port}", scenario)
                
                results.append({
                    "scenario": scenario_id,
                    "old": old_res,
                    "new": new_res
                })
                
        # Write results
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
            
        print(f"Wrote {len(results)} results to results.json")

    finally:
        # Cleanup
        print("Cleaning up...")
        if old_proc:
            old_proc.terminate()
            old_proc.wait(timeout=5)
            
        if new_proc:
            new_proc.terminate()
            new_proc.wait(timeout=5)
            
        # Clean up worktrees
        if old_worktree_dir and old_worktree_dir != current_dir:
            remove_worktree(old_worktree_dir)
            try:
                shutil.rmtree(old_worktree_dir, ignore_errors=True)
            except Exception:
                pass
                
        if new_worktree_dir and new_worktree_dir != current_dir:
            remove_worktree(new_worktree_dir)
            try:
                shutil.rmtree(new_worktree_dir, ignore_errors=True)
            except Exception:
                pass

if __name__ == "__main__":
    main()
