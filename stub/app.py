from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone

app = FastAPI()

class EMIRequest(BaseModel):
    principal: float
    annual_rate: float
    months: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/emi")
def calculate_emi(req: EMIRequest):
    return {
        "emi": 9999.99,
        "request_id": str(uuid.uuid4()),
        "generated_at": datetime.now(timezone.utc).isoformat()
    }
