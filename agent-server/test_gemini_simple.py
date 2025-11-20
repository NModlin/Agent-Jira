"""
Simple test to verify Gemini API works with tools.
"""
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from config import Config

@tool
def get_weather(location: str) -> str:
    """Get the weather for a location."""
    return f"The weather in {location} is sunny."

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model=Config.GEMINI_MODEL,
    google_api_key=Config.GOOGLE_API_KEY,
    temperature=0.7,
    convert_system_message_to_human=True
)

# Test 1: Simple message without tools
print("=" * 60)
print("Test 1: Simple message without tools")
print("=" * 60)
try:
    response = llm.invoke([HumanMessage(content="Hello, how are you?")])
    print(f"✓ Success: {response.content[:100]}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Message with tools bound
print("\n" + "=" * 60)
print("Test 2: Message with tools bound")
print("=" * 60)
try:
    llm_with_tools = llm.bind_tools([get_weather])
    response = llm_with_tools.invoke([HumanMessage(content="What's the weather in Paris?")])
    print(f"✓ Success: {response}")
except Exception as e:
    print(f"✗ Error: {e}")

