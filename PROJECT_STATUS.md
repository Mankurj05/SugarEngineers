# BlastProof Project Status & Component Matrix
**Date:** 2026-08-30

---

## Component Matrix

| Component | Expected Role | Observed Behavior / Evidence | Status |
|---|---|---|---|
| `engine/replay.py` | Dual server bootstrapper & scenario replayer | Spins up isolated uvicorn servers on ports 8001/8002 using temporary git worktrees, replays HTTP scenarios, cleans up worktrees. | **VERIFIED** |
| `engine/compare.py` | Semantic JSON comparator | Filters UUIDs/ISO timestamps when present on both sides, applies numeric float tolerance (0.01), catches status code and value drifts. Passes `--selftest`. | **VERIFIED** |
| `engine/impact_local.py` | Local AST import dependency analyzer | Traverses python AST import graphs and decorated route handlers in `demo_app/main.py`. Correctly maps changed files to affected endpoints. | **VERIFIED** |
| `engine/impact.py` | LatentGraph MCP provider wrapper | Checks MCP availability; logs honest fallback message to stderr when unconfigured and routes to `impact_local.py`. | **VERIFIED / FALLBACK** |
| `engine/explain.py` | Diff explanation generator | Parses unified git diffs, extracts exact changed file, line number, and code diff hunks. Produces deterministic scenario explanation sentences. | **VERIFIED** |
| `engine/judge.py` | Decision classification engine | Matches drifted scenarios against `decisions.json` rules dynamically using file paths and extracted keywords. Handles `changed_files=None` safely. | **VERIFIED** |
| `engine/teach.py` | Invariant proposal recorder | Generates proposal text based on `report.json` data. Appends proposal to `proposed_invariants.md` when MCP write is unconfigured, logging fallback reason. | **VERIFIED** |
| `engine/cli.py` | Master 1-command pipeline orchestrator | Orchestrates impact → replay → compare → explain → judge → report.json & ui/report-data.js. Aborts cleanly on replay failure. | **VERIFIED** |
| `ui/server.py` | FastAPI UI backend | Serves root `index.html`, `/api/report`, `/api/results`, `/api/run` (triggers CLI pipeline), and `/api/teach` (triggers teach.py). | **VERIFIED** |
| `index.html` | PR Safety Gate Dashboard | Single-page UI rendering Blast Radius, verification bar, root cause banner, expandable drift rows, raw evidence viewer, and honest teach error/receipt handler. | **VERIFIED** |
| `CONTRACTS.md` | Data contract specification | Specifies 5 top-level keys (`id`, `method`, `path`, `body`, `tags`). All 60 files in `scenarios/` comply and pass `--validate`. | **VERIFIED** |
| `README.md` | System documentation | Accurate architecture description, 6-step loop breakdown, exact run commands, and honest integration disclosure. | **VERIFIED** |

---

## Historical Defect Matrix

1. **Stale main branch:** **RESOLVED** (`main` is merged with `engine` and up-to-date)
2. **Duplicate UI files:** **RESOLVED** (`ui/index.html` deleted; root `index.html` served)
3. **Judge standalone crash:** **RESOLVED** (`changed_files=None` safely handled)
4. **Fabricated success receipt:** **RESOLVED** (UI displays `[ERROR]` on non-200 / failure)
5. **Wrong line numbers:** **RESOLVED** (`explain.py` computes exact hunk line offset: `interest.py:5`)
6. **Unverified PR claims:** **RESOLVED** (PR rule branches exist in remote git repository)
7. **Repository clutter:** **RESOLVED** (Scratch notes moved to `docs/`)
