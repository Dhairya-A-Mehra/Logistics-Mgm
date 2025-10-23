"""
Script to verify all tables are created in Supabase
Run this after starting the server to check table creation
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.database import engine
from sqlalchemy import inspect, text

def verify_tables():
    """Verify all tables exist in the database"""
    print("\n" + "="*60)
    print("VERIFYING DATABASE TABLES")
    print("="*60 + "\n")
    
    try:
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful\n")
        
        # Get inspector
        inspector = inspect(engine)
        
        # Expected tables
        expected_tables = [
            'customers',
            'warehouses',
            'vehicles',
            'orders',
            'shipments',
            'inventory',
            'vehicle_telemetry',
            'fuel_prices',
            'packaging_types',
            'documents',
            'agent_audit_logs'
        ]
        
        # Get actual tables
        actual_tables = inspector.get_table_names(schema='public')
        
        print(f"Expected tables: {len(expected_tables)}")
        print(f"Found tables: {len(actual_tables)}\n")
        
        # Check each expected table
        print("Table Status:")
        print("-" * 60)
        
        missing_tables = []
        for table in expected_tables:
            if table in actual_tables:
                # Get column count
                columns = inspector.get_columns(table, schema='public')
                print(f"✅ {table:<25} ({len(columns)} columns)")
            else:
                print(f"❌ {table:<25} (MISSING)")
                missing_tables.append(table)
        
        print("-" * 60)
        
        # Summary
        if missing_tables:
            print(f"\n⚠️  {len(missing_tables)} table(s) missing:")
            for table in missing_tables:
                print(f"   - {table}")
            print("\nTo create missing tables:")
            print("1. Start the server: uvicorn src.main:app --reload")
            print("2. Or run: python create_tables.py")
        else:
            print("\n✅ All tables created successfully!")
        
        # Show additional tables (if any)
        extra_tables = [t for t in actual_tables if t not in expected_tables]
        if extra_tables:
            print(f"\nAdditional tables found: {len(extra_tables)}")
            for table in extra_tables:
                print(f"   - {table}")
        
        print("\n" + "="*60)
        
        # Show detailed info for one table as example
        if 'customers' in actual_tables:
            print("\nExample: 'customers' table structure:")
            print("-" * 60)
            columns = inspector.get_columns('customers', schema='public')
            for col in columns:
                col_type = str(col['type'])
                nullable = "NULL" if col['nullable'] else "NOT NULL"
                print(f"  {col['name']:<20} {col_type:<20} {nullable}")
            print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Database credentials are correct in .env file")
        print("2. Supabase project is accessible")
        print("3. Database URL is properly formatted")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    verify_tables()
