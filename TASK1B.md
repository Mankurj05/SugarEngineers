# TASK 1B — Close out replay.py (ENGINE_TASKS.md task 1)

Re-read PROJECT.md and CONTRACTS.md before starting.

Task 1 (engine/replay.py) is built and boots correctly, but was never
verified against real scenarios because scenarios/ is empty. Two small
changes, no new features, no scope beyond what is listed here.

## Change 1: fail fast on zero scenarios

Currently replay.py prints "Found 0 matching scenarios" and then boots
both servers anyway, finishing with "Both servers healthy" and writing
an empty results.json. A run that replays nothing must not look like a
successful run.

Required: if the tag-filtered scenario list is empty, print a clear
error naming the scenarios directory and the tags that were requested,
exit with a non-zero status code, and do NOT create worktrees or start
any server.

Also: the dummy-scenario fallback currently in replay.py must never
activate implicitly. Either remove it, or put it behind an explicit
--dummy flag that is off by default. A real run must never silently
replay fabricated scenarios.

## Change 2: create test scenarios for the stub

Read stub/app.py and use its ACTUAL routes and request models — do not
invent paths. Create three files in scenarios/ that exactly match the
scenario schema in CONTRACTS.md:

- two scenarios that exercise the stub's EMI route, tagged ["emi"],
  with different principal / annual_rate / months values
- one scenario that exercises a different stub route (or the same route
  with clearly different input), tagged ["other"]

The third scenario tagged "other" is deliberate: it is how we verify
the tag filter actually excludes non-matching scenarios.

Every file must have exactly the keys: id, method, path, body, tags.
No extra keys.

## Done when

    python -m engine.replay --old HEAD --new HEAD --tags emi --app stub.app:app

prints that 2 scenarios matched (not 3), both health checks pass, and
results.json contains a top-level JSON array of exactly 2 objects, each
shaped {"scenario": <id>, "old": {"status": ..., "json": {...}},
"new": {"status": ..., "json": {...}}} per CONTRACTS.md.

And:

    python -m engine.replay --old HEAD --new HEAD --tags nosuchtag --app stub.app:app

exits non-zero without starting any server.