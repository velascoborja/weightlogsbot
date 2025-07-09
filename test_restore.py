#!/usr/bin/env python3
"""Test script for database restoration."""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import DB_FILE
from backup_manager import restore_if_needed, BackupManager

def test_restore():
    """Test database restoration."""
    print("🔄 Testing Database Restoration")
    print("=" * 40)
    
    # Check if database exists
    if os.path.exists(DB_FILE):
        file_size = os.path.getsize(DB_FILE)
        print(f"📊 Current database: {DB_FILE}")
        print(f"📏 File size: {file_size:,} bytes")
        
        # Backup current database
        print("\n💾 Creating backup of current database...")
        manager = BackupManager()
        backup_file = manager.create_backup()
        if backup_file:
            print(f"✅ Backup created: {backup_file}")
        else:
            print("❌ Backup failed")
    else:
        print("📊 No database file found")
    
    # Remove database file to simulate fresh deploy
    if os.path.exists(DB_FILE):
        print(f"\n🗑️ Removing database file: {DB_FILE}")
        os.remove(DB_FILE)
        print("✅ Database file removed")
    
    # Test restoration
    print("\n📥 Testing restoration...")
    success = restore_if_needed()
    
    if success:
        print("✅ Restoration successful!")
        
        # Check restored database
        if os.path.exists(DB_FILE):
            file_size = os.path.getsize(DB_FILE)
            print(f"📊 Restored database: {DB_FILE}")
            print(f"📏 File size: {file_size:,} bytes")
            
            # Test database connection
            try:
                import sqlite3
                conn = sqlite3.connect(DB_FILE)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM weights")
                count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(DISTINCT user_id) FROM weights")
                users = cursor.fetchone()[0]
                conn.close()
                
                print(f"📈 Records in database: {count}")
                print(f"👥 Unique users: {users}")
                
                if count > 0:
                    print("🎉 Database restoration successful with data!")
                else:
                    print("⚠️ Database restored but no data found")
                    
            except Exception as e:
                print(f"❌ Error reading restored database: {e}")
        else:
            print("❌ Database file not found after restoration")
    else:
        print("❌ Restoration failed")

def main():
    """Main test function."""
    test_restore()

if __name__ == "__main__":
    main() 