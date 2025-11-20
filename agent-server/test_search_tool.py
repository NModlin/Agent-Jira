import asyncio
import sys
from mcp_client import mcp_client
import json

async def test_search():
    try:
        print("Testing searchIssues tool...")
        print("=" * 60)
        
        jql = "project = HD AND assignee IS EMPTY AND status != Done ORDER BY created DESC"
        
        result = await mcp_client.call_tool("searchIssues", {
            "jql": jql,
            "fields": "summary,priority,created",
            "maxResults": 10
        })
        
        print(f"Result type: {type(result)}")
        print(f"Result: {result}")
        print("=" * 60)
        
        if hasattr(result, 'content'):
            print(f"Content: {result.content}")
            if result.content:
                print(f"First content item: {result.content[0]}")
                if hasattr(result.content[0], 'text'):
                    print(f"Text: {result.content[0].text}")
                    data = json.loads(result.content[0].text)
                    print(f"Parsed data: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_search())

