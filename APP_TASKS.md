# APP Tasks Checklist

## Task 1: Demo Banking Application (`demo-app/`)
- [x] Create seed data (`demo-app/data/seed.json`) with 20 fake customers and deterministic loan records.
- [x] Implement core interest module (`demo-app/core/interest.py`): `monthly_rate` and `emi` formulas.
- [x] Implement services:
  - [x] `demo-app/services/emi_service.py`
  - [x] `demo-app/services/loan_service.py`
  - [x] `demo-app/services/payment_service.py` (read-only balance calculation)
- [x] Implement FastAPI application & routes (`demo-app/main.py`):
  - [x] `GET /health` (returns 200 OK)
  - [x] `POST /api/emi`
  - [x] `GET /api/loan/{id}`
  - [x] `POST /api/payment`
  - [x] `GET /api/customer/{id}`
- [x] Verify HTTP response structure (standard payload with `request_id` and `generated_at`).
- [x] Verify standard error response structure for 400 / 404 cases.

## Task 2: Scenario Generator (`scenarios/generate.py`)
- [x] Implement scenario generation script sending requests to `http://127.0.0.1:8000`.
- [x] Generate ~60 scenario JSON files (`scenarios/<tag>_<number>.json`):
  - [x] ~20 EMI scenarios (including edge cases: 0% interest, 1-month, large principal).
  - [x] ~15 Loan scenarios.
  - [x] ~15 Payment scenarios.
  - [x] ~10 Customer scenarios.
- [x] Generate `scenarios/manifest.json` grouping scenario IDs by tag.

## Task 3: Verification & Determinism Testing
- [x] Start FastAPI server and verify health endpoint.
- [x] Execute scenario generator against live server.
- [x] Run repeat requests to confirm business fields are 100% deterministic while noise fields change.
