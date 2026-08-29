# BLASTPROOF — MASTER RECOVERY, VERIFICATION & COMPLETION TASK
## BuildSprint 2026 — LatentForce.ai
## Repository: `Mankurj05/SugarEngineers`

---

# 0. READ THIS FIRST

This document is NOT a suggestion list.

This is NOT a request to redesign the project from scratch.

This is NOT permission to declare existing work complete.

This is a recovery and verification specification.

Your job is to inspect the ACTUAL repository, determine what is REALLY implemented, repair what is broken, complete the missing pieces, verify the complete system, improve the UI, verify the LatentGraph MCP integration, and push the resulting work.

The biggest problem we have had during this project is not lack of code.

The biggest problem is false confidence.

Previous AI agents repeatedly declared things "100% complete" when they were not.

That must stop.

A README saying something works is NOT evidence.

A STATUS_TRACKER saying something works is NOT evidence.

A previous agent saying something works is NOT evidence.

A commit message saying something works is NOT evidence.

A function existing in a Python file is NOT evidence.

A mock response is NOT evidence.

A fallback implementation is NOT the same thing as the real integration.

A UI saying "Connected" is NOT evidence.

A generated receipt saying "Written to graph" is NOT evidence.

Only an independently verified execution path counts as implemented.

---

# 1. YOUR PRIMARY MISSION

Your mission is to bring the repository to a state where the following statement is TRUE:

> BlastProof takes a code change, determines the likely impact using LatentGraph where available, executes recorded scenarios against the old and new versions, performs a semantic behavioral comparison, explains meaningful behavioral drift, checks drift against recorded engineering decisions, and allows a human to explicitly confirm a proposed invariant/update.

The system must be honest about which parts use LatentGraph and which parts use local fallback logic.

If LatentGraph MCP is successfully connected:

USE IT.

If LatentGraph MCP cannot be connected:

DO NOT FAKE IT.

Use the documented fallback and expose the degraded mode clearly.

The final system must never pretend that a local AST analysis was a LatentGraph result.

---

# 2. PROJECT CONTEXT

Project name:

BlastProof

Team:

SugarEngineers

Repository:

`Mankurj05/SugarEngineers`

Primary working branch for Saubhagya:

`engine`

Primary integration branch:

`main`

There is also a branch:

`demo-change`

Do not assume branch contents are identical.

Verify them.

---

# 3. HACKATHON CONTEXT

Hackathon:

BuildSprint 2026 by LatentForce.ai

Duration:

48 hours

Start:

Friday 28 August 2026, 18:00 IST

End:

Sunday 30 August 2026, 18:00 IST

No grace period.

Allowed AI coding environment:

LatentCode

Do not introduce unauthorized AI coding tools into the development workflow.

---

# 4. JUDGING CRITERIA

Idea:

30%

Execution:

30%

Usefulness:

25%

Demo:

10%

Build in Public:

5%

There is also a separate SkillPatch prize.

This means the project cannot optimize only for code quantity.

The demo must be understandable.

The product must work.

The integration must be honest.

The project must demonstrate why it is useful to LatentForce.

---

# 5. THE CORE PRODUCT IDEA

BlastProof is a safety/verification layer for code changes.

The core question is:

> "I changed this code. What actually changed in the application's behavior, and was that change acceptable?"

The system should answer this with evidence.

The intended loop is:

1. IMPACT
2. EXECUTE
3. COMPARE
4. EXPLAIN
5. JUDGE
6. TEACH

---

# 6. THE CORE DIFFERENTIATOR

LatentGraph is intended to help understand code relationships.

BlastProof should NOT pretend to replace LatentGraph.

Instead:

LatentGraph answers:

> "What could this change affect?"

BlastProof answers:

> "What actually changed when we executed the affected behavior?"

Then BlastProof answers:

> "Was that behavioral change consistent with recorded engineering decisions?"

Then:

> "Should this verified knowledge be proposed back to the graph?"

The product relationship is therefore:

LATENTGRAPH = structural/contextual knowledge

BLASTPROOF = runtime behavioral evidence

---

# 7. IMPORTANT PRODUCT PRINCIPLE

Do NOT describe every behavioral difference as a bug.

A difference can be:

- intentional
- expected
- a regression
- unexplained
- environmental
- nondeterministic
- test noise

Therefore the system should use terminology such as:

"behavioral drift"

rather than automatically claiming:

"bug"

unless the evidence genuinely establishes a regression.

---

# 8. CURRENT REPOSITORY WARNING

The repository has already undergone several rounds of AI-generated implementation and cleanup.

Therefore:

DO NOT trust the current documentation blindly.

You must verify:

- source code
- imports
- function behavior
- CLI execution
- API execution
- scenario execution
- report generation
- UI behavior
- branch state
- Git history
- MCP configuration
- MCP authentication
- MCP tool invocation
- fallback behavior
- error handling

---

# 9. ABSOLUTE ANTI-HALLUCINATION RULE

Before changing anything:

INSPECT.

After changing anything:

RUN.

After running:

VERIFY OUTPUT.

After verifying:

DOCUMENT.

Never invert this order.

Do not write documentation first and then assume implementation follows it.

---

# 10. DO NOT TRUST STATUS DOCUMENTS

Files such as:

- STATUS_TRACKER.md
- task markdown files
- implementation notes
- handoff files
- README claims
- AI-generated completion reports

are useful as historical context only.

They are not proof.

If documentation says:

"MCP integrated"

you must inspect the code and actually invoke the MCP.

If documentation says:

"Teach writes to LatentGraph"

you must verify the write path.

If documentation says:

"Judge uses PR insights"

you must verify the actual runtime call.

---

# 11. FIRST TASK — FULL REPOSITORY AUDIT

Before writing significant code, inspect the complete repository.

Do NOT inspect only the first few files.

Do NOT rely on top-k search results.

Inspect the entire directory structure.

Inspect all relevant Markdown documentation.

Inspect all Python source.

Inspect configuration.

Inspect test files.

Inspect scenario data.

Inspect UI assets.

Inspect Git state.

---

# 12. REQUIRED REPOSITORY INVENTORY

Produce an internal inventory containing:

- every top-level directory
- every source file
- every test file
- every Markdown file
- every JSON data file
- every configuration file
- every HTML/CSS/JS file
- every requirements/dependency file
- every script
- every MCP-related configuration
- every generated artifact

Do not modify the repository during the inventory stage unless absolutely necessary.

---

# 13. BRANCH AUDIT

Inspect:

`main`

`engine`

`demo-change`

Determine:

- current HEAD
- latest commit
- divergence from main
- divergence from engine
- unmerged work
- stale branches
- files differing between branches

Do not assume main contains everything from engine.

Prove it.

---

# 14. GIT HISTORY AUDIT

Inspect recent commits.

Important existing commits include work described as:

- engine fixes
- UI fixes
- judge fixes
- explain fixes
- impact fixes
- documentation cleanup
- requirements changes

But again:

commit messages are historical evidence, not runtime evidence.

Verify the actual resulting files.

---

# 15. CURRENT KNOWN REPOSITORY STATE

Recent repository history indicates that the following work has been committed/merged:

- engine fixes
- UI rebuild
- judge fixes
- explanation fixes
- impact analysis fixes
- requirements updates
- documentation cleanup

This is encouraging.

It does NOT mean the system is finished.

---

# 16. KNOWN CRITICAL QUESTION

The most important unresolved area is:

LATENTGRAPH MCP INTEGRATION.

The previous project state indicated:

`lgraph` was installed.

However:

interactive authentication had not been successfully completed.

Therefore the system may still be using local AST fallback.

You MUST verify this yourself.

---

# 17. MCP DEFINITION OF DONE

MCP integration is complete ONLY if all of the following are true:

1. LatentGraph client/tooling is installed correctly.
2. Authentication is configured.
3. Authentication succeeds.
4. A real repository can be indexed or accessed.
5. A real LatentGraph query succeeds.
6. The application receives the actual MCP response.
7. The response is consumed by BlastProof.
8. The UI/report identifies that result as MCP-derived.
9. No mock response is being substituted.
10. Failure of MCP causes a controlled fallback.
11. Fallback mode is clearly identified.

---

# 18. MCP MUST NOT BE FAKED

Never write:

"LatentGraph connected"

unless a real tool invocation succeeded.

Never write:

"Graph updated"

unless the real write call succeeded.

Never create fake JSON that resembles a LatentGraph response and call it integration.

Never hardcode:

"9 files"

"4 endpoints"

"Decision #17"

or similar demo-specific graph results as though they came from MCP.

Demo data may exist.

It must be labeled demo/static data.

---

# 19. MCP TOOL AUDIT

Investigate the actual LatentGraph MCP capabilities available to the project.

Expected relevant concepts include tools such as:

- get_dependencies
- get_call_chain
- get_file
- get_pr_insights
- update_graph

Do not assume the exact schemas.

Inspect the installed/current tool definitions.

Use the actual schema.

---

# 20. MCP READ PATH

BlastProof's impact stage should conceptually do:

Changed code

↓

Identify changed file/function

↓

Ask LatentGraph

↓

Retrieve dependencies/call chain/relevant endpoints

↓

Construct predicted radius

↓

Use radius to select relevant scenarios

The important thing is not the exact implementation.

The important thing is that the data actually originates from LatentGraph when MCP is available.

---

# 21. MCP FALLBACK

Fallback is allowed.

Fallback is useful.

Fallback is not shameful.

Fake MCP is unacceptable.

If MCP fails:

Impact stage may use local AST/import/route analysis.

The report must say:

"Local fallback"

or an equally clear equivalent.

The UI must not visually imply that the graph produced the result.

---

# 22. MCP ERROR HANDLING

If authentication fails:

show a useful error.

If connection times out:

show a useful error.

If tool schema changes:

show a useful error.

If a tool returns malformed data:

show a useful error.

If LatentGraph is unavailable:

continue using fallback where safe.

Do not crash the entire application merely because MCP is unavailable.

---

# 23. MCP WRITE PATH

The Teach stage must be carefully designed.

It must NOT silently mutate the graph.

The intended workflow is:

Drift detected

↓

Evidence generated

↓

Proposed invariant generated

↓

Human reviews proposal

↓

Human clicks Confirm

↓

update_graph invoked

↓

actual result recorded

---

# 24. TEACH DEFINITION OF DONE

Teach is complete ONLY if:

- a proposal is generated from actual evidence
- the proposal is displayed
- human confirmation is required
- confirmation invokes the intended write path
- update_graph is actually called when MCP is live
- success is reported only after successful response
- failure is shown as failure
- no fake success receipt exists

---

# 25. TEACH FAILURE MODE

If `update_graph` fails:

DO NOT say:

"Successfully written to graph."

Instead show something equivalent to:

"Graph update was not completed."

Then include:

- error
- attempted action
- whether a local proposal was saved
- next action

---

# 26. CURRENT KNOWN TEACH RISK

Previous implementation history indicated that Teach had previously produced local proposals/receipts rather than proving a real graph write.

Therefore this must be explicitly tested.

Do not assume the latest fix solved it.

---

# 27. JUDGE STAGE

The Judge stage determines whether behavioral drift conflicts with recorded engineering decisions.

Potential categories:

- regression
- intentional
- unexplained

Do not hardcode a specific decision number.

Do not hardcode a specific rule.

Do not assume a decision exists.

---

# 28. PR INSIGHTS

If LatentGraph's `get_pr_insights` is available and intended for this purpose:

use the real tool.

Retrieve the relevant decisions.

Match the behavioral drift against them.

If MCP is unavailable:

fallback may use repository-local decision data.

But the report must identify the source.

---

# 29. NO FAKE PR CLAIMS

Never say:

"violates PR #42"

unless PR #42 actually exists and contains the relevant decision.

The repository history must support the claim.

If a local `decisions.json` says PR #42:

that is not enough by itself.

Verify the source where possible.

---

# 30. EXISTING PR CHECK

The repository history already contains evidence of a merged PR concerning:

customer endpoint independence from interest calculations.

Verify actual PR metadata and description.

Do not merely trust the commit title.

---

# 31. DECISIONS DATA

Inspect:

`decisions.json`

and all related decision/invariant files.

Determine:

- format
- provenance
- rule text
- PR references
- whether rules are manually authored
- whether rules are mined
- whether rules are from LatentGraph
- whether rules are static demo fixtures

Document this clearly.

---

# 32. IMPACT ENGINE

Inspect:

`engine/impact.py`

and:

`engine/impact_local.py`

Determine exactly:

- how changed files are identified
- how changed functions are identified
- how dependencies are found
- how endpoints are found
- how local fallback works
- whether MCP is actually invoked
- how errors are handled

---

# 33. IMPACT MUST BE DYNAMIC

Do not hardcode:

- routes
- endpoint names
- affected files
- dependency counts
- customer endpoint
- EMI endpoint

The demo may produce these values.

The code should derive them.

---

# 34. EXECUTION ENGINE

Inspect:

`engine/replay.py`

Determine:

- how scenarios are loaded
- how requests are constructed
- how the old application starts
- how the new application starts
- whether ports are isolated
- how processes are cleaned up
- how failures are represented
- whether requests actually execute

---

# 35. OLD VS NEW

BlastProof must compare:

OLD

against

NEW

The old version should come from a reproducible baseline.

The new version should represent the changed code.

Do not simply run the same application twice.

If both processes point at the same source tree, the comparison is invalid.

---

# 36. REPRODUCIBLE BASELINE

The demo should use a reproducible baseline such as:

- Git tag
- commit
- copied source tree
- temporary worktree

The chosen mechanism must be documented.

The critical property:

OLD and NEW must actually differ when the demo regression exists.

---

# 37. SCENARIO FORMAT

Inspect:

`scenario.json`

and related files.

Verify the actual schema.

Scenarios should represent deterministic, safe, repeatable application behavior.

Do not use real customer information.

Do not use real banking credentials.

Do not make real financial transactions.

---

# 38. RECORDED SCENARIOS

Use the phrase:

"recorded scenarios"

rather than:

"real traffic"

unless the system genuinely captures real traffic.

The hackathon demo should use synthetic/prepared scenarios.

---

# 39. SCENARIO SELECTION

Impact analysis should ideally reduce the number of scenarios executed.

Example:

60 total scenarios

↓

4 affected endpoints

↓

replay relevant subset

The numbers must be derived from actual data.

Do not fake them.

---

# 40. COMPARISON ENGINE

Inspect:

`engine/compare.py`

Verify:

- status code comparison
- response body comparison
- headers where relevant
- JSON normalization
- ignored noise
- meaningful business-field differences
- missing fields
- added fields
- removed fields

---

# 41. SEMANTIC COMPARISON

A raw string diff is insufficient.

For example:

OLD:

`{"amount":100,"request_id":"abc"}`

NEW:

`{"amount":100,"request_id":"xyz"}`

This should not necessarily be classified as meaningful drift.

But:

OLD:

`{"emi":14820}`

NEW:

`{"emi":10718}`

is meaningful.

---

# 42. NOISE FILTERING

Inspect exactly which fields are ignored.

Potential examples:

- UUIDs
- timestamps
- request IDs
- trace IDs
- generated tokens

Do not blindly ignore arbitrary fields.

A field should only be ignored when it is known to be nondeterministic and irrelevant to business behavior.

---

# 43. DANGEROUS NOISE FILTER BUG

Never ignore a field simply because it changed.

If:

`amount`

changes,

that is potentially meaningful.

If:

`status`

changes,

that is potentially meaningful.

If:

`emi`

changes,

that is definitely important for the banking demo.

---

# 44. EXPLANATION ENGINE

Inspect:

`engine/explain.py`

Verify that explanations derive from actual evidence.

The explanation should identify:

- scenario
- endpoint
- meaningful field
- old value
- new value
- changed source location if available

---

# 45. LINE NUMBER INTEGRITY

Line numbers are dangerous.

Do not generate:

"line 42"

unless line 42 actually corresponds to the relevant change.

Verify line calculations against the actual Git diff.

Previous implementation work specifically addressed explanation line calculation.

Retest it.

---

# 46. ROOT CAUSE

Root-cause explanation should be evidence-based.

Bad:

"Your interest calculation caused this."

Good:

"Scenario `/calculate-emi` returned `14820` before the change and `10718` after the change; the changed expression is in `interest.py:42`."

Even better:

"Behavioral drift in EMI output is associated with the changed normalization expression at `interest.py:42`; recorded decision X requires monthly normalization."

---

# 47. JUDGE LOGIC

Judge must not simply search for the word:

"EMI"

and conclude that a rule was violated.

Inspect the actual rule.

Determine relevance.

Explain why the drift matches the rule.

---

# 48. INTENTIONAL CHANGE

The system must allow an intentional change to be recognized as intentional if evidence supports it.

Do not label every difference as regression.

The UI should distinguish:

REGRESSION

INTENTIONAL

UNEXPLAINED

---

# 49. UNKNOWN DRIFT

If a behavioral change has no corresponding recorded decision:

show:

"Unexplained behavioral drift"

or equivalent.

Do not invent a rule.

Do not invent a decision.

---

# 50. REPORT CONTRACT

Inspect:

`results.json`

and:

`report.json`

Verify the actual schemas.

Ensure every stage produces compatible data.

Do not allow one stage to silently produce a schema different from what the next stage expects.

---

# 51. CONTRACTS.MD

Inspect:

`CONTRACTS.md`

carefully.

Treat it as a specification, not proof.

Cross-check every contract against the actual implementation.

Identify:

- fields that exist in docs but not code
- fields in code but not docs
- fields with inconsistent names
- nullable fields
- fallback indicators
- error structures

---

# 52. CLI

Inspect:

`engine/cli.py`

The CLI should provide a reliable end-to-end pipeline.

Expected conceptual pipeline:

impact

→ replay

→ compare

→ explain

→ judge

→ report

→ teach proposal

The exact ordering may differ if technically necessary.

---

# 53. CLI DEFINITION OF DONE

Run it from a clean environment.

Run it from the repository root.

Run it using documented commands.

It must:

- start
- execute
- produce output
- produce report
- exit cleanly
- report failures accurately

---

# 54. NO MANUAL MAGIC

If the pipeline requires:

"first run this hidden command"

then:

"edit this file manually"

then:

"copy this JSON"

then:

"refresh the browser"

the product is not truly end-to-end.

Reduce manual steps.

Document unavoidable setup.

---

# 55. API SERVER

Inspect:

`ui/server.py`

Verify:

- `/`
- `/api/report`
- `/api/run`
- `/api/teach`

or whatever endpoints currently exist.

Do not assume those endpoints are correct merely because they exist.

---

# 56. API ERROR HANDLING

Every API failure must return an honest error.

Never return:

HTTP 200

with:

`success: true`

when the underlying operation failed.

---

# 57. TEACH API

Especially test:

`/api/teach`

Cases:

1. successful local proposal
2. MCP unavailable
3. MCP update succeeds
4. MCP update fails
5. malformed report
6. missing report
7. repeated confirmation
8. empty proposal

---

# 58. UI REQUIREMENT

The UI is NOT a generic dashboard.

Do not create:

15 charts.

Do not create:

random metrics cards.

Do not create:

fake enterprise analytics.

The UI should make the central story obvious within seconds.

---

# 59. IDEAL UI FLOW

Screen should communicate:

WHAT CHANGED?

↓

WHAT COULD IT AFFECT?

↓

WHAT ACTUALLY CHANGED?

↓

WAS IT ALLOWED?

↓

WHAT SHOULD WE REMEMBER?

---

# 60. PRIMARY UI SCREEN

Recommended hierarchy:

1. Change summary
2. Impact radius
3. Verification status
4. Green/red scenario wall
5. Drift detail
6. Decision verdict
7. Evidence
8. Teach action

---

# 61. TOP-LEVEL STATUS

Show something like:

"BlastProof Verification"

with a concise status:

SAFE

DRIFT DETECTED

REGRESSION FOUND

UNEXPLAINED DRIFT

Do not use ambiguous generic status.

---

# 62. IMPACT CARD

Display:

Changed file(s)

Predicted affected files

Predicted endpoints

Scenario count

Source:

LatentGraph

or:

Local AST fallback

The source must be explicit.

---

# 63. EXECUTION CARD

Show:

OLD VERSION

NEW VERSION

Scenarios executed

Scenarios skipped

Execution duration

Failures

---

# 64. GREEN/RED WALL

This is the visual centerpiece.

Example:

57 PASS

3 DRIFT

The user should immediately understand:

most behavior stayed stable

a few behaviors changed

---

# 65. RED ROW

Each red row should contain:

Scenario

Endpoint

Changed field

Old value

New value

Verdict

Source location

Decision result

---

# 66. DRIFT DETAIL

Clicking a red row should reveal:

request

old response

new response

semantic diff

changed source

decision evidence

final verdict

---

# 67. RAW EVIDENCE

Keep raw response evidence accessible.

Do not hide all technical evidence behind an LLM summary.

A judge should be able to see:

"Here is the actual before response."

"Here is the actual after response."

---

# 68. LLM EXPLANATION

LLM explanation is optional enhancement.

It should NOT be the source of truth.

Source of truth:

actual execution.

LLM role:

summarize evidence.

---

# 69. LLM HALLUCINATION CONTROL

Never let the LLM invent:

- line numbers
- values
- endpoints
- PR numbers
- decisions
- execution results

Provide evidence as structured input.

Require explanations to reference only provided evidence.

---

# 70. DEMO REGRESSION

The demo needs a deliberate regression.

The proposed example is:

change interest normalization from:

`rate / 12`

to:

`rate / 365`

or an equivalent controlled behavioral regression.

Do not blindly use this exact change if it does not make sense in the actual demo app.

Verify the resulting output.

---

# 71. DEMO APPLICATION

The demo application should be:

small

deterministic

banking-style

safe

local

easy to start

easy to reset

The purpose is not to build a bank.

The purpose is to demonstrate behavioral verification.

---

# 72. DEMO ENDPOINTS

Potential endpoints:

- EMI calculation
- customer lookup
- account summary
- statement
- payment/reconciliation simulation

Only include endpoints actually implemented.

---

# 73. NO REAL FINANCIAL ACTIONS

Never call real banking APIs.

Never send real money.

Never use real customer information.

Never expose credentials.

Everything must be synthetic/local.

---

# 74. DECISION SEEDING

The demo needs at least one meaningful engineering decision.

Example conceptual rule:

"EMI calculations must use monthly normalization."

But the exact rule should be stored in the repository and associated with an actual source.

Do not merely print this sentence in the UI.

---

# 75. DECISION PROVENANCE

A decision should have:

- ID
- source
- text
- affected area
- provenance

Possible provenance:

PR

commit

LatentGraph

local fixture

The UI should make this clear.

---

# 76. TEACH PROPOSAL

When a new meaningful behavioral invariant is discovered:

show:

"Proposed invariant"

Then show:

"Why?"

with evidence.

Then:

Confirm

Cancel

---

# 77. HUMAN CONTROL

Teach MUST require explicit human confirmation.

Never automatically mutate the graph during a normal verification run.

This is both safer and more defensible.

---

# 78. GRAPH UPDATE RECEIPT

After confirmation, receipt must state exactly what happened.

Possible states:

"Proposed locally"

"Submitted to LatentGraph"

"Successfully updated LatentGraph"

"Update failed"

These are different states.

Do not collapse them.

---

# 79. FALLBACK RECEIPT

If MCP is unavailable:

"LatentGraph unavailable. Proposal saved locally. No remote graph mutation occurred."

That is honest.

---

# 80. SUCCESS RECEIPT

Only after an actual successful MCP response:

"LatentGraph updated successfully."

Include whatever safe identifier the tool actually returns.

Do not fabricate one.

---

# 81. TESTING REQUIREMENTS

Create/verify tests for:

impact

replay

comparison

explanation

judge

teach

CLI

API

MCP adapter

fallback

---

# 82. UNIT TESTS

At minimum:

comparison of identical responses

comparison with timestamp differences

comparison with UUID differences

meaningful numeric drift

missing field

added field

changed status

execution failure

malformed scenario

---

# 83. IMPACT TESTS

Test:

changed function

changed imported module

changed route handler

unrelated file

missing file

unsupported syntax

MCP unavailable

MCP available

---

# 84. JUDGE TESTS

Test:

matching decision

nonmatching decision

no decision

multiple decisions

invalid decision

MCP decision source

local fallback decision source

---

# 85. TEACH TESTS

Test:

proposal generated

human confirmation

MCP success

MCP failure

fallback

duplicate proposal

empty report

---

# 86. E2E TEST

A complete E2E test must perform:

1. baseline setup
2. new version setup
3. scenario execution
4. comparison
5. drift detection
6. explanation
7. judge
8. report generation
9. teach proposal
10. confirmation
11. receipt

---

# 87. E2E MUST BE FRESH

Do not reuse an old `report.json` and call the pipeline successful.

Delete generated artifacts.

Run from scratch.

Generate a new report.

Inspect timestamps/content.

---

# 88. STALE ARTIFACT CHECK

Look for:

- old report.json
- old results.json
- old receipts
- old screenshots
- old demo outputs
- temporary JSON
- duplicate UI
- obsolete HTML
- scratch scripts

Determine whether each is:

required

generated

ignored

obsolete

---

# 89. GENERATED FILE POLICY

Generated files should not masquerade as source-of-truth.

If generated artifacts are committed for demo purposes:

label them clearly.

---

# 90. UI DUPLICATION

Previous work reportedly removed a redundant UI file.

Verify that only the intended UI entrypoint remains.

Search for:

`index.html`

across the repository.

Do not assume the duplicate is gone.

---

# 91. README

README must accurately describe:

- what BlastProof is
- architecture
- setup
- execution
- MCP integration
- fallback
- limitations
- demo
- testing
- known limitations

---

# 92. README MCP LANGUAGE

If MCP is live:

say so.

If MCP is not live:

say so.

Do not use vague language like:

"integrated architecture"

if the actual runtime is fallback-only.

---

# 93. README DEMO CLAIMS

Every impressive claim must be reproducible.

If README says:

"60 scenarios"

there should actually be 60.

If README says:

"LatentGraph predicts"

the demo should actually invoke it.

---

# 94. DOCUMENTATION CLEANUP

The repository has recently moved scratch Markdown files into `docs/`.

Inspect the docs folder.

Do not delete historical documentation blindly.

But separate:

- authoritative documentation
- historical notes
- temporary AI instructions
- stale plans
- completed tasks

---

# 95. LONG MARKDOWN FILES

Some project Markdown files may contain hundreds of lines.

Read them.

Do not skim only headings.

Do not conclude:

"Task appears completed"

because the first section says so.

Trace each checklist item to actual code.

---

# 96. TASK STATUS METHOD

For every task in every relevant Markdown file:

classify:

DONE — verified by execution

PARTIAL — implementation exists but not fully verified

BROKEN — exists but fails

STALE — documentation no longer matches implementation

NOT STARTED

BLOCKED

Do not use:

"probably done."

---

# 97. PREVIOUS AI CLAIMS

Previous AI agents have overestimated completion.

Known historical problems included:

- stale main
- duplicate UI files
- standalone judge crash
- fabricated success receipt
- wrong explanation line numbers
- unverified PR claims
- repository clutter

Some commits appear to address these.

You MUST retest them.

---

# 98. STALE MAIN PROBLEM

Run Git comparison.

Determine whether:

`main`

contains current engine changes.

Do not rely on commit messages.

---

# 99. ENGINE BRANCH

Saubhagya's working branch is:

`engine`

Do not destroy it.

Do not force-push it.

Do not rewrite history unnecessarily.

Do not reset it destructively.

---

# 100. MAIN BRANCH

Main is the integration branch.

Any completed work intended for final submission should eventually be present on main.

Before merging:

test.

After merging:

test again.

---

# 101. PUSH REQUIREMENT

After completing the requested fixes:

commit them.

Push them to the appropriate branch.

Do not stop at:

"changes are ready."

The repository must actually contain them.

---

# 102. COMMIT HYGIENE

Use meaningful commit messages.

Examples:

`fix: make MCP status truthful`

`fix: prevent false teach success`

`test: add end-to-end blastproof verification`

`feat: wire LatentGraph MCP impact adapter`

Avoid:

`final final`

`working`

`AI fixes`

`done`

---

# 103. DO NOT DESTROY USER WORK

Before modifying files:

inspect Git status.

Preserve existing valid work.

Do not overwrite teammate work simply because another approach looks cleaner.

---

# 104. TEAM CONTEXT

Two people are working on the project.

Saubhagya:

engine lane

branch:

`engine`

Friend/teammate:

demo-app/scenarios/UI lane

branch:

`app` was the intended workflow historically.

Verify actual branch names before acting.

---

# 105. MERGE SAFETY

If work already exists in main:

do not recreate it unnecessarily.

If engine has additional fixes:

determine whether they are already merged.

Use commit comparison.

---

# 106. FINAL ARCHITECTURE

Target conceptual architecture:

Developer change

↓

BlastProof

↓

Impact Adapter

↓

LatentGraph MCP

or

Local fallback

↓

Scenario Selector

↓

OLD runner + NEW runner

↓

Semantic Comparator

↓

Evidence

↓

Explanation

↓

Decision Judge

↓

Report

↓

Human confirmation

↓

Teach adapter

↓

LatentGraph update_graph

---

# 107. SEPARATION OF CONCERNS

Keep these components separate.

Impact:

"What might be affected?"

Replay:

"Execute scenarios."

Compare:

"What differed?"

Explain:

"Explain evidence."

Judge:

"Does it conflict with known decisions?"

Teach:

"What knowledge should be proposed?"

Do not put the entire application in one script.

---

# 108. MCP ADAPTER

Prefer an isolated MCP integration module.

The rest of the application should not depend directly on MCP-specific implementation details.

For example conceptually:

`engine/mcp_client.py`

or equivalent.

Do not blindly create that exact filename if architecture already has a better adapter.

---

# 109. MCP RESULT NORMALIZATION

Normalize MCP responses into BlastProof's internal schema.

Do not leak raw MCP structures everywhere.

This protects the project from API changes.

---

# 110. MCP SOURCE FIELD

Internal impact data should carry something like:

`source = "latentgraph"`

or:

`source = "local_fallback"`

This must propagate into reports/UI.

---

# 111. FALLBACK FIELD

Never infer fallback merely because an error happened.

Explicitly record it.

Example:

`integration_mode: "fallback"`

---

# 112. ERROR PROVENANCE

When fallback occurs, preserve why.

Example:

`fallback_reason: "LatentGraph authentication unavailable"`

Do not hide this.

---

# 113. SECURITY

Never commit:

API keys

tokens

credentials

browser session data

`.env` secrets

personal access tokens

MCP authentication cookies

---

# 114. ENVIRONMENT VARIABLES

Use environment variables for secrets.

Provide:

`.env.example`

if needed.

Never provide a real secret in the example.

---

# 115. GITIGNORE

Inspect `.gitignore`.

Ensure secrets and local generated files are ignored.

---

# 116. MCP AUTH

Determine exactly how LatentGraph authentication works.

Do not invent environment variables.

Inspect official/current tooling documentation if available.

---

# 117. AUTH FAILURE

If authentication requires interactive browser setup and the hackathon environment prevents it:

do not waste unlimited hours.

Implement a clean adapter.

Use fallback.

Document the limitation.

But if authentication is actually available:

finish the integration.

---

# 118. MCP DEMO VALUE

If live MCP works, use it in the demo.

This is important because the project is specifically for LatentForce.

A generic runtime testing tool without LatentForce integration is significantly weaker.

---

# 119. IF MCP WORKS

The demo should visibly show:

"LatentGraph impact analysis"

then:

"BlastProof behavioral verification"

This makes the division of value obvious.

---

# 120. IF MCP DOES NOT WORK

Do not pretend.

Demo:

"LatentGraph adapter unavailable in this environment."

Then:

"BlastProof falls back to local structural analysis."

This is better than lying.

---

# 121. PRODUCT POSITIONING

Do NOT pitch BlastProof as:

"another AI coding assistant."

It is not.

Do NOT pitch it as:

"another dependency graph."

It is not.

Do NOT pitch it as:

"another test runner."

That misses the integration.

Pitch:

"behavioral proof for code changes."

---

# 122. ONE-SENTENCE PITCH

Preferred:

> BlastProof verifies whether a code change actually changed application behavior, traces the drift to its source, checks it against engineering decisions, and lets teams feed confirmed knowledge back into their code graph.

---

# 123. SHORTER PITCH

> LatentGraph tells us what might be affected. BlastProof runs the affected behavior and proves what actually changed.

---

# 124. DEMO PITCH

> We changed one line in an interest calculation. BlastProof identified the affected behavior, replayed the scenarios against old and new versions, caught the EMI drift, traced it to the changed line, checked the team's recorded rule, and asked for confirmation before teaching the result back to the graph.

---

# 125. DO NOT SAY

"AI guarantees your code is correct."

That is false.

---

# 126. DO NOT SAY

"We test every possible behavior."

That is false.

Recorded scenarios cover only what they cover.

---

# 127. DO NOT SAY

"We prove there are no bugs."

That is false.

---

# 128. SAY

"We provide evidence of behavioral drift across the scenarios we executed."

That is defensible.

---

# 129. DEMO LIMITATION

The demo uses a prepared scenario set.

Say this if asked.

That is not a weakness.

It is a controlled experiment.

---

# 130. DEMO EXPERIMENT

The strongest demonstration is:

baseline

↓

controlled change

↓

verification

↓

observable drift

↓

evidence

↓

decision

↓

human confirmation

---

# 131. DEMO TIMING

Target:

60–120 seconds.

Do not explain architecture for 90 seconds while the product sits idle.

---

# 132. DEMO ORDER

1. Show code change.
2. Run BlastProof.
3. Show impact.
4. Show execution.
5. Show green/red wall.
6. Click red drift.
7. Show evidence.
8. Show decision violation.
9. Confirm Teach.
10. Show receipt.

---

# 133. DEMO KILL SHOT

The strongest moment is not:

"Look at our dashboard."

It is:

"This output was 14,820 before the change."

"After the change it became 10,718."

"Here is the exact changed line."

"Here is the engineering decision."

"Here is the evidence."

---

# 134. UI POLISH

After correctness:

fix:

spacing

typography

alignment

responsive layout

loading states

error states

empty states

hover states

button hierarchy

visual hierarchy

---

# 135. DO NOT OVERDESIGN

The UI should feel like a developer safety tool.

Not:

crypto dashboard

gaming dashboard

generic SaaS template

AI chatbot

---

# 136. COLOR SEMANTICS

Use color consistently.

Green:

verified/stable

Red:

behavioral drift/regression

Orange:

unexplained/review

Neutral:

metadata

Do not rely on color alone.

---

# 137. ACCESSIBILITY

Status should include text/icon, not only color.

A user should be able to understand:

PASS

DRIFT

REGRESSION

without color perception.

---

# 138. LOADING STATE

When verification is running:

show actual stage:

Impact analysis

Selecting scenarios

Starting baseline

Starting new version

Replaying

Comparing

Judging

Generating report

---

# 139. LIVE PROGRESS

If practical, stream progress.

But do not spend hours building streaming infrastructure.

A truthful stage indicator is enough.

---

# 140. FAILURE STATE

If a scenario crashes:

show:

scenario

request

old/new side

error

continue/abort behavior

Do not classify infrastructure failure as behavioral regression.

---

# 141. IMPORTANT DISTINCTION

These are different:

Application response differs.

Application crashes.

Scenario could not execute.

Infrastructure failed.

MCP failed.

Do not mix them.

---

# 142. REPORT MODEL

Report should distinguish:

verified_same

behavioral_drift

execution_failure

infrastructure_failure

integration_failure

---

# 143. COVERAGE

If report shows coverage:

define exactly what coverage means.

Example:

"42/60 scenarios executed"

not:

"70% code coverage"

unless actual code coverage was measured.

---

# 144. IMPACT COVERAGE

Potential metric:

affected scenarios / total scenarios

This is understandable.

Do not invent percentages.

---

# 145. VERIFICATION SUMMARY

A useful report might show:

Total scenarios

Executed

Stable

Drifted

Failed

Skipped

---

# 146. SOURCE TRACE

For each meaningful drift:

scenario

→ endpoint

→ response field

→ changed source line

→ decision

This chain is the product's core evidence.

---

# 147. EVIDENCE CHAIN

Every conclusion should be traceable.

If the UI says:

"Regression"

there should be evidence supporting it.

---

# 148. NO BLACK BOX

Do not build a system where the LLM says:

"This is bad."

and that is the entire explanation.

---

# 149. LLM ROLE

LLM may assist:

classification

summarization

natural-language explanation

But deterministic evidence should drive:

execution

comparison

values

line locations

scenario identity

---

# 150. DETERMINISTIC CORE

The strongest architecture is:

deterministic evidence

+

AI interpretation

not:

AI-generated evidence

---

# 151. COMPARISON ALGORITHM

Prefer structured JSON comparison when possible.

Normalize:

objects

arrays where appropriate

known noise

numeric formats

nulls

---

# 152. ARRAY COMPARISON

Do not blindly sort arrays.

Order can be meaningful.

Only normalize order where the API contract says order is irrelevant.

---

# 153. NUMERIC COMPARISON

Do not blindly round all numbers.

Financial values require exact or domain-appropriate comparison.

---

# 154. FINANCIAL VALUES

For money:

prefer decimal-safe representations.

Do not use binary floating point carelessly for financial calculations.

---

# 155. DEMO DATA

Use realistic-looking synthetic values.

Do not use actual personal data.

---

# 156. SCENARIO RESET

Ensure scenarios do not contaminate each other.

If stateful:

reset database/state.

If stateless:

document it.

---

# 157. PROCESS CLEANUP

After each run:

terminate child processes.

release ports.

remove temporary files.

Do not leave zombie servers.

---

# 158. PORT MANAGEMENT

Avoid hardcoded ports if they cause conflicts.

If ports are fixed for simplicity:

check availability and fail cleanly.

---

# 159. TIMEOUTS

Every network/process operation needs a timeout.

Do not let the demo hang indefinitely.

---

# 160. RETRIES

Use retries carefully.

Do not retry application behavior in a way that changes semantics.

---

# 161. IDEMPOTENCY

Recorded scenarios should be safe to replay.

Especially important for any simulated payment/reconciliation behavior.

---

# 162. DATABASE

If the demo uses a database:

determine:

SQLite?

in-memory?

fixture?

Ensure reproducibility.

---

# 163. OLD DATABASE

Old and new versions should operate on equivalent initial state.

Otherwise differences may be caused by state rather than code.

---

# 164. NEW DATABASE

Same principle.

Reset to equivalent state.

---

# 165. ENVIRONMENT PARITY

Old and new versions should run with equivalent:

environment variables

database state

configuration

dependencies

scenario inputs

---

# 166. DEPENDENCY PARITY

Do not accidentally compare different dependency versions unless that is intentionally part of the test.

---

# 167. PYTHON ENVIRONMENT

Inspect:

`requirements.txt`

Ensure dependencies are sufficient.

No unused massive dependency pile unless justified.

---

# 168. STARTUP COMMAND

Document one reliable startup command.

Example conceptually:

`python -m ui.server`

or equivalent actual command.

Do not invent commands.

---

# 169. PIPELINE COMMAND

Document one reliable verification command.

Example conceptually:

`python -m engine.cli`

Use the actual command supported by the repository.

---

# 170. CLEAN CHECKOUT TEST

The final verification should ideally be performed from:

clean checkout

fresh environment

installed dependencies

documented setup

---

# 171. WINDOWS COMPATIBILITY

The primary development environment appears to be Windows/VS Code.

Test commands under Windows where possible.

Avoid Unix-only shell assumptions.

---

# 172. PATH HANDLING

Use Python/pathlib rather than fragile string concatenation.

---

# 173. SUBPROCESS HANDLING

Ensure subprocess commands work cross-platform.

Do not assume:

`bash`

exists.

---

# 174. FILE ENCODING

Use UTF-8.

Do not introduce encoding-dependent output.

---

# 175. LOGGING

Provide useful logs.

Avoid giant debug dumps in the UI.

---

# 176. DEBUG MODE

If debug mode exists:

make it explicit.

Do not show internal stack traces to judges by default.

---

# 177. ERROR RECEIPTS

Receipts should include:

operation

status

source

message

timestamp if useful

No secrets.

---

# 178. REPORT REPRODUCIBILITY

A report should be reproducible from the same:

old version

new version

scenario set

environment

configuration

---

# 179. REPORT TIMESTAMP

Useful but not sufficient.

A timestamp does not prove freshness.

---

# 180. REPORT VERSION

Include schema/version information if useful.

---

# 181. CONTRACT VALIDATION

Add schema validation where practical.

A broken stage should fail early.

---

# 182. MISSING FIELDS

Do not silently treat missing fields as:

empty string

zero

false

unless the schema says so.

---

# 183. NULL VS EMPTY

Distinguish:

null

empty list

empty string

missing field

---

# 184. UI EMPTY STATE

If there are no drifts:

show:

"No behavioral drift detected across executed scenarios."

Do not show:

"100% safe."

---

# 185. UI PARTIAL STATE

If 10 scenarios ran and 50 failed:

do not display:

"SAFE"

Display:

"Verification incomplete."

---

# 186. MCP PARTIAL STATE

If impact came from fallback but decisions came from MCP:

show both sources.

---

# 187. SOURCE BADGE

A simple source indicator is valuable:

LatentGraph

Local fallback

Local decision fixture

---

# 188. JUDGE CONFIDENCE

Avoid fake confidence percentages unless scientifically justified.

---

# 189. EXPLANATION CONFIDENCE

If LLM-generated:

label it as explanation.

Evidence remains authoritative.

---

# 190. PERFORMANCE

Do not optimize prematurely.

But avoid:

restarting the application for every scenario.

Prefer:

start once

replay many

if safe.

---

# 191. CONCURRENCY

Do not parallelize old/new execution if shared state makes results nondeterministic.

---

# 192. SCENARIO ORDER

Use deterministic ordering.

---

# 193. RESULT ORDER

Use deterministic ordering.

---

# 194. DEMO STABILITY

The demo must produce the same important result repeatedly.

Run it at least several times.

---

# 195. REPEAT DEMO TEST

Run:

clean

change

BlastProof

report

reset

repeat

The red row should reliably appear.

---

# 196. FALSE POSITIVE TEST

Run without the intentional regression.

Expected:

no meaningful regression.

---

# 197. FALSE NEGATIVE TEST

Run with the intentional regression.

Expected:

drift detected.

---

# 198. NOISE TEST

Introduce a timestamp/request-ID-only difference.

Expected:

not classified as meaningful business drift.

---

# 199. DECISION TEST

Introduce known rule violation.

Expected:

Judge identifies conflict.

---

# 200. INTENTIONAL CHANGE TEST

Introduce documented intentional change.

Expected:

system does not automatically call it a regression.

---

# 201. TEACH TEST

Confirm proposal.

Expected:

MCP update if live.

Otherwise honest fallback receipt.

---

# 202. MCP HEALTH CHECK

If practical, provide an internal health check.

For example:

MCP available

Authentication valid

Repository indexed

Read tool available

Write tool available

Do not expose secrets.

---

# 203. MCP CONNECTION TEST

Run a real read.

Save the result internally.

Confirm it is non-empty and relevant.

---

# 204. MCP WRITE TEST

Only perform write against a safe test/demo graph.

Never write arbitrary junk to production data.

---

# 205. APPROVAL SEMANTICS

If LatentGraph itself queues updates for approval:

respect that.

BlastProof should not pretend queued ≠ approved.

Report the actual state.

---

# 206. UPDATE_GRAPH RESULT

Inspect actual response semantics.

Possible:

queued

accepted

updated

failed

Do not collapse all into success.

---

# 207. GRAPH TEACH LANGUAGE

Use:

"proposed"

"submitted"

"queued"

"updated"

according to actual result.

---

# 208. GRAPH STALENESS

One product narrative is:

graph knowledge can become stale.

BlastProof can provide evidence that certain dependencies/behaviors were observed.

But do not claim BlastProof magically makes the graph intelligent.

---

# 209. TEACH VALUE

The Teach feature's value is:

verified evidence can become persistent team knowledge.

That is the product loop.

---

# 210. DO NOT OVERCLAIM

Do not say:

"the graph learns automatically."

Human confirmation exists.

---

# 211. PRODUCT LOOP

Best conceptual model:

READ

PROVE

JUDGE

TEACH

Then repeat.

---

# 212. GRAPH + RUNTIME

The strategic differentiator is:

static code understanding

+

runtime behavioral evidence.

---

# 213. COMPANY VALUE

The company benefits if BlastProof:

- increases trust in AI-generated changes
- provides evidence for migration/modernization
- reduces fear of silent regressions
- uses LatentGraph as an intelligence layer
- produces persistent engineering knowledge
- potentially becomes a PR/CI safety gate

---

# 214. CUSTOMER VALUE

For enterprise teams:

"Can we safely merge this?"

gets a more evidence-based answer.

---

# 215. BFSI VALUE

For banking-style workloads:

behavioral drift in:

EMI

interest

reconciliation

statements

balances

is expensive.

The demo should illustrate this without pretending to be production banking software.

---

# 216. CI/CD EXTENSION

Potential future extension:

PR integration.

But do not prioritize it over the core demo.

---

# 217. PR COMMENT

Stretch goal:

BlastProof posts a verification summary to a GitHub PR.

Only implement after core system is reliable.

---

# 218. REPORT EXPORT

Possible stretch:

HTML/PDF report.

Only after core system works.

---

# 219. PRIORITY ORDER

Priority:

P0 = correctness

P1 = real MCP integration

P1 = reliable E2E

P1 = honest UI

P2 = polished UX

P2 = demo stability

P3 = PR integration

P3 = export

---

# 220. DO NOT ADD FEATURES BEFORE P0/P1

No extra charts.

No multi-language engine.

No elaborate auth.

No cloud deployment.

No huge agent framework.

No unnecessary abstractions.

---

# 221. 48-HOUR DISCIPLINE

We have limited time.

Do not build a generalized enterprise platform.

Build a convincing vertical slice.

---

# 222. VERTICAL SLICE

The vertical slice is:

one code change

one demo app

one scenario set

one impact analysis

one behavioral regression

one decision

one verification report

one teach action

---

# 223. GENERALIZATION

General architecture is useful.

General feature support is not required.

---

# 224. SUPPORTED LANGUAGE

Python is sufficient for the demo.

Do not add Java/Go/JavaScript migration support just for optics.

---

# 225. SUPPORTED FRAMEWORK

One web framework is sufficient.

FastAPI is fine if already used.

---

# 226. DATABASE

One local database strategy is sufficient.

---

# 227. TRAFFIC

Do not add live traffic capture.

Recorded scenarios are safer and more deterministic.

---

# 228. PRIVACY

No real production traffic.

No real customer data.

---

# 229. SECURITY STORY

The product should actually improve confidence without introducing a new data leak.

---

# 230. SOURCE CONTROL

Do not commit `.env`.

Do not commit API keys.

Do not commit browser auth data.

---

# 231. AI CODING RULE

Development should follow hackathon rules.

LatentCode is the allowed AI coding tool.

Do not introduce Copilot/Claude Code/Cursor as coding dependencies.

---

# 232. MODEL INFRASTRUCTURE

Historical attempts included external model gateways.

Do not spend the remaining hackathon time trying random AI routing providers unless required by the actual application.

---

# 233. MODEL REQUIREMENT

If the application needs an LLM:

use the working allowed infrastructure.

Do not block the entire product on a secondary model provider.

---

# 234. LLM FALLBACK

If LLM explanation fails:

deterministic evidence should still be displayed.

The product should not become unusable.

---

# 235. CORE WITHOUT LLM

BlastProof must still function without natural-language generation.

It can show:

old value

new value

source line

decision

---

# 236. LLM AS ENHANCEMENT

LLM makes the explanation easier to understand.

It should not make the verification truthful.

---

# 237. TEST MODEL FAILURES

Test:

timeout

invalid response

empty response

malformed JSON

---

# 238. MODEL OUTPUT VALIDATION

If model output is expected to be JSON:

validate it.

Do not blindly parse arbitrary text.

---

# 239. PROMPT INJECTION

Scenario response content should not be allowed to manipulate system-level decisions.

Do not treat arbitrary application output as trusted instructions.

---

# 240. EVIDENCE BOUNDARY

LLM receives structured evidence.

Not arbitrary unlimited repository content unless necessary.

---

# 241. SOURCE OF TRUTH HIERARCHY

Highest:

actual execution evidence

Then:

actual Git diff

Then:

actual repository decision source

Then:

LatentGraph responses

Then:

LLM interpretation

Then:

documentation

Do not reverse this hierarchy.

---

# 242. WHY THIS MATTERS

A documentation file can be stale.

An execution result is current.

---

# 243. FINAL VERIFICATION SCRIPT

Create or verify a script/process that performs the full demo verification.

It should clearly report:

PASS/FAIL.

---

# 244. VERIFICATION OUTPUT

Example:

[PASS] baseline starts

[PASS] changed version starts

[PASS] scenarios replay

[PASS] semantic comparison

[PASS] drift detected

[PASS] explanation source

[PASS] decision match

[PASS] teach proposal

[PASS] MCP read

[PASS] MCP write

Only mark MCP checks PASS if real.

---

# 245. FALLBACK OUTPUT

If MCP unavailable:

[WARN] MCP unavailable

[PASS] local fallback

[PASS] behavioral verification

[SKIP] remote graph update

This is honest.

---

# 246. FINAL STATUS

Do not use:

"100% complete"

unless every required acceptance test has passed.

---

# 247. ACCEPTANCE LEVELS

Use:

GREEN = verified

YELLOW = implemented but not fully verified

RED = broken/missing

GRAY = intentionally out of scope

---

# 248. STATUS REPORT

At the end, generate an actual status report containing:

Component

Status

Evidence

Remaining issue

---

# 249. REQUIRED STATUS COMPONENTS

At minimum:

Impact

MCP Read

Fallback Impact

Replay

Compare

Explain

Judge

Teach

MCP Write

CLI

API

UI

Tests

E2E

Documentation

Git state

---

# 250. MCP STATUS EXAMPLE

BAD:

MCP: DONE

GOOD:

MCP Read: VERIFIED LIVE — tool X returned repository dependency data.

GOOD:

MCP Read: BLOCKED — authentication unavailable; fallback verified.

---

# 251. TEACH STATUS EXAMPLE

BAD:

Teach: DONE

GOOD:

Teach: LOCAL PROPOSAL VERIFIED; REMOTE WRITE NOT VERIFIED

or:

Teach: REMOTE UPDATE VERIFIED AGAINST TEST GRAPH

---

# 252. UI STATUS EXAMPLE

BAD:

UI: COMPLETE

GOOD:

UI: VERIFIED — `/api/report`, `/api/run`, `/api/teach` tested manually and through automated checks.

---

# 253. NO SELF-CERTIFICATION

Do not write a final report that merely repeats your own claims.

Each major claim must cite:

command

test

output

or source location.

---

# 254. TEST COMMAND LOG

Record exact commands used for final verification.

---

# 255. GIT LOG

Record final:

branch

commit SHA

working tree state

---

# 256. PUSH VERIFICATION

After push:

fetch/read the remote state.

Confirm commit exists remotely.

---

# 257. MAIN VERIFICATION

After merging/pushing:

inspect remote main.

Confirm expected files exist.

---

# 258. ENGINE VERIFICATION

Inspect engine branch.

Do not accidentally leave important final code only on engine.

---

# 259. DEMO BRANCH

Inspect `demo-change`.

Determine whether it contains the intended regression.

---

# 260. REGRESSION LOCATION

Identify the exact file and line involved in the demo regression.

Do not use an approximate line.

---

# 261. LINE DRIFT

If line changes after edits:

update generated evidence dynamically.

Never hardcode old line numbers.

---

# 262. DEMO RESET

Provide a reliable way to return from regression state to baseline.

---

# 263. DEMO SCRIPT

Create a short internal demo script:

1. baseline
2. change
3. run
4. inspect
5. explain
6. teach

---

# 264. DEMO FAILURE RECOVERY

If MCP fails during demo:

UI should gracefully switch to fallback.

Do not crash.

---

# 265. DEMO FAILURE RECOVERY 2

If one scenario fails:

show it as execution failure.

Continue other scenarios if safe.

---

# 266. DEMO FAILURE RECOVERY 3

If LLM fails:

show deterministic evidence.

---

# 267. DEMO FAILURE RECOVERY 4

If graph write fails:

show honest failure.

---

# 268. DEMO FAILURE RECOVERY 5

Never fabricate a successful state to preserve presentation.

---

# 269. VISUAL PRIORITY

The judge should notice:

RED DRIFT

before:

implementation details.

---

# 270. EXPLANATION PRIORITY

The judge should understand:

WHAT changed?

WHY it matters?

WHERE?

WHAT rule?

WHAT action?

---

# 271. REPORT PRIORITY

Do not overwhelm the judge.

Detailed evidence can be expandable.

---

# 272. UI COPY

Avoid technical jargon where unnecessary.

Instead of:

"response semantic equivalence failure"

use:

"Behavior changed"

Then show technical details underneath.

---

# 273. BUTTON COPY

Prefer:

"Run Verification"

"View Evidence"

"Confirm & Teach"

"Cancel"

Avoid:

"Execute"

"Mutate Graph"

unless technically necessary.

---

# 274. TEACH BUTTON

The button must visually communicate that it changes persistent knowledge.

---

# 275. CONFIRMATION

If graph write is live:

confirmation modal should say what will be written.

---

# 276. GRAPH UPDATE PREVIEW

Show:

Proposed invariant

Source/evidence

Reason

Destination

---

# 277. HUMAN GOVERNANCE

This makes the project more enterprise-credible.

---

# 278. ENTERPRISE CLAIM

Do not say:

"enterprise-ready."

Say:

"designed around evidence, traceability, and human approval."

---

# 279. AUDITABILITY

Useful metadata:

run ID

commit

baseline

new commit

scenario set

timestamp

integration mode

---

# 280. RUN ID

Generate deterministic/unique run IDs as appropriate.

---

# 281. COMMIT IDENTIFICATION

Report should identify old/new commit or version.

---

# 282. SCENARIO VERSION

Report should identify scenario set version if possible.

---

# 283. DECISION SOURCE

Report should identify decision source.

---

# 284. MCP SOURCE

Report should identify MCP/fallback.

---

# 285. REPRODUCTION

A judge should be able to reproduce the important result from README instructions.

---

# 286. DOCUMENTATION TEST

Actually follow the README from a clean environment.

If instructions fail:

fix them.

---

# 287. NO FAKE INSTALL

Do not claim a dependency is installed if the command fails.

---

# 288. REQUIREMENTS CLEANUP

Remove unnecessary dependencies where safe.

But do not perform large dependency refactoring during final hours.

---

# 289. TEST DEPENDENCIES

Ensure test dependencies are available.

---

# 290. IMPORT CHECK

Run a full import/compile check.

---

# 291. PYTHON COMPILE

Verify all project Python modules compile.

---

# 292. STATIC ERRORS

Fix obvious:

NameError

ImportError

AttributeError

TypeError

file-not-found

schema mismatch

---

# 293. STANDALONE SCRIPTS

Any script that is documented as executable must work standalone.

Previous judge standalone crash is a known historical concern.

Retest.

---

# 294. JUDGE STANDALONE

Run Judge independently with representative input.

---

# 295. EXPLAIN STANDALONE

Run Explain independently.

---

# 296. IMPACT STANDALONE

Run Impact independently.

---

# 297. COMPARE STANDALONE

Run Compare independently.

---

# 298. TEACH STANDALONE

Run Teach independently.

---

# 299. CLI INTEGRATION

Then run all of them through CLI.

---

# 300. API INTEGRATION

Then run through API.

---

# 301. UI INTEGRATION

Then run through browser.

---

# 302. FULL STACK

Final flow:

browser

→ API

→ CLI/pipeline

→ engine

→ app

→ report

---

# 303. MCP FULL STACK

If live:

browser

→ API

→ engine

→ MCP adapter

→ LatentGraph

→ engine

→ UI

---

# 304. MCP FALLBACK FULL STACK

If unavailable:

browser

→ API

→ engine

→ local AST

→ engine

→ UI

with explicit fallback indicator.

---

# 305. NO SILENT FALLBACK

The user must know whether MCP was used.

---

# 306. LATENCY

If MCP is slow:

show loading.

Do not make UI appear frozen.

---

# 307. TIMEOUT

Set reasonable timeout.

---

# 308. CACHING

Avoid stale MCP results unless caching is explicitly intended.

---

# 309. CACHE INVALIDATION

If graph changes:

do not blindly reuse stale impact data.

---

# 310. GRAPH STALENESS STORY

If discussing staleness:

make clear that BlastProof provides runtime evidence rather than magically solving all graph synchronization.

---

# 311. PRODUCT BOUNDARY

BlastProof is:

verification/evidence layer.

LatentGraph is:

code knowledge layer.

---

# 312. DO NOT BUILD LATENTGRAPH

Do not recreate their graph.

---

# 313. DO NOT BUILD A GENERIC CODE ASSISTANT

Not the project.

---

# 314. DO NOT BUILD A GENERIC TEST FRAMEWORK

Not the project.

---

# 315. DO NOT BUILD A CHATBOT

Chat is not the core product.

---

# 316. OPTIONAL CHAT

If existing UI has chat:

remove/deprioritize unless it directly helps evidence interrogation.

---

# 317. PRIORITY

Core proof > chat.

---

# 318. REPORT > CHAT

A judge needs the evidence immediately.

---

# 319. DEMO > FEATURES

A working 90-second demonstration is more valuable than ten incomplete features.

---

# 320. ENGINEERING QUALITY

Use:

small functions

clear interfaces

type hints where useful

meaningful errors

deterministic tests

---

# 321. AVOID OVERENGINEERING

Do not create:

10-layer abstraction

event bus

microservices

Kubernetes

cloud infrastructure

unless already required.

---

# 322. ARCHITECTURE DEPTH

A clean modular Python application is sufficient.

---

# 323. FILE ORGANIZATION

Preserve existing structure where sensible.

Do not reorganize everything just for aesthetics.

---

# 324. DOCS ORGANIZATION

Keep authoritative docs clear.

---

# 325. TODO CLEANUP

Search for:

TODO

FIXME

HACK

stub

mock

placeholder

Not every TODO is a problem.

Classify each.

---

# 326. MOCK SEARCH

Search for:

mock

fake

dummy

sample

hardcoded

fixture

fallback

demo

Determine which are legitimate.

---

# 327. HARD-CODED DATA

Any hardcoded data must be clearly fixture/demo data.

No hardcoded runtime results.

---

# 328. FAKE LATENTGRAPH

Search specifically for:

LatentGraph-looking JSON

fake dependency lists

fake tool responses

hardcoded graph IDs

fake update receipts

---

# 329. DELETE FAKE INTEGRATION

If fake MCP exists:

replace with real adapter or explicit fixture/fallback.

---

# 330. DEMO FIXTURE

A fixture is acceptable if explicitly labeled.

Example:

`fixtures/demo_decisions.json`

---

# 331. FIXTURE LABELING

UI should not say:

"LatentGraph decision"

if it came from a fixture.

Say:

"Demo decision fixture."

---

# 332. MCP REALITY

The strongest outcome:

live MCP.

Second-best:

honest fallback with working product.

Worst:

fake MCP.

---

# 333. JUDGE QUESTIONS

Prepare for:

"Did you actually use LatentGraph?"

Answer with actual tool evidence.

---

# 334. JUDGE QUESTION

"What happens if LatentGraph is unavailable?"

Answer:

local fallback.

---

# 335. JUDGE QUESTION

"Why can't LatentGraph itself do this?"

Answer:

LatentGraph provides structural/contextual understanding; BlastProof adds runtime behavioral evidence.

Do not claim features LatentForce does not have unless verified.

---

# 336. JUDGE QUESTION

"Isn't this just testing?"

Answer:

It is targeted verification guided by code intelligence and linked to engineering decisions.

---

# 337. JUDGE QUESTION

"Why replay scenarios?"

Answer:

Because static dependency analysis predicts potential impact, while execution provides evidence of actual behavior.

---

# 338. JUDGE QUESTION

"Can it prove correctness?"

Answer:

No. It can prove observed equivalence or drift for the scenarios executed.

That honesty increases credibility.

---

# 339. JUDGE QUESTION

"What if the change is intentional?"

Answer:

BlastProof reports drift and checks recorded decisions rather than blindly calling every difference a bug.

---

# 340. JUDGE QUESTION

"Why Teach?"

Answer:

Confirmed behavioral knowledge can become persistent team knowledge instead of disappearing after the investigation.

---

# 341. JUDGE QUESTION

"Why human confirmation?"

Answer:

Enterprise knowledge should not be silently mutated by an automated agent.

---

# 342. JUDGE QUESTION

"Does it work with real MCP?"

Answer ONLY according to the actual final verification.

---

# 343. NO LYING

This section is mandatory.

If something is incomplete:

say so.

If something is fallback:

say so.

If something is mocked:

say so.

If something is unverified:

say so.

---

# 344. FINAL CODE REVIEW

Before final push:

review every changed file.

Check:

imports

dead code

debug print

secrets

temporary paths

hardcoded values

broken links

---

# 345. FINAL UI REVIEW

Actually open the application.

Do not infer visual quality from HTML source.

---

# 346. FINAL DEMO REVIEW

Run the exact demo sequence.

Do not run an easier substitute.

---

# 347. FINAL MCP REVIEW

Actually invoke the MCP.

Do not inspect only configuration.

---

# 348. FINAL TEACH REVIEW

Actually click Confirm.

Do not merely call the proposal function.

---

# 349. FINAL REPORT REVIEW

Open generated report.

Check values.

---

# 350. FINAL EVIDENCE REVIEW

Open raw response evidence.

Confirm old/new values are real.

---

# 351. FINAL LINE REVIEW

Click source location.

Verify line.

---

# 352. FINAL DECISION REVIEW

Verify decision source.

---

# 353. FINAL GIT REVIEW

Check:

`git status`

`git log`

branch

remote

---

# 354. FINAL PUSH

Push final verified changes.

---

# 355. FINAL REMOTE REVIEW

Inspect remote repository after push.

---

# 356. FINAL MAIN REVIEW

Confirm main contains final intended implementation.

---

# 357. FINAL README REVIEW

README must match reality.

---

# 358. STATUS TRACKER UPDATE

Only after verification:

update status.

---

# 359. STATUS LANGUAGE

Use:

VERIFIED

NOT VERIFIED

BLOCKED

FALLBACK

rather than:

DONE

where evidence is incomplete.

---

# 360. FINAL STATUS TABLE

Create a final status table like:

| Component | Status | Evidence |
|---|---|---|
| Impact | | |
| LatentGraph Read | | |
| Local Fallback | | |
| Replay | | |
| Compare | | |
| Explain | | |
| Judge | | |
| Teach | | |
| LatentGraph Write | | |
| CLI | | |
| API | | |
| UI | | |
| Tests | | |
| E2E | | |

---

# 361. REQUIRED FINAL ANSWER

At the end of your work, report:

1. What was actually broken.
2. What you fixed.
3. What was already correct.
4. What you verified.
5. What remains blocked.
6. Whether MCP read is live.
7. Whether MCP write is live.
8. Whether fallback works.
9. Whether E2E works.
10. Exact final branch/commit.
11. Whether changes were pushed.

---

# 362. DO NOT SAY "ALL DONE"

Unless the evidence supports it.

---

# 363. DO NOT HIDE BLOCKERS

If authentication blocks MCP:

say it.

---

# 364. DO NOT WASTE TIME

If an external service is genuinely unavailable after reasonable verification:

stop fighting it.

Make fallback excellent.

---

# 365. BUT VERIFY FIRST

"Unavailable" must mean:

actually tested.

Not:

"the previous agent said it failed."

---

# 366. NO ASSUMPTIONS ABOUT LATENTGRAPH API

Use the actual installed/current schema.

---

# 367. NO ASSUMPTIONS ABOUT PR API

Use actual repository data.

---

# 368. NO ASSUMPTIONS ABOUT BRANCH STATE

Use actual Git data.

---

# 369. NO ASSUMPTIONS ABOUT UI

Open it.

---

# 370. NO ASSUMPTIONS ABOUT TESTS

Run them.

---

# 371. NO ASSUMPTIONS ABOUT REPORT

Generate it.

---

# 372. NO ASSUMPTIONS ABOUT TEACH

Execute it.

---

# 373. NO ASSUMPTIONS ABOUT MCP

Invoke it.

---

# 374. CRITICAL PRIORITY

If you have only a few hours remaining:

1. working behavioral comparison
2. real impact integration if possible
3. real Judge integration if possible
4. honest Teach
5. UI
6. polish
7. stretch features

---

# 375. DO NOT SACRIFICE CORE

Never sacrifice the working red/green verification moment for:

PR comments

PDF export

fancy animations

extra charts

multi-language support

---

# 376. DEMO RELIABILITY

The core demo should work repeatedly.

---

# 377. FAILURE BUDGET

It is acceptable for:

MCP to be unavailable.

It is NOT acceptable for:

the core local verification pipeline to be unreliable.

---

# 378. FALLBACK QUALITY

Fallback should not be a fake toy.

It should actually perform useful local analysis.

---

# 379. LOCAL AST

Inspect the existing AST implementation.

Determine whether it truly:

- parses source
- finds imports
- finds routes
- traverses dependencies
- identifies affected endpoints

---

# 380. AST LIMITATION

Document limitations.

AST dependency analysis is not equivalent to a complete runtime dependency graph.

---

# 381. GRAPH LIMITATION

LatentGraph output is also not proof of runtime behavior.

That is exactly why BlastProof exists.

---

# 382. PRODUCT LOGIC

The combination matters:

STATIC IMPACT

+

RUNTIME PROOF

+

DECISION CONTEXT

---

# 383. CORE VALUE

Not:

"more AI."

Instead:

"more evidence."

---

# 384. PRODUCT LANGUAGE

Use:

evidence

traceability

behavioral drift

verification

engineering decisions

human approval

persistent knowledge

---

# 385. AVOID BUZZWORDS

Avoid excessive:

agentic

autonomous

revolutionary

next-generation

AI-powered

unless necessary.

---

# 386. DEMO OPENING

Preferred:

"We changed one line. The question is whether anything important changed because of it."

---

# 387. DEMO MIDDLE

"LatentGraph tells us where the change could matter. BlastProof executes the affected behavior."

---

# 388. DEMO END

"We found the drift, proved it with before/after evidence, checked the team's decision, and only then asked permission to teach it back."

---

# 389. PRODUCT LOOP SUMMARY

READ

What could be affected?

PROVE

What actually changed?

JUDGE

Was it allowed?

TEACH

Should we remember it?

---

# 390. THIS IS THE PRODUCT

Everything else is implementation detail.

---

# 391. FINAL ACCEPTANCE TEST A

No-change baseline.

Expected:

all meaningful scenarios stable.

---

# 392. FINAL ACCEPTANCE TEST B

Known regression.

Expected:

specific drift.

---

# 393. FINAL ACCEPTANCE TEST C

Noise-only difference.

Expected:

ignored.

---

# 394. FINAL ACCEPTANCE TEST D

Known decision violation.

Expected:

Judge identifies it.

---

# 395. FINAL ACCEPTANCE TEST E

Unknown drift.

Expected:

unexplained/review.

---

# 396. FINAL ACCEPTANCE TEST F

MCP unavailable.

Expected:

fallback.

---

# 397. FINAL ACCEPTANCE TEST G

MCP read available.

Expected:

actual graph data.

---

# 398. FINAL ACCEPTANCE TEST H

MCP write available.

Expected:

actual update operation after human confirmation.

---

# 399. FINAL ACCEPTANCE TEST I

MCP write fails.

Expected:

honest failure.

---

# 400. FINAL ACCEPTANCE TEST J

UI loads.

Expected:

no console-breaking errors.

---

# 401. FINAL ACCEPTANCE TEST K

API fails.

Expected:

honest error.

---

# 402. FINAL ACCEPTANCE TEST L

CLI runs.

Expected:

clean completion.

---

# 403. FINAL ACCEPTANCE TEST M

Fresh checkout.

Expected:

documented setup works.

---

# 404. FINAL ACCEPTANCE TEST N

Repeated demo.

Expected:

same important result.

---

# 405. FINAL ACCEPTANCE TEST O

Git repository.

Expected:

clean intended state.

---

# 406. FINAL ACCEPTANCE TEST P

Remote.

Expected:

final commit pushed.

---

# 407. DO NOT DELETE HISTORY

Preserve useful Git history.

---

# 408. DO NOT FORCE PUSH

Unless explicitly required and safe.

---

# 409. DO NOT RESET MAIN

Do not perform destructive history operations.

---

# 410. DO NOT CHANGE OWNERSHIP

Do not change repository ownership/settings.

---

# 411. DO NOT CREATE SECRETS

Never.

---

# 412. DO NOT COMMIT SECRETS

Never.

---

# 413. DO NOT FABRICATE TEST RESULTS

Never.

---

# 414. DO NOT FABRICATE MCP RESULTS

Never.

---

# 415. DO NOT FABRICATE PR RESULTS

Never.

---

# 416. DO NOT FABRICATE GRAPH WRITES

Never.

---

# 417. DO NOT FABRICATE LINE NUMBERS

Never.

---

# 418. DO NOT FABRICATE COVERAGE

Never.

---

# 419. DO NOT FABRICATE PERFORMANCE

Never.

---

# 420. DO NOT FABRICATE BUSINESS IMPACT

Never.

---

# 421. HONEST DEMO

A smaller honest demo is better than a fake impressive demo.

---

# 422. CODE QUALITY

Fix real defects.

Do not merely alter wording to make status look better.

---

# 423. DOCUMENTATION QUALITY

Documentation should describe current behavior.

---

# 424. TEST QUALITY

Tests should test behavior.

Not merely:

"file imports successfully."

---

# 425. E2E QUALITY

E2E should execute the real system.

Not mocks everywhere.

---

# 426. MCP TEST QUALITY

MCP tests should distinguish:

mock adapter tests

from:

live integration tests.

---

# 427. LABEL MOCK TESTS

Clearly label them.

---

# 428. LIVE TEST

If live integration cannot run in CI:

provide a manual verification command.

---

# 429. MANUAL VERIFICATION

Document prerequisites.

---

# 430. AUTH DOCUMENTATION

Explain setup without exposing credentials.

---

# 431. MCP DEMO MODE

If a demo fixture exists:

name it explicitly.

---

# 432. FALLBACK DEMO

Fallback must be visually distinguishable.

---

# 433. REPORT SOURCE

Every impact result should identify source.

---

# 434. REPORT DECISION SOURCE

Every decision should identify source.

---

# 435. REPORT TEACH SOURCE

Every Teach action should identify destination/result.

---

# 436. REPORT EXECUTION SOURCE

Record baseline/new versions.

---

# 437. TRACEABILITY

A reviewer should be able to trace:

change

→ impact

→ scenario

→ result

→ source

→ decision

→ teach

---

# 438. THIS IS THE AUDIT TRAIL

That traceability is more valuable than a pretty dashboard.

---

# 439. PERFORMANCE TARGET

Do not promise a fixed execution time.

Measure it.

---

# 440. DEMO TARGET

The demo should preferably finish within approximately two minutes.

---

# 441. HACKATHON TARGET

The project should feel like:

a coherent product

not:

five unrelated scripts.

---

# 442. INTEGRATION TARGET

LatentGraph should feel like a natural component.

---

# 443. COMPANY VALUE TARGET

The judge should understand:

"this extends what LatentForce is already building."

---

# 444. DIFFERENTIATION TARGET

Do not merely reproduce LatentGraph's dependency graph.

---

# 445. DIFFERENTIATION TARGET 2

Do not merely reproduce PR insights.

---

# 446. DIFFERENTIATION TARGET 3

Do not merely reproduce migration verification.

---

# 447. DIFFERENTIATION TARGET 4

The core new layer is:

runtime behavioral evidence tied to predicted impact and engineering decisions.

---

# 448. TEACH DIFFERENTIATION

The feedback loop:

verified evidence

→ proposed persistent knowledge

is a useful differentiator.

---

# 449. HUMAN APPROVAL DIFFERENTIATION

Human confirmation makes the workflow enterprise-safe.

---

# 450. FINAL PRODUCT DESCRIPTION

BlastProof is a developer safety gate that connects static code impact analysis with runtime behavioral verification.

---

# 451. FINAL PRODUCT DESCRIPTION 2

A change is not considered safe merely because an AI generated it.

BlastProof executes evidence.

---

# 452. FINAL PRODUCT DESCRIPTION 3

It compares old and new behavior and identifies meaningful drift.

---

# 453. FINAL PRODUCT DESCRIPTION 4

It links drift to source changes.

---

# 454. FINAL PRODUCT DESCRIPTION 5

It checks drift against recorded engineering decisions.

---

# 455. FINAL PRODUCT DESCRIPTION 6

It lets a human confirm what should become persistent knowledge.

---

# 456. FINAL PRODUCT DESCRIPTION 7

When LatentGraph is available, its graph becomes the structural intelligence layer.

---

# 457. FINAL PRODUCT DESCRIPTION 8

When it is unavailable, BlastProof remains useful through explicit local fallback.

---

# 458. IMPORTANT LIMITATION

BlastProof does not prove all possible application behavior.

---

# 459. IMPORTANT LIMITATION 2

Recorded scenarios define the observed behavioral surface.

---

# 460. IMPORTANT LIMITATION 3

Static impact analysis can miss dynamic behavior.

---

# 461. IMPORTANT LIMITATION 4

LLM explanations can be imperfect.

Therefore evidence must remain visible.

---

# 462. IMPORTANT LIMITATION 5

MCP availability depends on authentication/environment.

---

# 463. HONESTY

These limitations should increase credibility rather than be hidden.

---

# 464. FINAL REVIEW OF KNOWN HISTORICAL ISSUES

Explicitly retest:

stale main

duplicate UI

judge standalone crash

fake success receipt

wrong explanation line

unverified PR claims

repo clutter

MCP false-positive status

---

# 465. MCP FALSE-POSITIVE STATUS

This is especially important.

Search code for language such as:

"connected"

"success"

"updated"

"written"

"LatentGraph"

Verify every such claim.

---

# 466. RECEIPT FALSE POSITIVE

Search:

"success"

"written"

"updated"

in Teach/UI code.

Trace each to actual operation.

---

# 467. HARD-CODED DEMO RESULT SEARCH

Search for:

14820

10718

4102

42

17

9

4

60

Determine whether these are:

fixtures

tests

hardcoded runtime values

---

# 468. IF HARDCODED RUNTIME

Remove.

---

# 469. IF DEMO FIXTURE

Label.

---

# 470. IF TEST

Keep.

---

# 471. DECISION IDs

Search all references to:

PR #42

Decision #17

and similar.

Verify provenance.

---

# 472. FINAL UI SEARCH

Search for stale text such as:

"100% complete"

"connected"

"graph updated"

"safe"

Ensure wording matches actual state.

---

# 473. FINAL DOC SEARCH

Search Markdown for claims that conflict with implementation.

Correct them.

---

# 474. FINAL TASK FILE

After completion, this handoff itself should not become the only source of truth.

The repository status should reflect reality.

---

# 475. FINAL COMMIT

Commit:

code

tests

docs

UI

configuration changes

only when appropriate.

---

# 476. PUSH

Push final commit.

---

# 477. POST-PUSH VERIFICATION

Fetch remote.

Confirm commit.

Confirm files.

---

# 478. FINAL RESPONSE FORMAT

Return:

## VERIFIED

List verified components.

## FIXED

List actual fixes.

## BLOCKED

List genuine blockers.

## MCP

State read status.

State write status.

State fallback.

## E2E

State exact result.

## UI

State manual verification.

## GIT

Branch.

Commit.

Push status.

---

# 479. NO MARKETING LANGUAGE

Final engineering report should be factual.

---

# 480. NO "TRUST ME"

Evidence instead.

---

# 481. NO "SHOULD WORK"

Run it.

---

# 482. NO "I BELIEVE"

Verify it.

---

# 483. NO "PROBABLY"

Determine it.

---

# 484. NO "100%"

Unless acceptance tests prove it.

---

# 485. NO SILENT ASSUMPTIONS

Document uncertainty.

---

# 486. FINAL PRIORITY

If a conflict exists between:

more features

and

more reliability

choose reliability.

---

# 487. FINAL PRIORITY 2

If a conflict exists between:

beautiful UI

and

correct MCP integration

choose MCP integration.

---

# 488. FINAL PRIORITY 3

If a conflict exists between:

MCP polish

and

working local verification

choose working verification.

---

# 489. FINAL PRIORITY 4

If MCP cannot be made live after genuine verification:

make fallback excellent and honest.

---

# 490. FINAL PRIORITY 5

Do not spend the entire remaining hackathon chasing an unavailable external service.

---

# 491. FINAL PRIORITY 6

Do not add unrelated features.

---

# 492. FINAL PRIORITY 7

Do not rewrite functioning code unnecessarily.

---

# 493. FINAL PRIORITY 8

Do not delete working teammate code without understanding it.

---

# 494. FINAL PRIORITY 9

Do not assume branch state.

---

# 495. FINAL PRIORITY 10

Do not trust previous AI completion claims.

---

# 496. FINAL DEFINITION OF DONE

BlastProof is DONE only when:

A real code change can be made.

The system identifies the changed scope.

LatentGraph is used when genuinely available.

Fallback works when it is not.

Old and new versions actually execute.

Recorded scenarios actually replay.

Responses are semantically compared.

Meaningful drift is detected.

Noise is filtered.

Evidence is displayed.

Source location is accurate.

Recorded decisions are evaluated honestly.

Drift is classified.

A Teach proposal is generated.

Human confirmation is required.

MCP update_graph is actually invoked when live.

Success/failure is accurately reported.

The UI communicates the entire flow.

The complete pipeline works from a fresh run.

The regression demo works repeatedly.

Tests pass.

Documentation matches reality.

Git state is clean enough for submission.

Final work is pushed.

---

# 497. ABSOLUTE FINAL RULE

If you cannot prove that something works:

DO NOT MARK IT DONE.

---

# 498. ABSOLUTE FINAL RULE 2

If something is mocked:

LABEL IT MOCKED.

---

# 499. ABSOLUTE FINAL RULE 3

If something uses fallback:

LABEL IT FALLBACK.

---

# 500. ABSOLUTE FINAL RULE 4

If something is blocked:

LABEL IT BLOCKED.

---

# 501. ABSOLUTE FINAL RULE 5

If something works:

SHOW THE EVIDENCE.

---

# 502. FINAL COMMAND TO THE CODING AGENT

Now begin.

Do NOT immediately start modifying files.

First audit the repository completely.

Inspect all relevant Markdown instructions.

Inspect all source.

Inspect all tests.

Inspect branches.

Inspect Git history.

Inspect MCP configuration.

Inspect LatentGraph integration.

Then produce an internal discrepancy list.

Only after that begin fixes.

---

# 503. REQUIRED FIRST REPORT

Before substantial modification, report internally:

1. Current branch.
2. Current commit.
3. Main commit.
4. Engine commit.
5. Relevant files.
6. Claimed implementation status.
7. Actual implementation status.
8. MCP status.
9. UI status.
10. E2E status.
11. Critical defects.
12. Exact next actions.

---

# 504. DO NOT STOP AFTER THE AUDIT

The audit is not the deliverable.

Fix the problems.

---

# 505. DO NOT STOP AFTER FIXES

Run the tests.

---

# 506. DO NOT STOP AFTER TESTS

Run E2E.

---

# 507. DO NOT STOP AFTER E2E

Run the UI.

---

# 508. DO NOT STOP AFTER UI

Verify MCP.

---

# 509. DO NOT STOP AFTER MCP

Run the final demo.

---

# 510. DO NOT STOP AFTER DEMO

Update documentation.

---

# 511. DO NOT STOP AFTER DOCUMENTATION

Commit.

---

# 512. DO NOT STOP AFTER COMMIT

Push.

---

# 513. DO NOT STOP AFTER PUSH

Verify remote state.

---

# 514. FINAL REQUIREMENT

After all work is complete, push the final changes to the correct repository/branch.

Then provide the exact:

branch

commit SHA

and pushed status.

---

# 515. FINAL REQUIREMENT 2

Do not claim the project is complete if any P0/P1 acceptance test is failing.

---

# 516. FINAL REQUIREMENT 3

Do not hide MCP limitations.

---

# 517. FINAL REQUIREMENT 4

Do not fabricate graph operations.

---

# 518. FINAL REQUIREMENT 5

Do not fabricate evidence.

---

# 519. FINAL REQUIREMENT 6

Do not fabricate PR provenance.

---

# 520. FINAL REQUIREMENT 7

Do not fabricate line numbers.

---

# 521. FINAL REQUIREMENT 8

Do not fabricate test results.

---

# 522. FINAL REQUIREMENT 9

Do not leave the repository in a worse state than you found it.

---

# 523. FINAL REQUIREMENT 10

The final result must be a coherent, runnable, demonstrable BlastProof vertical slice — not a collection of disconnected features.

---

# 524. END STATE

The judge should be able to watch this:

CODE CHANGE

↓

LATENTGRAPH / IMPACT

↓

TARGETED SCENARIOS

↓

OLD VS NEW

↓

GREEN + RED

↓

REAL EVIDENCE

↓

SOURCE LINE

↓

ENGINEERING DECISION

↓

VERDICT

↓

HUMAN CONFIRMATION

↓

TEACH

and understand the entire product without needing a five-minute explanation.

---

# 525. THE SINGLE MOST IMPORTANT TEST

Change one line.

Run BlastProof.

Make the system catch the resulting behavioral regression.

Show exactly why.

Then confirm the knowledge update.

If that works reliably and honestly, the project is strong.

If that does not work, everything else is secondary.

---

# 526. START NOW

Audit first.

Verify second.

Fix third.

Test fourth.

Polish fifth.

Push last.

Never reverse that order.