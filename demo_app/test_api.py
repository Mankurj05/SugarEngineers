import pytest
from fastapi.testclient import TestClient
from demo_app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"] == {"status": "ok"}

def test_emi():
    response = client.post("/api/emi", json={"principal": 500000, "annual_rate": 12, "tenure_months": 60})
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "meta" in data
    assert "request_id" in data["meta"]
    assert "generated_at" in data["meta"]
    
    assert data["data"]["principal"] == 500000
    assert data["data"]["annual_rate"] == 12
    assert data["data"]["tenure_months"] == 60
    assert data["data"]["emi"] == 11122.22

def test_loan():
    response = client.get("/api/loan/L-101")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["principal"] == 50000
    assert data["data"]["rate"] == 5.5

def test_payment():
    # Read-only payment check
    response = client.post("/api/payment", json={"loan_id": "L-101", "payments_made": 5})
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["loan_id"] == "L-101"
    assert data["data"]["payments_made"] == 5

def test_customer():
    response = client.get("/api/customer/1")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Alice Smith"
    assert len(data["data"]["loans"]) == 1
