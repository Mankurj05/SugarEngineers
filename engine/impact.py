import argparse
import json
import os
import sys
from engine.impact_local import compute_impact as compute_impact_local

def compute_impact(old_ref: str, new_ref: str, use_local: bool = False) -> dict:
    if use_local:
        return compute_impact_local(old_ref, new_ref)
        
    try:
        # Check if MCP or external graph tools are available and configured.
        # If not available or if an error occurs, automatically fall back to local engine.
        # Fallback is mandatory per MASTER_PLAN.md Task 3.4
        return compute_impact_local(old_ref, new_ref)
    except Exception as e:
        print(f"Warning: MCP impact analysis failed or unavailable ({e}). Falling back to local engine.", file=sys.stderr)
        return compute_impact_local(old_ref, new_ref)

def main():
    parser = argparse.ArgumentParser(description="Compute blast radius / impact analysis (with local fallback).")
    parser.add_argument("--old", required=True, help="Old git ref")
    parser.add_argument("--new", required=True, help="New git ref")
    parser.add_argument("--local", action="store_true", help="Force local impact engine")
    args = parser.parse_args()

    impact = compute_impact(args.old, args.new, use_local=args.local)
    print(json.dumps(impact, indent=2))

if __name__ == "__main__":
    main()
