"""
Test Ollama model with multiple tools to see if the number of tools is the issue.
"""
import asyncio
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain.tools import tool

@tool
async def tool1(message: str) -> str:
    """Tool 1 description."""
    return f"Tool1: {message}"

@tool
async def tool2(message: str) -> str:
    """Tool 2 description."""
    return f"Tool2: {message}"

@tool
async def tool3(message: str) -> str:
    """Tool 3 description."""
    return f"Tool3: {message}"

@tool
async def tool4(message: str) -> str:
    """Tool 4 description."""
    return f"Tool4: {message}"

@tool
async def tool5(message: str) -> str:
    """Tool 5 description."""
    return f"Tool5: {message}"

@tool
async def tool6(message: str) -> str:
    """Tool 6 description."""
    return f"Tool6: {message}"

async def test_with_multiple_tools():
    print("Testing Ollama model with 6 tools...")
    print("=" * 60)
    
    try:
        # Create LLM
        llm = ChatOllama(
            base_url="http://localhost:11434",
            model="gemini-3-pro-preview",
            temperature=0.7
        )
        
        # Bind 6 tools to LLM
        tools = [tool1, tool2, tool3, tool4, tool5, tool6]
        print(f"Binding {len(tools)} tools to LLM...")
        llm_with_tools = llm.bind_tools(tools)
        
        # Simple test message
        messages = [HumanMessage(content="Use tool1 to echo 'Hello'")]
        
        print("Sending message with tool request...")
        response = llm_with_tools.invoke(messages)
        
        print(f"Response content: {response.content}")
        print(f"Tool calls: {response.tool_calls if hasattr(response, 'tool_calls') else 'None'}")
        print("=" * 60)
        print("SUCCESS! Model works with 6 tools.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_multiple_tools())

