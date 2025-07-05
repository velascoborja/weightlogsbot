#!/usr/bin/env python3
"""Simple test script to verify bot functionality."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        import config
        print("✓ config imported")
        
        import database
        print("✓ database imported")
        
        import handlers
        print("✓ handlers imported")
        
        import jobs
        print("✓ jobs imported")
        
        import main
        print("✓ main imported")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_config():
    """Test configuration."""
    print("\nTesting configuration...")
    try:
        from config import validate_config
        validate_config()
        print("✓ Configuration valid")
        return True
    except Exception as e:
        print(f"✗ Configuration error: {e}")
        return False

def test_database():
    """Test database operations."""
    print("\nTesting database...")
    try:
        from database import init_db, save_weight, get_weights
        import datetime as dt
        
        init_db()
        print("✓ Database initialized")
        
        # Test save and retrieve
        test_user_id = 999999
        test_date = dt.date.today()
        test_weight = 70.5
        
        save_weight(test_user_id, test_date, test_weight)
        print("✓ Weight saved")
        
        weights = get_weights(test_user_id, test_date, test_date)
        if weights and weights[0][1] == test_weight:
            print("✓ Weight retrieved correctly")
            return True
        else:
            print("✗ Weight retrieval failed")
            return False
            
    except Exception as e:
        print(f"✗ Database error: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Bot Test Suite ===\n")
    
    tests = [
        ("Imports", test_imports),
        ("Configuration", test_config),
        ("Database", test_database),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
    
    print(f"\n=== Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All tests passed! Bot should work correctly.")
        print("\nTo run the bot:")
        print("1. Set your TELEGRAM_TOKEN environment variable")
        print("2. Run: python main.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 