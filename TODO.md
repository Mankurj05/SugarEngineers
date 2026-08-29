# BlastProof TODO & Verification Status Board

---

## P0 — Truth and Verification

### T001 — Audit repository
- **Priority:** P0
- **Owner:** engine
- **File:** Repository-wide
- **Reason:** Previous completion claims were unverified.
- **Acceptance:** All relevant files inventoried in `FORENSIC_AUDIT.md`.
- **Verification:** `FORENSIC_AUDIT.md` complete.
- **Status:** **VERIFIED**

### T002 — Verify branch state
- **Priority:** P0
- **Owner:** engine
- **File:** Git metadata
- **Reason:** `main` and `engine` relationship needed verification.
- **Acceptance:** `main` merged with `engine`; all defect fixes present on `main`.
- **Verification:** `git log` and `git diff main engine`.
- **Status:** **VERIFIED**

### T003 — Reproduce and fix historical defects
- **Priority:** P0
- **Owner:** engine
- **File:** Repository-wide
- **Reason:** Seven historical defects reported.
- **Acceptance:** All 7 defects reproduced, fixed, and verified.
- **Verification:** `FORENSIC_AUDIT.md` & `FINAL_VERIFICATION.md`.
- **Status:** **VERIFIED**

---

## P1 — Core Runtime & Pipeline

### T004 — Verify replay engine
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/replay.py`
- **Reason:** Dual server execution is core to behavioural diff.
- **Acceptance:** Scenarios execute over HTTP across worktree revisions (`v1.0` vs `demo-change`).
- **Verification:** CLI pipeline run.
- **Status:** **VERIFIED**

### T005 — Verify comparator engine
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/compare.py`
- **Reason:** False positives and swallowed drifts destroy utility.
- **Acceptance:** Noise filtered only when present on both sides; numeric drift caught.
- **Verification:** `python -m engine.compare --selftest`.
- **Status:** **VERIFIED**

### T006 — Verify local AST impact analysis
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/impact_local.py`
- **Reason:** AST dependency analysis provides resilient local blast radius.
- **Acceptance:** Radius maps AST imports and route handlers dynamically.
- **Verification:** Check 1, 2, and 3 verification runs.
- **Status:** **VERIFIED**

### T007 — Verify LatentGraph MCP provider
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/impact.py`
- **Reason:** Honest integration disclosure required.
- **Acceptance:** Logs stderr fallback message when MCP key unconfigured.
- **Verification:** `MCP_VERIFICATION.md`.
- **Status:** **VERIFIED (FALLBACK ONLY)**

### T008 — Verify diff explanation engine
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/explain.py`
- **Reason:** Explanations must reflect exact file, line, and diff.
- **Acceptance:** Computes exact 1-indexed changed line offset (`interest.py:5`).
- **Verification:** `report.json` inspection.
- **Status:** **VERIFIED**

### T009 — Verify decision judge engine
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/judge.py`
- **Reason:** Classify drifts against team decision rules without crashing.
- **Acceptance:** Handles `changed_files=None` safely and matches rules dynamically.
- **Verification:** Standalone `judge.py` test run.
- **Status:** **VERIFIED**

### T010 — Verify teach & invariant proposal
- **Priority:** P1
- **Owner:** engine
- **File:** `engine/teach.py`
- **Reason:** Invariant proposals must be evidence-based and governed.
- **Acceptance:** Generates proposal from `report.json` and records fallback receipt.
- **Verification:** `python -m engine.teach --confirm`.
- **Status:** **VERIFIED**

### T011 — Verify UI server & dashboard
- **Priority:** P1
- **Owner:** app
- **File:** `ui/server.py` & `index.html`
- **Reason:** PR Safety Gate UI must visualize evidence and serve execution endpoints.
- **Acceptance:** Single-page dashboard displays radius, drift rows, raw evidence, and honest error receipts.
- **Verification:** `UI_VERIFICATION.md`.
- **Status:** **VERIFIED**
