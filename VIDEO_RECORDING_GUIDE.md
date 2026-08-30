# BlastProof MCP Integration - Video Recording Guide

## Quick Start Options

### Option 1: Fully Automated (Recommended)
```bash
python run_blastproof_demo.py
```
This single command runs everything automatically:
- Shows MCP diagnostics
- Demonstrates before/after project ID fix
- Generates report automatically
- Starts UI server
- Displays results in browser

### Option 2: Manual Step-by-Step
Follow the detailed steps below for manual control over each part of the demonstration.

## Overview
This guide provides step-by-step instructions for recording a video demonstrating the BlastProof application's blast radius detection and regression analysis capabilities with MCP integration.

## Changes Made

### 1. Project ID Configuration Fix
**Files Modified:**
- `engine/impact.py` (line 26)
- `engine/teach.py` (line 54)

**Change:** Updated hardcoded project ID from `cb278f60-3b7b-4a08-b34e-b08331497f72` to the correct project ID from `.lgraph/config.json`: `a2650a68-2120-4c13-9f48-bcc1331e132e`

**Impact:** This ensures the MCP client connects to the correct LatentGraph project for blast radius analysis.

### 2. UI Structure Verification
The UI is properly structured with:
- LatentGraph MCP status indicator
- Blast radius prediction panel
- Pipeline status visualization
- Scenario execution results
- Regression detection display

## Pre-Recording Setup

### 1. Start the UI Server
```bash
cd ui
python server.py
```
The server will start on `http://127.0.0.1:5500`

### 2. Open Browser
Navigate to `http://127.0.0.1:5500` in your browser

## Video Recording Script

### Part 1: Before Fix Demonstration

**Step 1: Show the Problem with Wrong Project ID**
First, let's temporarily break the project ID to show the before state:
- Open `engine/impact.py` line 26
- Change the project ID to the wrong one: `cb278f60-3b7b-4a08-b34e-b08331497f72`
- Open `engine/teach.py` line 54
- Change to the same wrong project ID

**Step 2: Show MCP Connection Failure**
Run the impact analysis with the wrong ID:
```bash
python -m engine.impact --old main --new demo-change --verbose
```
- Show the error: "404 Not Found - Project not found or access denied"
- Explain: "The wrong project ID prevents MCP from connecting to LatentGraph"
- Note that it falls back to local AST with 0 endpoints detected

**Step 3: Try to Generate Report (Will Fail)**
```bash
python -m engine.generate_report --old main --new demo-change
```
- Show that it fails or returns incomplete data
- Explain: "Without proper MCP connection, we can't get accurate blast radius data"

**Step 4: Show UI with Missing Data**
- Open browser to `http://127.0.0.1:5500`
- Show that the UI displays "Could not load report.json" or empty sections
- Explain: "The UI can't display data because MCP isn't working"

### Part 2: Apply the Fix

**Step 1: Show the Code Changes**
Open the modified files and fix the project IDs:
- Open `engine/impact.py` line 26
- Change from wrong ID to correct ID: `a2650a68-2120-4c13-9f48-bcc1331e132e`
- Open `engine/teach.py` line 54
- Change from wrong ID to correct ID: `a2650a68-2120-4c13-9f48-bcc1331e132e`

**Step 2: Verify Configuration**
Show the `.lgraph/config.json` file to confirm the correct project ID:
```json
{
  "project_id": "a2650a68-2120-4c13-9f48-bcc1331e132e",
  "project_name": "BlastProof"
}
```
Explain: "Now the project IDs match the LatentGraph configuration"

### Part 3: After Fix Demonstration

**Step 1: Generate Report with Fixed MCP Connection**
```bash
python -m engine.generate_report --old main --new demo-change
```
- Show the successful output: "Generated report.json with impact data from mcp_dynamic_graph_parser"
- Point to "MCP READ SUCCESS" in the verbose output
- Highlight the 4 detected endpoints: `/api/orders`, `/api/checkout`, `/api/products`, `/api/carts/quote`
- Show the dynamic graph parsing results

**Step 2: Verify MCP Connection**
```bash
python -m engine.impact --old main --new demo-change --verbose
```
- Show that the MCP connection now works correctly
- Highlight the successful JSON-RPC response
- Note the correct project ID being used
- Show the source tagging: "mcp_dynamic_graph_parser"

**Step 3: Refresh the UI**
- Refresh the browser page at `http://127.0.0.1:5500`
- Show that the UI now displays the MCP data
- Point to the "Predicted Radius" section showing the 4 affected endpoints
- Show the "MCP Connected" status indicator
- Note the changed files and affected files displayed

**Step 4: Show Pipeline Status**
- Point to the "Pipeline Status" panel
- Explain each step:
  - Graph Impact Read (AST dependencies mapped via MCP)
  - Twin-Port Replay (Replayed generic scenarios)
  - Semantic Diffing (UUID/noise masking applied)
  - Rule Judgement (Checked against decisions.json)

### Part 4: MCP Integration Deep Dive

**Step 1: Show MCP Client Implementation**
Open `engine/mcp_client.py` and explain:
- How it constructs JSON-RPC requests
- The environment variable handling
- The subprocess communication with LatentGraph
- Error handling and response parsing

**Step 2: Show Impact Analysis Logic**
Open `engine/impact.py` and explain:
- The fallback mechanism (MCP first, then local AST)
- The dynamic graph parsing logic
- How it maps LatentGraph responses to blast radius
- The source tagging for transparency

**Step 3: Show Teach Functionality**
Open `engine/teach.py` and explain:
- How it generates invariants
- The MCP update_graph integration
- The fallback to local file storage
- The receipt handling for user feedback

## Key Observations to Highlight

### MCP Integration Benefits
1. **Accurate Dependency Tracking**: LatentGraph provides real dependency analysis
2. **Dynamic Blast Radius**: Automatically traces affected files and endpoints
3. **Transparency**: Clear source tagging (MCP vs fallback)
4. **Robustness**: Graceful fallback to local AST if MCP fails

### Blast Radius Detection
1. **Changed Files**: Shows which Python files were modified
2. **Affected Endpoints**: Maps changes to API endpoints
3. **Graph Analysis**: Uses LatentGraph's dependency graph
4. **Dynamic Discovery**: No hardcoded mappings

### Regression Analysis
1. **Semantic Diffing**: Compares API responses intelligently
2. **Rule Judgement**: Checks against established decisions
3. **Scenario Coverage**: Tests multiple use cases
4. **Clear Reporting**: Shows identical, regression, intentional, and unexplained

## Commands Summary

### Diagnostic Commands
```bash
# Check MCP integration status
python -m engine.mcp_diagnostic

# Run impact analysis with verbose output
python -m engine.impact --old main --new demo-change --verbose

# Force local fallback (for testing)
python -m engine.impact --old main --new demo-change --local
```

### UI Commands
```bash
# Start the UI server
cd ui
python server.py

# Access the dashboard
# Open browser to http://127.0.0.1:5500
```

### Teach/Update Commands
```bash
# Generate a proposal (read-only)
python -m engine.teach --scenario cart_discount

# Commit a proposal to the graph
python -m engine.teach --confirm --scenario cart_discount
```

## Full Pipeline Command
```bash
# Run the complete verification pipeline
python -m engine.cli --old main --new demo-change --app demo_app.main:app
```

## Expected Results

### Before Fix
- MCP connection may fail or use wrong project
- Blast radius detection may be incomplete
- Endpoints may not be correctly identified
- MCP errors in verbose output

### After Fix
- MCP connection succeeds with correct project
- Accurate blast radius detection
- Correct endpoint identification
- Clean MCP responses in verbose output
- UI shows proper MCP status

## Troubleshooting

### If MCP Connection Fails
1. Check project ID in `.lgraph/config.json`
2. Verify API key is configured
3. Run `lgraph status` to check connection
4. Check LatentGraph daemon is running

### If UI Shows Loading
1. Ensure `report.json` exists
2. Run the full pipeline first
3. Check server is running on port 5500
4. Check browser console for errors

### If Impact Analysis Shows No Results
1. Verify branches exist: `git branch -a`
2. Check there are actual changes between branches
3. Use `--verbose` flag to see MCP queries
4. Check if Python files were changed

## Conclusion

This demonstrates how BlastProof leverages LatentGraph MCP for accurate blast radius detection and regression analysis, with robust fallback mechanisms and transparent reporting. The project ID fix ensures proper connectivity to the correct LatentGraph project for accurate dependency analysis.