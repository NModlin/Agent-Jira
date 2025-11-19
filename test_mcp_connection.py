"""
Test script to connect to the Atlassian MCP server running in Docker.
"""
import subprocess
import json
import sys


def send_mcp_request(container_name, request):
    """Send a JSON-RPC request to the MCP server."""
    cmd = ["docker", "exec", "-i", container_name, "mcp-atlassian"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send request
        request_json = json.dumps(request) + "\n"
        stdout, stderr = process.communicate(input=request_json, timeout=10)
        
        print(f"STDERR: {stderr}")
        print(f"STDOUT: {stdout}")
        
        # Parse responses
        for line in stdout.split("\n"):
            if line.strip() and line.startswith("{"):
                try:
                    response = json.loads(line)
                    print(f"\nParsed response: {json.dumps(response, indent=2)}")
                except json.JSONDecodeError as e:
                    print(f"Failed to parse line: {line}")
                    print(f"Error: {e}")
        
        return stdout
        
    except subprocess.TimeoutExpired:
        process.kill()
        print("Request timed out")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def main():
    container_name = "friendly_goldberg"
    
    print("=" * 60)
    print("Testing Atlassian MCP Server Connection")
    print("=" * 60)
    
    # Step 1: Initialize
    print("\n1. Sending initialize request...")
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    send_mcp_request(container_name, init_request)
    
    # Step 2: List tools
    print("\n2. Sending tools/list request...")
    tools_request = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    send_mcp_request(container_name, tools_request)


if __name__ == "__main__":
    main()

