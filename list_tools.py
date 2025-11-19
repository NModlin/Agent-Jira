import asyncio
import logging
import sys
import os

# Add agent-server to path
sys.path.append(os.path.join(os.getcwd(), 'agent-server'))

# Configure logging
logging.basicConfig(level=logging.INFO)

from mcp_client import mcp_client

async def main():
    print("Listing tools...")
    try:
        tools = await mcp_client.list_tools()
        print(f"Found {len(tools)} tools:")
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")
            print(f"  Schema: {tool.inputSchema}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
