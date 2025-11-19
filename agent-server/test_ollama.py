"""
Quick test script to verify Ollama is working with LangChain.
Run this before starting the full agent server.
"""
import sys
import requests
from config import Config

def test_ollama_connection():
    """Test if Ollama is running and accessible."""
    print("🔍 Testing Ollama connection...")
    
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama is running at {Config.OLLAMA_BASE_URL}")
            
            # List available models
            models = response.json().get('models', [])
            if models:
                print(f"\n📦 Available models:")
                for model in models:
                    print(f"   - {model['name']}")
            else:
                print("\n⚠️  No models found. Please run: ollama pull llama3.1")
                return False
            
            return True
        else:
            print(f"❌ Ollama returned status code: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to Ollama at {Config.OLLAMA_BASE_URL}")
        print("\nPlease make sure Ollama is running:")
        print("  - Windows: Start Ollama from the Start menu")
        print("  - Mac/Linux: Run 'ollama serve' in a terminal")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def test_ollama_model():
    """Test if the configured model is available."""
    print(f"\n🔍 Testing model: {Config.OLLAMA_MODEL}...")
    
    try:
        response = requests.get(f"{Config.OLLAMA_BASE_URL}/api/tags", timeout=5)
        models = response.json().get('models', [])
        model_names = [m['name'] for m in models]
        
        # Check if the configured model exists (with or without :latest tag)
        model_found = False
        for name in model_names:
            if Config.OLLAMA_MODEL in name or name.startswith(Config.OLLAMA_MODEL + ':'):
                model_found = True
                print(f"✅ Model '{Config.OLLAMA_MODEL}' is available")
                break
        
        if not model_found:
            print(f"❌ Model '{Config.OLLAMA_MODEL}' not found")
            print(f"\nPlease download it:")
            print(f"  ollama pull {Config.OLLAMA_MODEL}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking model: {str(e)}")
        return False


def test_langchain_ollama():
    """Test LangChain integration with Ollama."""
    print("\n🔍 Testing LangChain integration...")
    
    try:
        from langchain_community.chat_models import ChatOllama
        from langchain_core.messages import HumanMessage
        
        # Create a simple chat model
        llm = ChatOllama(
            base_url=Config.OLLAMA_BASE_URL,
            model=Config.OLLAMA_MODEL,
            temperature=0.7
        )
        
        print(f"✅ LangChain ChatOllama initialized")
        
        # Test a simple query
        print("\n💬 Testing with a simple query...")
        print("   Query: 'Say hello in one sentence'")
        
        response = llm.invoke([HumanMessage(content="Say hello in one sentence")])
        
        print(f"   Response: {response.content}")
        print("\n✅ LangChain integration working!")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        print("\nPlease install langchain-community:")
        print("  pip install langchain-community")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Ollama + LangChain Test Suite")
    print("=" * 60)
    print()
    
    # Test 1: Ollama connection
    if not test_ollama_connection():
        print("\n❌ Ollama connection test failed")
        sys.exit(1)
    
    # Test 2: Model availability
    if not test_ollama_model():
        print("\n❌ Model availability test failed")
        sys.exit(1)
    
    # Test 3: LangChain integration
    if not test_langchain_ollama():
        print("\n❌ LangChain integration test failed")
        sys.exit(1)
    
    # All tests passed
    print("\n" + "=" * 60)
    print("✅ All tests passed! Ollama is ready to use.")
    print("=" * 60)
    print("\nYou can now start the agent server:")
    print("  python app.py")
    print()


if __name__ == "__main__":
    main()

