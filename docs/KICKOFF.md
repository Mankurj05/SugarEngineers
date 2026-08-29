
You are the sole code writer for a 48-hour hackathon project. Before writing any
feature code, read this whole message, then do ONLY the setup task at the end
(create reference docs). Do not start building modules until I say "start task 1".

## 1. THE PROJECT — BlastProof

One line: a safety gate for code changes. When a developer changes code, we
(a) find what the change could affect, (b) actually RUN the app before and after
the change and replay saved requests to prove what changed, (c) check every
change against the team's recorded decisions, and (d) save confirmed findings
back into a knowledge graph.

The pipeline has 6 steps:
1. IMPACT — query the LatentGraph MCP server (get_dependencies, get_call_chain,
   get_file) for the changed files → output a "blast radius": affected files +
   affected API endpoints.
2. EXECUTE — boot the OLD app version (a git tag, via git worktree, port 8001)
   and the NEW version (HEAD, port 8002); replay only the saved request
   scenarios whose tags match the affected endpoints; collect both responses.
3. COMPARE — semantic diff of old vs new response per scenario. Ignore noise
   keys (request_id, generated_at, trace_id, UUID-shaped strings,
   ISO-timestamp-shaped strings). Numbers compare with 0.01 tolerance.
   Status-code difference = instant drift. Verdict: identical | drift.
4. EXPLAIN — one LLM call per drifted scenario (input: code diff + field diffs +
   call path) → one plain sentence naming file:line and old→new value.
5. JUDGE — for each drift, fetch recorded team decisions via MCP get_pr_insights
   (fallback: local decisions.json). LLM classifies: VIOLATES <rule> |
   MATCHES_INTENT | UNCOVERED → verdicts regression | intentional | unexplained.
6. TEACH — propose an invariant; on human Confirm only, call MCP update_graph
   (fallback: append to proposed_invariants.md). Never write automatically.

## 2. REPO AND MY LANE

- Repo: SugarEngineers. Two people, two branches:
  - branch `engine` (ME, this session): everything under engine/ plus the CLI.
  - branch `app` (teammate, separate session): demo-app/, scenarios/, ui/.
- I merge to main via pull requests. YOU NEVER TOUCH demo-app/, scenarios/, or
  ui/ in this session — not even to "fix" something. If engine code needs a
  change there, tell me and stop.
- The seam between the two halves is report.json (schema below). Both sides
  code against the schemas, not against each other's code.

## 3. DATA CONTRACTS (fixed — do not redesign)

Scenario file (scenarios/*.json), written by teammate's generator:
{ "id": "emi_017", "method": "POST", "path": "/api/emi",
  "body": {"principal": 500000, "annual_rate": 12, "months": 60},
  "tags": ["emi"] }

Radius (output of impact step):
{ "changed": ["core/interest.py"],
  "affected_files": ["services/emi_service.py", "..."],
  "affected_endpoints": ["/api/emi", "/api/loan/{id}"],
  "call_paths": ["monthly_rate -> calculate_emi -> emi_endpoint"] }

results.json (output of replay):
[ { "scenario": "emi_017",
    "old": {"status": 200, "json": {...}},
    "new": {"status": 200, "json": {...}} } ]

report.json (final output, read by teammate's UI):
{ "summary": {"total": 58, "identical": 55, "intentional": 2,
              "regression": 1, "unexplained": 0},
  "radius": { ...radius object... },
  "results": [ { "scenario": "emi_017", "verdict": "regression",
                 "diffs": [{"path": "emi", "old": 14820.0, "new": 10718.4}],
                 "explanation": "one sentence",
                 "rule": {"id": "D-17", "text": "...", "source": "PR #4"} } ] }

## 4. MODULE PLAN FOR THIS LANE (build order — one module per task)

- Task 1: engine/replay.py — boot old+new via git worktree + uvicorn subprocess,
  health-check both, replay tag-filtered scenarios with httpx (5s timeout,
  sequential), write results.json, clean shutdown. CLI:
  python -m engine.replay --old v1.0 --new HEAD --tags emi,loan
- Task 2: engine/compare.py — the semantic diff per section 1 step 3, dot-path
  mismatches, writes verdict+diffs.
- Task 3: stub/ — a tiny throwaway FastAPI app (GET /health + one dummy POST)
  so replay can be smoke-tested before the real demo app exists. Deleted later.
- Task 4: engine/impact.py (MCP) + engine/impact_local.py (Python ast import
  scan + FastAPI route-decorator parsing; same radius output). --local flag
  switches. [MCP tools will be connected later — build local first.]
- Task 5: engine/explain.py — one LLM call per drift, cached by
  (scenario_id, diff_hash).
- Task 6: engine/judge.py — get_pr_insights with decisions.json fallback,
  three-way classification.
- Task 7: engine/teach.py — proposal + Confirm-gated update_graph.
- Task 8: engine/cli.py — one command chains everything and writes report.json.

## 5. STANDING RULES FOR THIS SESSION — never violate

1. Python 3.11+, dependencies only: fastapi, uvicorn, httpx. Ask me before
   adding ANY other dependency.
2. Small modules, no frameworks, no async pools, no databases. Sequential and
   simple beats clever.
3. Determinism is sacred: no randomness, no wall-clock in business logic.
4. Every module ends with a "done when" check I can run in one command; print
   it when you finish the module.
5. When unsure, ask me — do not invent scope. Never add features I didn't list.
6. Stay on branch `engine`. Never commit to main.

## 6. YOUR ONLY TASK RIGHT NOW — create the reference docs, then stop

Create these three files at repo root so you can re-read them anytime you lose
context (re-read them at the start of every task):
- PROJECT.md — the concept and 6-step pipeline from section 1, in your words,
  plus the "standing rules" from section 5 verbatim.
- CONTRACTS.md — the four data schemas from section 3, verbatim.
- ENGINE_TASKS.md — the 8 tasks from section 4 as a checklist with their
  "done when" conditions; we tick them as we go.

Then print a one-paragraph summary of the project back to me to prove
understanding, and WAIT for me to say "start task 1".