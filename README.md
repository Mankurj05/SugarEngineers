# BLASTPROOF — Behavioural Diff & PR Safety Gate Engine

BlastProof is a lightweight, zero-instrumentation behavioural diff engine that detects API regressions before code reaches production. It replays real production scenarios across git commits, computes blast radius via AST static analysis, generates diff-derived explanations, and judges changes against recorded team decisions.

---

## The Six-Step BlastProof Loop

1. **Impact / Blast Radius (`engine/impact.py` / `engine/impact_local.py`)**: Computes affected files and endpoints using AST dependency traversal.
2. **Targeted Replay (`engine/replay.py`)**: Spins up isolated dual uvicorn servers using git worktrees and replays scenarios matching radius tags.
3. **Semantic Compare (`engine/compare.py`)**: Computes structural diffs ignoring dynamic noise keys (UUIDs, ISO timestamps).
4. **Diff Explanation (`engine/explain.py`)**: Parses unified git diffs to generate plain-English explanations identifying exact modified files, line numbers, and code changes.
5. **Decision Judgement (`engine/judge.py`)**: Classifies drifted scenarios against recorded team decisions (`decisions.json`).
6. **Invariant Teaching (`engine/teach.py`)**: Generates and commits invariant proposals to document verified system behaviour.

---

## Quick Start & Exact Run Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Compare Engine Self-Test
```bash
python -m engine.compare --selftest
```

### 3. Run One-Command Pipeline
```bash
python -m engine.cli --old v1.0 --new demo-change --app demo_app.main:app
```
*Produces `report.json` and `ui/report-data.js`.*

### 4. Start UI Dashboard Server
```bash
python -m uvicorn ui.server:app --port 5500
```
Open **`http://127.0.0.1:5500`** in your browser to view the interactive PR Safety Gate.

---

## Architecture Overview

| Module | Responsibility |
|---|---|
| `engine/cli.py` | One-command CLI pipeline orchestrating impact, replay, compare, explain, judge, and report generation. |
| `engine/impact.py` | Blast radius interface with fallback to local AST engine. |
| `engine/impact_local.py` | AST import graph builder and route-handler dependency analyzer. |
| `engine/replay.py` | Git worktree manager, dual uvicorn bootstrapper, and HTTP scenario replayer. |
| `engine/compare.py` | Semantic JSON comparison with float tolerance and noise filtering. |
| `engine/explain.py` | Unified git diff parser and scenario explanation generator. |
| `engine/judge.py` | Dynamic rule classifier judging drifts against `decisions.json`. |
| `engine/teach.py` | Invariant proposal generator and recorder. |
| `ui/server.py` | FastAPI UI server delivering the dashboard and live execution endpoints. |

---

## Honest Architecture & Integration Status

BlastProof is designed against LatentGraph's MCP surface (`get_dependencies`, `get_file`, `get_pr_insights`, `update_graph`). Interactive MCP key authentication was not configured in the non-interactive hackathon environment; the shipped build uses an equivalent local AST engine (`impact_local.py`) and a local decisions corpus (`decisions.json`). The integration points are isolated in `impact.py`, `judge.py` and `teach.py`.

Every component features a local, zero-dependency fallback path designed for high resilience when external services or credentials are unavailable.
