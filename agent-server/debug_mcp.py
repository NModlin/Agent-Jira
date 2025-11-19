import asyncio
import logging

logging.basicConfig(level=logging.INFO)

from mcp_client import mcp_client

async def main():
    print("Testing jira_search from agent-server directory...")
    try:
        result = await mcp_client.call_tool("jira_search", {
            "jql": "project = HD AND type = Bug",
            "limit": 5
        })
        
        print(f"Result: {result.content}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())

