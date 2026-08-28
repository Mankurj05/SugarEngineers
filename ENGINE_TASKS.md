# Engine Tasks

- [ ] **Task 1:** `engine/replay.py` — boot old+new via git worktree + uvicorn subprocess, health-check both, replay tag-filtered scenarios with httpx (5s timeout, sequential), write `results.json`, clean shutdown. 
  - CLI: `python -m engine.replay --old v1.0 --new HEAD --tags emi,loan`
- [ ] **Task 2:** `engine/compare.py` — the semantic diff per section 1 step 3, dot-path mismatches, writes verdict+diffs.
- [ ] **Task 3:** `stub/` — a tiny throwaway FastAPI app (GET `/health` + one dummy POST) so replay can be smoke-tested before the real demo app exists. Deleted later.
- [ ] **Task 4:** `engine/impact.py` (MCP) + `engine/impact_local.py` (Python ast import scan + FastAPI route-decorator parsing; same radius output). `--local` flag switches. [MCP tools will be connected later — build local first.]
- [ ] **Task 5:** `engine/explain.py` — one LLM call per drift, cached by `(scenario_id, diff_hash)`.
- [ ] **Task 6:** `engine/judge.py` — `get_pr_insights` with `decisions.json` fallback, three-way classification.
- [ ] **Task 7:** `engine/teach.py` — proposal + Confirm-gated `update_graph`.
- [ ] **Task 8:** `engine/cli.py` — one command chains everything and writes `report.json`.
