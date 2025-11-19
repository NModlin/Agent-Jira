"""
MCP Client for connecting to Atlassian MCP server running in Docker.
This replaces the direct Jira API integration with MCP protocol.
"""
import asyncio
import subprocess
import json
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class MCPClient:
    """Client for interacting with Atlassian MCP server via Docker."""
    
    def __init__(self, container_name: str = "friendly_goldberg"):
        """
        Initialize MCP client.
        
        Args:
            container_name: Name or ID of the Docker container running MCP server
        """
        self.container_name = container_name
        self.available_tools = []
        
    async def initialize(self):
        """Initialize connection and discover available tools."""
        try:
            # List available tools from MCP server
            tools = await self._call_mcp_method("tools/list", {})
            self.available_tools = tools.get("tools", [])
            logger.info(f"Discovered {len(self.available_tools)} MCP tools")
            for tool in self.available_tools:
                logger.info(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize MCP client: {e}")
            return False
    
    async def _call_mcp_method(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP method via Docker exec.
        
        Args:
            method: MCP method name (e.g., "tools/list", "tools/call")
            params: Method parameters
            
        Returns:
            Response from MCP server
        """
        # Create JSON-RPC request
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }
        
        # Execute via docker exec with stdin
        cmd = [
            "docker", "exec", "-i", self.container_name,
            "mcp-atlassian"
        ]
        
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Send request
            request_json = json.dumps(request) + "\n"
            stdout, stderr = await process.communicate(input=request_json.encode())
            
            if process.returncode != 0:
                error_msg = stderr.decode() if stderr else "Unknown error"
                raise Exception(f"MCP call failed: {error_msg}")
            
            # Parse response
            response_text = stdout.decode().strip()
            if not response_text:
                raise Exception("Empty response from MCP server")
            
            # Handle multiple JSON objects (MCP may send multiple responses)
            lines = response_text.split("\n")
            for line in lines:
                if line.strip():
                    try:
                        response = json.loads(line)
                        if "result" in response:
                            return response["result"]
                        elif "error" in response:
                            raise Exception(f"MCP error: {response['error']}")
                    except json.JSONDecodeError:
                        continue
            
            raise Exception("No valid response found")
            
        except Exception as e:
            logger.error(f"Error calling MCP method {method}: {e}")
            raise
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Call an MCP tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
            
        Returns:
            Tool result
        """
        params = {
            "name": tool_name,
            "arguments": arguments
        }
        
        result = await self._call_mcp_method("tools/call", params)
        return result
    
    async def search_jira_issues(self, jql: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search Jira issues using JQL.
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results
            
        Returns:
            List of issues
        """
        result = await self.call_tool("jira_search_issues", {
            "jql": jql,
            "maxResults": max_results
        })
        return result.get("content", [])
    
    async def get_jira_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Get a specific Jira issue.
        
        Args:
            issue_key: Issue key (e.g., "PROJ-123")
            
        Returns:
            Issue details
        """
        result = await self.call_tool("jira_get_issue", {
            "issueKey": issue_key
        })
        return result.get("content", {})


# Global MCP client instance
mcp_client = MCPClient()

