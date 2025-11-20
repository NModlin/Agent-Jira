"""
Test Ollama model WITH tools to see if tool calling is the issue.
"""
import asyncio
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain.tools import tool

@tool
def simple_test_tool(message: str) -> str:
    """A simple test tool that echoes the message."""
    return f"Echo: {message}"

async def test_with_tools():
    print("Testing Ollama model WITH tools...")
    print("=" * 60)
    
    try:
        # Create LLM
        llm = ChatOllama(
            base_url="http://localhost:11434",
            model="gemini-3-pro-preview",
            temperature=0.7
        )
        
        # Bind tools to LLM
        print("Binding tools to LLM...")
        llm_with_tools = llm.bind_tools([simple_test_tool])
        
        # Simple test message
        messages = [HumanMessage(content="Use the simple_test_tool to echo 'Hello World'")]
        
        print("Sending message with tool request...")
        response = llm_with_tools.invoke(messages)
        
        print(f"Response: {response}")
        print(f"Tool calls: {response.tool_calls if hasattr(response, 'tool_calls') else 'None'}")
        print("=" * 60)
        print("SUCCESS! Model works with tools.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_tools())

