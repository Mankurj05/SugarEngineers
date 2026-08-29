# APP Notes

## Overview
BlastProof App component consists of a deterministic FastAPI banking application (`demo-app/`) and an HTTP scenario generator (`scenarios/generate.py`).
The application models loan calculations, customer profiles, loan lookups, and payments, serving as the target system for replay-based regression and safety testing.

## Key Rules & Constraints
1. **Determinism:** All business logic outputs must be 100% deterministic given identical inputs. Seed data is static (`demo-app/data/seed.json` with 20 customers) and payment operations are strictly read-only calculations.
2. **Noise Fields:** Every HTTP response must include dynamic noise fields (`request_id` [UUID4] and `generated_at` [ISO timestamp]), which will be ignored by the engine's semantic comparator.
3. **Interest Logic:** ALL interest math lives strictly in `demo-app/core/interest.py`. No duplicating interest math in services or routes.
4. **Error Format:** Standardized error response structure across `/api/*`:
   ```json
   {
     "success": false,
     "data": null,
     "error": { "message": "..." },
     "request_id": "...",
     "generated_at": "..."
   }
   ```
5. **Code Ownership & Boundaries:**
   - Work ONLY on branch `app`.
   - NEVER touch anything in `engine/`.
   - Allowed dependencies: `fastapi`, `uvicorn`. Standard library for scenario generation.

## Dependencies & Architecture Flow
`payment_service` -> `emi_service` -> `interest.py`
`loan_service` -> `interest.py`
