import sys
import json
import subprocess
import os

def run_mcp_command(project_id, tool_name, args):
    # We must pass the project_id explicitly since it's required for the tool calls
    args["project_id"] = project_id
    
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": args
        }
    }
    
    # Needs a newline at the end of the JSON payload for standard JSON-RPC over stdio
    payload_str = json.dumps(payload) + "\n"
    
    env = os.environ.copy()
    env["LGRAPH_PROJECT_ID"] = project_id
    
    process = subprocess.Popen(
        ["npx.cmd", "@latentforce/latentgraph@1.0.68"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env
    )
    
    stdout_data, stderr_data = process.communicate(input=payload_str)
    
    # Let's print out the raw data for debugging
    print(f"RAW MCP STDOUT:\n{stdout_data}", file=sys.stderr)
    print(f"RAW MCP STDERR:\n{stderr_data}", file=sys.stderr)
    
    # The output might have warning prefixes, we need to extract the JSON line
    for line in stdout_data.split('\n'):
        if line.startswith('{'):
            try:
                response = json.loads(line)
                if response.get("error") or response.get("result", {}).get("isError"):
                    return {"status": "error", "message": str(response)}
                return {"status": "success", "data": response["result"]["content"][0]["text"]}
            except json.JSONDecodeError:
                continue
    
    return {"status": "error", "message": "Failed to parse MCP response"}
