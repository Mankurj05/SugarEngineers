from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uuid
from datetime import datetime, timezone
import time

from demo_app.services.emi_service import EMIService
from demo_app.services.loan_service import LoanService
from demo_app.services.payment_service import PaymentService

app = FastAPI(title="Demo Banking Application")

loan_service = LoanService()
payment_service = PaymentService(loan_service)

# Request Models
class EMIRequest(BaseModel):
    principal: float
    annual_rate: float
    tenure_months: int

class PaymentRequest(BaseModel):
    loan_id: str
    payments_made: int

# Middleware to add standard response structure
@app.middleware("http")
async def add_standard_response_structure(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()
    
    response = await call_next(request)
    
    # Process only if we're sending JSON response and not an error handled by exception handler
    # FastAPI handles JSONResponse specifically, but for standard models we need to hook here or via APIRoute
    # For simplicity in this demo, we'll let custom responses pass through and standardize the output directly in the routes
    # But we inject request_id as header anyway
    response.headers["X-Request-ID"] = request_id
    
    return response

# Custom Exception Handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.status_code,
                "message": exc.detail
            },
            "meta": {
                "request_id": request.headers.get("X-Request-ID", str(uuid.uuid4())),
                "generated_at": datetime.now(timezone.utc).isoformat()
            }
        },
    )

def success_response(data: dict) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": {
            "request_id": str(uuid.uuid4()),
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
    }

@app.get("/health")
async def health_check():
    return success_response({"status": "ok"})

@app.post("/api/emi")
async def calculate_emi_endpoint(request: EMIRequest):
    if request.principal <= 0 or request.tenure_months <= 0 or request.annual_rate < 0:
        raise HTTPException(status_code=400, detail="Invalid loan parameters. Principal and tenure must be > 0. Rate must be >= 0.")
        
    emi = EMIService.compute_emi(request.principal, request.annual_rate, request.tenure_months)
    return success_response({
        "principal": request.principal,
        "annual_rate": request.annual_rate,
        "tenure_months": request.tenure_months,
        "emi": emi
    })

@app.get("/api/loan/{loan_id}")
async def get_loan(loan_id: str):
    loan = loan_service.get_loan(loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail=f"Loan not found: {loan_id}")
    return success_response(loan)

@app.post("/api/payment")
async def calculate_payment_balance(request: PaymentRequest):
    if request.payments_made < 0:
        raise HTTPException(status_code=400, detail="Payments made cannot be negative")
        
    balance_info = payment_service.calculate_balance(request.loan_id, request.payments_made)
    if not balance_info:
        raise HTTPException(status_code=404, detail=f"Loan not found: {request.loan_id}")
        
    return success_response(balance_info)

@app.get("/api/customer/{customer_id}")
async def get_customer(customer_id: int):
    customer = loan_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail=f"Customer not found: {customer_id}")
    return success_response(customer)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
