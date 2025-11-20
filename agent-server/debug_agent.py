import asyncio
import os
import sys
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from agent import agent_app
from langchain_core.messages import HumanMessage

async def test():
    try:
        print("=" * 60, flush=True)
        print("DEBUG: Starting agent test...", flush=True)
        print("=" * 60, flush=True)

        result = await agent_app.ainvoke({
            "messages": [HumanMessage(content="Show me unassigned tickets")]
        })

        print("\n" + "=" * 60, flush=True)
        print("DEBUG: Agent completed successfully!", flush=True)
        print("=" * 60, flush=True)
        print(f"Result: {result}", flush=True)

    except Exception as e:
        print("\n" + "=" * 60, flush=True)
        print("ERROR: Exception caught in test:", flush=True)
        print("=" * 60, flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test())
