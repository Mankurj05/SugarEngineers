# BLASTPROOF — FULL CODE AUDIT AND REMEDIATION PLAN

**Every file in the repository has been read line by line. This document lists
every defect with file and line number, and specifies the fix.**

Read this entire file before writing any code.

---

## THE HEADLINE

The foundation is genuinely good. The layer on top of it is not.

**Real and working:** the replay engine, the semantic comparator, the demo
banking app, and 60 contract-valid scenarios. That is a real behavioural diff
tool and it works.

**Fabricated:** the LatentGraph integration, the explanation generator, the
rule classifier, the invariant writer, and the UI's receipt. These produce
plausible-looking output using hardcoded strings. They do not do the work they
claim, and several contain comments asserting capabilities that are absent
from the code.

The judges built LatentGraph. `engine/impact.py` is the first file they will
open. It currently claims an MCP integration and contains none.

---

# PART 1 — WHAT IS REAL (do not rewrite these)

| File | Verdict | Notes |
|---|---|---|
| `engine/replay.py` | **REAL** | Git worktrees, dual uvicorn boot, health checks, tag filtering, httpx replay, clean teardown, fail-fast on zero scenarios. Verified working. |
| `engine/compare.py` | **REAL** | Semantic diff, noise keys, UUID/ISO patterns, 0.01 float tolerance, dot-paths, recursion, list handling. `--selftest` passes. One weakness — see Defect 9. |
| `demo_app/**` | **REAL** | Clean layering. `interest.py` isolates the math. `emi_service` imports it directly, `payment_service` imports it directly plus `loan_service`. Response envelope with `request_id`/`generated_at` noise. Deterministic. |
| `scenarios/*.json` | **REAL** | 60 files, 0 contract violations, no duplicate ids, 20/15/15/10. |
| `engine/impact_local.py` lines 12–94 | **REAL** | The AST import-graph construction and two-level dependent walk are genuine. |

Everything below this line is broken, fake, or missing.

---

# PART 2 — DEFECTS

## 🔴 DEFECT 1 — `engine/impact.py`: claims MCP integration, contains none

```python
try:
    # Check if MCP or external graph tools are available and configured.
    return compute_impact_local(old_ref, new_ref)      # "MCP" branch
except Exception as e:
    return compute_impact_local(old_ref, new_ref)      # "fallback" branch
```

Both branches call the local engine. No MCP client, no import, no network call.
The `try/except` exists only to make the file *look* like it queries a graph
and degrades gracefully. The comment asserts a capability the code lacks.

**This is the highest-severity defect.** It is a misrepresentation, not an
incomplete feature.

---

## 🔴 DEFECT 2 — `engine/impact_local.py` lines 127–156: endpoint mapping is hardcoded

I previously told Saubhagya this module was fully real. **That was wrong and I
am correcting it.** The import graph is real. The file-to-endpoint mapping is
not:

```python
if route == "/api/emi":
    if any("interest.py" in f or "emi_service.py" in f for f in affected_set):
        call_paths.append("get_monthly_rate -> calculate_emi -> calculate_emi_endpoint")
elif route == "/api/payment":
    ...
elif route.startswith("/api/loan"):
    if any("loan_service.py" in f for f in affected_set):
elif route.startswith("/api/customer"):
    if any("customer" in f for f in affected_set):
```

Problems:

1. **Route strings are hardcoded.** Add a fifth endpoint to the app and the
   radius cannot see it. This is not analysis, it is a lookup table for one
   specific application.
2. **`call_paths` are string literals** (lines 142, 146, 150). They are not
   derived from the code. `"get_loan -> get_loan"` on line 150 is not even a
   call path.
3. **Line 152 is dead code.** `any("customer" in f ...)` matches no file in the
   project — no filename contains "customer". The customer endpoint is
   excluded from the radius by accident, not by analysis. The negative control
   we have been celebrating is currently a coincidence.

The output happens to be right for this one change. Change anything about the
app and it stops being right.

---

## 🔴 DEFECT 3 — `engine/explain.py` line 58: the explanation is a hardcoded string

```python
explanation = f"EMI {diff_text} — caused by interest.py:5 (annual_rate / 12 → annual_rate / 365), reached via {path_text}."
```

The file name, the line number, and the description of the change are **string
literals**. Consequences:

- Change any other file and every explanation still says
  `interest.py:5 (annual_rate / 12 → annual_rate / 365)`. It describes a change
  it never examined.
- Every explanation begins with the literal word `"EMI"`, including the 12
  payment scenarios, which are not EMI calculations.
- **Line 68** computes the real `git diff`. **Line 42** accepts it as a
  parameter. It is used **only as a cache key** and never read. The premise of
  the module is absent.
- **Line 49** comments `# Attempt LLM call if available`. There is no LLM call,
  no HTTP client, no API import in the file.

**Test that exposes it:** change a different file, run the pipeline, and the
explanation still blames `interest.py:5`.

---

## 🔴 DEFECT 4 — `engine/judge.py` lines 29–41: hardcoded rule IDs, no violation check

```python
if rule["id"] == "D-17":
    if "interest.py" in file:
        return "regression", {...}
elif rule["id"] == "D-31" and "payment_service.py" in file:
    return "regression", {...}
```

1. **Rule IDs are hardcoded.** Add `D-50` to `decisions.json` and the judge
   ignores it. It does not judge against decisions; it pattern-matches two
   literals.
2. **It never checks whether the drift violates the rule.** It only checks that
   *a rule exists for an affected file*. Any drift in a file with any rule is
   `regression`, whatever changed — including a change the rule permits.
3. **Line 52 passes `explanation` into `classify_drift`, which ignores it.**
   The classification reads neither the explanation, nor the diff, nor the
   values.
4. **Line 70** hardcodes `affected_files` with the comment
   `# Assume interest.py was affected if running test`.
5. No `get_pr_insights` call exists.

**The "remove D-17 → becomes unexplained" test proves nothing.** It proves an
`if` statement checked a list. Do not present it as evidence of live
judgement — anyone who opens the file sees it immediately.

---

## 🔴 DEFECT 5 — `engine/teach.py`: fabricated proposal and no write path

**Lines 15–18** — `generate_proposal` returns a hardcoded string that:
- ignores its `scenario_id` argument
- claims the change affects **`/api/loan`** — provably false, loan is our
  negative control
- claims **"Verified across 50 scenarios"** — the real figures are 35 replayed,
  25 drifted

Two statements contradicted by our own `report.json`.

**Lines 27–32** — `commit_proposal`'s `try` block opens with the comment
`# Fallback path`. There is no primary path. No `update_graph`, no MCP. The
docstring claims *"Primary: MCP update_graph (if available)"*, which is false.

---

## 🔴 DEFECT 6 — `ui/index.html`: fabricated receipt on screen

**Line ~424:**
```html
<span class="receipt" id="receipt-${index}">Written to graph — pending_edit_id: bp_938xf</span>
```

`bp_938xf` is a **hardcoded fake ID**. `confirmTeach()` (line ~448) changes the
button text and un-hides that span. **It calls nothing.** No graph write, no
`teach.py`, not even the markdown fallback.

The page asserts on screen that an invariant was written to LatentGraph. Nothing
was written anywhere. **This is the single worst thing in the project** because
it is the closing beat of the demo you plan to film.

---

## 🟠 DEFECT 7 — `ui/index.html`: "View Evidence" shows no evidence

```html
Old:<pre>${JSON.stringify(firstDiff ? firstDiff.old : null, null, 2)}</pre>
New:<pre>${JSON.stringify(firstDiff ? firstDiff.new : null, null, 2)}</pre>
```

It renders the single scalar already shown in the row — `858.37` and `834.15`.
It never shows the raw old and new response bodies. The button that exists to
answer *"is this real?"* shows the same two numbers again.

Also: only `diffs[0]` is ever rendered. Scenarios with several changed fields
show one.

---

## 🟠 DEFECT 8 — `ui/index.html`: wrong data source and wrong fallback

- **Line ~298** fetches `report_sample.json` — the sample I wrote, not the
  pipeline's output. The pushed UI renders fake numbers.
- The **embedded fallback** (lines ~303–325) contains `total: 50`,
  `regression: 18` and `/api/loan/{loan_id}` in the radius. None of that is
  true. Opened by double-click (`file://` blocks `fetch`), this fallback is
  what renders.
- `engine/cli.py` **already writes `ui/report-data.js`** (line 104) containing
  `window.BLASTPROOF_REPORT`. The UI never loads it.

Note: the local copy on Saubhagya's machine renders correct numbers, so the
local UI is ahead of what is pushed. Whatever is running locally must be
committed.

---

## 🟠 DEFECT 9 — `engine/compare.py` lines 49–51: over-aggressive noise skip

```python
if (isinstance(ov, str) and (UUID_PATTERN.match(ov) or ISO_TIMESTAMP_PATTERN.match(ov))) or \
   (isinstance(nv, str) and (...)):
    continue
```

If **either** side matches the pattern, the field is skipped. So:
- a real business date changing from one ISO date to another is silently ignored
- old `"a1b2c3d4-..."` → new `"ERROR"` is silently ignored

For a tool whose pitch is *"we prove what changed"*, silently swallowing
changes is a credibility hole. **Fix: require BOTH sides to match the pattern.**
The existing self-test still passes (both sides are UUIDs there).

---

## 🟠 DEFECT 10 — `engine/cli.py` lines 41–47: replay failure is swallowed

```python
except subprocess.CalledProcessError:
    print("      No scenarios matched or replay failed.")
    results_data = []
    json.dump([], f)
```

A crashed replay produces an empty `results.json`, then the pipeline continues
and writes a `report.json` with `total: 0` — which renders as a clean green
gate. **A failed run must not look like a passing run.** This is the same class
of bug we deliberately fixed in `replay.py` in Task 1B.

---

## 🟡 DEFECT 11 — `engine/cli.py` lines 88–89: breaks the report contract

```python
if no_llm:
    counts["drift"] = sum(...)
```

Adds a fifth key to `summary`, which `CONTRACTS.md` freezes at four. The UI's
verification bar does not render it, so `--no-llm` silently shows
`0 regression` while 25 scenarios drifted.

---

## 🟡 DEFECT 12 — `requirements.txt` is incomplete: a fresh clone cannot run

```
fastapi==0.110.0
uvicorn==0.27.1
pydantic==2.6.4
```

**`httpx` is missing** — `replay.py` cannot fire a single request without it.
`pytest` is missing and the demo app ships tests. A judge cloning the repo and
following the README (which does not exist) cannot run anything.

---

## 🟡 DEFECT 13 — No README

Submission requirement. Absent from `main`.

---

## 🟡 DEFECT 14 — Repository clutter

On `main` right now:

- **`index.html` at the repo root** — a second, different copy of the UI. Two
  UIs in one repo. Delete one.
- **`masterpan.md`** — junk duplicate of `MASTER_PLAN.md`.
- **`stub/`** — the throwaway test app. `ENGINE_TASKS.md` says "Deleted later."
  It is obsolete now that `demo_app` exists.
- `TASK1B.md`, `TASK2.md`, `TASK_SCENARIOS.md`, `WHAT_WE_BUILT.md`,
  `STATUS_TRACKER.md`, `APP_TASKS.md`, `APP_NOTES.md`, `mayank.md`,
  `KICKOFF.md` — nine scratch files in the root. Move them to a `docs/` folder
  or delete them. Execution is 30% of the score and the root directory is the
  first thing a judge sees.

---

# PART 3 — THE FIXES

Work top to bottom. **Commit and push after each task.** Paste real command
output when reporting, not summaries.

---

## TASK 0 — Dependencies (5 minutes, do this first)

Replace `requirements.txt` with:

```
fastapi==0.110.0
uvicorn==0.27.1
pydantic==2.6.4
httpx==0.27.0
pytest==8.1.1
```

Add any package later tasks need as you go.

Verify from a clean environment:
```
pip install -r requirements.txt
python -m engine.compare --selftest
```

---

## TASK A — Real LatentGraph MCP integration (timebox: 2 hours)

**Highest-value remaining work.** The entire differentiation claim rests on it.

### A.1 — Install and initialise

```
npm install -g @latentforce/latentgraph
lgraph --version
```

Free key: **https://latentgraph.latentforce.ai/auth**
Configure it however `lgraph` expects — check `lgraph --help`; it is usually an
env var or `lgraph login`.

```
lgraph start
lgraph init
lgraph add latent-code
```

**Restart the LatentCode session after `lgraph add latent-code`** or the MCP
tools will not register. Then confirm the graph indexed this repo:

```
lgraph status
```

If any step fails, **record the exact error text** and go to A.4. Do not fake it.

### A.2 — `engine/impact.py`: real graph queries

Replace the fake `try/except` with actual calls:

| Need | Tool |
|---|---|
| which files import this file | `get_dependencies(file)` → incoming edges |
| what does this symbol call | `get_call_chain(symbol)` |
| which endpoints does this file serve | `get_file(file)` → served-endpoints field |

Walk dependents two levels. Emit the identical radius shape.

- Responses are fenced `toon` blocks (compact tab-delimited JSON) — parse them.
- Tools accept an optional `project_id`; set `LGRAPH_PROJECT_ID` if needed.
- If `toon` parsing becomes a time sink, `ask_codebase` with a targeted
  question and parsing file-path citations is an acceptable secondary path.

**The fallback must be real.** Wrap each call; on exception log
`"MCP unavailable: <actual error text>, falling back to local AST engine"` to
stderr, then call `impact_local`. Add a `--verbose` flag that prints each MCP
call and its response, so the integration is visible on camera.

**DONE WHEN:** `python -m engine.impact --old v1.0 --new demo-change --verbose`
shows real MCP calls, and `--local` still forces the AST engine, and both agree
on `affected_endpoints`.

### A.3 — `engine/judge.py`: real `get_pr_insights`

Call `get_pr_insights(file)` per affected file. It returns:

```
{invariants: [{text, severity, pr_source}], decisions: [{text, tradeoffs, pr_source}]}
```

Use that as the rule corpus, falling back to `decisions.json` with a logged
reason.

### A.4 — If MCP does not work within 2 hours: be honest

Delete every comment and code path claiming MCP. Then either delete
`engine/impact.py` and have the CLI call `impact_local` directly, or keep it as
a thin shim that states plainly it is not wired. And in the README:

> BlastProof is designed against LatentGraph's MCP surface
> (`get_dependencies`, `get_file`, `get_pr_insights`, `update_graph`). MCP
> wiring was not completed within the hackathon window; the shipped build uses
> an equivalent local AST engine and a local decisions corpus. The integration
> points are isolated in `impact.py`, `judge.py` and `teach.py`.

**An honestly-labelled gap scores better than a stub that gets found.**

---

## TASK B — Make `impact_local.py` genuinely analyse (1 hour)

Delete the hardcoded route `if/elif` chain (lines 127–156) entirely.

**Real algorithm:**

1. Parse `demo_app/main.py` with `ast`. For each decorated route handler,
   record the route string and the handler function node.
2. Walk each handler's body for `ast.Call` and `ast.Attribute` nodes to find
   which module-level names it uses — `EMIService`, `loan_service`,
   `payment_service`.
3. Resolve those names to the files they were imported from, using the import
   graph already built on lines 27–75.
4. A route is in the radius when any file reachable from its handler (through
   the import graph, transitively) is in `affected_files`. **No route string may
   appear in the logic.**
5. Build `call_paths` by chaining the resolved names — changed symbol →
   intermediate function → handler. Derive it; do not write literals.

**DONE WHEN — three checks:**
- `--old v1.0 --new demo-change` still gives `/api/emi` and `/api/payment`,
  and still excludes loan and customer — **now for the right reason.**
- Add a fifth endpoint to `demo_app/main.py` that calls `emi_service`. It
  appears in the radius with no change to `impact_local.py`.
- Modify `loan_service.py` only. The radius contains `/api/loan` and
  `/api/customer` (both use `loan_service`) and excludes `/api/emi`.

That last check is the strongest proof the analysis is real, and it is a great
thing to show a judge.

---

## TASK C — Make `explain.py` actually explain (45 minutes)

Pick one option and describe it honestly in the README.

### C1 — Real model call (preferred)

We have BuildSprint credits via the latentrouter gateway.

```
You are a code-change analyst. Given:

CODE DIFF:
{the real git diff already computed on line 68 — actually pass it}

RESPONSE DIFFERENCES:
{this scenario's diffs array}

CALL PATH:
{this scenario's call path from the radius}

Write ONE sentence explaining what changed and why. Name the exact file and
line. State the old and new business value. Do not speculate beyond the diff.
Do not use jargon.
```

- One call per drifted scenario, sequential.
- Keep the cache keyed on `(scenario_id, code_diff hash)`.
- On API failure use C2's generator and **log that the fallback fired**.

### C2 — Honest deterministic explainer

If no model is reachable:

- **Parse the real diff.** Extract the changed file and line number from the
  `git diff` hunk headers. Never hardcode `interest.py:5`.
- Quote the actual removed and added source lines.
- Do not prefix with `"EMI"` — use the scenario's endpoint or the diff path.
- Call it "a deterministic diff-derived explanation generator" in the README.
  That is a defensible choice — reproducible, no tokens, no provider
  dependency. It is only a problem if you call it an LLM.

**DONE WHEN:** add a line to `demo_app/services/loan_service.py`, run the
pipeline, and the explanation names **that** file — not `interest.py:5`.

---

## TASK D — Make `judge.py` a real classifier (45 minutes)

Delete the hardcoded `if rule["id"] == "D-17"` branches.

1. Collect every rule whose `file` matches any file in the radius. **No rule ID
   may appear in the code.** Adding `D-50` to `decisions.json` must work with
   no code change.
2. Decide whether the drift violates each candidate rule:
   - **With a model:** send explanation + diffs + rule text; require exactly one
     of `VIOLATES <id>` / `MATCHES_INTENT` / `UNCOVERED` plus a one-sentence
     reason. Store the reason.
   - **Without a model:** derive it from the rule's own text — a rule naming
     `annual_rate / 12` is violated when the diff removes that expression.
     From the rule and the diff, never from an ID.
3. Emit `regression` / `intentional` / `unexplained` plus the matched rule.
4. Delete the hardcoded `affected_files` on line 70; take it from the radius.

**DONE WHEN:** a new rule `D-50` for a different file matches a drift there
with no code change; D-17 present → `regression`; D-17 removed →
`unexplained`.

---

## TASK E — Make `teach.py` honest (30 minutes)

1. `generate_proposal` must use **real data**: the scenario id, the affected
   endpoints from the radius, the actual drift count from the report. It
   currently claims `/api/loan` and "50 scenarios", both false.
2. Implement the real `update_graph` call if MCP came up in Task A. On success
   return the genuine `pending_edit_id`.
3. Make the fallback a real fallback: try the graph, and on failure append to
   `proposed_invariants.md` and return
   `"Appended to proposed_invariants.md (graph unavailable: <reason>)"`.
4. **The receipt must never claim a graph write that did not happen.**

---

## TASK F — Fix `compare.py` noise handling (15 minutes)

Change lines 49–51 to require **both** sides to match the pattern before
skipping. Add a fourth self-test fixture: old is a UUID, new is `"ERROR"` →
must be reported as drift, not skipped.

---

## TASK G — Fix `cli.py` (20 minutes)

1. **Lines 41–47:** a replay failure must abort with a non-zero exit and a
   clear message. Never write an empty `results.json` and continue.
2. **Lines 88–89:** remove the extra `drift` key. In `--no-llm` mode, map
   `drift` → `unexplained` in the summary so the four-key contract holds and
   the UI's bar is accurate.
3. Keep the `ui/report-data.js` write — that part is correct.

---

## TASK H — Rebuild the UI as a live tool (2 hours) — APP LANE

### H.1 — A small server

Create `ui/server.py` — FastAPI, roughly 60 lines:

- `GET /` → serve `ui/index.html`
- `GET /api/report` → return current `report.json`
- `POST /api/run` → run
  `python -m engine.cli --old v1.0 --new demo-change --app demo_app.main:app`
  as a subprocess, then return the fresh `report.json`
- `POST /api/teach` `{"scenario": "emi_1"}` → run
  `python -m engine.teach --confirm --scenario emi_1` and return **the actual
  receipt string that command printed**

Run: `python -m uvicorn ui.server:app --port 5500`

This turns the demo from "a rendered JSON file" into "watch it run", and makes
Confirm & Teach real.

### H.2 — Fix the results list

- **Group by root cause.** All 25 regressions share one. Show
  `🔴 25 scenarios · 1 root cause · interest.py:5` expanding to the individual
  scenarios. Biggest readability win available.
- **Collapsed by default.** One line per row; expand on click.
- **Render every diff**, not just `diffs[0]`.
- **Real `[View Evidence]`**: two-column raw old vs new response JSON pulled
  from `results.json` — not the scalar that is already on screen.

### H.3 — A "Run BlastProof" button

Top right, prominent. Click → `POST /api/run` → spinner → results populate.
The screen going from empty to a verdict while being watched is the demo's
centre of gravity.

### H.4 — Receipt honesty

Delete `pending_edit_id: bp_938xf`. The receipt text must come from the server
response. If `teach.py` wrote to `proposed_invariants.md`, the receipt says so.

### H.5 — Data source

Load `report-data.js` via `<script src="report-data.js">` (works over `file://`,
unlike `fetch`), or fetch `/api/report` when the server is running. Delete the
embedded fallback with the wrong numbers, or replace it with real data.

---

## TASK I — README (30 minutes)

Must contain:

- What BlastProof is, in two sentences
- The six-step loop
- **Exact run instructions:** `pip install -r requirements.txt`, the pipeline
  command, how to start the UI
- Architecture: which module does what
- **An honest "what is wired and what is not" section**
- The fallback design — every MCP step has a local path — presented as
  deliberate resilience, which it is

---

## TASK J — Clean the repository (15 minutes)

- Delete the stray root `index.html` (duplicate UI) and `masterpan.md` (junk).
- Delete `stub/` — obsolete since `demo_app` exists.
- Move `TASK*.md`, `APP_*.md`, `KICKOFF.md`, `WHAT_WE_BUILT.md`,
  `STATUS_TRACKER.md`, `mayank.md`, `MASTER_PLAN.md` into `docs/`.
- Root should hold: `README.md`, `CONTRACTS.md`, `PROJECT.md`,
  `decisions.json`, `requirements.txt`, `.gitignore`, and the four code
  directories.

---

# PART 4 — PRIORITY AND TIME

| # | Task | Time | Why |
|---|---|---|---|
| 1 | **0** — requirements.txt | 5 min | A fresh clone cannot run without `httpx` |
| 2 | **E + H.4** — teach + receipt honesty | 45 min | The UI asserts a graph write that never happens, in the shot you will film |
| 3 | **A** — real MCP | 2 h cap | The entire differentiation claim |
| 4 | **B** — real endpoint analysis | 1 h | The negative control is currently a coincidence |
| 5 | **C** — real explain | 45 min | Hardcoded to one specific change |
| 6 | **D** — real judge | 45 min | Hardcoded rule IDs |
| 7 | **H** — live UI | 2 h | Static render → working tool |
| 8 | **G + F** — cli and compare fixes | 35 min | Failure masking, silent skips |
| 9 | **I** — README | 30 min | Submission requirement |
| 10 | **J** — repo cleanup | 15 min | First impression, 30% execution weight |

≈ 9 hours against ~23 remaining. It fits with room for the video.

**If time runs short, drop in this order:** A (take the honest statement in
A.4), then H.3, then C1 and D's model paths (keep the deterministic versions).
**Never drop tasks 0, 2, 9.**

---

# PART 5 — RULES FOR THIS WORK

1. **No hardcoded demo values in logic.** No file names, line numbers, route
   strings, rule IDs, or scenario counts. If it only works for `interest.py`,
   it is broken.
2. **No comment may claim a capability the code lacks.**
3. **No fabricated receipts, IDs, or confirmations anywhere in the UI.** Every
   string shown to a user must come from something that actually happened.
4. **Every fallback logs the real reason it fired.**
5. **The universal test: change a different file.** The pipeline must describe
   *that* change correctly. This is what separates a tool from a demo script.
6. Never force-push. Never rewrite pushed history. Commit and push per task.
7. One LatentCode session in this repo at a time.

---

# PART 6 — REPORTING

After each task, print:

1. Task letter and what changed.
2. **The actual command run and its actual output.** Not a summary.
3. Task A: whether MCP connected; if not, the exact error text.
4. Tasks B, C, D: the output of the different-file test.
5. `git log --oneline -1`.

**Do not mark a task complete without pasting output that proves it.**
"Verified" with no output is not verification — that is how five fabricated
modules reached the final day.
