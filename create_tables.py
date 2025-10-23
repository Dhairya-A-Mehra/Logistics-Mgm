"""
Script to manually create all database tables in Supabase
Run this if tables are not created automatically
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database import Base, engine
# Import all models to register them with Base
from src.models import (
    Customer, Warehouse, Vehicle, Order, Shipment,
    Inventory, VehicleTelemetry, FuelPrice, PackagingType,
    Document, AgentAuditLog
)

def create_tables():
    """Create all database tables"""
    print("\n" + "="*60)
    print("CREATING DATABASE TABLES")
    print("="*60 + "\n")
    
    try:
        print("Connecting to database...")
        
        # Create all tables
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ All tables created successfully!")
        print("\nTables created:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
        
        print("\n" + "="*60)
        print("NEXT STEPS:")
        print("="*60)
        print("1. Verify tables in Supabase Dashboard → Table Editor")
        print("2. Run: python verify_tables.py")
        print("3. Start server: uvicorn src.main:app --reload")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        print("\nPossible issues:")
        print("1. Check DATABASE_URL in .env file")
        print("2. Verify Supabase credentials")
        print("3. Ensure network connection to Supabase")
        print("4. Check if tables already exist")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    create_tables()
