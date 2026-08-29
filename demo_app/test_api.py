import pytest
from fastapi.testclient import TestClient
from demo_app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_emi():
    response = client.post("/api/emi", json={"principal": 500000, "annual_rate": 12, "months": 60})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "request_id" in data
    assert "generated_at" in data
    
    assert data["data"]["principal"] == 500000
    assert data["data"]["annual_rate"] == 12
    assert data["data"]["months"] == 60
    assert data["data"]["emi"] == 11122.22

def test_loan():
    response = client.get("/api/loan/loan_002")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["principal"] == 250000
    assert data["data"]["annual_rate"] == 10.5
    assert data["data"]["duration_months"] == 36

def test_payment():
    # Read-only payment check
    response = client.post("/api/payment", json={"loan_id": "loan_002", "amount": 10000})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["loan_id"] == "loan_002"
    assert data["data"]["payment_amount"] == 10000
    assert data["data"]["resulting_outstanding_balance"] == 203582.81
    
    # Verify the seed wasn't modified
    response2 = client.post("/api/payment", json={"loan_id": "loan_002", "amount": 10000})
    assert response2.json()["data"]["resulting_outstanding_balance"] == 203582.81

def test_customer():
    response = client.get("/api/customer/cust_002")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Bob Johnson"
    assert len(data["data"]["loans_summary"]) == 1
