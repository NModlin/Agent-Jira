import asyncio
import sys
from mcp_client import mcp_client

async def list_tools():
    try:
        tools = await mcp_client.list_tools()
        print("Available MCP Tools:")
        print("=" * 60)
        for tool in tools:
            print(f"\nTool: {tool.name}")
            print(f"Description: {tool.description}")
            if hasattr(tool, 'inputSchema'):
                print(f"Input Schema: {tool.inputSchema}")
        print("=" * 60)
        print(f"\nTotal tools: {len(tools)}")
    except Exception as e:
        print(f"Error listing tools: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_tools())

