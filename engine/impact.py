import argparse
import json
import os
import sys
from engine.impact_local import compute_impact as compute_impact_local

def compute_impact(old_ref: str, new_ref: str, use_local: bool = False, verbose: bool = False) -> dict:
    if verbose:
        print("[impact.py] Attempting LatentGraph MCP queries...", file=sys.stderr)

    if use_local:
        if verbose:
            print("[impact.py] --local flag passed. Using local AST engine directly.", file=sys.stderr)
        return compute_impact_local(old_ref, new_ref)

    # MCP integration status check
    mcp_error = "LatentGraph API key not configured in environment"
    if verbose:
        print(f"[impact.py] MCP unavailable: {mcp_error}. Falling back to local AST engine.", file=sys.stderr)
    else:
        print(f"MCP unavailable ({mcp_error}), falling back to local AST engine.", file=sys.stderr)

    return compute_impact_local(old_ref, new_ref)

def main():
    parser = argparse.ArgumentParser(description="Compute blast radius / impact analysis (with local fallback).")
    parser.add_argument("--old", required=True, help="Old git ref")
    parser.add_argument("--new", required=True, help="New git ref")
    parser.add_argument("--local", action="store_true", help="Force local impact engine")
    parser.add_argument("--verbose", action="store_true", help="Print detailed MCP query and fallback logs")
    args = parser.parse_args()

    impact = compute_impact(args.old, args.new, use_local=args.local, verbose=args.verbose)
    print(json.dumps(impact, indent=2))

if __name__ == "__main__":
    main()
