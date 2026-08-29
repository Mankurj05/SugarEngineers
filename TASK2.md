# TASK 2 — engine/compare.py (ENGINE_TASKS.md task 2)

Re-read PROJECT.md and CONTRACTS.md before starting.

Build engine/compare.py: a semantic differ that reads results.json and
assigns each scenario a verdict of "identical" or "drift".

## Input

results.json, exactly the shape frozen in CONTRACTS.md:
a top-level JSON array of
{"scenario": "<id>", "old": {"status": int, "json": {...}},
                     "new": {"status": int, "json": {...}}}

If the real results.json does not match this, STOP and report it.
Do not adapt compare.py to a different shape — replay.py gets fixed
instead. The contract is frozen.

## Output

A JSON array, one object per scenario:
{"scenario": "<id>", "verdict": "identical" | "drift",
 "diffs": [{"path": "emi", "old": 14820.0, "new": 10718.4}]}

Key names and the diffs shape must match CONTRACTS.md exactly, because
later tasks (explain.py, judge.py) add "explanation" and "rule" keys to
these same objects to form report.json. Do not rename anything.

Verdicts here are ONLY "identical" or "drift". The values "regression",
"intentional" and "unexplained" belong to judge.py (task 6) and must
not appear in this module.

## Comparison rules, applied IN THIS ORDER

1. Status codes differ -> verdict "drift" immediately, no further
   comparison, no diffs walk.
2. Deep-walk both json objects together, key by key:
   a. Skip the key entirely if it is "request_id", "generated_at", or
      "trace_id"; or if its value matches a UUID pattern (8-4-4-4-12
      hex); or if its value matches an ISO timestamp pattern
      (YYYY-MM-DDTHH:MM:SS).
   b. Both values numeric -> equal if abs(old - new) < 0.01
   c. Both values strings -> strict equality
   d. Both values dicts -> recurse
   e. Both values lists -> element by element, same order; differing
      lengths is a drift
   f. Type mismatch -> drift
3. Record every mismatch as {"path", "old", "new"} using dot notation,
   including list indices: "schedule.0.interest"
4. Any mismatch -> "drift". No mismatches -> "identical".

## Constraints

No new dependencies. Standard library only for this module.
Keep it small and readable — this is the module judges are most likely
to actually open and read.

## Done when

Both of these pass.

1. Real data:
       python -m engine.compare --results results.json
   On a same-version replay every scenario returns "identical" with an
   empty diffs list. If any scenario shows drift, the ignore list is
   incomplete — fix it before continuing.

2. Self-proving fixtures. Create tests/fixtures_compare.json holding
   three hand-written old/new pairs, and a command that runs them:
       python -m engine.compare --selftest
   The three cases and their required results:
   - noise only: request_id and generated_at differ, every other value
     identical  ->  "identical", diffs empty
   - real drift: a numeric field differs (e.g. emi 14820.0 vs 10718.4)
     while request_id and generated_at ALSO differ  ->  "drift" with
     exactly one diff, path naming the numeric field only
   - float tolerance: a number differs by 0.005  ->  "identical"
   All three must pass and the command must exit non-zero if any fail.

The fixtures exist because the stub app may not emit noise fields. The
ignore list must be proven now, not assumed.