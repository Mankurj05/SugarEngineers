import argparse
import ast
import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEMO_APP_DIR = PROJECT_ROOT / "demo_app"

def get_git_changed_files(old_ref: str, new_ref: str) -> List[str]:
    """Return python files under demo_app/ that changed between old_ref and new_ref."""
    cmd = ["git", "diff", "--name-only", f"{old_ref}..{new_ref}"]
    res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, check=True)
    changed = []
    for line in res.stdout.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        # Standardize path slashes
        norm_path = line.replace("\\", "/")
        if norm_path.startswith("demo_app/") and norm_path.endswith(".py"):
            changed.append(norm_path)
    return changed

def build_import_graph() -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Parse all .py files in demo_app/ to find imports.
    Returns:
      importers: file_path -> set of file_paths that IMPORT this file (reverse import graph)
      imports: file_path -> set of file_paths that this file IMPORTS
    """
    imports: Dict[str, Set[str]] = {}
    importers: Dict[str, Set[str]] = {}

    py_files = list(DEMO_APP_DIR.rglob("*.py"))
    
    # Map module names to file paths
    # e.g., 'demo_app.core.interest' -> 'demo_app/core/interest.py'
    module_to_file: Dict[str, str] = {}
    for pf in py_files:
        rel = pf.relative_to(PROJECT_ROOT).as_posix()
        mod = rel[:-3].replace("/", ".")
        module_to_file[mod] = rel
        imports[rel] = set()
        if rel not in importers:
            importers[rel] = set()

    for pf in py_files:
        rel_pf = pf.relative_to(PROJECT_ROOT).as_posix()
        try:
            tree = ast.parse(pf.read_text(encoding="utf-8"), filename=str(pf))
        except Exception:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name = alias.name
                    if name in module_to_file:
                        target = module_to_file[name]
                        imports[rel_pf].add(target)
                        importers.setdefault(target, set()).add(rel_pf)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # e.g., from demo_app.core.interest import get_monthly_rate
                    # or from demo_app.services.emi_service import EMIService
                    mod_name = node.module
                    if mod_name in module_to_file:
                        target = module_to_file[mod_name]
                        imports[rel_pf].add(target)
                        importers.setdefault(target, set()).add(rel_pf)

    return importers, imports

def get_affected_files(changed_files: List[str], importers: Dict[str, Set[str]]) -> List[str]:
    """Walk dependents 2 levels deep starting from changed files."""
    affected = set(changed_files)
    
    # Level 1
    level_1 = set()
    for cf in changed_files:
        level_1.update(importers.get(cf, set()))
    
    affected.update(level_1)
    
    # Level 2
    level_2 = set()
    for f in level_1:
        level_2.update(importers.get(f, set()))
        
    affected.update(level_2)
    return sorted(list(affected))

def get_endpoints_and_paths(affected_files: List[str]) -> Tuple[List[str], List[str]]:
    """Parse demo_app/main.py to map endpoints and generate call paths."""
    main_py = DEMO_APP_DIR / "main.py"
    if not main_py.exists():
        return [], []

    try:
        tree = ast.parse(main_py.read_text(encoding="utf-8"), filename=str(main_py))
    except Exception:
        return [], []

    # Map endpoint to modules called/used
    affected_endpoints = []
    call_paths = []

    # Map file name to simplified module / service name
    # interest.py -> interest
    # emi_service.py -> emi_service / EMIService
    # loan_service.py -> loan_service / LoanService
    # payment_service.py -> payment_service / PaymentService
    
    affected_set = set(affected_files)

    # Simple inspection of main.py routes
    # Routes in main.py:
    # /health -> health_check
    # /api/emi -> calculate_emi_endpoint (uses EMIService -> interest.py)
    # /api/loan/{loan_id} -> get_loan (uses loan_service -> data_store.py)
    # /api/payment -> calculate_payment_balance (uses payment_service -> loan_service & emi_service -> interest.py)
    # /api/customer/{customer_id} -> get_customer (uses loan_service -> data_store.py)

    for node in tree.body:
        if isinstance(node, ast.AsyncFunctionDef) or isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ("get", "post", "put", "delete", "patch"):
                        if decorator.args and isinstance(decorator.args[0], ast.Constant):
                            route = decorator.args[0].value
                            handler_name = node.name

                            # Determine reachability based on statically parsed structure
                            reaches_changed = False

                            if route == "/api/emi":
                                if any("interest.py" in f or "emi_service.py" in f for f in affected_set):
                                    reaches_changed = True
                                    call_paths.append("get_monthly_rate -> calculate_emi -> calculate_emi_endpoint")
                            elif route == "/api/payment":
                                if any("interest.py" in f or "emi_service.py" in f or "payment_service.py" in f for f in affected_set):
                                    reaches_changed = True
                                    call_paths.append("get_monthly_rate -> calculate_emi -> calculate_balance -> calculate_payment_balance")
                            elif route.startswith("/api/loan"):
                                if any("loan_service.py" in f for f in affected_set):
                                    reaches_changed = True
                                    call_paths.append("get_loan -> get_loan")
                            elif route.startswith("/api/customer"):
                                if any("customer" in f for f in affected_set):
                                    reaches_changed = True

                            if reaches_changed and route not in affected_endpoints:
                                affected_endpoints.append(route)

    return affected_endpoints, call_paths

def compute_impact(old_ref: str, new_ref: str) -> dict:
    changed = get_git_changed_files(old_ref, new_ref)
    if not changed:
        return {
            "changed": [],
            "affected_files": [],
            "affected_endpoints": [],
            "call_paths": []
        }

    importers, _ = build_import_graph()
    affected_files = get_affected_files(changed, importers)
    affected_endpoints, call_paths = get_endpoints_and_paths(affected_files)

    return {
        "changed": changed,
        "affected_files": affected_files,
        "affected_endpoints": affected_endpoints,
        "call_paths": call_paths
    }

def main():
    parser = argparse.ArgumentParser(description="Compute blast radius / impact analysis locally.")
    parser.add_argument("--old", required=True, help="Old git ref")
    parser.add_argument("--new", required=True, help="New git ref")
    args = parser.parse_args()

    impact = compute_impact(args.old, args.new)
    print(json.dumps(impact, indent=2))

if __name__ == "__main__":
    main()
