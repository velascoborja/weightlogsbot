#!/usr/bin/env python3
"""Test script for database language functionality."""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tempfile
from database import init_db, save_user_language, get_user_language
from config import DB_FILE, DB_DIR

def test_language_database():
    """Test the language preference database functionality."""
    print("Testing language preference database...")
    
    # Initialize database
    init_db()
    print("✓ Database initialized with user_preferences table")
    
    # Test saving and retrieving language preferences
    test_user_id = 12345
    
    # Test default language (should be 'es')
    default_lang = get_user_language(test_user_id)
    print(f"✓ Default language for new user: {default_lang}")
    assert default_lang == 'es', f"Expected 'es', got '{default_lang}'"
    
    # Test saving English preference
    save_user_language(test_user_id, 'en')
    saved_lang = get_user_language(test_user_id)
    print(f"✓ Saved and retrieved English: {saved_lang}")
    assert saved_lang == 'en', f"Expected 'en', got '{saved_lang}'"
    
    # Test saving Spanish preference
    save_user_language(test_user_id, 'es')
    saved_lang = get_user_language(test_user_id)
    print(f"✓ Saved and retrieved Spanish: {saved_lang}")
    assert saved_lang == 'es', f"Expected 'es', got '{saved_lang}'"
    
    # Test with another user
    test_user_id_2 = 67890
    save_user_language(test_user_id_2, 'en')
    lang_2 = get_user_language(test_user_id_2)
    print(f"✓ Second user language: {lang_2}")
    assert lang_2 == 'en', f"Expected 'en', got '{lang_2}'"
    
    # Verify first user's language is still correct
    lang_1_again = get_user_language(test_user_id)
    print(f"✓ First user language unchanged: {lang_1_again}")
    assert lang_1_again == 'es', f"Expected 'es', got '{lang_1_again}'"
    
    print("✅ All language database tests passed!")
    return True

if __name__ == "__main__":
    try:
        test_language_database()
        print("\n🎉 Language database test passed!")
    except Exception as e:
        print(f"\n❌ Language database test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
