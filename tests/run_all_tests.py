#!/usr/bin/env python3
"""Main test runner for all tests."""

import sys
import os
import subprocess
import importlib.util

def run_test_file(test_file):
    """Run a specific test file."""
    print(f"\n{'='*60}")
    print(f"Running: {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def main():
    """Run all test files in the tests directory."""
    print("🧪 Running All Tests for Telegram Weight Tracker Bot")
    print("="*60)
    
    # Get all test files
    test_dir = os.path.dirname(os.path.abspath(__file__))
    test_files = [
        "test_bot.py",
        "test_database.py", 
        "test_diario.py"
    ]
    
    # Filter to only existing files
    existing_tests = []
    for test_file in test_files:
        test_path = os.path.join(test_dir, test_file)
        if os.path.exists(test_path):
            existing_tests.append(test_path)
        else:
            print(f"⚠️  Test file not found: {test_file}")
    
    if not existing_tests:
        print("❌ No test files found!")
        return 1
    
    # Run all tests
    passed = 0
    total = len(existing_tests)
    
    for test_file in existing_tests:
        if run_test_file(test_file):
            passed += 1
            print(f"✅ {os.path.basename(test_file)} passed")
        else:
            print(f"❌ {os.path.basename(test_file)} failed")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Test Summary: {passed}/{total} test suites passed")
    print('='*60)
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run.")
        print("\nTo start the bot:")
        print("1. Set your TELEGRAM_TOKEN environment variable")
        print("2. Run: python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 