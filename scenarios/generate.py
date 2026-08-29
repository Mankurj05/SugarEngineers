import json
import os
from pathlib import Path

SCENARIOS_DIR = Path("scenarios")

def save_scenario(tag, number, method, path, request_data):
    filename = f"{tag}_{number}.json"
    filepath = SCENARIOS_DIR / filename
    
    scenario_id = f"{tag}_{number}"
    
    scenario = {
        "id": scenario_id,
        "method": method,
        "path": path,
        "body": request_data if request_data is not None else {},
        "tags": [tag]
    }
    
    with open(filepath, "w") as f:
        json.dump(scenario, f, indent=2)
        
    return scenario_id

def generate_emi_scenarios():
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
        scenario_id = save_scenario(tag, i, "POST", "/api/emi", payload)
        ids.append(scenario_id)
        
    return ids

def generate_loan_scenarios():
    tag = "loan"
    ids = []
    
    # We know we have L-101 to L-120 in seed data
    loan_ids_to_fetch = [f"L-{100+i}" for i in range(1, 13)]  # 12 valid loans
    
    # Error cases (404)
    error_cases = ["L-999", "INVALID", "L-0"]  # 3 invalid loans
    
    all_cases = loan_ids_to_fetch + error_cases
    
    for i, loan_id in enumerate(all_cases, 1):
        path = f"/api/loan/{loan_id}"
        scenario_id = save_scenario(tag, i, "GET", path, {})
        ids.append(scenario_id)
        
    return ids

def generate_payment_scenarios():
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
        scenario_id = save_scenario(tag, i, "POST", "/api/payment", payload)
        ids.append(scenario_id)
        
    return ids

def generate_customer_scenarios():
    tag = "customer"
    ids = []
    
    # 7 valid customers
    customer_ids = [1, 2, 4, 10, 15, 19, 20] 
    
    # 3 invalid customers
    error_cases = [99, 1000, 0]
    
    all_cases = customer_ids + error_cases
    
    for i, cust_id in enumerate(all_cases, 1):
        path = f"/api/customer/{cust_id}"
        scenario_id = save_scenario(tag, i, "GET", path, {})
        ids.append(scenario_id)
        
    return ids

def main():
    SCENARIOS_DIR.mkdir(exist_ok=True)
    
    # Clean up old scenario files that start with emi_00*, etc. if we can,
    # but the instructions specifically mentioned "delete the duplicate emi_001-emi_020 set"
    # I'll do that in bash afterwards.
    
    manifest = {}
    
    print("Generating EMI scenarios...")
    manifest["emi"] = generate_emi_scenarios()
    print(f"Generated {len(manifest['emi'])} EMI scenarios")
    
    print("Generating Loan scenarios...")
    manifest["loan"] = generate_loan_scenarios()
    print(f"Generated {len(manifest['loan'])} Loan scenarios")
    
    print("Generating Payment scenarios...")
    manifest["payment"] = generate_payment_scenarios()
    print(f"Generated {len(manifest['payment'])} Payment scenarios")
    
    print("Generating Customer scenarios...")
    manifest["customer"] = generate_customer_scenarios()
    print(f"Generated {len(manifest['customer'])} Customer scenarios")
        
    manifest_path = SCENARIOS_DIR / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    total = sum(len(ids) for ids in manifest.values())
    print(f"Success! Generated {total} total scenarios and saved manifest.json")

if __name__ == "__main__":
    main()
