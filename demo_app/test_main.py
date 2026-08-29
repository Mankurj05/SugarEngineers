import pytest
from fastapi.testclient import TestClient
from demo_app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"
    assert "meta" in data
    assert "request_id" in data["meta"]
    assert "generated_at" in data["meta"]

def test_get_customer_success():
    response = client.get("/api/customer/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Alice Smith"
    
def test_get_customer_not_found():
    response = client.get("/api/customer/999")
    assert response.status_code == 404
    data = response.json()
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["code"] == 404
    assert data["error"]["message"] == "Customer not found: 999"

def test_emi_calculation_success():
    payload = {
        "principal": 50000,
        "annual_rate": 5.5,
        "tenure_months": 60
    }
    response = client.post("/api/emi", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "emi" in data["data"]
    # 50000 at 5.5% for 60 months
    # Monthly rate = 0.055 / 12 = 0.0045833
    # EMI = 50000 * 0.0045833 * (1.0045833)^60 / ((1.0045833)^60 - 1) = ~955.05
    assert data["data"]["emi"] == 955.06

def test_emi_calculation_invalid_params():
    payload = {
        "principal": -100,
        "annual_rate": 5.5,
        "tenure_months": 60
    }
    response = client.post("/api/emi", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == 400

def test_get_loan_success():
    response = client.get("/api/loan/L-101")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["id"] == "L-101"
    assert data["data"]["principal"] == 50000

def test_get_loan_not_found():
    response = client.get("/api/loan/NON-EXISTENT")
    assert response.status_code == 404
    
def test_calculate_payment():
    payload = {
        "loan_id": "L-101",
        "payments_made": 10
    }
    response = client.post("/api/payment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["loan_id"] == "L-101"
    assert data["data"]["payments_made"] == 10
    assert "remaining_balance" in data["data"]
