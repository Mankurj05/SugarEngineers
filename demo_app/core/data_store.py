import json
import os
from typing import Dict, Any

SEED_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "seed.json")

def load_seed_data() -> Dict[str, Any]:
    with open(SEED_FILE, "r") as f:
        return json.load(f)

def get_customer(customer_id: str) -> Dict[str, Any]:
    data = load_seed_data()
    for customer in data:
        if customer["id"] == customer_id:
            return customer
    return None

def get_loan(loan_id: str) -> Dict[str, Any]:
    data = load_seed_data()
    for customer in data:
        for loan in customer.get("loans", []):
            if loan["id"] == loan_id:
                # Attach customer_id to loan for convenience
                loan["customer_id"] = customer["id"]
                return loan
    return None
