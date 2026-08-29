# TASK — Fix scenario files to match CONTRACTS.md

Re-read PROJECT.md and CONTRACTS.md before starting.

main now has both lanes. The demo app is in demo_app/. The scenario files
in scenarios/ do NOT match the frozen contract, so engine/replay.py cannot
read any of them. Fix the generator and regenerate.

## The problem

Current generated files look like this — WRONG:

    {"id": "emi_1", "tag": "emi",
     "request": {"method": "POST", "endpoint": "/api/emi", "body": {...}},
     "expected_status": 200, "response": {...}}

CONTRACTS.md requires exactly this — five top-level keys, nothing else:

    {"id": "emi_1", "method": "POST", "path": "/api/emi",
     "body": {"principal": 10000, "annual_rate": 5.5, "tenure_months": 12},
     "tags": ["emi"]}

Differences: `tag` (string) must be `tags` (array). `method`, `path` and
`body` must be top level, not nested under `request`. `endpoint` is called
`path`. Drop `expected_status` and `response` entirely — BlastProof records
real responses at replay time, that is the entire point of the tool.

## Required changes

1. Read demo_app/main.py and demo_app/core/schemas.py first. Body field
   names in every scenario must match what the app's Pydantic models
   actually accept. Do not guess.
2. Rewrite scenarios/generate.py to emit the contract shape above.
3. Delete the orphan duplicate set scenarios/emi_001.json through
   scenarios/emi_020.json. They use `months` instead of the field the app
   expects and duplicate the emi_1..emi_20 set.
4. Regenerate all scenarios: 20 emi, 15 loan, 15 payment, 10 customer.
   Include edge cases in the emi set: 1-month tenure, 0% rate, and a very
   large principal.
5. Rewrite scenarios/manifest.json to group the regenerated IDs by tag.
6. Every scenario must hit a real endpoint that exists in demo_app/main.py
   with data that exists in demo_app/data/seed.json. A scenario that 404s
   is a broken scenario.

## Constraints

Do not change CONTRACTS.md. Do not change engine/replay.py or
engine/compare.py. The contract is frozen; the scenarios are what is wrong.

## Done when

All three pass.

1. Every file in scenarios/ except manifest.json and generate.py has
   exactly the keys id, method, path, body, tags — and tags is a list.
   Add a --validate flag to generate.py that checks this and exits
   non-zero on any violation.

2. Replay runs against the real app and matches the right count:

       python -m engine.replay --old HEAD --new HEAD --tags emi --app demo_app.main:app

   It must boot both servers, match 20 emi scenarios, and write 20 results.

3. Every one of those comes back identical despite the differing
   request_id and generated_at on every response:

       