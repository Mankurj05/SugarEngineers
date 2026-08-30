import json
import subprocess
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
REPORT_FILE = PROJECT_ROOT / "report.json"
RESULTS_FILE = PROJECT_ROOT / "results.json"
INDEX_HTML = PROJECT_ROOT / "index.html"
REPORT_DATA_JS = PROJECT_ROOT / "ui" / "report-data.js"

app = FastAPI(title="BlastProof UI Server")

class TeachRequest(BaseModel):
    scenario: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    if INDEX_HTML.exists():
        return HTMLResponse(content=INDEX_HTML.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>BlastProof UI index.html not found</h1>", status_code=404)

@app.get("/report.json")
async def get_report_json_file():
    if not REPORT_FILE.exists():
        # Fallback to generating or serving results as report if report.json is missing
        if RESULTS_FILE.exists():
            with open(RESULTS_FILE, "r", encoding="utf-8") as f:
                res = json.load(f)
                return {
                    "summary": {"total": len(res), "identical": 0, "intentional": 0, "regression": len(res), "unexplained": 0},
                    "radius": {"source": "mcp"},
                    "results": res
                }
        raise HTTPException(status_code=404, detail="report.json not found.")
    return FileResponse(REPORT_FILE, media_type="application/json")

@app.get("/api/report")
async def get_report():
    if not REPORT_FILE.exists():
        raise HTTPException(status_code=404, detail="report.json not found. Run pipeline first.")
    with open(REPORT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/api/results")
async def get_results():
    if not RESULTS_FILE.exists():
        raise HTTPException(status_code=404, detail="results.json not found.")
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/ui/report-data.js")
async def get_report_data_js():
    if not REPORT_DATA_JS.exists():
        raise HTTPException(status_code=404, detail="report-data.js not found. Run pipeline first.")
    return FileResponse(REPORT_DATA_JS, media_type="application/javascript")

@app.post("/api/run")
async def run_pipeline():
    cmd = [
        sys.executable, "-m", "engine.cli",
        "--old", "main",
        "--new", "demo-change",
        "--app", "demo_app.main:app"
    ]
    try:
        res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, check=True)
        if REPORT_FILE.exists():
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"status": "success", "stdout": res.stdout}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Pipeline execution failed: {e.stderr or e.stdout}")

@app.post("/api/teach")
async def teach_invariant(req: TeachRequest):
    cmd = [
        sys.executable, "-m", "engine.teach",
        "--confirm",
        "--scenario", req.scenario
    ]
    try:
        res = subprocess.run(cmd, cwd=str(PROJECT_ROOT), capture_output=True, text=True, check=True)
        receipt_text = res.stdout.strip()
        status = "fallback"
        msg = receipt_text
        
        # Parse the python output to surface exact MCP status to the UI
        if "(mcp_graph_write)" in receipt_text:
            status = "success"
            parts = receipt_text.split("): ", 1)
            if len(parts) > 1: msg = parts[1]
        elif "(fallback_local_file)" in receipt_text:
            status = "fallback"
            parts = receipt_text.split("): ", 1)
            if len(parts) > 1: msg = parts[1]
            
        return {"status": status, "message": msg, "scenario": req.scenario}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Teach execution failed: {e.stderr or e.stdout}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5500)
