# BLASTPROOF — FINAL SOLUTIONS

**Everything remaining, with exact fixes. Work top to bottom.**

Time at writing: **Saturday 16:11 IST. 21h48m to code freeze (Sun 14:00),
25h48m to submission (Sun 18:00).**

Verified state: the engine is real. `impact_local` does genuine AST dependency
analysis (proved by changing a different file and getting a different, correct
radius), `explain` parses the real git diff, `judge` has no hardcoded rule IDs,
`teach` reads real report data, `compare --selftest` passes, and the UI server
runs the real pipeline. What remains are five concrete fixes and one rebuild.

---

# PART A — MERGE TO MAIN (15 min) 🔴 DO THIS FIRST

Nothing else matters until judges can see the work. Right now `engine` is at
`3ff5d2c` and `main` is at `d747a48`, and engine is **not** an ancestor of
main. All ten fix commits exist only on `engine`. `main` still contains
`stub/`, no README, and the old fabricated modules.

There is also a file collision to resolve: the live UI is now the **repo-root**
`index.html` (that is what `ui/server.py` line 13 serves). But `main` still
carries the old `ui/index.html` — the one with the fake `pending_edit_id:
bp_938xf` receipt. If you merge without deleting it, both survive and a judge
may open the wrong one.

```bash
# 1. get onto main and take the engine work
git checkout main
git pull
git merge engine -m "Merge engine lane: real AST impact analysis, diff-derived explanations, dynamic rule judgement, honest teach receipts, live UI server, README"

# 2. remove the superseded UI (the one with the fabricated receipt)
git rm ui/index.html

# 3. remove leftover scratch files still in the root
git rm masterpan.md mayank.md KICKOFF.md TASK1B.md TASK2.md TASK_SCENARIOS.md
git rm WHAT_WE_BUILT.md STATUS_TRACKER.md APP_NOTES.md APP_TASKS.md
git rm -r stub

# 4. keep the reference docs, move them out of the root
mkdir -p docs
git mv MASTER_PLAN.md docs/
git mv ENGINE_TASKS.md docs/

git commit -m "chore: remove superseded UI and scratch files; move reference docs to docs/"
git push
git checkout engine
git merge main -m "merge main into engine"
git push
```

**Verify — paste this output:**
```bash
git ls-tree --name-only origin/main
git ls-tree -r --name-only origin/main | grep -E "index.html|ui/"
```

`main`'s root should contain only: `.gitignore`, `README.md`, `CONTRACTS.md`,
`PROJECT.md`, `decisions.json`, `requirements.txt`, `index.html`, and the
directories `demo_app/`, `engine/`, `scenarios/`, `ui/`, `docs/`.
There must be exactly **one** `index.html`.

If the merge conflicts, **stop and report the conflicting files.** Do not
resolve them alone.

---

# PART B — VERIFY THE DECISION PRs (10 min)

`decisions.json` cites `PR #4`, `PR #2`, `PR #3`, `PR #1`. Four branches exist
on the remote — `rule-emi-normalization`, `rule-response-envelope`,
`rule-readonly-payments`, `rule-independent-customer` — but each has **zero
diff against main**, which means they are either already merged or empty.

The JUDGE step's credibility rests on these being real recorded decisions.
Open `github.com/Mankurj05/SugarEngineers/pulls?q=is:pr` and confirm:

1. PRs #1–#4 exist.
2. Each description **states the rule in plain English** — this is the text a
   graph would mine. A PR titled "rule" with an empty body is worth nothing.
3. The PR numbers match what `decisions.json` claims. If PR #1 is actually the
   response-envelope rule and `decisions.json` says D-40 (customer
   independence) is PR #1, fix `decisions.json` to match reality.

If the PRs do not exist, create them now — the branches are already pushed, so
it is four "New pull request" clicks with a paragraph each. Suggested bodies:

- **EMI must use monthly normalization (`annual_rate / 12`) per lending
  convention.** Daily normalization understates the monthly instalment and is
  incorrect for an amortising loan product. Any change to
  `demo_app/core/interest.py` that alters the divisor changes every EMI figure
  the platform reports.
- **All `/api/*` responses use the `{success, data, meta}` envelope.** Clients
  depend on the shape being uniform; `meta` carries `request_id` and
  `generated_at` for tracing and must not be promoted into `data`.
- **Payment endpoints must remain read-only and never mutate stored state.**
  `calculate_balance` computes and returns; it never writes. This is what makes
  replaying the same request 60 times safe.
- **The customer endpoint must not depend on interest calculations.** Customer
  profile data is independent of loan math; introducing a dependency would put
  `/api/customer` into the blast radius of every rate change.

That last one is worth writing carefully — it is the rule your negative control
demonstrates.

---

# PART C — LATENTGRAPH MCP (2 hours, hard timebox) 🔴 HIGHEST VALUE

Four of the six pipeline steps were designed to consume LatentForce's own
product. All four currently run on their fallback. **One working call changes
the story.** If you get only one, make it `get_pr_insights` in the judge — that
is their Part-3 blog flagship and the most impressive to consume.

## C.1 — Install

```bash
npm install -g @latentforce/latentgraph
lgraph --version
```

Get a free key at **https://latentgraph.latentforce.ai/auth**.

```bash
lgraph --help          # find how it wants the key: env var or `lgraph login`
lgraph start
lgraph init            # run from the repo root so it indexes THIS repo
lgraph add latent-code
```

**Restart the LatentCode session after `lgraph add latent-code`** or the MCP
tools will not register.

```bash
lgraph status          # confirm the repo actually indexed
```

Add whatever the client needs to `requirements.txt` as you go.

If any step fails, **record the exact error string** and jump to C.5.

## C.2 — `engine/impact.py`: real graph queries

Replace the current hardcoded "MCP unavailable" message with a real attempt.

| What you need | Tool |
|---|---|
| files that import this file | `get_dependencies(file)` → incoming edges |
| callers/callees of a symbol | `get_call_chain(symbol)` |
| endpoints a file serves | `get_file(file)` → served-endpoints field |

Structure:

```python
def compute_impact(old_ref, new_ref, use_local=False, verbose=False):
    if use_local:
        return compute_impact_local(old_ref, new_ref)
    try:
        changed = get_git_changed_files(old_ref, new_ref)
        affected = set(changed)
        for f in changed:                      # two levels, same as local
            deps = mcp_get_dependencies(f)
            affected.update(deps)
            for d in deps:
                affected.update(mcp_get_dependencies(d))
        endpoints = set()
        for f in affected:
            endpoints.update(mcp_get_file(f).get("endpoints", []))
        paths = [mcp_get_call_chain(sym) for sym in changed_symbols(old_ref, new_ref)]
        if verbose:
            print(f"[impact] MCP returned {len(affected)} files, {len(endpoints)} endpoints", file=sys.stderr)
        return {"changed": changed, "affected_files": sorted(affected),
                "affected_endpoints": sorted(endpoints), "call_paths": paths}
    except Exception as e:
        print(f"[impact] MCP unavailable ({e!r}), falling back to local AST engine", file=sys.stderr)
        return compute_impact_local(old_ref, new_ref)
```

The exception message must print the **real** exception, not a canned string.
That is the difference between a genuine fallback and the one you had before.

**Parsing note:** LatentGraph MCP tools return fenced `toon` blocks — compact
tab-delimited JSON. Write one `parse_toon()` helper and reuse it. If toon
parsing eats more than 30 minutes, switch to `ask_codebase` with a targeted
question and parse the file-path citations out of the prose answer. That still
counts as consuming the graph.

Tools accept an optional `project_id`; set `LGRAPH_PROJECT_ID` if required.

## C.3 — `engine/judge.py`: real `get_pr_insights`

This is the one to prioritise if you only get one working.

```python
def load_rules(affected_files, verbose=False):
    rules = []
    for f in affected_files:
        try:
            insights = mcp_get_pr_insights(f)
            for inv in insights.get("invariants", []):
                rules.append({"id": inv.get("id") or f"INV-{len(rules)}",
                              "file": f, "text": inv["text"],
                              "source": inv.get("pr_source", "PR history"),
                              "severity": inv.get("severity", "medium")})
            for dec in insights.get("decisions", []):
                rules.append({"id": dec.get("id") or f"DEC-{len(rules)}",
                              "file": f, "text": dec["text"],
                              "source": dec.get("pr_source", "PR history"),
                              "severity": "medium"})
        except Exception as e:
            print(f"[judge] get_pr_insights unavailable for {f} ({e!r})", file=sys.stderr)
    if not rules:
        print("[judge] falling back to local decisions.json", file=sys.stderr)
        rules = load_decisions()
    return rules
```

The classification logic already works on a rule list — feed it this one and
nothing downstream changes.

**Demo payoff:** the rule shown on a red row would then be sourced from an
actual PR the graph mined, not a JSON file you wrote. That is a genuinely
different claim.

## C.4 — `engine/teach.py`: real `update_graph`

```python
def commit_proposal(proposal_text, affected_file):
    try:
        result = mcp_update_graph({"file": affected_file,
                                   "annotation": proposal_text,
                                   "type": "invariant"})
        edit_id = result.get("pending_edit_id")
        return "mcp_update_graph", f"Queued for owner approval — pending_edit_id: {edit_id}"
    except Exception as e:
        entry = f"- [{datetime.datetime.now().isoformat()}] {proposal_text}\n"
        PROPOSED_INVARIANTS_FILE.open("a", encoding="utf-8").write(entry)
        return "fallback_local_file", f"Appended to proposed_invariants.md (graph unavailable: {e!r})"
```

The receipt string must always describe what actually happened. Never a canned
message.

## C.5 — If MCP does not land in 2 hours

Stop cleanly. Delete anything that implies a live connection and make the
README section explicit — it already exists, just sharpen it:

> BlastProof is designed against LatentGraph's MCP surface
> (`get_dependencies`, `get_file`, `get_pr_insights`, `update_graph`). We were
> unable to complete key configuration within the hackathon window, so the
> shipped build runs the fallback path for all four: a local AST dependency
> engine and a local decisions corpus. Every integration point is isolated
> behind a single function in `impact.py`, `judge.py` and `teach.py`, so the
> swap is one implementation each.

Then say it out loud in the demo. **An honestly labelled gap scores better than
a stub someone discovers**, and "we designed to your API and shipped the
fallback" is a respectable engineering answer.

---

# PART D — TWO REAL BUGS (20 min)

## D.1 — `engine/judge.py` crashes when called standalone

Reproduced:
```
classify_drift(item, ["demo_app/core/interest.py"], decisions)
→ TypeError: argument of type 'NoneType' is not iterable
```

Line 46 evaluates `file in changed_files` where `changed_files` defaults to
`None`. `cli.py` always passes it, so the pipeline is safe — but
`python -m engine.judge` crashes whenever no rule keyword matches, and a judge
running the module directly will hit it.

**Fix — two lines:**

```python
# signature: default to empty list, not None
def classify_drift(item, affected_files, decisions, changed_files=None):
    changed_files = changed_files or []
    ...
    # line 46
    if match or file in changed_files:
```

Same in `judge_results`. Then re-run the reproduction above — it must return
`("unexplained", None)` instead of crashing.

## D.2 — `index.html` fabricates a receipt when the request fails

Lines 560 and 563 print
`"[RECEIPT] Appended invariant proposal for scenario X to proposed_invariants.md (graph unavailable: MCP tool not initialized)"`
in the **error** branches. That asserts a successful write for a call that
failed. Same class of defect as the `bp_938xf` literal you already removed.

**Fix:**

```javascript
} else {
    receipt.classList.add('receipt--error');
    receipt.innerText = `Could not record the invariant — server returned ${res.status}. Check the pipeline server is running.`;
}
} catch (err) {
    receipt.classList.add('receipt--error');
    receipt.innerText = `Could not reach the pipeline server. Start it with: python -m uvicorn ui.server:app --port 5500`;
}
```

The only place a success receipt may come from is `data.receipt` — the string
`teach.py` actually printed.

## D.3 — `explain.py` reports the hunk-start line (5 min, optional)

It says `interest.py:2`; the changed `return` is on line 5. It records the hunk
header's start line rather than counting to the changed line. In
`parse_git_diff`, track an offset as you walk the hunk body — increment for
context and `+` lines — and report `current_line + offset` at the first `-`/`+`
pair. Cosmetic, but a judge reading closely will spot it.

---

# PART E — THE UI REBUILD 🎨

The current page works but looks like a default dark dashboard. This section is
a complete design specification. **Follow it precisely** — do not substitute
your own palette or fonts.

## E.0 — Design direction

The subject is **instrumentation**: a measuring device that fires known signals
at two versions of a system and reports what moved. Not a SaaS dashboard, not a
terminal. The reference points are lab equipment and seismograph readouts —
precise, calm, mostly monochrome, with colour reserved for meaning.

**Three rules that carry the whole design:**

1. **Semantic colour is not decoration.** Red, amber, violet and green mean
   exactly one thing each (the four verdicts). The interface accent is a
   separate hue used only for things you can click. Never use a verdict colour
   on a button.
2. **Show what was NOT tested.** The radius panel lists excluded endpoints in
   muted strike-through alongside the included ones. This is the single most
   differentiating thing on screen — it proves the tool targeted rather than
   ran everything. No competitor's screenshot will have it.
3. **Group by cause, not by row.** 25 regressions from one root cause is one
   finding, not 25. The list is organised by cause; scenarios nest inside.

## E.1 — Colour tokens

Cool-neutral greys with a slight blue bias, so they read as chosen rather than
inherited. Define these on `:root` and use them everywhere — never a raw hex in
a component.

```css
:root {
  /* surfaces — light */
  --ground:       #EEF1F4;
  --surface:      #FFFFFF;
  --surface-sunk: #E4E8ED;
  --line:         #CFD6DE;
  --line-strong:  #A8B4C0;

  /* ink */
  --ink:          #10161D;
  --ink-muted:    #55636F;
  --ink-faint:    #8593A0;

  /* interface accent — interactive only, never a verdict */
  --accent:       #1F6F8B;
  --accent-hover: #185870;
  --accent-wash:  #E2EEF2;

  /* verdicts — meaning only, never decoration */
  --regression:      #B3261E;
  --regression-wash: #FBE9E7;
  --intentional:     #A15C00;
  --intentional-wash:#FBF0DF;
  --unexplained:     #5B4B8A;
  --unexplained-wash:#EDEAF5;
  --identical:       #1E7A4C;
  --identical-wash:  #E4F2EA;
}
```

**Note on `unexplained`:** the original plan used yellow next to amber, which is
nearly indistinguishable at a glance. Violet-slate is a distinct hue and reads
correctly as "a human needs to look at this" rather than "a milder warning."
This is a deliberate improvement — keep it.

Dark theme — redefine **only** the tokens, three times so all three viewer
states work:

```css
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground: #0E1218; --surface: #161C24; --surface-sunk: #10151C;
    --line: #26303B; --line-strong: #3A4756;
    --ink: #E6EBF0; --ink-muted: #98A6B4; --ink-faint: #6B7986;
    --accent: #4FA8C4; --accent-hover: #6FBED6; --accent-wash: #16303A;
    --regression: #F0776C; --regression-wash: #2E1614;
    --intentional: #DFA33F; --intentional-wash: #2C2113;
    --unexplained: #A695D8; --unexplained-wash: #201C2E;
    --identical: #4FBE87; --identical-wash: #12271C;
  }
}
:root[data-theme="dark"] { /* repeat the same block */ }
```

`body` must set `background: var(--ground)` explicitly.

## E.2 — Typography

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
```

- **Archivo** 600/700 — the wordmark, section headings, stat numbers. Set the
  wordmark at `letter-spacing: -0.02em`.
- **IBM Plex Sans** 400/500 — all prose: explanations, rule text, labels.
- **IBM Plex Mono** 400/500 — every machine value: file paths, dot-paths,
  endpoints, numbers, scenario ids, receipts. Always with
  `font-variant-numeric: tabular-nums`.

Do **not** use Inter or Space Grotesk.

Type scale — stay on it:
`11px` (uppercase labels, `letter-spacing: 0.08em`) · `13px` (secondary/meta) ·
`15px` (body) · `18px` (finding titles) · `28px` (stat numbers) ·
`22px` (wordmark).

Explanation prose gets `max-width: 68ch`.

## E.3 — Layout

A single centred column, `max-width: 1120px`, `padding: 0 32px`. Sibling groups
laid out with flex/grid and `gap` — never per-element margins.

### Header (sticky)

```
BLASTPROOF                    v1.0 → demo-change        [ Run BlastProof ]
2 endpoints in radius · 35 of 60 scenarios replayed
```

- Wordmark in Archivo 700, 22px, `--ink`.
- Refs in IBM Plex Mono 13px, `--ink-muted`, with a `→` between them.
- Second line 13px `--ink-muted` — it states the thesis before anything else.
- **Run button:** solid `--accent`, white text, 15px Plex Sans 500,
  `padding: 10px 20px`, `border-radius: 6px`. While running: replace the label
  with a 1.2s pulsing dot row and the current step from the CLI's `[n/6]`
  output. Respect `prefers-reduced-motion` — swap the pulse for a static
  "Running…".
- Sticky, `background: var(--surface)`, `border-bottom: 1px solid var(--line)`.

### Readout strip — four stat tiles

A `grid-template-columns: repeat(4, 1fr)` with `gap: 1px` on a `--line`
background, so the tiles read as one instrument panel rather than four floating
cards.

Each tile: `background: var(--surface)`, `padding: 20px 24px`.
- Number: Archivo 700, 28px, tabular-nums, in the verdict colour.
- Label: 11px uppercase, `letter-spacing: 0.08em`, `--ink-muted`.
- A 3px top stripe in the verdict colour.

`35 SCENARIOS` (ink) · `10 UNCHANGED` (identical) · `0 INTENTIONAL`
(intentional) · `25 REGRESSION` (regression).

A stat that is zero renders at 40% opacity — present but visibly inactive.

### Blast radius panel

```
BLAST RADIUS                                    demo_app/core/interest.py

  IN RADIUS      POST /api/emi        POST /api/payment
  EXCLUDED       GET /api/loan/{id}   GET /api/customer/{id}

  ↳ EMIService → calculate_emi_endpoint
  ↳ payment_service → calculate_payment_balance
```

- Two rows, each with an 11px uppercase label in `--ink-faint` on the left and
  endpoint chips on the right.
- **In-radius chips:** `--accent-wash` background, `--accent` text, 1px
  `--accent` border at 30% opacity, Plex Mono 13px, `border-radius: 4px`.
- **Excluded chips:** transparent background, `--ink-faint` text, dashed
  `--line` border, `text-decoration: line-through`,
  `text-decoration-thickness: 1px`.
- Call paths below in Plex Mono 13px `--ink-muted`, each prefixed `↳`.
- Excluded endpoints come from all routes in the app minus the radius. Expose
  the full route list in `report.json` (add `all_endpoints` to `radius`) so the
  UI does not hardcode them.

**Say this line in the demo while pointing at that row:** *"We didn't tell it
to skip customer and loan. The dependency graph did."*

### Findings — grouped by root cause

One group card per distinct explanation cause.

```
┌─ 4px left stripe in --regression ──────────────────────────┐
│ 🔴 REGRESSION                                    25 scenarios│
│ EMI and payment balances changed across all rate-dependent  │
│ endpoints                                                    │
│ demo_app/core/interest.py:5                                  │
│   (annual_rate / 12)  →  (annual_rate / 365)                │
│                                                              │
│ ⌐ VIOLATES D-17 · PR #4                                      │
│   "EMI must use monthly normalization (annual_rate / 12)     │
│    per lending convention"                                   │
│                                                              │
│ [ Show 25 scenarios ]   [ Confirm & Teach ]                  │
└──────────────────────────────────────────────────────────────┘
```

- Card: `background: var(--surface)`, `border: 1px solid var(--line)`,
  `border-left: 4px solid var(--regression)`, `border-radius: 8px`,
  `padding: 24px`.
- Verdict pill: uppercase 11px, verdict-wash background, verdict text colour.
- Count on the right, Plex Mono 13px `--ink-muted`.
- Code change: Plex Mono 15px. Old value `--regression` with
  `text-decoration: line-through`; new value `--ink`; a plain `→` between them
  in `--ink-faint`.
- **Rule block:** `--surface-sunk` background, 3px left border in
  `--unexplained`, rule text in Plex Sans *italic* 15px, `id · source` above it
  in 11px uppercase mono. It must read as a quotation from the team's own
  history, not as UI chrome.

**Scenario list** (collapsed by default). On expand, a table: scenario id
(mono), endpoint (mono, `--ink-muted`), `old → new` (mono, tabular-nums), and a
`View evidence` link per row. `max-height: 420px; overflow-y: auto` so 25 rows
never push the page.

**Evidence panel** — the thing you click when a judge asks "is this real?"
Two columns, `v1.0` and `demo-change`, raw JSON from `GET /api/results`, in
Plex Mono 12px on `--surface-sunk`. **Highlight the differing lines** with a
`--regression-wash` background. Ignored noise keys (`request_id`,
`generated_at`) rendered at 45% opacity with a small `ignored` tag — this shows
the comparator's judgement visually and is worth more than any explanation.

**Unchanged group** — one quiet card, no stripe:
`✓ 10 scenarios executed with identical behaviour` and a `Show all` toggle.

### Confirm & Teach

- Secondary style: transparent, 1px `--accent` border, `--accent` text.
- Click → label becomes `Recording…` → replace with the real receipt from
  `POST /api/teach`.
- Success receipt: Plex Mono 13px, `--identical-wash` background, 3px left
  border `--identical`, `padding: 10px 14px`, text exactly as `teach.py`
  returned it.
- Failure receipt: same shape, `--regression-wash` / `--regression`, saying
  what failed and how to fix it. **Never a canned success string.**

## E.4 — Empty and error states

- **No report yet:** centred, `--ink-muted`: "No analysis yet." plus a 15px
  line: "Run BlastProof to replay the affected scenarios across `v1.0` and
  `demo-change`." Do not render empty tiles.
- **Server unreachable:** "Can't reach the pipeline server." and the exact
  command in a mono block: `python -m uvicorn ui.server:app --port 5500`.
  Errors say what to do, never "something went wrong."

## E.5 — Craft checklist

- [ ] Every colour comes from a token. No raw hex in a component rule.
- [ ] No colour defined **only** inside a `@media` or `[data-theme]` block.
- [ ] `body` sets `background: var(--ground)` explicitly.
- [ ] Verdict colours never appear on a button; the accent never encodes state.
- [ ] All numeric columns use `font-variant-numeric: tabular-nums`.
- [ ] Visible `:focus-visible` outline on every interactive element.
- [ ] `@media (prefers-reduced-motion: reduce)` disables the pulse.
- [ ] Evidence panel and scenario table each have `overflow-x: auto`; the page
      body never scrolls sideways.
- [ ] Checked at 1920×1080 — that is what gets recorded.
- [ ] `<title>BlastProof Gate</title>`

---

# PART F — SKILLPATCH (10 min) 💰 ₹5,000 + $50 credits

Separate prize track, near-zero effort, and **currently unclaimed by either of
you.**

1. **Rotate the exposed key first.** The SkillPatch `sk_live_` key was pasted
   in chat before the hackathon started and has never been confirmed rotated.
   Go to SkillPatch Settings → regenerate → re-run setup. Do this before
   anything else touches the account.
2. Browse **skillpatch.dev** and install at least one skill each. Pick
   something that genuinely fits this project — a code-review, testing, or
   documentation skill — so you can say a true sentence about how it helped.
3. **Write down the exact skill name.** It has to be declared on the submission
   form.
4. Use it for something real, even small — running it over `engine/compare.py`
   or generating part of the README. One honest sentence about what it did is
   enough.

---

# PART G — SUBMISSION (Sunday, after the 14:00 freeze)

- [ ] Demo video, **2:00 or under**
- [ ] `/export` from **Saubhagya's** LatentCode session
- [ ] `/export` from **Mayank's** LatentCode session
- [ ] Google Drive folder with the video + both transcripts
- [ ] Sharing set to **"anyone with the link can view"**
- [ ] **Link opened in a private browser window to confirm** — an unshared
      folder is a silent disqualification
- [ ] Build-in-Public post published inside the window, tagging **@LatentForce**
- [ ] SkillPatch skill names for both members
- [ ] agentrouter API key deleted or regenerated (exposed in screenshots)
- [ ] Google Form submitted by the team leader **before 18:00 IST**

## The 90 seconds

1. Gate screen, no analysis yet.
2. Change one line live: `annual_rate / 12` → `annual_rate / 365`.
3. Click **Run BlastProof**. Radius appears — 2 endpoints in, **2 struck
   through**. *"We didn't tell it to skip customer and loan. The dependency
   graph did."*
4. Tiles fill: 35 scenarios, 10 unchanged, 25 regression.
5. Open the finding: cause line, old → new, and the violated rule with its PR.
6. **View evidence** — raw before/after, noise fields visibly greyed out.
   *"Every response has a different request id and timestamp. It ignored them."*
7. **Confirm & Teach** → real receipt.
8. *"Their graph told us where to look. We proved what changed. Their memory
   said it wasn't allowed. And what we confirmed goes back."*

**If the judge asks whether the classification is real:** delete D-17 from
`decisions.json` live and re-run. All 25 rows flip from regression to
unexplained. That is ten seconds and it settles the question.

**Framing discipline:** never "you don't have this" or "we found your gap."
Always *"we built on your public stack."* If they say they have something
internal: *"then we independently arrived at your roadmap using only your
public tools."*

---

# PRIORITY AND TIME

| # | Part | Time | Why |
|---|---|---|---|
| 1 | **A** — merge + delete `ui/index.html` | 15 min | Judges clone `main`; it is stale and holds the fabricated-receipt UI |
| 2 | **D** — judge crash + UI receipt | 20 min | One crashes, one asserts something false |
| 3 | **B** — verify the PRs | 10 min | The JUDGE story rests on them |
| 4 | **C** — MCP | 2 h cap | The entire differentiation claim |
| 5 | **E** — UI rebuild | 2–3 h | This is what the video films |
| 6 | **F** — SkillPatch | 10 min | ₹5,000, unclaimed |
| 7 | **G** — submission | 1.5 h | Non-negotiable |

≈ 7 hours against ~21 remaining.

**If time runs short, cut in this order:** C (take the honest README statement),
then E.4, then D.3. **Never cut A, D.1, D.2, F or G.**

## Rules

1. No hardcoded demo values in logic. No file names, line numbers, route
   strings, rule IDs or counts.
2. No comment claiming a capability the code lacks.
3. No fabricated receipt, id, or confirmation anywhere. Every string shown to a
   person must come from something that actually happened.
4. Every fallback logs the real reason it fired.
5. Never force-push. Never rewrite pushed history. Commit and push per part.
6. One LatentCode session in this repo at a time.
7. Report the **actual command output** for every part. "Verified" with no
   output is not verification.
