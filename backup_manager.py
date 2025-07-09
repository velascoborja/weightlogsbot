"""Backup manager for SQLite database using Supabase Storage."""

import os
import shutil
import tempfile
from datetime import datetime
from typing import Optional

try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

from config import DB_FILE

class BackupManager:
    """Manages database backups to Supabase Storage."""
    
    def __init__(self):
        from config import SUPABASE_URL, SUPABASE_ANON_KEY
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_ANON_KEY
        self.bucket_name = "weightlogs-backups"
        
        if SUPABASE_AVAILABLE and self.supabase_url and self.supabase_key:
            self.supabase: Optional[Client] = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            print("⚠️ Supabase not configured. Backups will be disabled.")
    
    def create_backup(self) -> Optional[str]:
        """Create a backup of the database and upload to Supabase."""
        if not self.supabase or not os.path.exists(DB_FILE):
            return None
        
        try:
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"weights_backup_{timestamp}.db"
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as temp_file:
                temp_path = temp_file.name
            
            # Copy database to temp file
            shutil.copy2(DB_FILE, temp_path)
            
            # Upload to Supabase Storage
            with open(temp_path, 'rb') as f:
                self.supabase.storage.from_(self.bucket_name).upload(
                    path=backup_filename,
                    file=f,
                    file_options={"content-type": "application/x-sqlite3"}
                )
            
            # Clean up temp file
            os.unlink(temp_path)
            
            print(f"✅ Backup created: {backup_filename}")
            return backup_filename
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    def restore_latest_backup(self) -> bool:
        """Restore the latest backup from Supabase Storage."""
        if not self.supabase:
            return False
        
        try:
            # List all backups
            backups = self.supabase.storage.from_(self.bucket_name).list()
            
            if not backups:
                print("ℹ️ No backups found")
                return False
            
            # Find the latest backup
            backup_files = [f for f in backups if f.startswith("weights_backup_")]
            if not backup_files:
                print("ℹ️ No backup files found")
                return False
            
            # Sort by timestamp (newest first)
            backup_files.sort(reverse=True)
            latest_backup = backup_files[0]
            
            print(f"📥 Restoring from: {latest_backup}")
            
            # Download backup
            response = self.supabase.storage.from_(self.bucket_name).download(latest_backup)
            
            # Create database directory if needed
            os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
            
            # Write backup to database file
            with open(DB_FILE, 'wb') as f:
                f.write(response)
            
            print(f"✅ Restored from: {latest_backup}")
            return True
            
        except Exception as e:
            print(f"❌ Restore failed: {e}")
            return False
    
    def list_backups(self) -> list:
        """List all available backups."""
        if not self.supabase:
            return []
        
        try:
            backups = self.supabase.storage.from_(self.bucket_name).list()
            backup_files = [f for f in backups if f.startswith("weights_backup_")]
            backup_files.sort(reverse=True)
            return backup_files
        except Exception as e:
            print(f"❌ Failed to list backups: {e}")
            return []

def auto_backup():
    """Create automatic backup if Supabase is configured."""
    manager = BackupManager()
    if manager.supabase:
        return manager.create_backup()
    return None

def restore_if_needed():
    """Restore from backup if database doesn't exist."""
    if not os.path.exists(DB_FILE):
        print("📥 Database not found, attempting to restore from backup...")
        manager = BackupManager()
        return manager.restore_latest_backup()
    return False 