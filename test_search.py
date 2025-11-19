import asyncio
import logging
import sys
import os
import json

# Add agent-server to path
sys.path.append(os.path.join(os.getcwd(), 'agent-server'))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from mcp_client import mcp_client

async def main():
    print("Testing jira_search tool...")
    try:
        jql = "project = HD AND type = Bug"
        print(f"JQL: {jql}")
        
        result = await mcp_client.call_tool("jira_search", {
            "jql": jql,
            "limit": 5
        })
        
        print(f"Result type: {type(result)}")
        print(f"Result content: {result.content}")
        
        if result.content:
            print(f"First content item text: {result.content[0].text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
