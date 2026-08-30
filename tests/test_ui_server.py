import json
import pytest
from fastapi.testclient import TestClient
from ui.server import app, REPORT_FILE, RESULTS_FILE, REPORT_DATA_JS

@pytest.fixture
def client():
    return TestClient(app)

def test_serve_dashboard(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "BlastProof" in response.text

def test_get_report_json(client, tmp_path, monkeypatch):
    test_report = {
        "summary": {
            "total": 2,
            "identical": 1,
            "intentional": 0,
            "regression": 1,
            "unexplained": 0
        },
        "radius": {"endpoints": ["/api/cart"], "changed": ["demo_app/core/interest.py"]},
        "results": [
            {
                "scenario": "cart_discount",
                "verdict": "regression",
                "diffs": [{"path": "discount", "old": 10, "new": 5}]
            }
        ]
    }
    
    report_file = tmp_path / "report.json"
    report_file.write_text(json.dumps(test_report), encoding="utf-8")
    monkeypatch.setattr("ui.server.REPORT_FILE", report_file)
    
    # Test /api/report
    res_api = client.get("/api/report")
    assert res_api.status_code == 200
    assert res_api.json() == test_report

    # Test /report.json direct static endpoint
    res_file = client.get("/report.json")
    assert res_file.status_code == 200
    assert res_file.json() == test_report

def test_get_report_data_js(client, tmp_path, monkeypatch):
    js_file = tmp_path / "report-data.js"
    js_file.write_text("window.BLASTPROOF_REPORT = {};", encoding="utf-8")
    monkeypatch.setattr("ui.server.REPORT_DATA_JS", js_file)

    res = client.get("/ui/report-data.js")
    assert res.status_code == 200
    assert "window.BLASTPROOF_REPORT" in res.text
