# BlastProof — Friend/APP Developer Task

## Role

You are the sole code writer for the **APP side** of the BlastProof hackathon project.

BlastProof is a safety gate for code changes. It compares application behavior between an old and new version by replaying recorded HTTP scenarios.

### My responsibility

I own:

* `demo-app/` — target FastAPI banking application
* `scenarios/` — recorded HTTP scenarios
* `ui/` — small PR safety-gate UI, later

### My teammate's responsibility

My teammate owns:

* `engine/`

**NEVER modify, create, delete, or refactor anything inside `engine/`.**

The integration boundary is:

* `scenarios/*.json` → consumed by the engine
* `report.json` → produced by the engine and consumed by my UI
* `CONTRACTS.md` → shared contract; do not change schemas without agreement

---

# 1. NON-NEGOTIABLE RULES

## Code ownership

* All code must be written through this LatentCode session.
* Do not use Copilot or another AI coding assistant.
* Do not modify `engine/`.
* Work only on branch `app`.
* Do not commit directly to `main`.
* Do not silently redesign shared schemas.

## Dependencies

Keep dependencies minimal.

Allowed:

* `fastapi`
* `uvicorn`

Before adding any other dependency, ask for approval.

For scenario generation, prefer Python standard library where practical.

## Application behavior

The application MUST be deterministic.

This means:

* Same business input → same business output.
* No randomness in business calculations.
* No wall-clock time in business fields.
* Seed data is fixed.
* Payment operations are read-only.

However, every HTTP response must contain these deliberate noise fields:

```json
{
  "request_id": "uuid4-value",
  "generated_at": "current ISO timestamp"
}
```

The engine's semantic comparator will intentionally ignore these fields.

## Interest calculation

ALL interest-related mathematics must live in:

```text
demo-app/core/interest.py
```

Do not duplicate interest calculations in services or routes.

This is critical because the hackathon demo intentionally changes one line in this file:

```python
annual_rate / 12
```

to:

```python
annual_rate / 365
```

BlastProof must detect the resulting behavioral drift.

---

# 2. REPOSITORY STRUCTURE

The relevant structure is:

```text
blastproof/
├── demo-app/
│   ├── main.py
│   ├── core/
│   │   └── interest.py
│   ├── services/
│   │   ├── emi_service.py
│   │   ├── loan_service.py
│   │   └── payment_service.py
│   └── data/
│       └── seed.json
│
├── scenarios/
│   ├── generate.py
│   ├── manifest.json
│   └── *.json
│
├── engine/
│   └── # teammate-owned — DO NOT TOUCH
│
├── ui/
│   └── # later
│
├── CONTRACTS.md
├── decisions.json
└── README.md
```

---

# 3. TASK 1 — BUILD THE DEMO BANKING APP

Create a FastAPI application under:

```text
demo-app/
```

## Required files

### `demo-app/main.py`

Responsibilities:

* Create FastAPI application.
* Register all API routes.
* Provide:

```text
GET /health
```

which returns HTTP `200`.

Routes:

```text
POST /api/emi
GET  /api/loan/{id}
POST /api/payment
GET  /api/customer/{id}
```

---

## `demo-app/core/interest.py`

This is the most important business module.

Implement:

```python
monthly_rate(annual_rate)
```

and:

```python
emi(principal, annual_rate, months)
```

Use the standard loan EMI formula.

Monthly interest rate:

```text
annual_rate / 12 / 100
```

The implementation should correctly handle:

* normal interest rates
* `0%`
* one-month loans
* large principals

Example:

```text
principal = 500000
annual_rate = 12
months = 60
```

should produce a deterministic EMI value.

Do not put timestamps, UUIDs, HTTP logic, or database logic here.

---

# 4. SERVICES

## `demo-app/services/emi_service.py`

Uses:

```text
core/interest.py
```

Responsible for EMI calculations and the EMI response/business structure.

---

## `demo-app/services/loan_service.py`

Uses:

```text
core/interest.py
```

Responsible for:

* retrieving a seeded loan
* calculating EMI
* generating the remaining repayment schedule

The result must be deterministic.

---

## `demo-app/services/payment_service.py`

Uses:

```text
emi_service.py`
```

This dependency is intentional.

The dependency chain should therefore demonstrate:

```text
payment_service
      ↓
emi_service
      ↓
interest.py
```

Payment endpoint must be strictly **read-only**.

It must calculate and return the recomputed outstanding balance but must NEVER modify `seed.json`.

---

# 5. SEED DATA

Create:

```text
demo-app/data/seed.json
```

Include approximately:

```text
20 fake customers
```

Each customer should have fixed deterministic data.

Customers should have:

* id
* name
* contact/profile information
* loans

Loans should contain enough information to support:

* loan lookup
* EMI calculation
* remaining schedule
* payment calculation

Do not use real people's personal information.

Use fictional names and values.

---

# 6. API CONTRACT

## POST `/api/emi`

Request:

```json
{
  "principal": 500000,
  "annual_rate": 12,
  "months": 60
}
```

Response must contain the calculated EMI/breakdown plus:

```json
{
  "request_id": "uuid",
  "generated_at": "2026-08-29T..."
}
```

The exact business response structure should remain simple and deterministic.

---

## GET `/api/loan/{id}`

Return:

* loan information
* principal
* annual rate
* duration
* EMI
* remaining schedule

Also include:

```json
{
  "request_id": "uuid",
  "generated_at": "..."
}
```

---

## POST `/api/payment`

Request:

```json
{
  "loan_id": 1,
  "amount": 5000
}
```

Return:

* payment amount
* previous/recomputed balance as appropriate
* resulting outstanding balance

But DO NOT persist or modify the payment.

Every identical request must produce identical business fields.

Also include:

```json
{
  "request_id": "uuid",
  "generated_at": "..."
}
```

---

## GET `/api/customer/{id}`

Return:

* customer profile
* loan summary

Also include:

```json
{
  "request_id": "uuid",
  "generated_at": "..."
}
```

---

# 7. ERROR HANDLING

Use sensible HTTP status codes.

Examples:

```text
200 — successful request
400 — invalid request
404 — customer/loan not found
```

Keep error responses deterministic except for:

```text
request_id
generated_at
```

The future Judge/LatentGraph demo will use a recorded rule that `/api/*` errors follow a consistent structure.

Prefer a consistent structure such as:

```json
{
  "success": false,
  "data": null,
  "error": {
    "message": "Loan not found"
  },
  "request_id": "...",
  "generated_at": "..."
}
```

---

# 8. DETERMINISM REQUIREMENT

This is extremely important.

For:

```text
POST /api/emi
```

with:

```json
{
  "principal": 500000,
  "annual_rate": 12,
  "months": 60
}
```

run the request multiple times.

The business fields must be identical every time.

Only:

```text
request_id
generated_at
```

are expected to change.

The engine's comparator will ignore those two fields.

---

# 9. TASK 2 — SCENARIO GENERATOR

Create:

```text
scenarios/generate.py
```

The script should send approximately **60 requests** to the running demo application.

Prefer Python's standard library HTTP functionality unless an already-approved dependency is required.

Target:

```text
http://127.0.0.1:8000
```

The script should save requests, NOT responses.

Each scenario must look like:

```json
{
  "id": "emi_017",
  "method": "POST",
  "path": "/api/emi",
  "body": {
    "principal": 500000,
    "annual_rate": 12,
    "months": 60
  },
  "tags": [
    "emi"
  ]
}
```

---

# 10. SCENARIO MIX

Generate approximately:

```text
20 EMI scenarios
15 loan scenarios
15 payment scenarios
10 customer scenarios
```

Total:

```text
60 scenarios
```

## EMI scenarios

Include varied values.

Must include:

* normal loan
* small principal
* large principal
* different interest rates
* different durations
* 0% interest
* 1-month duration
* large principal
* other reasonable edge cases

Example:

```text
500000 / 12% / 60 months
100000 / 8% / 24 months
10000 / 0% / 12 months
5000 / 10% / 1 month
10000000 / 15% / 120 months
```

---

## Loan scenarios

Approximately 15.

Use valid seeded loan IDs.

Example:

```text
loan_001
loan_002
loan_003
...
```

Ensure all selected IDs actually exist.

---

## Payment scenarios

Approximately 15.

Use valid loan IDs and varied payment amounts.

Remember:

**Payment must remain read-only.**

Running the scenario generator multiple times must not change the underlying seed data.

---

## Customer scenarios

Approximately 10.

Use valid customer IDs.

---

# 11. SCENARIO FILE NAMING

Use:

```text
scenarios/<tag>_<number>.json
```

Examples:

```text
emi_001.json
emi_002.json
loan_001.json
payment_001.json
customer_001.json
```

Each file contains:

```json
{
  "id": "...",
  "method": "...",
  "path": "...",
  "body": {},
  "tags": ["..."]
}
```

---

# 12. MANIFEST

Create:

```text
scenarios/manifest.json
```

It should list scenario IDs grouped by tag.

Example:

```json
{
  "emi": [
    "emi_001",
    "emi_002"
  ],
  "loan": [
    "loan_001"
  ],
  "payment": [
    "payment_001"
  ],
  "customer": [
    "customer_001"
  ]
}
```

The manifest must correspond exactly to the scenario files.

---

# 13. DEMO REGRESSION

The hackathon demo intentionally creates this change:

### Original

```python
annual_rate / 12
```

### Demo change

```python
annual_rate / 365
```

Do NOT change this during initial app construction.

The initial application must contain the correct monthly normalization.

Later, a separate branch called:

```text
demo-change
```

will contain ONLY this intentional one-line modification.

That branch must NOT be merged into main.

BlastProof will compare:

```text
v1.0
```

against:

```text
demo-change
```

and detect the behavioral drift.

---

# 14. GIT WORKFLOW

Work only on:

```text
app
```

Initial setup:

```bash
git checkout -b app
```

After the application and scenarios are complete:

```bash
git add .
git commit -m "Build demo banking app and scenarios"
git push -u origin app
```

Create a PR:

```text
app → main
```

After the PR is merged, the team will tag:

```text
v1.0
```

Then create:

```text
demo-change
```

from the correct baseline.

Change ONLY:

```text
annual_rate / 12
```

to:

```text
annual_rate / 365
```

Do not merge `demo-change`.

---

# 15. ACCEPTANCE CHECKLIST

Task 1 is complete only when all of these work:

* [ ] FastAPI starts successfully.
* [ ] `GET /health` returns 200.
* [ ] `POST /api/emi` works.
* [ ] `GET /api/loan/{id}` works.
* [ ] `POST /api/payment` works.
* [ ] `GET /api/customer/{id}` works.
* [ ] 20 customers exist.
* [ ] Loans are fixed/deterministic.
* [ ] Payment endpoint never mutates seed data.
* [ ] Interest calculation exists only in `core/interest.py`.
* [ ] Every response contains `request_id`.
* [ ] Every response contains `generated_at`.
* [ ] Business fields remain deterministic.
* [ ] 0% EMI works.
* [ ] 1-month EMI works.
* [ ] Large principal works.

Task 2 is complete only when:

* [ ] Approximately 60 scenarios exist.
* [ ] ~20 EMI scenarios.
* [ ] ~15 loan scenarios.
* [ ] ~15 payment scenarios.
* [ ] ~10 customer scenarios.
* [ ] Edge cases included.
* [ ] Every scenario has `id`.
* [ ] Every scenario has `method`.
* [ ] Every scenario has `path`.
* [ ] Every scenario has `body` when appropriate.
* [ ] Every scenario has `tags`.
* [ ] `manifest.json` exists.
* [ ] Manifest matches actual files.

---

# 16. DO NOT DO YET

Do NOT implement:

* `engine/`
* LatentGraph MCP integration
* impact analysis
* replay engine
* semantic comparator
* LLM explanation
* Judge
* Teach/update_graph
* decision PRs
* UI

Those are later tasks.

For now:

```text
BUILD APP
    ↓
GENERATE SCENARIOS
    ↓
TEST DETERMINISM
    ↓
STOP
```

---

# 17. FIRST ACTION

Before writing application code:

1. Read this file.
2. Inspect the repository.
3. Confirm the current branch.
4. Create:

```text
APP_NOTES.md
APP_TASKS.md
```

5. Explain your understanding in one paragraph.
6. STOP and wait for my confirmation.

Do not start building the app until I give the next instruction.
