import asyncio
import sys
from mcp_client import mcp_client

async def list_resources():
    try:
        resources = await mcp_client.list_resources()
        print("Available MCP Resources:")
        print("=" * 60)
        for resource in resources:
            print(f"\nResource: {resource.name}")
            print(f"URI: {resource.uri}")
            print(f"Description: {resource.description}")
            if hasattr(resource, 'mimeType'):
                print(f"MIME Type: {resource.mimeType}")
        print("=" * 60)
        print(f"\nTotal resources: {len(resources)}")
    except Exception as e:
        print(f"Error listing resources: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(list_resources())

