# Project: BlastProof

## Concept
BlastProof is a safety gate for code changes designed to run during the change process. It identifies the "blast radius" of a change, executes the application before and after the change using saved requests relevant to the affected endpoints, semantically compares the responses to detect drift, uses an LLM to explain the drift, judges the drift against recorded team decisions (regression vs intentional), and proposes new invariants for the team's knowledge graph.

## The 6-Step Pipeline
1. **IMPACT:** Determine affected files and API endpoints by querying the LatentGraph MCP server for the changed files. Output a "blast radius".
2. **EXECUTE:** Boot the OLD version (git tag) and NEW version (HEAD) of the app. Replay saved request scenarios matching the affected endpoints and collect responses.
3. **COMPARE:** Perform a semantic diff of old vs new responses per scenario, ignoring noise keys (like request_id, UUIDs, timestamps) and allowing a 0.01 tolerance for numbers. Status-code differences indicate instant drift. Verdicts: `identical` or `drift`.
4. **EXPLAIN:** For each drifted scenario, make one LLM call (input: code diff + field diffs + call path) to generate a single plain sentence explaining the change (file:line and old→new value).
5. **JUDGE:** For each drift, fetch team decisions via MCP `get_pr_insights` (fallback to `decisions.json`). An LLM classifies the drift as `VIOLATES <rule>`, `MATCHES_INTENT`, or `UNCOVERED`, resulting in verdicts of `regression`, `intentional`, or `unexplained`.
6. **TEACH:** Propose an invariant. Upon human confirmation only, call MCP `update_graph` (fallback: append to `proposed_invariants.md`). *Never write automatically.*

## Standing Rules for this Session
1. Python 3.11+, dependencies only: fastapi, uvicorn, httpx. Ask me before
   adding ANY other dependency.
2. Small modules, no frameworks, no async pools, no databases. Sequential and
   simple beats clever.
3. Determinism is sacred: no randomness, no wall-clock in business logic.
4. Every module ends with a "done when" check I can run in one command; print
   it when you finish the module.
5. When unsure, ask me — do not invent scope. Never add features I didn't list.
6. Stay on branch `engine`. Never commit to main.
