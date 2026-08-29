# BlastProof Final Verification & Acceptance Gate
**Date:** 2026-08-30

---

## Acceptance Gate Checklist

### 1. Repository Cleanliness & Structure
- [x] Clean `git status` on `main` and `engine` branches.
- [x] `main` contains all commits and fixes from `engine`.
- [x] No accidental temporary files, bytecode, or duplicate HTML entrypoints (`ui/index.html` deleted).
- [x] Scratch notes moved to `docs/`.
- **Evidence:** `git status` clean; `git diff origin/main origin/engine` shows only minor formatting/sample differences.

### 2. Execution Engine (`engine/replay.py`)
- [x] Old revision (`v1.0`) executes in isolated git worktree on port 8001.
- [x] New revision (`demo-change`) executes in isolated git worktree on port 8002.
- [x] Scenarios execute over HTTP with health checks.
- [x] Worktrees and uvicorn server processes clean up reliably after execution.
- **Evidence:** E2E CLI run completes 35 scenario executions and cleans up worktrees at `C:\Users\LUNARP~1\AppData\Local\Temp\blastproof_*`.

### 3. Comparison Engine (`engine/compare.py`)
- [x] Identical scenarios produce `identical` verdict.
- [x] Business field changes produce `drift` verdict.
- [x] UUIDs and ISO timestamps ignored **only** when present on both sides.
- [x] Value changes from UUID to string (e.g., `"ERROR"`) correctly caught as drift.
- [x] Passes `--selftest`.
- **Evidence:** `python -m engine.compare --selftest` returns `PASS: Self-test successful.`

### 4. Impact Analysis (`engine/impact_local.py` & `engine/impact.py`)
- [x] Traverses AST import graph and decorated FastAPI route handlers in `demo_app/main.py`.
- [x] Dynamic dependency traversal picks up added endpoints without hardcoded strings.
- [x] Handles MCP status honestly with stderr fallback logging when unconfigured.
- **Evidence:** `v1.0..demo-change` produces `/api/emi` and `/api/payment` radius while excluding `/api/loan` and `/api/customer`. Adding a 5th endpoint dynamically updates radius without changing `impact_local.py`.

### 5. Explanation Engine (`engine/explain.py`)
- [x] Parses unified git diffs (`parse_git_diff`).
- [x] Computes exact 1-indexed changed line offset (`demo_app/core/interest.py:5`).
- [x] Formats clear explanation referencing actual scenario ID, diff paths, values, changed code, and call path.
- **Evidence:** `report.json` contains `"explanation": "Scenario emi_1 (data.emi 858.37 → 834.15) — caused by change in demo_app/core/interest.py:5 (return (annual_rate / 12) / 100 → return (annual_rate / 365) / 100), reached via EMIService -> calculate_emi_endpoint."`

### 6. Decision Classification Engine (`engine/judge.py`)
- [x] Executes standalone without crashing when `changed_files=None`.
- [x] Dynamically extracts rule keywords and matches affected files against `decisions.json`.
- [x] Correctly classifies violations as `regression` and unmapped drifts as `unexplained`.
- **Evidence:** `python -c "from engine.judge import judge_results; print(judge_results([{'scenario':'emi_1', 'verdict':'drift'}], ['demo_app/core/interest.py']))"` runs safely and returns `unexplained`. With `D-17` present, returns `regression` with rule metadata.

### 7. Invariant Proposal Engine (`engine/teach.py`)
- [x] Generates proposal text from actual `report.json` data.
- [x] Requires `--confirm` flag for writing.
- [x] Appends proposal to `proposed_invariants.md` when MCP write is unavailable, reporting fallback reason honestly.
- **Evidence:** `python -m engine.teach --confirm --scenario emi_1` outputs `PROPOSAL COMMITTED (fallback_local_file): Appended to proposed_invariants.md (graph unavailable: MCP tool not initialized)`.

### 8. User Interface (`index.html` & `ui/server.py`)
- [x] FastAPI server (`ui/server.py`) serves dashboard and live execution endpoints.
- [x] UI displays Blast Radius, verification bar, root-cause banner, expandable drift rows, and raw evidence viewer.
- [x] UI handles teach action with real execution receipts and displays `[ERROR]` on failure instead of fabricating success.
- **Evidence:** Server starts cleanly on port 5500; `index.html` verified end-to-end.

---

## FINAL ACCEPTANCE VERDICT

**READY FOR SUBMISSION**

All acceptance gate checklist items pass with verifiable evidence.
