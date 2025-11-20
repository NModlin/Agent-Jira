import asyncio
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Import the tool
from mcp_tools import get_unassigned_queue

async def test():
    print("Testing get_unassigned_queue tool directly...")
    print("=" * 60)

    try:
        # The @tool decorator wraps the function, so we need to invoke it
        result = await get_unassigned_queue.ainvoke({})
        print(f"Result: {result}")
        print("=" * 60)
        print("SUCCESS!")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())

