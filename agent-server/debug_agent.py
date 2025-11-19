import asyncio
import os
os.environ["LANGCHAIN_TRACING_V2"] = "false"

from agent import agent_app
from langchain_core.messages import HumanMessage

async def test():
    try:
        print("Invoking agent...")
        result = await agent_app.ainvoke({
            "messages": [HumanMessage(content="Show me unassigned tickets")]
        })
        print("Result:", result)
    except Exception as e:
        print("Error caught in test:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test())
