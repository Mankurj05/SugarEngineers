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

def build_import_graph() -> Tuple[Dict[str, Set[str]], Dict[str, Set[str]], Dict[str, str]]:
    """
    Parse all .py files in demo_app/ to find imports.
    Returns:
      importers: file_path -> set of file_paths that IMPORT this file (reverse import graph)
      imports: file_path -> set of file_paths that this file IMPORTS (forward import graph)
      symbol_to_file: symbol_name -> file_path where symbol is defined/imported from
    """
    imports: Dict[str, Set[str]] = {}
    importers: Dict[str, Set[str]] = {}
    symbol_to_file: Dict[str, str] = {}

    py_files = list(DEMO_APP_DIR.rglob("*.py"))
    
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
                        symbol = alias.asname or alias.name.split(".")[-1]
                        symbol_to_file[f"{rel_pf}:{symbol}"] = target
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    mod_name = node.module
                    if mod_name in module_to_file:
                        target = module_to_file[mod_name]
                        imports[rel_pf].add(target)
                        importers.setdefault(target, set()).add(rel_pf)
                        for alias in node.names:
                            symbol = alias.asname or alias.name
                            symbol_to_file[f"{rel_pf}:{symbol}"] = target

    return importers, imports, symbol_to_file

def get_affected_files(changed_files: List[str], importers: Dict[str, Set[str]]) -> List[str]:
    """Walk dependents 2 levels deep starting from changed files."""
    affected = set(changed_files)
    
    level_1 = set()
    for cf in changed_files:
        level_1.update(importers.get(cf, set()))
    
    affected.update(level_1)
    
    level_2 = set()
    for f in level_1:
        level_2.update(importers.get(f, set()))
        
    affected.update(level_2)
    return sorted(list(affected))

def get_transitive_dependencies(start_file: str, imports: Dict[str, Set[str]]) -> Set[str]:
    """Get all files imported directly or indirectly by start_file."""
    visited = set()
    stack = [start_file]
    while stack:
        curr = stack.pop()
        if curr not in visited:
            visited.add(curr)
            for imp in imports.get(curr, set()):
                if imp not in visited:
                    stack.append(imp)
    return visited

def get_endpoints_and_paths(affected_files: List[str], imports: Dict[str, Set[str]], symbol_to_file: Dict[str, str]) -> Tuple[List[str], List[str]]:
    """Parse demo_app/main.py dynamically to map endpoints and call paths based on AST."""
    main_py = DEMO_APP_DIR / "main.py"
    if not main_py.exists():
        return [], []

    rel_main = main_py.relative_to(PROJECT_ROOT).as_posix()
    affected_set = set(affected_files)

    try:
        tree = ast.parse(main_py.read_text(encoding="utf-8"), filename=str(main_py))
    except Exception:
        return [], []

    affected_endpoints = []
    call_paths = []

    # Parse imports in main.py to resolve instantiated variables / called services
    main_symbols: Dict[str, str] = {} # name -> source_file
    for key, target_file in symbol_to_file.items():
        if key.startswith(f"{rel_main}:"):
            sym = key.split(":", 1)[1]
            main_symbols[sym] = target_file

    # Track instances created in main.py, e.g., loan_service = LoanService()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    var_name = target.id
                    if isinstance(node.value, ast.Call):
                        if isinstance(node.value.func, ast.Name):
                            class_name = node.value.func.id
                            if class_name in main_symbols:
                                main_symbols[var_name] = main_symbols[class_name]

    # Inspect route handlers
    for node in tree.body:
        if isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef)):
            handler_name = node.name
            route_path = None

            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Attribute):
                    if decorator.func.attr in ("get", "post", "put", "delete", "patch"):
                        if decorator.args and isinstance(decorator.args[0], ast.Constant):
                            route_path = decorator.args[0].value

            if not route_path:
                continue

            # Walk function body to find called symbols
            called_symbols = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Name):
                    if child.id in main_symbols:
                        called_symbols.add(child.id)
                elif isinstance(child, ast.Attribute):
                    if isinstance(child.value, ast.Name) and child.value.id in main_symbols:
                        called_symbols.add(child.value.id)

            # Check reachability for each called symbol
            reaches_affected = False
            symbol_paths = []

            for sym in called_symbols:
                target_file = main_symbols[sym]
                deps = get_transitive_dependencies(target_file, imports)
                
                # Check if any affected file is in the dependency closure
                hit_affected = deps.intersection(affected_set)
                if hit_affected:
                    reaches_affected = True
                    symbol_paths.append(f"{sym} -> {handler_name}")

            if reaches_affected:
                if route_path not in affected_endpoints:
                    affected_endpoints.append(route_path)
                for sp in symbol_paths:
                    if sp not in call_paths:
                        call_paths.append(sp)

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

    importers, imports, symbol_to_file = build_import_graph()
    affected_files = get_affected_files(changed, importers)
    affected_endpoints, call_paths = get_endpoints_and_paths(affected_files, imports, symbol_to_file)

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
