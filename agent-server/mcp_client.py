import asyncio
import logging
import os
import traceback
from contextlib import asynccontextmanager
from typing import Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)

# Docker container name for the Atlassian MCP server
MCP_CONTAINER = "friendly_goldberg"

class MCPClient:
    _instance = None
    _session: Optional[ClientSession] = None
    _exit_stack = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MCPClient, cls).__new__(cls)
        return cls._instance

    @asynccontextmanager
    async def get_session(self):
        """
        Get a session to the MCP server.
        This manages the connection lifecycle.
        """
        # If we already have a session, yield it (simplified for now, 
        # ideally we'd check if it's still active)
        # For this implementation, we'll create a new connection per request 
        # to ensure stability, as keeping stdio open can be tricky in some envs.
        # Optimization: Implement persistent connection if latency is high.
        
        server_params = StdioServerParameters(
            command="docker",
            args=["exec", "-i", MCP_CONTAINER, "mcp-atlassian"],
            env=None # Inherit env
        )
        
        logger.info(f"Executing: docker exec -i {MCP_CONTAINER} mcp-atlassian")
        
        try:
            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    yield session
        except Exception as e:
            logger.error(f"Error connecting to MCP server: {e}")
            traceback.print_exc()
            raise

    async def list_tools(self):
        """List available tools from the MCP server."""
        async with self.get_session() as session:
            result = await session.list_tools()
            return result.tools

    async def call_tool(self, name: str, arguments: dict):
        """Call a tool on the MCP server."""
        logger.info(f"Calling MCP tool: {name} with arguments: {arguments}")
        async with self.get_session() as session:
            result = await session.call_tool(name, arguments)
            logger.info(f"MCP tool returned: {result}")
            return result

# Global client instance
mcp_client = MCPClient()
