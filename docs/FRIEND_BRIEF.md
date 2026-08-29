# BLASTPROOF — APP LANE BRIEF (Mayank)

**Read this whole file before writing anything. It takes five minutes and will
save you hours.**

---

## 1. WHERE THE PROJECT STANDS

### What I (Saubhagya) have built and verified

**`engine/replay.py` — done and tested.**
Takes two git refs. Creates a git worktree for each, boots both versions of
the banking app simultaneously on ports 8001 and 8002 via uvicorn, waits for
both `/health` checks to return 200, filters scenarios by tag, fires each
request at both servers with httpx, and writes both responses side by side
into `results.json`. Cleans up both servers and both worktrees at the end.
If zero scenarios match the requested tags it exits non-zero without booting
anything — a run that tests nothing must not look like a run that passed.

**`engine/compare.py` — done and tested.**
The semantic differ. This is the piece the whole product rests on. Every
response from your app carries a fresh `request_id` and `generated_at`, so a
naive JSON comparison would flag all 60 scenarios as changed and the tool
would be useless. compare.py ignores those fields at any nesting depth
(including inside your `meta` block), treats numbers as equal within 0.01 to
absorb floating-point noise in the EMI math, walks nested dicts and lists,
and reports every real mismatch as a dot-path like `data.emi`. It has a
built-in self-test with three fixtures — noise-only, real drift, and float
tolerance — that all pass.

**Verified working against YOUR app:**
- All 60 scenarios replay successfully against `demo_app.main:app`
- All 20 emi scenarios return `identical` even though `request_id` and
  `generated_at` differ on every single response
- 60 scenario files, zero contract violations, no duplicate ids,
  correct distribution: 20 emi / 15 loan / 15 payment / 10 customer

**On main and clean:** both lanes merged, `.gitignore` in place, build
artifacts untracked.

### What is still missing

- The `v1.0` tag and the `demo-change` branch (I'm doing this right now)
- `impact.py` — the blast radius (mine)
- `explain.py`, `judge.py`, `teach.py`, `cli.py` (all mine)
- `decisions.json` (mine, but needs your PR numbers)
- **The entire UI (yours — and it is the single biggest unstarted item)**

---

## 2. WHAT YOU BUILT WELL

Credit where it's due — `demo_app/` is good work.

- All the interest math lives in one function in one file, exactly as the
  design needs. That is what makes a one-line change ripple to four endpoints.
- The service layer creates a real two-level dependency:
  `payment_service → emi_service → interest.py`. That indirect path is what
  proves the blast radius walks more than one hop. Getting that shape right
  matters more than it looks.
- All four endpoints exist, plus `/health`, with a consistent
  `{success, data, meta}` envelope.
- `request_id` and `generated_at` are present as deliberate noise — which is
  what let me prove the comparator can ignore them.
- Seed data is fixed and deterministic. Same input, same output, every time.
- You wrote pytest tests nobody asked for.

The engine works against your app right now. That's not nothing.

---

## 3. WHAT WENT WRONG — read this, the pattern matters more than the bugs

### 3.1 You built without pulling the contracts. This cost us hours.

`CONTRACTS.md` was sitting on the `engine` branch. You branched off an old
`main` that didn't have it, and generated 60 scenario files in a completely
different schema:

```json
// what you generated — the engine cannot read this
{"id": "emi_1", "tag": "emi",
 "request": {"method": "POST", "endpoint": "/api/emi", "body": {...}},
 "expected_status": 200, "response": {...}}
```

```json
// what CONTRACTS.md requires — five top-level keys, nothing else
{"id": "emi_1", "method": "POST", "path": "/api/emi",
 "body": {"principal": 10000, "annual_rate": 5.5, "tenure_months": 12},
 "tags": ["emi"]}
```

`tag` singular instead of `tags` as an array. `method` and `path` buried under
`request`. `path` renamed to `endpoint`. My replay filters on `tags` and reads
top-level `method`/`path`/`body` — it matched **zero** of your 60 files and hit
its fail-fast guard. All 60 had to be regenerated.

**The rule from now on: `git pull origin main` before starting any new piece
of work, and read `CONTRACTS.md` before writing anything that crosses between
our two lanes.** The seam is exactly two things — `scenarios/*.json` (you
write, I read) and `report.json` (I write, you read). Those two schemas are
frozen. If you think one needs to change, we both agree first and we both
update CONTRACTS.md. Never change one unilaterally.

### 3.2 You stored expected responses inside the scenario files

The originals carried `expected_status` and a full `response` block with a
recorded `request_id` and a frozen `generated_at`.

That's a misunderstanding of what we're building. BlastProof does **not**
compare against stored expectations. It runs the old version and the new
version live, at the same time, and compares them **to each other**. That's
the entire pitch — runtime proof, not stored assertions.

Storing a response makes the file wrong the moment the app changes. And
freezing a timestamp inside a file whose whole purpose is to test
timestamp-insensitivity is the exact opposite of what it's for.

### 3.3 Two conflicting scenario sets, neither cleaned up

`emi_001`–`emi_020` and `emi_1`–`emi_20` both existed, with different body
field names — one used `months`, the other `tenure_months`. `manifest.json`
pointed at one set. If nobody had caught it, the demo would have replayed 40
emi scenarios and half would have returned 422 on stage.

### 3.4 You committed build artifacts

Thirteen `.pyc` files and a `server.log` went into the repo because there was
no `.gitignore` on your branch. Execution is 30% of the score, and a judge
opening a repo full of compiled bytecode forms an opinion in two seconds.
Already cleaned up.

### 3.5 You merged to main with the message "Merge branch 'app'"

Our plan says merges go through PRs with real descriptions — not for
ceremony, but because those descriptions become the material our JUDGE step
mines later via `get_pr_insights`. A one-word merge commit teaches the graph
nothing. This one actually costs us a feature.

### The pattern

None of this was fatal and all of it is fixed. But *build fast, don't check
the contract, don't clean up* is exactly the pattern that becomes
unrecoverable at 2 AM on submission night. Pull before you build. Read the
contract before you write across the seam. Delete what you replaced.

---

## 4. WHAT I'M DOING NEXT (so we don't collide)

In this order, all in `engine/`:

1. Tag `v1.0`, create the `demo-change` branch with `rate/12 → rate/365` in
   `interest.py`, and prove the detection works end to end.
2. `impact_local.py` — compute the blast radius by walking imports with the
   `ast` module, so we replay only the affected endpoints instead of
   everything.
3. `impact.py` — the same thing via LatentGraph's MCP server, with the local
   version as an automatic fallback.
4. `explain.py` — one plain-English sentence per drift, naming the file and
   line that caused it.
5. `judge.py` — classify each drift against recorded team decisions:
   regression / intentional / unexplained.
6. `teach.py` — propose an invariant and write it back to the graph, only on
   a human clicking Confirm.
7. `cli.py` — one command that runs all six steps and writes `report.json`.

**I will not touch `demo_app/`, `scenarios/`, or `ui/`.** Those are yours.

**Do not touch `engine/` or `scenarios/`.** The 60 scenario files are
validated and frozen — regenerating them risks reintroducing the schema
break, and everything downstream depends on them.

---

## 5. YOUR WORK — in priority order

### 🔴 PRIORITY 1: THE UI. Start now. Nothing else first.

This is the largest unstarted item in the project and it is what the 2-minute
demo video actually films. The engine can be perfect and we still lose
presentation points if the demo is a terminal printing JSON.

**Crucial: you are NOT blocked on me.** The `report.json` contract is frozen
and reproduced below. Build against a hand-written sample file. When my
engine produces the real one, it will drop straight in.

#### What it is

A **PR safety gate** — one screen, the thing a developer sees before merging.
Not a testing dashboard. Not an analytics tool. It should look like something
an enterprise would put in front of a merge button.

Single HTML file with inline CSS and JS is ideal. No build step, no framework,
no npm install. It has to run reliably on a laptop during a recording.

#### The exact contract it reads — `report.json`

```json
{
  "summary": {
    "total": 50,
    "identical": 30,
    "intentional": 2,
    "regression": 18,
    "unexplained": 0
  },
  "radius": {
    "changed": ["demo_app/core/interest.py"],
    "affected_files": [
      "demo_app/services/emi_service.py",
      "demo_app/services/loan_service.py",
      "demo_app/services/payment_service.py",
      "demo_app/main.py"
    ],
    "affected_endpoints": ["/api/emi", "/api/loan/{loan_id}", "/api/payment"],
    "call_paths": ["get_monthly_rate -> calculate_emi -> calculate_emi_endpoint"]
  },
  "results": [
    {
      "scenario": "emi_1",
      "verdict": "regression",
      "diffs": [
        {"path": "data.emi", "old": 858.37, "new": 831.02},
        {"path": "data.total_interest", "old": 300.44, "new": 27.12}
      ],
      "explanation": "EMI 858.37 -> 831.02 - caused by interest.py:5 (rate/12 -> rate/365), reached via get_monthly_rate -> calculate_emi.",
      "rule": {
        "id": "D-17",
        "text": "EMI must use monthly normalization (annual_rate / 12) per lending convention",
        "source": "PR #4"
      }
    },
    {
      "scenario": "loan_3",
      "verdict": "intentional",
      "diffs": [{"path": "data.schedule.0.interest", "old": 229.16, "new": 7.53}],
      "explanation": "Loan schedule interest changed following the rate normalization change.",
      "rule": null
    },
    {
      "scenario": "customer_2",
      "verdict": "identical",
      "diffs": [],
      "explanation": null,
      "rule": null
    }
  ]
}
```

**Field notes:**
- `verdict` is one of exactly four values: `identical`, `regression`,
  `intentional`, `unexplained`.
- `explanation` and `rule` are `null` on identical rows, and `rule` can be
  `null` on drifted rows too (when nothing in PR history covers it). Handle
  nulls — don't crash on them.
- `diffs[].path` is dot notation and can include list indices:
  `data.schedule.0.interest`.
- `old` and `new` can be numbers, strings, booleans, or null.

#### The screen, top to bottom

**1. Header**
`BLASTPROOF` as the title. Below it, the branch or PR being checked, and the
list of changed files from `radius.changed`. Keep it to one or two lines.

**2. Radius card**
> **Blast radius: 4 affected files · 3 affected endpoints**
> `/api/emi` `/api/loan/{loan_id}` `/api/payment`

List the endpoints as chips or a simple inline list. This card is where the
targeting story is visible — a viewer should notice that `/api/customer` is
**absent**. That absence is the proof we're not just running everything.

If you can show `radius.call_paths` somewhere small, do — it makes the
dependency walk concrete.

**3. Verification bar**
One prominent line, the biggest text after the header:

> **50 scenarios · 30 ✓ unchanged · 2 ⚠ intentional · 18 🔴 regression · 0 🟡 unexplained**

Drive it entirely from `summary`. Don't recount from `results`.

**4. Drift list**
One row per non-identical scenario. Identical rows should be collapsed into a
single summary line ("30 scenarios unchanged") or hidden behind a toggle —
do **not** render 30 green rows, it buries the signal.

Each row shows:
- the scenario id and the endpoint it hit
- the first diff as `old → new` (e.g. `858.37 → 831.02`)
- a verdict badge

Colours:
- 🔴 `regression` — red, this broke a recorded rule
- ⚠ `intentional` — amber, changed on purpose
- 🟡 `unexplained` — yellow, no rule covers it, needs a human
- ✓ `identical` — green

Sort regressions to the top. The red rows are the story.

**5. Row detail — click to expand**

- The `explanation` sentence, prominently. This is the payoff.
- The violated rule: `rule.text` and `rule.source` (e.g. "PR #4"). Style it
  as a quoted rule, not body text — it should read as *the team already
  decided this*.
- **`[View Evidence]`** — reveals the raw old and new JSON side by side. It
  can be a simple two-column `<pre>` block. This exists so a judge can ask
  "is this real?" and we click one button.
- **`[Confirm & Teach]`** — a button that fires a callback and then shows a
  receipt line: "Written to graph — pending_edit_id: xyz". For now, wire it to
  a stub function and display a hardcoded receipt. I'll give you the real
  hook when `teach.py` exists.

**6. Nothing else.**
No charts. No graphs. No settings page. No login. No navigation bar. No
"about" section. Every extra screen is time stolen from polishing the one
screen that gets filmed. If you find yourself building a second page, stop.

#### Design notes

- Dark background reads well on video and makes the red/amber/green badges
  pop.
- Generous spacing. On a 2-minute video the viewer has about 8 seconds per
  screen — it must be scannable, not dense.
- Use a monospace font for values, paths, and JSON. Sans-serif for prose.
- Test it at 1920×1080. That's what gets recorded.

#### DONE WHEN

- Given the sample `report.json` above, every section renders correctly.
- Rows expand and collapse.
- `[View Evidence]` shows old vs new JSON.
- `[Confirm & Teach]` fires and displays a receipt.
- Null `explanation` and null `rule` don't break anything.
- It opens by double-clicking the HTML file. No server, no build step.

**Target: done by tonight.** Polish tomorrow morning.

---

### 🟠 PRIORITY 2: Seeded decision PRs

After the UI is functional, not before.

Create three or four real PRs on the repo whose **descriptions state a rule**.
These are what LatentGraph's `get_pr_insights` mines, and they're what make
our JUDGE step demonstrably real rather than reading from a file we wrote
ourselves. This is the difference between "we check against rules" and "we
check against rules the team actually recorded in PR history."

Use these descriptions:

1. **"EMI must use monthly normalization (annual_rate / 12) per lending
   convention."** Explain that daily normalization would understate the
   monthly instalment and is wrong for a lending product.
2. **"All /api/* responses use the {success, data, meta} envelope."** Explain
   that clients depend on the shape being uniform.
3. **"Payment endpoints must remain read-only and never mutate stored
   state."** Explain that this makes replay safe to run repeatedly.
4. **"The customer endpoint must not depend on interest calculations."**
   Explain that customer profile data is independent of loan math.

Each PR can be a tiny real change — a docstring, a comment, a test. The
content barely matters; the **description** is the deliverable.

**Then send me the PR numbers GitHub assigns.** I need them for
`decisions.json` so the rules cite real sources rather than made-up ones.

Rule #1 is the one our planted regression violates. That's the row that turns
red in the demo.

---

### 🟡 PRIORITY 3: Housekeeping

- **Install at least one SkillPatch skill** from skillpatch.dev and note its
  exact name. Required for the ₹5,000 category prize and it has to be declared
  on the submission form. Two minutes.
- **Keep your LatentCode session alive.** You need to run `/export` from it on
  Sunday. Every member who wrote code must submit their own transcript. If you
  lose the session you lose the transcript, and that's a submission
  requirement, not a nice-to-have.
- **Do not touch `scenarios/`.** Frozen and validated.
- **Do not commit directly to `main`.** Branch, PR, merge with a real
  description.
- **Only one LatentCode session in this repo at a time.** Two ran concurrently
  earlier and produced duplicate commits and a reset on a pushed branch we had
  to untangle.

---

## 6. RULES FOR THE REST OF THE HACKATHON

1. **`git pull origin main` before starting anything new.**
2. **Never force-push. Never `git reset --hard` on a pushed branch. Never
   amend a pushed commit.** If a merge conflicts, stop and tell me.
3. **Never change a frozen schema alone.** `scenarios/*.json` and
   `report.json` need both of us to agree, and both of us update
   `CONTRACTS.md`.
4. **Commit and push after every finished piece.** Work on one laptop is work
   that can vanish.
5. **Delete what you replace.** Don't leave two versions of anything.
6. **LatentCode writes all project code.** No other AI tool touches it —
   that's hackathon rule 3 and it's a disqualifier.

---

## 7. THE CLOCK

| When | What |
|---|---|
| **Tonight** | UI functional against a sample report.json |
| **Sunday morning** | UI polished, decision PRs made, PR numbers sent to me |
| **Sunday 14:00** | **HARD STOP ON ALL CODE.** No exceptions. |
| Sunday 14:00–18:00 | Demo video, both `/export` transcripts, Drive folder, Build-in-Public post, README, submission form |
| **Sunday 18:00** | Form submitted, or we're disqualified. No grace period. |

Both of us need our own `/export`. Both need a SkillPatch skill name. The
Drive folder must be set to "anyone with the link can view" and **tested in a
private browser window** — an unshared folder is a silent disqualification.

---

## 8. THE DEMO YOU'RE BUILDING TOWARD

90 seconds:

1. Banking app running, BlastProof gate screen — all green.
2. Change one line live: `rate/12` → `rate/365`.
3. Run BlastProof. The radius appears — 4 files, 3 endpoints, and
   `/api/customer` visibly absent.
4. Scenarios replay. Most green. A block of red.
5. Click a red row: old value, new value, the causing line, and the violated
   rule with its PR source.
6. Click `[Confirm & Teach]` → the receipt appears.
7. Close: *"Their graph told us where to look. We proved what changed. Their
   memory said it wasn't allowed. And now the graph is smarter."*

**Steps 1, 3, 4, 5 and 6 are all your screen.** The engine does the work, but
the UI is what the judges actually see. That's why it's priority one.
