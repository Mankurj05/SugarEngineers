import argparse
import json
import re
import sys
from typing import Any, Dict, List

# Strict regex for UUIDs (8-4-4-4-12)
UUID_PATTERN = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)

# Regex for ISO 8601 timestamps (covers standard variations)
ISO_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$"
)

# Keys explicitly ignored
IGNORE_KEYS = {"request_id", "generated_at", "trace_id"}

def is_noise(key: str, value: Any) -> bool:
    if key in IGNORE_KEYS:
        return True
    if isinstance(value, str):
        if UUID_PATTERN.match(value) or ISO_TIMESTAMP_PATTERN.match(value):
            return True
    return False

def is_noise_val(val: Any) -> bool:
    if isinstance(val, str):
        return bool(UUID_PATTERN.match(val) or ISO_TIMESTAMP_PATTERN.match(val))
    return False

def compare_values(old_val: Any, new_val: Any, path: str, diffs: List[Dict[str, Any]]) -> None:
    # Type mismatch is an automatic drift
    if type(old_val) != type(new_val):
        if isinstance(old_val, (int, float)) and isinstance(new_val, (int, float)):
            pass
        else:
            diffs.append({"path": path, "old": old_val, "new": new_val})
            return

    # Dicts
    if isinstance(old_val, dict):
        all_keys = set(old_val.keys()) | set(new_val.keys())
        for k in sorted(all_keys):
            if k in IGNORE_KEYS:
                continue
            
            ov = old_val.get(k)
            nv = new_val.get(k)
            
            # Require BOTH sides to match noise pattern before skipping
            if is_noise_val(ov) and is_noise_val(nv):
                continue
            
            p = f"{path}.{k}" if path else k
            if k not in old_val:
                diffs.append({"path": p, "old": None, "new": nv})
            elif k not in new_val:
                diffs.append({"path": p, "old": ov, "new": None})
            else:
                compare_values(ov, nv, p, diffs)
                
    # Lists
    elif isinstance(old_val, list):
        if len(old_val) != len(new_val):
            diffs.append({"path": path, "old": f"List of length {len(old_val)}", "new": f"List of length {len(new_val)}"})
            return
            
        for i, (ov, nv) in enumerate(zip(old_val, new_val)):
            p = f"{path}.{i}" if path else str(i)
            compare_values(ov, nv, p, diffs)
            
    # Numbers
    elif isinstance(old_val, (int, float)):
        if abs(old_val - new_val) >= 0.01:
            diffs.append({"path": path, "old": old_val, "new": new_val})
            
    # Strings and everything else
    else:
        if old_val != new_val:
            diffs.append({"path": path, "old": old_val, "new": new_val})

def compare_scenario(scenario_data: Dict[str, Any]) -> Dict[str, Any]:
    scenario_id = scenario_data.get("scenario")
    old_data = scenario_data.get("old", {})
    new_data = scenario_data.get("new", {})
    
    old_status = old_data.get("status")
    new_status = new_data.get("status")
    
    # 1. Status codes differ
    if old_status != new_status:
        return {
            "scenario": scenario_id,
            "verdict": "drift",
            "diffs": [{"path": "status", "old": old_status, "new": new_status}]
        }
        
    old_json = old_data.get("json", {})
    new_json = new_data.get("json", {})
    
    diffs = []
    
    if isinstance(old_json, dict) and isinstance(new_json, dict):
        compare_values(old_json, new_json, "", diffs)
    elif isinstance(old_json, list) and isinstance(new_json, list):
        compare_values(old_json, new_json, "", diffs)
    else:
        compare_values(old_json, new_json, "root", diffs)
        
    return {
        "scenario": scenario_id,
        "verdict": "drift" if diffs else "identical",
        "diffs": diffs
    }

def compare_results(results_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    output = []
    for scenario_data in results_data:
        result = compare_scenario(scenario_data)
        output.append(result)
    return output

def run_selftest():
    print("Running compare.py self-test...")
    
    noise_only = {
        "scenario": "noise_test",
        "old": {
            "status": 200,
            "json": {
                "emi": 1000.0,
                "request_id": "12345678-1234-1234-1234-123456789012",
                "generated_at": "2026-08-28T12:00:00Z",
                "unnamed_uuid": "87654321-4321-4321-4321-210987654321"
            }
        },
        "new": {
            "status": 200,
            "json": {
                "emi": 1000.0,
                "request_id": "87654321-4321-4321-4321-210987654321",
                "generated_at": "2026-08-28T12:00:01Z",
                "unnamed_uuid": "12345678-1234-1234-1234-123456789012"
            }
        }
    }
    
    real_drift = {
        "scenario": "drift_test",
        "old": {
            "status": 200,
            "json": {
                "emi": 14820.0,
                "request_id": "12345678-1234-1234-1234-123456789012"
            }
        },
        "new": {
            "status": 200,
            "json": {
                "emi": 10718.4,
                "request_id": "87654321-4321-4321-4321-210987654321"
            }
        }
    }
    
    float_tolerance = {
        "scenario": "float_test",
        "old": {
            "status": 200,
            "json": {
                "emi": 14820.004
            }
        },
        "new": {
            "status": 200,
            "json": {
                "emi": 14820.010
            }
        }
    }

    uuid_to_error = {
        "scenario": "uuid_to_error_test",
        "old": {
            "status": 200,
            "json": {
                "session_id": "12345678-1234-1234-1234-123456789012"
            }
        },
        "new": {
            "status": 200,
            "json": {
                "session_id": "ERROR"
            }
        }
    }
    
    res1 = compare_scenario(noise_only)
    if res1["verdict"] != "identical" or len(res1["diffs"]) > 0:
        print("FAIL: Noise-only scenario drifted")
        print(json.dumps(res1, indent=2))
        sys.exit(1)
        
    res2 = compare_scenario(real_drift)
    if res2["verdict"] != "drift" or len(res2["diffs"]) != 1 or res2["diffs"][0]["path"] != "emi":
        print("FAIL: Real drift scenario did not catch only the numeric drift")
        print(json.dumps(res2, indent=2))
        sys.exit(1)
        
    res3 = compare_scenario(float_tolerance)
    if res3["verdict"] != "identical" or len(res3["diffs"]) > 0:
        print("FAIL: Float tolerance scenario drifted (diff was 0.006)")
        print(json.dumps(res3, indent=2))
        sys.exit(1)

    res4 = compare_scenario(uuid_to_error)
    if res4["verdict"] != "drift" or len(res4["diffs"]) != 1 or res4["diffs"][0]["new"] != "ERROR":
        print("FAIL: UUID to ERROR scenario was silently swallowed as noise")
        print(json.dumps(res4, indent=2))
        sys.exit(1)
        
    print("PASS: Self-test successful.")
    
def main():
    parser = argparse.ArgumentParser(description="Compare old and new scenario results")
    parser.add_argument("--results", help="Path to results.json")
    parser.add_argument("--selftest", action="store_true", help="Run self-proving fixtures")
    args = parser.parse_args()
    
    if args.selftest:
        run_selftest()
        sys.exit(0)
        
    if not args.results:
        parser.error("--results is required unless running --selftest")
        
    try:
        with open(args.results, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {args.results}: {e}")
        sys.exit(1)
        
    if not isinstance(data, list):
        print("Error: results.json must contain a top-level JSON array.")
        sys.exit(1)
        
    output = compare_results(data)
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
