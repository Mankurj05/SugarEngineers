# BlastProof Quick Start Guide

## One-Command Demo Run

### Option 1: Full Automated Demo (Recommended)
```bash
python run_blastproof_demo.py
```
This runs everything automatically:
- Checks MCP diagnostics
- Shows before/after project ID fix
- Generates report automatically
- Starts UI server
- Opens browser to http://127.0.0.1:5500

### Option 2: Manual Step-by-Step

**1. Check MCP Status**
```bash
python -m engine.mcp_diagnostic
```

**2. Fix Project IDs (if needed)**
- Edit `engine/impact.py` line 26: Change to `a2650a68-2120-4c13-9f48-bcc1331e132e`
- Edit `engine/teach.py` line 54: Change to `a2650a68-2120-4c13-9f48-bcc1331e132e`

**3. Generate Report**
```bash
python -m engine.generate_report --old main --new demo-change
```

**4. Start UI Server**
```bash
cd ui
python server.py
```

**5. Open Browser**
Navigate to: http://127.0.0.1:5500

## Video Recording Commands

For your video recording, use these commands in sequence:

### Part 1: Show Problem (Wrong ID)
```bash
python -m engine.impact --old main --new demo-change --verbose
```
*Shows 404 error and 0 endpoints*

### Part 2: Fix Project IDs
Edit the files as shown above, then:

### Part 3: Show Solution (Correct ID)
```bash
python -m engine.generate_report --old main --new demo-change
```
*Shows MCP success with 4 endpoints*

### Part 4: View Results
Open browser to http://127.0.0.1:5500

## Key Files Modified

- `engine/impact.py` (line 26) - Project ID
- `engine/teach.py` (line 54) - Project ID  
- `engine/generate_report.py` - New automatic report generation
- `engine/cli.py` - Updated with fallback report generation
- `ui/server.py` - Added report-data.js serving

## Expected Results

✅ MCP diagnostic: All 4 checks passing
✅ Impact analysis: 4 endpoints detected
✅ Report generation: Automatic
✅ UI display: Blast radius data shown

## Troubleshooting

**If MCP fails:**
- Check project ID in `.lgraph/config.json`
- Run `lgraph status` to verify connection
- Ensure LatentGraph daemon is running

**If UI shows no data:**
- Run `python -m engine.generate_report --old main --new demo-change`
- Refresh browser
- Check browser console for errors

**If port 5500 is busy:**
- Kill existing server process
- Or use different port in `ui/server.py`