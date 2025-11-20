"""
Test Ollama model without tools to see if the basic model works.
"""
import asyncio
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

async def test_simple():
    print("Testing Ollama model without tools...")
    print("=" * 60)
    
    try:
        # Create LLM without tools
        llm = ChatOllama(
            base_url="http://localhost:11434",
            model="gemini-3-pro-preview",
            temperature=0.7
        )
        
        # Simple test message
        messages = [HumanMessage(content="Hello! Can you respond with 'Yes, I'm working'?")]
        
        print("Sending simple message to model...")
        response = llm.invoke(messages)
        
        print(f"Response: {response.content}")
        print("=" * 60)
        print("SUCCESS! Model works without tools.")
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_simple())

