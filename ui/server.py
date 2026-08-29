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

app = FastAPI(title="BlastProof UI Server")

class TeachRequest(BaseModel):
    scenario: str

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    if INDEX_HTML.exists():
        return HTMLResponse(content=INDEX_HTML.read_text(encoding="utf-8"))
    return HTMLResponse(content="<h1>BlastProof UI index.html not found</h1>", status_code=404)

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

@app.post("/api/run")
async def run_pipeline():
    cmd = [
        sys.executable, "-m", "engine.cli",
        "--old", "v1.0",
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
        return {"success": True, "scenario": req.scenario, "receipt": receipt_text}
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Teach execution failed: {e.stderr or e.stdout}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5500)
