#!/usr/bin/env python3
"""Test script for Supabase configuration."""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import SUPABASE_URL, SUPABASE_ANON_KEY

def test_supabase_config():
    """Test Supabase configuration."""
    print("🔧 Testing Supabase Configuration")
    print("=" * 40)
    
    # Check if environment variables are set
    print(f"SUPABASE_URL: {'✅ Set' if SUPABASE_URL else '❌ Not set'}")
    print(f"SUPABASE_ANON_KEY: {'✅ Set' if SUPABASE_ANON_KEY else '❌ Not set'}")
    
    if not SUPABASE_URL or not SUPABASE_ANON_KEY:
        print("\n❌ Supabase credentials not configured!")
        print("Please set the following environment variables:")
        print("  SUPABASE_URL=your_supabase_project_url")
        print("  SUPABASE_ANON_KEY=your_supabase_anon_key")
        return False
    
    # Try to import and test Supabase connection
    try:
        from supabase import create_client, Client
        
        print("\n🔌 Testing Supabase connection...")
        supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
        
        # Test storage access
        print("📦 Testing storage access...")
        bucket_name = "weightlogs-backups"
        
        # Try to list buckets (this will fail if bucket doesn't exist, but connection works)
        try:
            buckets = supabase.storage.list_buckets()
            print(f"✅ Found {len(buckets)} buckets")
            
            # Check if our bucket exists
            bucket_exists = any(bucket.name == bucket_name for bucket in buckets)
            if bucket_exists:
                print(f"✅ Bucket '{bucket_name}' exists")
            else:
                print(f"⚠️ Bucket '{bucket_name}' not found - you need to create it")
                print("   Go to Supabase Dashboard → Storage → Create bucket")
                print(f"   Bucket name: {bucket_name}")
                print("   Make it public (for file uploads)")
        except Exception as e:
            print(f"⚠️ Could not list buckets: {e}")
            print("   This might be normal if the bucket doesn't exist yet")
        
        print("\n✅ Supabase connection successful!")
        return True
        
    except ImportError:
        print("\n❌ Supabase library not installed!")
        print("Run: pip install supabase")
        return False
    except Exception as e:
        print(f"\n❌ Supabase connection failed: {e}")
        return False

def main():
    """Main test function."""
    success = test_supabase_config()
    
    if success:
        print("\n🎉 Supabase is ready to use!")
        print("Your bot will now automatically backup the database.")
    else:
        print("\n⚠️ Please configure Supabase before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main() 