# BLASTPROOF — MASTER EXECUTION PLAN
### Everything remaining, start to finish. Read this file before every task.

---

## SECTION 0 — HOW TO USE THIS FILE

**If you are an AI coding assistant (LatentCode) reading this file:**

1. This file is the single source of truth for what to build next. Work through
   it top to bottom. Do not skip ahead.
2. Before starting ANY task, re-read `PROJECT.md` and `CONTRACTS.md`.
3. Each task has: a GOAL, the FILES it touches, STEPS, and a DONE WHEN block.
   You are not finished until every command in DONE WHEN actually passes when
   you run it. Do not mark a task complete based on reading the code and
   believing it is correct. Run the commands.
4. Where you see **🛑 STOP AND REPORT**, halt completely. Print the requested
   information and wait for the human. Do not continue to the next task.
5. Never invent scope. If a task does not ask for a feature, do not add it.
   If you think something extra is needed, say so at the STOP point and let
   the human decide.
6. If a DONE WHEN check fails, do not rationalize it, do not adapt the
   contract to match your code, and do not declare partial success. Report
   the failure with the exact output.
7. If a task appears to already be done, verify it by RUNNING the DONE WHEN
   commands, then say so and move on. Do not redo completed work.

**Only ONE LatentCode session may work in this repo at a time.** Two sessions
ran concurrently earlier today and produced duplicate commits, a `git reset
--hard` on a pushed branch, and a merge that had to be untangled. If a second
session is open, close it.

---

## SECTION 1 — WHERE WE ARE RIGHT NOW

**Time context:** Saturday afternoon. Hackathon ends **Sunday 30 Aug 18:00 IST**.
Hard stop on all code: **Sunday 14:00 IST**. Everything after that is recording,
exporting, uploading and submitting.

### What is genuinely DONE and verified

| Piece | Status | Verified how |
|---|---|---|
| Reference docs (PROJECT.md, CONTRACTS.md, ENGINE_TASKS.md) | ✅ on main | file listing |
| `engine/replay.py` — worktree boot, health-check, tag filter, results.json | ✅ works | ran against stub and against demo_app |
| `engine/replay.py` fail-fast on zero scenarios | ✅ works | `--tags nosuchtag` exits non-zero |
| `engine/compare.py` — semantic diff, noise ignore, float tolerance | ✅ works | `--selftest` passes; 20 real replays return identical |
| `stub/app.py` | ✅ done, now obsolete | replaced by demo_app |
| `demo_app/` — 4 endpoints, layered services, seed data, tests | ✅ on main | code reviewed |
| 60 scenarios in contract shape | ✅ verified | 0 violations, no dup ids, 20/15/15/10 |
| `.gitignore`, build artifacts untracked | ✅ clean | `git ls-tree` clean |
| Both lanes merged to `main` | ✅ done | main = 41250f4 |

**Checkpoint 1 is PASSED.** Replay boots two versions of the real banking app,
fires the real scenarios at both, and the comparator correctly reports them
identical despite every response carrying a different `request_id` and
`generated_at`. The engine and the app are genuinely talking.

### What is NOT done

- ❌ No `v1.0` tag exists. Nothing is pinned as the "old" version.
- ❌ No `demo-change` branch. The planted regression does not exist yet.
- ❌ **We have never once seen BlastProof detect a drift against the real app.**
  Every green run so far compared identical code to itself.
- ❌ `engine/impact.py` and `engine/impact_local.py` — not started (Task 4)
- ❌ `engine/explain.py` — not started (Task 5)
- ❌ `engine/judge.py` — not started (Task 6)
- ❌ `engine/teach.py` — not started (Task 7)
- ❌ `engine/cli.py` — not started (Task 8)
- ❌ `decisions.json` — not started (blocks the JUDGE step)
- ❌ Seeded decision PRs — not started
- ❌ UI — not started. **This is the largest single unstarted item.**
- ❌ LatentGraph MCP setup — not started
- ❌ SkillPatch skill installed by either member — not done
- ❌ SkillPatch API key rotation — flagged as exposed, still not confirmed done
- ❌ README, demo video, Build-in-Public post, `/export` transcripts,
  Google Drive folder, submission form — none started

### Honest assessment

The engine lane is in good shape and ahead of where most teams would be. The
two hardest technical pieces — subprocess/worktree orchestration and the
semantic comparator — are built and tested. That is real.

The risk is not the engine. The risk is that **there is no user interface**,
and a hackathon judged 10% on presentation with a 2-minute video will not be
won by a command line printing JSON. The UI is the friend's lane and has not
been started. It needs to start now.

The second risk is that six of the eight engine modules do not exist, and the
last four (explain, judge, teach, cli) are what make this BlastProof rather
than a diff tool. There is time, but only if nothing else goes sideways.

---

## SECTION 2 — GROUND RULES (never violate these)

### Git rules
1. **Never force-push.** Not with `-f`, not with `--force-with-lease`.
2. **Never rewrite pushed history.** No `git reset --hard` on a branch that
   has been pushed, no `commit --amend` on a pushed commit, no rebase of
   published commits. This already happened once today and had to be
   recovered by merging a duplicate commit.
3. **Never merge `demo-change` into `main`.** It exists only as a diff target.
4. **Never run `git add -A` on `main` casually.** The Windows checkout makes
   ~20 files show as modified purely from CRLF line endings.
   `git diff --ignore-cr-at-eol --stat` returns empty, proving nothing really
   changed. Committing that noise puts a meaningless 100-file diff in the
   history that judges will read.
5. If a merge conflicts, **STOP and report the conflicting files.** Do not
   resolve conflicts autonomously.
6. Commit after every completed task, with a message that says what changed
   and why. These messages are `get_pr_insights` material later.

### Code rules
1. Python 3.11+. Dependencies: `fastapi`, `uvicorn`, `httpx`, `pydantic` only.
   `engine/compare.py` must stay standard-library only.
2. Small, readable modules. No async pools, no databases, no frameworks.
3. Business logic must be deterministic — identical input, identical output.
4. Every module ends with a runnable test command.
5. **Every step that uses the LatentGraph MCP must have a local fallback.**
   No exceptions. The demo can never depend on a network service being up.
6. Do not modify `CONTRACTS.md`. The schemas are frozen. If code disagrees
   with the contract, the code is wrong.
7. Do not touch files in the other lane without saying so at a STOP point.

### Hackathon compliance rules
1. **LatentCode is the only tool permitted to write project code.** Every line
   in the repo must trace to a LatentCode session transcript.
2. Both team members need their own `/export` transcript. Both must have
   written code.
3. Repo history must match the transcripts. No fabricated commits.
4. Nothing built before 28 Aug 18:00 IST may be submitted.

### The frozen contracts (reproduced here so you never have to guess)

**Scenario file** — `scenarios/*.json`, exactly five top-level keys:
```json
{
  "id": "emi_1",
  "method": "POST",
  "path": "/api/emi",
  "body": {"principal": 10000, "annual_rate": 5.5, "tenure_months": 12},
  "tags": ["emi"]
}
```

**Radius** — output of the impact step:
```json
{
  "changed": ["demo_app/core/interest.py"],
  "affected_files": ["demo_app/services/emi_service.py", "..."],
  "affected_endpoints": ["/api/emi", "/api/loan/{loan_id}"],
  "call_paths": ["get_monthly_rate -> calculate_emi -> calculate_emi_endpoint"]
}
```

**results.json** — output of replay, a top-level array:
```json
[
  {
    "scenario": "emi_1",
    "old": {"status": 200, "json": {"...": "..."}},
    "new": {"status": 200, "json": {"...": "..."}}
  }
]
```

**report.json** — the final output, what the UI reads:
```json
{
  "summary": {"total": 60, "identical": 40, "intentional": 2, "regression": 18, "unexplained": 0},
  "radius": {},
  "results": [
    {
      "scenario": "emi_1",
      "verdict": "regression",
      "diffs": [{"path": "data.emi", "old": 858.37, "new": 831.02}],
      "explanation": "EMI changed from 858.37 to 831.02 due to interest.py:5",
      "rule": {"id": "D-17", "text": "EMI uses monthly normalization", "source": "PR #4"}
    }
  ]
}
```

**decisions.json** — the local fallback for recorded team decisions:
```json
[
  {
    "id": "D-17",
    "file": "demo_app/core/interest.py",
    "text": "EMI must use monthly normalization (annual_rate / 12) per lending convention",
    "source": "PR #4",
    "severity": "high"
  }
]
```

**Verdict vocabulary — do not mix these up:**
- `compare.py` produces only `identical` or `drift`.
- `judge.py` upgrades a `drift` into `regression`, `intentional`, or `unexplained`.
- `regression` / `intentional` / `unexplained` must never appear in compare.py.

---

## SECTION 3 — PHASE 2: PROVE THE DETECTION WORKS

> **This is the most important phase in the entire project.** Until it passes,
> we have never seen BlastProof catch anything. Everything else is decoration
> on top of this moment.

### TODO — Phase 2
- [ ] 2.1 Tag `v1.0` on main
- [ ] 2.2 Create the `demo-change` branch with the planted regression
- [ ] 2.3 Run the full cross-version replay
- [ ] 2.4 Compare and interpret the verdicts
- [ ] 🛑 STOP AND REPORT

---

### TASK 2.1 — Tag the "before" version

**Goal:** pin the current correct state of the app as `v1.0`.

**Steps:**
```
git checkout main
git pull
git status
```
Confirm you are on main and up to date. If `git status` shows modified files,
verify with `git diff --ignore-cr-at-eol --stat` that it is only CRLF noise,
then `git checkout -- .` to discard it.

```
git tag v1.0
git push origin v1.0
```

**DONE WHEN:**
```
git ls-remote --tags origin
```
shows `refs/tags/v1.0`.

---

### TASK 2.2 — Create the planted regression

**Goal:** produce a second version of the app that differs by exactly one line.

**File:** `demo_app/core/interest.py`

**Steps:**
```
git checkout -b demo-change
```

In `demo_app/core/interest.py`, the function `get_monthly_rate` currently reads:
```python
return (annual_rate / 12) / 100
```
Change it to divide by 365 instead of 12:
```python
return (annual_rate / 365) / 100
```

**Change ONLY that divisor.** Do not touch `calculate_emi`, any service, any
endpoint, any test. A one-line diff is the entire point — it demonstrates that
a trivial-looking change ripples through four endpoints.

```
git commit -am "demo: switch annual rate normalization from monthly to daily"
git push -u origin demo-change
```

**DO NOT MERGE THIS BRANCH.** It is the "new" side of the diff and nothing else.

**DONE WHEN:**
```
git diff v1.0..demo-change --stat
```
shows exactly one file changed, with 1 insertion and 1 deletion.

Then return to the working branch:
```
git checkout engine
git merge main -m "merge main into engine"
```

---

### TASK 2.3 — Run the cross-version replay

**Goal:** fire all 60 scenarios at both versions simultaneously.

**Command:**
```
python -m engine.replay --old v1.0 --new demo-change --tags emi,loan,payment,customer --app demo_app.main:app
```

`replay.py` creates a worktree for any ref that is not `HEAD`, so both sides
run from clean checkouts. Neither depends on your working tree.

**Watch for:** both health checks passing before any scenario is fired. If a
server does not come up, the results are meaningless — stop and diagnose
rather than proceeding.

**DONE WHEN:** `results.json` contains 60 objects, each with `scenario`, `old`
and `new` keys, and both worktrees were removed cleanly at the end.

---

### TASK 2.4 — Compare and interpret

**Command:**
```
python -m engine.compare --results results.json > comparison.json
```

**Now count the verdicts per tag** and report them. The expected outcome:

| Tag | Count | Expected verdict | Why |
|---|---|---|---|
| emi | 20 | **drift** | EMI is computed directly from `get_monthly_rate` |
| loan | 15 | **drift** — verify | only if loan_service computes through interest.py |
| payment | 15 | **drift** — verify | payment_service → emi_service → interest.py |
| customer | 10 | **identical** | no dependency path to interest.py at all |

**The customer scenarios staying green is the single most important result in
this project.** It is the negative control. It proves the tool reports what
actually changed rather than flagging everything. If all 60 go red, BlastProof
is just a diff tool and the blast-radius story collapses.

**If customer scenarios show drift:** STOP. Do not explain it away. Either the
comparator has a bug or the app has an unintended dependency. Report which
fields differ on a customer scenario and stop.

---

### 🛑 STOP AND REPORT — END OF PHASE 2

Print all of the following and wait:

1. Verdict counts per tag: how many `identical`, how many `drift`, for each of
   emi / loan / payment / customer.
2. For one emi scenario: the scenario id, the exact dot-path that changed, the
   old value, and the new value.
3. Whether loan and payment drifted, and by reading the code, state whether
   they reach `interest.py` directly or through `emi_service`.
4. Confirmation that all 10 customer scenarios are `identical`.
5. Whether any scenario returned a non-200 status on either side.

---

## SECTION 4 — PHASE 3: THE BLAST RADIUS

> Goal: stop replaying everything. Compute which endpoints a change can
> possibly affect, and replay only those. This is what makes BlastProof
> *targeted* rather than a test runner.

**Build the LOCAL version first.** MCP integration is timeboxed and optional;
the local version is the one the demo must be able to fall back to.

### TODO — Phase 3
- [ ] 3.1 `engine/impact_local.py` — AST-based dependency walk
- [ ] 3.2 Verify the radius against known-correct answers
- [ ] 🛑 STOP AND REPORT
- [ ] 3.3 (timeboxed, optional) LatentGraph MCP setup
- [ ] 3.4 (timeboxed, optional) `engine/impact.py` — MCP version

---

### TASK 3.1 — `engine/impact_local.py`

**Goal:** given two git refs, compute which files and endpoints a change
could affect, using only the Python standard library.

**Algorithm:**

1. **Find changed files.**
   ```
   git diff --name-only <old_ref>..<new_ref>
   ```
   Filter to `.py` files under `demo_app/`. This is the `changed` list.

2. **Build a reverse import graph.** Walk every `.py` file under `demo_app/`
   with the `ast` module. For each file, collect `import` and `from ... import`
   statements. Resolve them to file paths within the project. Invert the result
   so you can ask: *which files import THIS file?*

3. **Walk dependents two levels deep.** Starting from each changed file, find
   its importers, then find THEIR importers. Two levels is deliberate and
   sufficient:
   `interest.py` → `emi_service.py` → `payment_service.py` and `main.py`.
   This is what proves the radius follows indirect paths.
   Collect everything into `affected_files`.

4. **Map files to endpoints.** Parse `demo_app/main.py` with `ast`. Find every
   function decorated with `@app.get(...)`, `@app.post(...)`, etc., and record
   the route string. For each route handler, determine which modules it calls
   into. A route belongs in `affected_endpoints` if its handler reaches any
   file in `affected_files`.

5. **Produce call paths.** For each changed function, produce at least one
   human-readable chain like
   `get_monthly_rate -> calculate_emi -> calculate_emi_endpoint`.
   A simple caller-name chain is sufficient — this is used for display in the
   EXPLAIN step, not for logic.

6. **Write the radius** in exactly the shape given in Section 2.

**CLI:**
```
python -m engine.impact_local --old v1.0 --new demo-change
```
Prints the radius JSON to stdout. Also expose a function that the CLI in
Task 8 can import directly.

**Constraints:** standard library only. No third-party parsers. Do not import
the app — parse it statically. Importing would execute code and is fragile.

---

### TASK 3.2 — Verify the radius

Three checks. All three must pass.

**Check A — the real change:**
```
python -m engine.impact_local --old v1.0 --new demo-change
```
Must report:
- `changed` contains `demo_app/core/interest.py`
- `affected_files` includes `emi_service.py`, `loan_service.py`,
  `payment_service.py` and `main.py`
- `affected_endpoints` includes `/api/emi`, the loan route and the payment route
- `affected_endpoints` **does NOT include the customer route**

That last line is the test that matters. If the customer endpoint appears in
the radius, the dependency walk is wrong.

**Check B — a zero-dependency change:**
Make a trivial edit to a file nothing imports (e.g. add a blank line to
`README.md` or `WHAT_WE_BUILT.md`), commit it on a scratch branch, and run the
impact step against it. The radius must be **empty** — no affected files, no
affected endpoints. Delete the scratch branch afterward.

**Check C — targeted replay:**
Feed the radius's endpoints into replay as tags and confirm that only the
matching scenarios run. Roughly 50 scenarios should replay, and the 10
customer scenarios should be skipped entirely — not replayed and marked
identical, but never fired at all.

---

### 🛑 STOP AND REPORT — after Task 3.2

Print the full radius JSON from Check A, the empty radius from Check B, and
the scenario count from Check C. Then wait.

---

### TASK 3.3 — LatentGraph MCP setup (TIMEBOXED: 2 HOURS, ABANDON IF IT FIGHTS)

This is the step that connects us to the organizer's own product. It is worth
real points on innovation, but **it is not worth the demo.** If it is not
working after two hours, ship `--local` and move on. Set a timer.

```
npm install -g @latentforce/latentgraph
```
Get a free key at https://latentgraph.latentforce.ai/auth
```
lgraph start
lgraph init
lgraph add latent-code
```
Restart the LatentCode session after `lgraph add latent-code`, or the MCP
tools will not appear.

Set `LGRAPH_PROJECT_ID` in the environment if the tools require a project id.

**Notes from the MCP server's docs:** tool responses come back as fenced `toon`
blocks — compact tab-delimited JSON. Parse them accordingly. If toon parsing
becomes a time sink, `ask_codebase` with a targeted question and parsing the
file-path citations out of the answer is an acceptable secondary path.

---

### TASK 3.4 — `engine/impact.py` (MCP version)

Same output shape as `impact_local.py`. Different data source:

| Step | MCP tool |
|---|---|
| who imports this file | `get_dependencies(file)` — read the incoming edges |
| what does this symbol call | `get_call_chain(symbol)` |
| what endpoints does this file serve | `get_file(file)` — read the served-endpoints field |

Walk dependents two levels, exactly as the local version does.

**Fallback is mandatory.** A `--local` flag on the CLI must switch to
`impact_local`. Additionally, if any MCP call raises or times out, log a clear
warning and fall back to the local engine automatically. **The pipeline must
never fail because a network service is down.**

**DONE WHEN:** `impact.py` and `impact_local.py` produce the same
`affected_endpoints` for the `v1.0..demo-change` diff. They may differ in
`affected_files` detail — that is fine, the graph knows more than the AST does.
The endpoints must agree.

---

## SECTION 5 — PHASE 4: EXPLANATION AND JUDGEMENT

> Goal: stop showing raw diffs. Say what changed in one English sentence, then
> say whether the team already decided it wasn't allowed.

### TODO — Phase 4
- [ ] 4.1 `engine/explain.py`
- [ ] 4.2 `decisions.json` seeded with real rules
- [ ] 4.3 `engine/judge.py`
- [ ] 🛑 STOP AND REPORT

---

### TASK 4.1 — `engine/explain.py`

**Goal:** one plain-English sentence per drifted scenario.

**Scope:** one LLM call per drifted **scenario**, not per drifted field. One
call covers all the diffs in that scenario. Sequential, not parallel.

**Prompt structure:**
```
You are a code-change analyst. Given:

CODE DIFF:
<output of: git diff v1.0..demo-change -- demo_app/core/interest.py>

RESPONSE DIFFERENCES:
<the diffs array for this scenario from the compare step>

CALL PATH:
<from the radius's call_paths>

Write ONE sentence explaining what changed and why.
Name the exact file:line. State the old and new business value.
Do not speculate beyond the diff. Do not use jargon.
```

**Target output shape:**
> "EMI ₹858.37 → ₹831.02 — caused by interest.py:5 (rate/12 → rate/365),
> reached via get_monthly_rate → calculate_emi."

**Caching (required):** hash `(scenario_id + code_diff_content)`. Same hash
returns the cached explanation. Store the cache in a gitignored local file.
Without this, every development re-run burns tokens on identical work.

**Failure handling:** if the LLM call fails, write a fallback explanation built
mechanically from the diff — e.g. `"data.emi changed from 858.37 to 831.02"` —
and continue. A failed explanation must never abort the pipeline.

**DONE WHEN:** run against the Phase 2 `comparison.json`; every drifted
scenario gets one sentence naming a file and a line number; a second run
produces identical output and makes zero LLM calls.

---

### TASK 4.2 — `decisions.json`

**Goal:** the local fallback corpus of recorded team decisions.

Create `decisions.json` at the repo root using the shape in Section 2. Seed it
with these four rules, which correspond to real design decisions in the app:

1. **D-17** — `demo_app/core/interest.py` — "EMI must use monthly
   normalization (annual_rate / 12) per lending convention" — severity high
2. **D-22** — `demo_app/main.py` — "All /api/* responses use the
   {success, data, meta} envelope" — severity medium
3. **D-31** — `demo_app/services/payment_service.py` — "Payment endpoints must
   remain read-only and never mutate stored state" — severity high
4. **D-40** — `demo_app/main.py` — "The customer endpoint must not depend on
   interest calculations" — severity medium

`source` fields should reference PR numbers. Coordinate with the app lane so
those PR numbers correspond to real PRs (see Section 7).

D-17 is the rule the planted `rate/365` change violates. That is the one that
turns a yellow row red in the demo.

---

### TASK 4.3 — `engine/judge.py`

**Goal:** classify each drift against recorded decisions.

**Steps per drifted scenario:**
1. Take the affected files from the radius.
2. **Primary source:** `get_pr_insights(file)` via MCP, which returns
   `{invariants: [{text, severity, pr_source}], decisions: [{text, tradeoffs, pr_source}]}`.
3. **Fallback:** if MCP is unavailable or returns empty, read `decisions.json`
   and select rules whose `file` matches an affected file.
4. **Classification call:**
```
Given this behavioral drift:
<explanation from the explain step>

And these recorded team decisions:
<the relevant decisions and invariants>

Classify as exactly ONE of:
- VIOLATES <decision-id>: the drift contradicts a recorded rule
- MATCHES_INTENT: the drift is consistent with the stated purpose of the change
- UNCOVERED: no recorded decision covers this behavior

Answer in one line: CLASSIFICATION — one sentence reason.
```
5. **Map to verdicts:**
   - `VIOLATES` → `regression`
   - `MATCHES_INTENT` → `intentional`
   - `UNCOVERED` → `unexplained`
6. Attach the matched rule to the result as
   `{"id", "text", "source"}` per the report.json contract.

**DONE WHEN — two checks:**
- With D-17 present in `decisions.json`, the emi drifts classify as
  `regression` and cite D-17.
- Temporarily remove D-17, re-run, and the same drifts classify as
  `unexplained`. Restore D-17 afterward.

That second check is the one to demo if a judge asks whether the classification
is real or hardcoded.

---

### 🛑 STOP AND REPORT — after Task 4.3

Print: the explanation sentence for one emi scenario; its classification and
cited rule; and the before/after of the D-17-removed test.

---

## SECTION 6 — PHASE 5: TEACH AND THE ONE-COMMAND PIPELINE

### TODO — Phase 5
- [ ] 5.1 `engine/teach.py`
- [ ] 5.2 `engine/cli.py`
- [ ] 🛑 STOP AND REPORT

---

### TASK 5.1 — `engine/teach.py`

**Goal:** turn a confirmed finding into a proposed invariant, and write it back
to the graph — only when a human clicks Confirm.

**Proposal generation:** from a classified drift, produce a sentence like:
> "Changing annual-rate normalization in demo_app/core/interest.py changes EMI
> output for /api/emi, /api/loan and /api/payment. Verified across 50 scenarios
> on 2026-08-30."

**Write path:**
- **Primary:** MCP `update_graph` with a file-annotation edit on the affected
  file. Their API queues it for owner approval and returns a `pending_edit_id`.
  Surface that id as a receipt — it is proof the write happened.
- **Fallback:** append the invariant text to `proposed_invariants.md` at the
  repo root.

**CRITICAL:** the write must **never** happen automatically. It happens only
when explicitly invoked with a confirm flag, representing a human clicking
[Confirm & Teach] in the UI. This mirrors LatentForce's own approval-queued
design and is a deliberate talking point — say "we propose, the human decides"
in the demo.

Expose two entry points: one that generates the proposal (safe, read-only) and
one that commits it (requires the confirm flag).

**DONE WHEN:** running the proposal generator prints a proposal and writes
nothing. Running with the confirm flag either returns a `pending_edit_id` or
appends to `proposed_invariants.md`, and says which path it took.

---

### TASK 5.2 — `engine/cli.py`

**Goal:** one command runs all six steps and writes `report.json`.

**Command:**
```
python -m engine.cli --old v1.0 --new demo-change --app demo_app.main:app
```

**Flow:** impact → replay (filtered by the radius) → compare → explain (drifts
only) → judge (drifts only) → write `report.json`. Teach is invoked separately
on confirmation, not as part of the chain.

**Flags:**
- `--local` forces the local impact engine
- `--no-llm` skips explain and judge, producing a report with `identical` and
  `drift` verdicts only. **This flag is your demo insurance.** If the LLM
  provider is down on Sunday, this still produces a working demo.

**Output:** `report.json` in exactly the shape in Section 2. The `summary`
counts must add up to `total`.

**DONE WHEN:**
- The one command produces a valid `report.json`.
- `--no-llm` also produces a valid `report.json` with the same scenario count.
- `report.json` parses and every result object has `scenario`, `verdict` and
  `diffs`; drifted ones additionally have `explanation` and `rule`.

---

### 🛑 STOP AND REPORT — after Task 5.2

Print the `summary` block from `report.json` and one full `results` entry with
verdict `regression`.

---

## SECTION 7 — THE APP LANE (what the friend does)

> Hand this section to him directly. He is idle and this is the critical path
> for the demo now.

### What he has done well

The demo app is genuinely good work. `core/interest.py` isolates all the math
in one function, the service layer creates a real two-level dependency
(`payment_service → emi_service → interest`), all four endpoints exist with a
consistent response envelope, `request_id` and `generated_at` are present as
the deliberate noise the comparator has to survive, seed data is fixed and
deterministic, and he wrote pytest tests nobody asked for. That is a solid
foundation and the engine works against it.

### What went wrong — read this, because the pattern matters

**1. He built against the bare skeleton instead of pulling the contracts.**
`CONTRACTS.md` was sitting on the `engine` branch. He branched from an old
`main` that didn't have it, and generated 60 scenario files in a completely
different schema — `tag` instead of `tags`, `method`/`path` nested under a
`request` object, `endpoint` instead of `path`. The engine could not read a
single one of them. This cost hours and had to be regenerated from scratch.
**Rule going forward: `git pull origin main` before starting any new piece of
work, and read CONTRACTS.md before writing anything that crosses the seam.**

**2. He recorded expected responses inside the scenario files.** The original
files carried `expected_status` and a full `response` block with a recorded
`request_id` and `generated_at`. That is a misunderstanding of what the product
does. BlastProof does not compare against stored expectations — it runs both
versions live and compares them to each other. Storing a response makes the
file stale the moment the app changes. It also would have embedded a fixed
timestamp into a file whose whole purpose is to test timestamp-insensitivity.

**3. He generated two conflicting sets of scenarios and cleaned up neither.**
`emi_001`–`emi_020` and `emi_1`–`emi_20` both existed, with different body
field names. `manifest.json` pointed at one set. If nobody had caught it, the
demo would have replayed 40 emi scenarios, half of which would have 422'd.

**4. He committed build artifacts.** Thirteen `.pyc` files and a `server.log`
went into the repo because he had no `.gitignore`. On a hackathon scored 30% on
execution, a repo full of compiled bytecode is a bad first impression. Already
cleaned up.

**5. He merged straight to `main` with the message "Merge branch 'app'".**
Our own plan says merges happen via PRs with meaningful descriptions, precisely
because those descriptions become `get_pr_insights` material for our JUDGE
step. A one-word merge commit teaches the graph nothing.

None of this is catastrophic and all of it is fixed. But the pattern — build
fast, don't check the contract, don't clean up — is exactly what turns into an
unrecoverable mess at 2 AM on submission night. Pull before you build. Read the
contract before you write across the seam.

### What he must do now, in priority order

#### 🔴 D4 — THE UI (start immediately, it is the critical path)

This is the largest unstarted item in the project and the thing the demo video
actually shows. Not a dashboard — a **PR safety gate**. One page, reads
`report.json`, no build step if possible (a single HTML file with inline CSS
and JS is fine and preferable).

**Sections, top to bottom:**

1. **Header** — `BLASTPROOF`, the branch or PR being checked, and the list of
   changed files.
2. **Radius card** — "N affected files · N affected endpoints", with the
   endpoints listed. This is where the targeting story is visible.
3. **Verification bar** — one line, big:
   `60 scenarios · 40 ✓ unchanged · 2 ⚠ intentional · 18 🔴 regression`
4. **Drift list** — one row per non-identical scenario: endpoint name, the
   old → new value, and a verdict badge. Colour-coded: red for regression,
   amber for intentional, yellow for unexplained. Identical rows collapsed or
   summarised, not listed individually.
5. **Row detail** (click to expand):
   - the explanation sentence
   - the violated rule text and its PR source
   - `[View Evidence]` — raw old and new JSON side by side
   - `[Confirm & Teach]` — fires a callback and shows the receipt
6. **Nothing else.** No charts. No settings page. No auth. No navigation. No
   login screen. Every extra screen is time stolen from polish on the one
   screen that gets filmed.

**Build it against a hand-written sample `report.json` first** so it is not
blocked waiting for the engine. The contract is frozen and is in Section 2 —
build to that, and it will work with the real file when it arrives.

**Done when:** given a valid `report.json`, the page renders every section,
rows expand, and the Confirm button fires a callback and shows a receipt.

#### 🟠 D3 — Seeded decision PRs

Create three or four real PRs on the repo whose descriptions state a rule.
These are what `get_pr_insights` will later mine, and they make the JUDGE step
demonstrably real rather than reading from a file we wrote ourselves.

Suggested PR descriptions, matching the `decisions.json` entries in Task 4.2:
- "EMI must use monthly normalization (annual_rate / 12) per lending convention"
- "All /api/* responses use the {success, data, meta} envelope"
- "Payment endpoints must remain read-only and never mutate stored state"
- "The customer endpoint must not depend on interest calculations"

Note the PR numbers GitHub assigns and pass them to the engine lane so
`decisions.json` cites real sources.

#### 🟡 Housekeeping
- Install at least one SkillPatch skill and note its exact name — required to
  enter the ₹5,000 category prize, and it must be declared on the form.
- **Do not touch `scenarios/` again.** All 60 files are validated and frozen.
  Any regeneration risks reintroducing the schema break.
- Do not commit to `main` directly. Branch, PR, merge with a real description.

---

## SECTION 8 — VERIFICATION CHECKLIST (run before recording the video)

Every one of these must pass. Do not record until they do.

- [ ] **1. Seeded regression.** The planted `rate/365` change is caught, and
      only the interest-dependent scenarios are flagged. Not more, not fewer.
- [ ] **2. Determinism.** Run the same replay twice against unchanged code.
      100% identical both times. Any variance means a noise field is leaking
      through the comparator.
- [ ] **3. Radius sanity.** Change a file nothing imports. Radius is empty,
      zero scenarios replayed.
- [ ] **4. Judge sanity.** With D-17 in `decisions.json`, the emi drift is a
      `regression` citing D-17. With D-17 removed, the same drift is
      `unexplained`. Restore D-17.
- [ ] **5. Negative control.** The 10 customer scenarios never appear in the
      radius and never turn red.
- [ ] **6. Full pipeline.** `python -m engine.cli` runs every step and produces
      a `report.json` the UI renders correctly.
- [ ] **7. Offline insurance.** `--no-llm` and `--local` both produce a valid
      report with no network dependency at all.
- [ ] **8. Demo dry run.** Walk the exact 90-second sequence once. Time it.
      Over 2 minutes means cut something.

---

## SECTION 9 — THE DEMO (90 seconds, rehearse it)

1. Show the banking app running and the gate screen — all green.
2. Change one line live: `rate/12` → `rate/365`.
3. Run BlastProof. The radius appears: N files, N endpoints — and customer is
   visibly absent.
4. Scenarios replay. Most green. A block of red.
5. Click a red row: old value, new value, the causing line, and the violated
   rule with its PR source.
6. Click `[Confirm & Teach]` → show the receipt.
7. Close with the line:
   > "Their graph told us where to look. We proved what changed. Their memory
   > said it wasn't allowed. And now the graph is smarter."

**The pitch line, if you need one sentence:**
> "Your graph knows what the code is. Your learnings know what the team
> decided. BlastProof proves what the change actually did — and checks it
> against both."

**Framing discipline — never say "you don't have this" or "we found your gap."**
Always: "we built on your public stack — LatentGraph for targeting,
pr_insights for judgement, update_graph for learning." If a judge says they
have something internal, the answer is: "we independently arrived at your
roadmap using only your public tools." That reads as a compliment, not a
correction.

---

## SECTION 10 — SUBMISSION (Sunday, after the 14:00 code freeze)

- [ ] Demo video recorded, **2 minutes or under**
- [ ] `/export` transcript from **Saubhagya's** LatentCode session
- [ ] `/export` transcript from **the friend's** LatentCode session
- [ ] Google Drive folder created, video + both transcripts uploaded
- [ ] Sharing set to "anyone with the link can view"
- [ ] **Link tested in a private browser window** — an unshared Drive folder
      is a silent disqualification
- [ ] Build-in-Public post published during the window, tagging **@LatentForce**
- [ ] README finalised: what it is, how to run it, the architecture, the
      fallback design
- [ ] SkillPatch skill names noted for both members
- [ ] SkillPatch API key rotated (it was exposed in chat and has still not
      been confirmed rotated)
- [ ] agentrouter API key deleted or regenerated (exposed in screenshots)
- [ ] Google Form submitted by the team leader **before 18:00 IST**

---

## SECTION 11 — REPORTING SCHEDULE

At each 🛑 STOP point, the human reports the printed output to the monitor
before continuing. The stop points are:

| # | After | Report |
|---|---|---|
| 1 | Phase 2 (Task 2.4) | verdict counts per tag, one concrete old→new value |
| 2 | Phase 3 (Task 3.2) | the three radius checks |
| 3 | Phase 4 (Task 4.3) | one explanation, one classification, the D-17 test |
| 4 | Phase 5 (Task 5.2) | report.json summary and one regression entry |
| 5 | Section 8 | the full verification checklist, pass/fail per line |

**Push after every completed task, not at the end of a phase.** Work that
exists only on one laptop is work that can vanish.

---

## SECTION 12 — IF TIME RUNS SHORT

Cut from the top of the list, never the bottom. Each line below is still a
complete, demoable product on its own.

1. Replay + compare + UI — a working behavioural diff gate. **Already achieved.**
2. \+ local impact — targeted replay driven by real dependency analysis.
3. \+ explain — plain-English cause for every drift.
4. \+ judge — enforcement against recorded team decisions.
5. \+ MCP impact — the radius comes from LatentGraph itself.
6. \+ teach — verified findings written back to the graph.

If it is Sunday morning and the MCP is fighting you, ship `--local` and spend
the time on the video instead. A polished demo of levels 1–4 beats a broken
demo of level 6, every single time.

**A working demo you can show beats an ambitious one you cannot.**
