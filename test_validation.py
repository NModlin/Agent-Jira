"""
Test configuration validation
Verifies that missing required variables are caught
"""
import sys
import os

def test_jira_validation():
    """Test that Jira Tool Server validation catches missing JIRA_PROJECT"""
    print("\n" + "="*60)
    print("TESTING JIRA TOOL SERVER VALIDATION")
    print("="*60)
    
    # Save original env
    original_project = os.environ.get('JIRA_PROJECT')
    
    try:
        # Remove JIRA_PROJECT from environment
        if 'JIRA_PROJECT' in os.environ:
            del os.environ['JIRA_PROJECT']
        
        # Clear cached modules
        if 'config' in sys.modules:
            del sys.modules['config']
        
        # Change to jira-tool-server directory
        os.chdir('jira-tool-server')
        sys.path.insert(0, os.getcwd())
        
        print("\n[TEST] Importing config without JIRA_PROJECT...")
        from config import Config
        
        print(f"JIRA_PROJECT value: {Config.JIRA_PROJECT}")
        
        if Config.JIRA_PROJECT is None:
            print("✅ JIRA_PROJECT is None (as expected)")
        
        print("\n[TEST] Running validation (should fail)...")
        try:
            Config.validate()
            print("❌ Validation passed when it should have failed!")
            return False
        except ValueError as e:
            print(f"✅ Validation correctly failed: {e}")
            if 'JIRA_PROJECT' in str(e):
                print("✅ Error message mentions JIRA_PROJECT")
                return True
            else:
                print("❌ Error message doesn't mention JIRA_PROJECT")
                return False
                
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Restore original env
        if original_project:
            os.environ['JIRA_PROJECT'] = original_project
        os.chdir('..')
        if sys.path and sys.path[0].endswith('jira-tool-server'):
            sys.path.pop(0)


def test_config_loading():
    """Test that configuration loads correctly with all variables"""
    print("\n" + "="*60)
    print("TESTING CONFIGURATION LOADING")
    print("="*60)
    
    # Set JIRA_PROJECT
    os.environ['JIRA_PROJECT'] = 'TEST_PROJECT'
    
    # Clear cached modules
    if 'config' in sys.modules:
        del sys.modules['config']
    
    # Change to jira-tool-server directory
    os.chdir('jira-tool-server')
    sys.path.insert(0, os.getcwd())
    
    try:
        print("\n[TEST] Importing config with JIRA_PROJECT set...")
        from config import Config
        
        print(f"JIRA_PROJECT value: {Config.JIRA_PROJECT}")
        
        if Config.JIRA_PROJECT == 'TEST_PROJECT':
            print("✅ JIRA_PROJECT loaded correctly")
        else:
            print(f"❌ JIRA_PROJECT has wrong value: {Config.JIRA_PROJECT}")
            return False
        
        print("\n[TEST] Running validation (should pass)...")
        try:
            Config.validate()
            print("✅ Validation passed")
            return True
        except ValueError as e:
            print(f"❌ Validation failed: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        os.chdir('..')
        if sys.path and sys.path[0].endswith('jira-tool-server'):
            sys.path.pop(0)


def main():
    """Run validation tests"""
    print("\n" + "="*60)
    print("CONFIGURATION VALIDATION TESTS")
    print("="*60)
    
    results = []
    
    # Test validation catches missing variables
    results.append(("Validation catches missing JIRA_PROJECT", test_jira_validation()))
    
    # Test configuration loads correctly
    results.append(("Configuration loads with all variables", test_config_loading()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 ALL VALIDATION TESTS PASSED!")
        return 0
    else:
        print("\n⚠️  SOME VALIDATION TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())

