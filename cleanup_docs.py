"""
Script to clean up temporary and irrelevant documentation files
Keeps only essential files
"""
import os
from pathlib import Path

# Files to DELETE (temporary/troubleshooting docs)
files_to_delete = [
    "BCRYPT_FIX.md",
    "BCRYPT_VERSION_FIX.md",
    "NETWORK_ISSUE_FIX.md",
    "PERMISSIONS_CLARIFICATION.md",
    "PERMISSIONS_UPDATED.md",
    "ROLE_SETUP_GUIDE.md",
    "SIMPLIFIED_ROLES.md",
    "DATABASE_MODELS_COMPLETE.md",
    "fix_bcrypt.ps1",
    "test_imports.py",
]

# Files to KEEP (essential)
files_to_keep = [
    "README.md",
    "FINAL_PERMISSIONS.md",
    "SYNC_MODELS_TO_SUPABASE.md",
    "INSTALL_PGVECTOR.md",
    "requirements.txt",
    ".env",
    ".env.example",
    ".gitignore",
    "LICENSE",
    "create_admin.py",
    "create_tables.py",
    "verify_tables.py",
    "test_db_connection.py",
]

def cleanup():
    """Remove temporary documentation files"""
    root_dir = Path(__file__).parent
    
    print("\n" + "="*60)
    print("CLEANING UP TEMPORARY FILES")
    print("="*60 + "\n")
    
    deleted_count = 0
    
    for filename in files_to_delete:
        file_path = root_dir / filename
        if file_path.exists():
            try:
                os.remove(file_path)
                print(f"✅ Deleted: {filename}")
                deleted_count += 1
            except Exception as e:
                print(f"❌ Error deleting {filename}: {e}")
        else:
            print(f"⏭️  Skipped: {filename} (not found)")
    
    print("\n" + "="*60)
    print(f"CLEANUP COMPLETE - {deleted_count} files deleted")
    print("="*60)
    
    print("\nRemaining essential files:")
    print("-" * 60)
    for filename in files_to_keep:
        file_path = root_dir / filename
        if file_path.exists():
            print(f"  ✓ {filename}")
    
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    response = input("Are you sure you want to delete temporary files? (yes/no): ")
    if response.lower() in ['yes', 'y']:
        cleanup()
    else:
        print("\nCleanup cancelled.")
