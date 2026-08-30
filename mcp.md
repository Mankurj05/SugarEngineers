You are responsible for implementing the LatentGraph MCP integration for the BlastProof project.

I will personally handle the LatentGraph account creation and API key. Do NOT ask me to implement code manually. Your job is to prepare and configure everything in the repository needed for BlastProof to use the real LatentGraph MCP.

I am also providing the official @latentforce/latentgraph README. Treat that README as the source of truth for installation, configuration, MCP tools, authentication, and integration.

==================================================
GOAL
==================================================

Build the BlastProof integration so that:

    BlastProof
        ↓
    engine/impact.py
        ↓
    LatentGraph MCP
        ↓
    dependency / call-chain / file information
        ↓
    Blast Radius
        ↓
    replay only affected scenarios

And later:

    Confirm & Teach
        ↓
    engine/teach.py
        ↓
    LatentGraph MCP
        ↓
    update_graph

The Local AST implementation must remain as the fallback.

==================================================
STEP 1 — INSPECT THE CURRENT PROJECT
==================================================

Before changing anything, inspect:

- engine/mcp_client.py
- engine/impact.py
- engine/impact_local.py
- engine/teach.py
- engine/judge.py
- engine/cli.py
- CONTRACTS.md
- README.md
- all existing MCP configuration files
- all existing LatentGraph-related code

Determine what is already implemented and avoid duplicating functionality.

Do NOT modify unrelated code.

Do NOT modify the demo app unless required for MCP integration.

==================================================
STEP 2 — INSTALL / CONFIGURE LATENTGRAPH
==================================================

Use the official LatentGraph README.

The README specifies the package:

    @latentforce/latentgraph

and installation:

    npm install -g @latentforce/latentgraph

Ensure the project environment can use the `lgraph` CLI.

Verify:

    lgraph --version

Do not install random MCP packages if the official LatentGraph CLI already provides the MCP server.

==================================================
STEP 3 — PROJECT INITIALIZATION
==================================================

Prepare the repository for LatentGraph.

The official workflow is conceptually:

    lgraph start
    lgraph init
    lgraph status

The project must ultimately have the required LatentGraph project configuration, including:

    .lgraph/config.json

and, where required:

    .lgraph/scan_target.json

Do not commit secrets.

==================================================
STEP 4 — MCP CONFIGURATION FOR LATENTCODE
==================================================

The official README explicitly supports:

    lgraph add latent-code

Use the official LatentGraph mechanism to configure the MCP server for LatentCode.

Do NOT invent an MCP server URL.

Do NOT invent an MCP tool name.

Do NOT create a fake MCP implementation.

Use the official `lgraph add latent-code` integration.

If the command creates a configuration file, inspect the generated configuration and verify that it points to the real LatentGraph MCP server.

==================================================
STEP 5 — AUTHENTICATION
==================================================

I will create the LatentGraph account and obtain the API key.

The official README states that LatentGraph uses an API key and supports:

    lgraph start -k <API_KEY> -n "<PROJECT_NAME>"

Do NOT hardcode my API key anywhere in source code.

Do NOT commit the API key.

Do NOT print the API key.

If the CLI requires me to enter the API key interactively, stop and tell me exactly what command I need to run.

If the API key is already configured, verify it without exposing the secret.

==================================================
STEP 6 — INDEX THIS PROJECT
==================================================

Once authentication/project configuration is available, initialize/index the BlastProof repository.

Use the official LatentGraph commands.

The goal is for LatentGraph to understand:

    demo-app/
    engine/
    scenarios/

and especially the Python dependency graph.

Make sure Python files are included in the scan target.

Do not invent scan configuration if the default auto-detection is sufficient.

After indexing, run:

    lgraph status

and verify the project is actually connected/indexed.

==================================================
STEP 7 — VERIFY THE REAL MCP TOOLS
==================================================

The official README says LatentGraph exposes these MCP tools:

    get_project_overview
    get_module_info
    get_file
    get_dependencies
    get_call_chain
    get_symbol
    get_pr_insights
    ask_codebase
    update_graph

Verify that the configured MCP server exposes these tools.

For BlastProof, the important tools are:

    get_file
    get_dependencies
    get_call_chain
    get_pr_insights
    update_graph

Do not assume argument schemas.

Inspect the actual MCP tool definitions and use their real schemas.

==================================================
STEP 8 — IMPLEMENT / FIX engine/mcp_client.py
==================================================

Create or update the MCP client abstraction.

It should provide clean methods corresponding to the required operations:

    get_file(...)
    get_dependencies(...)
    get_call_chain(...)
    get_pr_insights(...)
    update_graph(...)

The rest of BlastProof should not need to know MCP protocol details.

Handle:

- authentication failures
- connection failures
- missing tools
- invalid responses
- timeouts

with useful errors.

Never fake a successful MCP response.

==================================================
STEP 9 — IMPLEMENT IMPACT USING REAL MCP
==================================================

engine/impact.py must use LatentGraph MCP as the PRIMARY source.

For a changed file such as:

    demo-app/core/interest.py

use LatentGraph to determine:

- incoming dependencies
- outgoing dependencies
- affected files
- affected symbols
- API endpoints
- relevant call chains

Use the actual LatentGraph tool responses.

Produce BlastProof's normalized blast-radius structure.

Clearly mark:

    source = "LATENTGRAPH"

when MCP succeeds.

==================================================
STEP 10 — KEEP AST FALLBACK
==================================================

If MCP cannot connect or authenticate:

    DO NOT FAKE MCP RESULTS.

Instead:

    engine/impact_local.py

must be used.

Clearly mark:

    source = "LOCAL_AST_FALLBACK"

The UI/report must be able to distinguish:

    LATENTGRAPH

from:

    LOCAL_AST_FALLBACK

The fallback must not be removed.

==================================================
STEP 11 — PR INSIGHTS / JUDGE
==================================================

Connect the Judge to the real:

    get_pr_insights

MCP tool.

Use it to retrieve recorded:

- invariants
- decisions
- PR grounding

Normalize the response for engine/judge.py.

If no LatentGraph insight exists, use the project's existing decisions.json fallback according to the contract.

Never invent a PR decision.

==================================================
STEP 12 — TEACH
==================================================

Inspect engine/teach.py.

Implement the real LatentGraph:

    update_graph

MCP operation using the actual schema.

The flow must be:

    developer clicks Confirm & Teach
            ↓
        teach.py
            ↓
       update_graph
            ↓
     LatentGraph
            ↓
      pending edit / result

The official README says `update_graph` is the single write tool and that graph edits are queued for owner approval.

Do NOT automatically teach.

Do NOT claim the invariant was written unless the real MCP call succeeded.

If the write is unavailable, return the proposed invariant and clearly state that the graph write was not completed.

==================================================
STEP 13 — CREATE MCP DIAGNOSTIC
==================================================

Create a small diagnostic command/test for the team.

It should verify:

1. LatentGraph CLI installed
2. Project configuration exists
3. API authentication is available
4. LatentGraph project is reachable
5. Project is indexed
6. MCP server is configured
7. Required MCP tools are available

Required tools:

    get_file
    get_dependencies
    get_call_chain
    get_pr_insights
    update_graph

Do NOT perform an unwanted permanent graph write during diagnostics.

==================================================
STEP 14 — TEST BLASTPROOF IMPACT
==================================================

After MCP is configured, test against the actual banking application.

The intended dependency path is approximately:

    interest.py
        ↓
    emi_service.py
        ↓
    loan_service.py
        ↓
    payment_service.py

And relevant API endpoints should be discoverable through the graph.

Use actual LatentGraph results.

Do NOT hardcode:

    9 files
    4 endpoints

unless LatentGraph actually returns those results.

==================================================
STEP 15 — TEST MCP FAILURE FALLBACK
==================================================

Temporarily simulate an MCP connection failure in a safe way.

Verify:

    MCP fails
       ↓
    useful MCP error
       ↓
    LOCAL_AST_FALLBACK
       ↓
    BlastProof continues

Restore normal configuration afterward.

==================================================
IMPORTANT RULES
==================================================

1. Use the official LatentGraph README as the source of truth.
2. Use the real LatentGraph MCP.
3. Do not fake MCP responses.
4. Do not hardcode API credentials.
5. Do not commit secrets.
6. Keep Local AST fallback.
7. Clearly expose degraded/fallback mode.
8. Do not modify engine behavior unrelated to MCP.
9. Do not change shared contracts without approval.
10. Do not automatically call update_graph.
11. Do not claim graph writes succeeded unless verified.
12. Do not invent MCP endpoints/tool schemas.
13. Do not use a random third-party MCP implementation when the official CLI provides the integration.
14. Keep the implementation compatible with the existing BlastProof architecture.

==================================================
FINAL OUTPUT
==================================================

When finished, report:

- What LatentGraph configuration was found/created
- Exact commands required from me
- Whether authentication succeeded
- Project ID (safe to display)
- Whether indexing succeeded
- MCP server configuration status
- Actual MCP tools discovered
- Files changed
- How impact.py uses MCP
- How get_pr_insights is connected
- How update_graph is connected
- How AST fallback works
- Exact verification commands
- Exact test results
- Any remaining action I personally need to perform

If you need my API key, NEVER ask me to paste it into source code or chat.

Instead, tell me the exact official `lgraph` command where I should provide it securely.