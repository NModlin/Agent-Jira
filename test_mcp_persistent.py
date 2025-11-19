"""
Test persistent connection to Atlassian MCP server.
This maintains a single stdio connection for multiple requests.
"""
import subprocess
import json
import time
import threading


class MCPClient:
    def __init__(self, container_name):
        self.container_name = container_name
        self.process = None
        self.initialized = False
        self.request_id = 0
        
    def start(self):
        """Start the MCP server process."""
        cmd = ["docker", "exec", "-i", self.container_name, "mcp-atlassian"]
        self.process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        print("✅ MCP server process started")
        
        # Start stderr reader thread
        def read_stderr():
            for line in self.process.stderr:
                print(f"[STDERR] {line.rstrip()}")
        
        stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        stderr_thread.start()
        
    def send_request(self, method, params=None):
        """Send a JSON-RPC request and read response."""
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        print(f"\n📤 Sending: {method}")
        print(f"   Request: {json.dumps(request, indent=2)}")
        
        # Send request
        request_json = json.dumps(request) + "\n"
        self.process.stdin.write(request_json)
        self.process.stdin.flush()
        
        # Read response
        response_line = self.process.stdout.readline()
        if response_line:
            try:
                response = json.loads(response_line)
                print(f"📥 Response: {json.dumps(response, indent=2)}")
                return response
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse response: {response_line}")
                print(f"   Error: {e}")
                return None
        else:
            print("❌ No response received")
            return None
    
    def send_notification(self, method, params=None):
        """Send a JSON-RPC notification (no response expected)."""
        notification = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {}
        }

        print(f"\n📤 Sending notification: {method}")
        notification_json = json.dumps(notification) + "\n"
        self.process.stdin.write(notification_json)
        self.process.stdin.flush()

    def initialize(self):
        """Initialize the MCP session."""
        response = self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })

        if response and "result" in response:
            # Send initialized notification
            self.send_notification("notifications/initialized", {})
            time.sleep(0.5)  # Give server time to process
            self.initialized = True
            print("✅ MCP session initialized")
            return response["result"]
        else:
            print("❌ Failed to initialize")
            return None
    
    def list_tools(self):
        """List available tools."""
        if not self.initialized:
            print("❌ Session not initialized")
            return None
        
        response = self.send_request("tools/list", {})
        if response and "result" in response:
            return response["result"]
        return None
    
    def call_tool(self, name, arguments):
        """Call a tool."""
        if not self.initialized:
            print("❌ Session not initialized")
            return None
        
        response = self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
        if response and "result" in response:
            return response["result"]
        return None
    
    def close(self):
        """Close the connection."""
        if self.process:
            self.process.stdin.close()
            self.process.terminate()
            self.process.wait(timeout=5)
            print("✅ MCP connection closed")


def main():
    print("=" * 70)
    print("Testing Persistent MCP Connection to Atlassian MCP Server")
    print("=" * 70)
    
    client = MCPClient("b6d58f3d1f5d")
    
    try:
        # Start connection
        print("\n1️⃣  Starting MCP server process...")
        client.start()
        time.sleep(1)
        
        # Initialize
        print("\n2️⃣  Initializing MCP session...")
        init_result = client.initialize()
        if not init_result:
            print("❌ Initialization failed, exiting")
            return
        
        print(f"\n   Server: {init_result.get('serverInfo', {}).get('name')}")
        print(f"   Version: {init_result.get('serverInfo', {}).get('version')}")
        
        # List tools
        print("\n3️⃣  Listing available tools...")
        tools_result = client.list_tools()
        if tools_result and "tools" in tools_result:
            tools = tools_result["tools"]
            print(f"\n   Found {len(tools)} tools:")
            for tool in tools:
                print(f"   - {tool.get('name')}: {tool.get('description', 'No description')}")
                if "inputSchema" in tool:
                    print(f"     Parameters: {list(tool['inputSchema'].get('properties', {}).keys())}")
        
        # Try calling a tool
        print("\n4️⃣  Testing jira_search tool...")
        result = client.call_tool("jira_search", {
            "jql": "project = HD AND type = Bug",
            "limit": 3
        })
        
        if result:
            print("\n   ✅ Tool call successful!")
            print(f"   Result: {json.dumps(result, indent=2)[:500]}...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n5️⃣  Closing connection...")
        client.close()


if __name__ == "__main__":
    main()

