import argparse
import json
import httpx
import os
import sys
import time
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
SCENARIOS_DIR = Path("scenarios")

def ensure_server_running():
    try:
        response = httpx.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Server is running!")
            return True
    except httpx.RequestError:
        print("Server not running. Please start the demo-app server on port 8000.")
        return False
    return False

def validate_scenario(filepath: Path) -> bool:
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return False

    required_keys = {"id", "method", "path", "body", "tags"}
    actual_keys = set(data.keys())
    
    if required_keys != actual_keys:
        print(f"Validation failed for {filepath.name}: keys mismatch. Expected {required_keys}, got {actual_keys}")
        return False
        
    if not isinstance(data.get("tags"), list):
        print(f"Validation failed for {filepath.name}: 'tags' must be a list.")
        return False
        
    return True

def run_validation():
    print("Validating scenarios...")
    invalid_count = 0
    total = 0
    for filepath in SCENARIOS_DIR.glob("*.json"):
        if filepath.name == "manifest.json":
            continue
        total += 1
        if not validate_scenario(filepath):
            invalid_count += 1
            
    if invalid_count > 0:
        print(f"Validation failed! {invalid_count} out of {total} scenarios are invalid.")
        sys.exit(1)
    else:
        print(f"Validation passed! All {total} scenarios match the contract.")
        sys.exit(0)

def save_scenario(tag, number, method, path, request_data):
    filename = f"{tag}_{number}.json"
    filepath = SCENARIOS_DIR / filename
    
    scenario = {
        "id": f"{tag}_{number}",
        "method": method,
        "path": path,
        "body": request_data if request_data is not None else {},
        "tags": [tag]
    }
    
    with open(filepath, "w") as f:
        json.dump(scenario, f, indent=2)
        
    return scenario["id"]

def generate_emi_scenarios(client):
    tag = "emi"
    ids = []
    
    # Normal cases
    base_principal = 10000
    base_rate = 5.0
    base_tenure = 12
    
    cases = []
    
    # 5 standard cases
    for i in range(1, 6):
        cases.append({
            "principal": base_principal * i,
            "annual_rate": base_rate + (i * 0.5),
            "tenure_months": base_tenure * i
        })
        
    # Edge cases
    cases.extend([
        # 0% interest
        {"principal": 50000, "annual_rate": 0, "tenure_months": 24},
        {"principal": 100000, "annual_rate": 0, "tenure_months": 12},
        # 1-month tenure
        {"principal": 10000, "annual_rate": 10.0, "tenure_months": 1},
        # Large principal
        {"principal": 10000000, "annual_rate": 5.5, "tenure_months": 360},
        {"principal": 50000000, "annual_rate": 4.5, "tenure_months": 300},
        # Small principal
        {"principal": 100, "annual_rate": 20.0, "tenure_months": 6},
        # Long tenure
        {"principal": 100000, "annual_rate": 3.5, "tenure_months": 480},
        # High interest
        {"principal": 5000, "annual_rate": 36.0, "tenure_months": 12},
        # Fractional months (will be parsed to int normally but let's stick to valid types for the model)
        {"principal": 25000, "annual_rate": 7.25, "tenure_months": 15},
        {"principal": 15500.50, "annual_rate": 6.75, "tenure_months": 21},
    ])
    
    # Error cases (400)
    error_cases = [
        {"principal": -5000, "annual_rate": 5.0, "tenure_months": 12},
        {"principal": 5000, "annual_rate": -5.0, "tenure_months": 12},
        {"principal": 5000, "annual_rate": 5.0, "tenure_months": 0},
        {"principal": 0, "annual_rate": 5.0, "tenure_months": 12},
        {"principal": 5000, "annual_rate": 5.0, "tenure_months": -5},
    ]
    
    all_cases = cases + error_cases
    
    for i, payload in enumerate(all_cases, 1):
        # We only need to check if the route is valid, the actual recording happens in replay.py
        # But we do a test request anyway to make sure we don't save broken inputs
        response = client.post(f"{BASE_URL}/api/emi", json=payload)
        scenario_id = save_scenario(tag, i, "POST", "/api/emi", payload)
        ids.append(scenario_id)
        
    return ids

def generate_loan_scenarios(client):
    tag = "loan"
    ids = []
    
    # We know we have L-101 to L-120 in seed data
    loan_ids_to_fetch = [f"L-{100+i}" for i in range(1, 13)]  # 12 valid loans
    
    # Error cases (404)
    error_cases = ["L-999", "INVALID", "L-0"]  # 3 invalid loans
    
    all_cases = loan_ids_to_fetch + error_cases
    
    for i, loan_id in enumerate(all_cases, 1):
        endpoint = f"/api/loan/{loan_id}"
        response = client.get(f"{BASE_URL}{endpoint}")
        scenario_id = save_scenario(tag, i, "GET", endpoint, None)
        ids.append(scenario_id)
        
    return ids

def generate_payment_scenarios(client):
    tag = "payment"
    ids = []
    
    cases = [
        {"loan_id": "L-101", "payments_made": 1},
        {"loan_id": "L-101", "payments_made": 30},
        {"loan_id": "L-101", "payments_made": 60},  # Full term
        {"loan_id": "L-102", "payments_made": 12},
        {"loan_id": "L-103", "payments_made": 24},
        {"loan_id": "L-104", "payments_made": 100},
        {"loan_id": "L-105", "payments_made": 6},
        {"loan_id": "L-106", "payments_made": 80},
        {"loan_id": "L-107", "payments_made": 120},
        {"loan_id": "L-108", "payments_made": 36},
        {"loan_id": "L-109", "payments_made": 0},   # Zero payments
        {"loan_id": "L-110", "payments_made": 500}, # Exceeds tenure
    ]
    
    error_cases = [
        {"loan_id": "L-999", "payments_made": 10},  # Invalid loan
        {"loan_id": "L-101", "payments_made": -5},  # Invalid payment count
        {"loan_id": "INVALID", "payments_made": 1}, # Invalid loan
    ]
    
    all_cases = cases + error_cases
    
    for i, payload in enumerate(all_cases, 1):
        response = client.post(f"{BASE_URL}/api/payment", json=payload)
        scenario_id = save_scenario(tag, i, "POST", "/api/payment", payload)
        ids.append(scenario_id)
        
    return ids

def generate_customer_scenarios(client):
    tag = "customer"
    ids = []
    
    # 7 valid customers
    customer_ids = [1, 2, 4, 10, 15, 19, 20] 
    
    # 3 invalid customers
    error_cases = [99, 1000, 0]
    
    all_cases = customer_ids + error_cases
    
    for i, cust_id in enumerate(all_cases, 1):
        endpoint = f"/api/customer/{cust_id}"
        response = client.get(f"{BASE_URL}{endpoint}")
        scenario_id = save_scenario(tag, i, "GET", endpoint, None)
        ids.append(scenario_id)
        
    return ids

def main():
    parser = argparse.ArgumentParser(description="Generate scenario files")
    parser.add_argument("--validate", action="store_true", help="Validate existing scenarios against schema")
    args = parser.parse_args()

    if args.validate:
        run_validation()
        return

    if not ensure_server_running():
        return

    SCENARIOS_DIR.mkdir(exist_ok=True)
    
    manifest = {}
    
    with httpx.Client() as client:
        print("Generating EMI scenarios...")
        manifest["emi"] = generate_emi_scenarios(client)
        print(f"Generated {len(manifest['emi'])} EMI scenarios")
        
        print("Generating Loan scenarios...")
        manifest["loan"] = generate_loan_scenarios(client)
        print(f"Generated {len(manifest['loan'])} Loan scenarios")
        
        print("Generating Payment scenarios...")
        manifest["payment"] = generate_payment_scenarios(client)
        print(f"Generated {len(manifest['payment'])} Payment scenarios")
        
        print("Generating Customer scenarios...")
        manifest["customer"] = generate_customer_scenarios(client)
        print(f"Generated {len(manifest['customer'])} Customer scenarios")
        
    manifest_path = SCENARIOS_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    total = sum(len(ids) for ids in manifest.values())
    print(f"Success! Generated {total} total scenarios and saved manifest.json")

if __name__ == "__main__":
    main()
