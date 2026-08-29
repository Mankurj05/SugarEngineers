import json
from pathlib import Path
from typing import Optional, Dict, Any, List

class LoanService:
    def __init__(self, data_file: str = "demo_app/data/seed.json"):
        self.data_file = data_file
        self._data = None
        
    def _load_data(self) -> List[Dict[str, Any]]:
        if self._data is None:
            path = Path(self.data_file)
            if not path.exists():
                return []
            with open(path, "r") as f:
                self._data = json.load(f)
        return self._data
        
    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve customer by ID."""
        data = self._load_data()
        for customer in data:
            if customer["id"] == customer_id:
                return customer
        return None
        
    def get_loan(self, loan_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve loan by ID."""
        data = self._load_data()
        for customer in data:
            for loan in customer.get("loans", []):
                if loan["id"] == loan_id:
                    # Inject customer ID for context
                    loan_with_context = loan.copy()
                    loan_with_context["customer_id"] = customer["id"]
                    return loan_with_context
        return None
