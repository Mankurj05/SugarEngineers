# BlastProof UI Verification Report
**Date:** 2026-08-30

---

## 1. UI Architecture & Entrypoint

- **Authoritative HTML:** `index.html` (located at repository root).
- **Redundant UI File:** `ui/index.html` has been removed to prevent state/file collisions.
- **Server:** `ui/server.py` (FastAPI + Uvicorn server).
  - `GET /` → Serves root `index.html`.
  - `GET /api/report` → Serves `report.json`.
  - `GET /api/results` → Serves `results.json`.
  - `POST /api/run` → Executes `python -m engine.cli --old v1.0 --new demo-change --app demo_app.main:app` as a subprocess and returns fresh report.
  - `POST /api/teach` → Executes `python -m engine.teach --confirm --scenario <scenario_id>` and returns actual execution receipt.

---

## 2. Visual & Functional Features Verified

1. **Header & Control Bar:**
   - Display project title (`BLASTPROOF PR Gate`), git refs (`v1.0..demo-change`), and interactive `⚡ Run BlastProof` button.
2. **Blast Radius Analysis Card:**
   - Displays affected files count (4) and affected endpoints (`/api/emi`, `/api/payment`).
3. **Verification Bar:**
   - Displays scenario total (35), unchanged count (10), intentional count (0), and regression count (25).
4. **Root Cause Banner:**
   - Displays `🔴 Root Cause Grouping: 25 regressions traced to 1 primary change: demo_app/core/interest.py`.
5. **Expandable Drift Rows:**
   - Shows scenario name, verdict badge (`REGRESSION`), explanation sentence, and full list of numeric diffs (`data.emi 858.37 → 834.15`).
6. **Violated Rule Box:**
   - Displays rule ID (`D-17`), source (`PR #4`), and rule text (`EMI must use monthly normalization (annual_rate / 12) per lending convention`).
7. **View Evidence Toggle:**
   - Toggles side-by-side view of raw `OLD RESPONSE BODY (v1.0)` and `NEW RESPONSE BODY (demo-change)` fetched live from `/api/results`.
8. **Confirm & Teach Action & Honest Receipts:**
   - `Confirm & Teach` button calls `/api/teach`.
   - Displays real receipt output returned by `teach.py`. On HTTP error or server failure, displays `[ERROR] Failed to record invariant...` instead of a fabricated success message.

---

## 3. UI Verdict

**VERIFIED AND FUNCTIONAL**
