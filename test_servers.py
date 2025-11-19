"""
Test script for AgentJira servers
Tests configuration, imports, and basic functionality
"""
import sys
import os

def test_jira_tool_server():
    """Test Jira Tool Server configuration and imports"""
    print("\n" + "="*60)
    print("TESTING JIRA TOOL SERVER")
    print("="*60)
    
    # Change to jira-tool-server directory
    os.chdir('jira-tool-server')
    sys.path.insert(0, os.getcwd())
    
    try:
        # Test 1: Import config
        print("\n[TEST 1] Importing config...")
        from config import Config
        print("✅ Config imported successfully")
        
        # Test 2: Check configuration values
        print("\n[TEST 2] Checking configuration values...")
        print(f"  JIRA_URL: {Config.JIRA_URL}")
        print(f"  JIRA_PROJECT: {Config.JIRA_PROJECT}")
        print(f"  JIRA_STORY_POINTS_FIELD: {Config.JIRA_STORY_POINTS_FIELD}")
        print(f"  FLASK_PORT: {Config.FLASK_PORT}")
        print(f"  FLASK_DEBUG: {Config.FLASK_DEBUG}")
        
        if Config.JIRA_PROJECT:
            print("✅ JIRA_PROJECT is configured")
        else:
            print("⚠️  JIRA_PROJECT is not set (will fail validation)")
        
        if Config.JIRA_STORY_POINTS_FIELD == 'customfield_10016':
            print("✅ JIRA_STORY_POINTS_FIELD has default value")
        else:
            print(f"ℹ️  JIRA_STORY_POINTS_FIELD is custom: {Config.JIRA_STORY_POINTS_FIELD}")
        
        # Test 3: Validate configuration
        print("\n[TEST 3] Validating configuration...")
        try:
            Config.validate()
            print("✅ Configuration validation passed")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
        
        # Test 4: Import JiraClient
        print("\n[TEST 4] Importing JiraClient...")
        from jira_client import JiraClient
        print("✅ JiraClient imported successfully")
        
        # Test 5: Import Flask app
        print("\n[TEST 5] Importing Flask app...")
        from app import app
        print("✅ Flask app imported successfully")
        
        print("\n" + "="*60)
        print("✅ JIRA TOOL SERVER: ALL TESTS PASSED")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir('..')
        sys.path.pop(0)


def test_agent_server():
    """Test Agent Server configuration and imports"""
    print("\n" + "="*60)
    print("TESTING AGENT SERVER")
    print("="*60)

    # Change to agent-server directory
    os.chdir('agent-server')

    # Clear any cached config module
    if 'config' in sys.modules:
        del sys.modules['config']

    sys.path.insert(0, os.getcwd())

    try:
        # Test 1: Import config
        print("\n[TEST 1] Importing config...")
        import config
        AgentConfig = config.Config
        print("✅ Config imported successfully")
        
        # Test 2: Check configuration values
        print("\n[TEST 2] Checking configuration values...")
        print(f"  LLM_PROVIDER: {AgentConfig.LLM_PROVIDER}")
        print(f"  OLLAMA_BASE_URL: {AgentConfig.OLLAMA_BASE_URL}")
        print(f"  OLLAMA_MODEL: {AgentConfig.OLLAMA_MODEL}")
        print(f"  FLASK_PORT: {AgentConfig.FLASK_PORT}")
        print(f"  FLASK_DEBUG: {AgentConfig.FLASK_DEBUG}")
        print(f"  JIRA_TOOL_SERVER_URL: {AgentConfig.JIRA_TOOL_SERVER_URL}")

        if AgentConfig.LLM_PROVIDER == 'ollama':
            print("✅ LLM_PROVIDER defaults to 'ollama' (correct)")
        else:
            print(f"ℹ️  LLM_PROVIDER is set to: {AgentConfig.LLM_PROVIDER}")

        # Test 3: Validate configuration
        print("\n[TEST 3] Validating configuration...")
        try:
            AgentConfig.validate()
            print("✅ Configuration validation passed")
        except ValueError as e:
            print(f"❌ Configuration validation failed: {e}")
            return False
        
        # Test 4: Import agent
        print("\n[TEST 4] Importing agent...")
        from agent import agent_app
        print(f"✅ Agent imported successfully")
        print(f"  Agent type: {type(agent_app).__name__}")
        
        # Test 5: Import Flask app
        print("\n[TEST 5] Importing Flask app...")
        from app import app
        print("✅ Flask app imported successfully")
        
        print("\n" + "="*60)
        print("✅ AGENT SERVER: ALL TESTS PASSED")
        print("="*60)
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir('..')
        sys.path.pop(0)


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AGENTJIRA SERVER TESTS")
    print("="*60)
    
    results = []
    
    # Test Jira Tool Server
    results.append(("Jira Tool Server", test_jira_tool_server()))
    
    # Test Agent Server
    results.append(("Agent Server", test_agent_server()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())

