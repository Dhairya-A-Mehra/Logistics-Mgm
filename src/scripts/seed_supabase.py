"""
Updated Supabase seeding script with:
1. Removed hashed_password dependency
2. Better foreign key handling
3. Improved error recovery
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from supabase import create_client, Client

# Configuration
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
ENV_PATH = BASE_DIR / ".env"
BATCH_SIZE = 500

# Load environment
load_dotenv(dotenv_path=ENV_PATH)

# Standardized environment variables
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
# Accept either SUPABASE_SERVICE_ROLE_KEY or SUPABASE_SERVICE_KEY (some setups use the shorter name)
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv(
    "SUPABASE_SERVICE_KEY"
)

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Missing Supabase credentials in .env file")
    print("   Required variables:")
    print("   - NEXT_PUBLIC_SUPABASE_URL")
    print("   - SUPABASE_SERVICE_ROLE_KEY")
    sys.exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL.strip(), SUPABASE_KEY.strip())


def load_json(name: str) -> List[Dict[str, Any]]:
    """Load JSON data from file"""
    p = DATA_DIR / f"{name}.json"
    if not p.exists():
        print(f"⚠️  Missing dataset: {p}")
        return []
    return json.loads(p.read_text(encoding="utf-8"))


def batched(rows: List[Dict[str, Any]], size: int = BATCH_SIZE):
    """Batch data for efficient processing"""
    for i in range(0, len(rows), size):
        yield rows[i : i + size]


def safe_upsert(table: str, rows: List[Dict[str, Any]], on_conflict: str | None = None):
    """Safe upsert with error handling and schema validation"""
    if not rows:
        return

    # Get table schema to filter valid columns
    try:
        res = supabase.table(table).select("*").limit(1).execute()
        valid_columns = set(res.data[0].keys()) if res.data else set()
    except Exception as e:
        print(f"⚠️  Could not get schema for {table}: {str(e)}")
        valid_columns = set()

    for chunk in batched(rows):
        # Filter out invalid columns
        filtered_chunk = []
        for row in chunk:
            filtered_row = {
                k: v for k, v in row.items() if not valid_columns or k in valid_columns
            }
            filtered_chunk.append(filtered_row)

        try:
            if on_conflict:
                res = (
                    supabase.table(table)
                    .upsert(filtered_chunk, on_conflict=on_conflict)
                    .execute()
                )
            else:
                res = supabase.table(table).upsert(filtered_chunk).execute()

            if getattr(res, "error", None):
                print(f"❌ Error upserting into {table}: {res.error}")
                print(
                    f"   First failed row: {json.dumps(filtered_chunk[0], indent=2) if filtered_chunk else '[]'}"
                )
                # Try to continue with next batch
                continue
        except Exception as e:
            print(f"❌ Error upserting into {table}: {str(e)}")
            continue


def seed_customers(customers: List[Dict[str, Any]]):
    """Special handling for customer seeding"""
    if not customers:
        return
    # Get a list of valid columns from the table to avoid sending unknown fields
    try:
        schema_res = supabase.table("customers").select("*").limit(1).execute()
        valid_columns = set(schema_res.data[0].keys()) if schema_res.data else set()
    except Exception as e:
        print(f"⚠️  Could not get schema for customers: {str(e)}")
        valid_columns = set()

    for customer in customers:
        try:
            # Remove hashed_password if present
            customer.pop("hashed_password", None)

            # Filter out any keys not present in the table schema
            if valid_columns:
                filtered = {k: v for k, v in customer.items() if k in valid_columns}
            else:
                filtered = dict(customer)

            # First try normal upsert by customer_id
            res = (
                supabase.table("customers")
                .upsert(filtered, on_conflict="customer_id")
                .execute()
            )

            if getattr(res, "error", None):
                # Handle email conflicts (unique constraint)
                if (
                    getattr(res, "error", None)
                    and getattr(res.error, "code", "") == "23505"
                    and "email" in str(res.error)
                ):
                    # Find existing customer with this email
                    existing = (
                        supabase.table("customers")
                        .select("customer_id")
                        .eq("email", customer.get("email"))
                        .execute()
                    )

                    if existing.data:
                        # Update existing record instead
                        filtered["customer_id"] = existing.data[0]["customer_id"]
                        res = (
                            supabase.table("customers")
                            .upsert(filtered, on_conflict="customer_id")
                            .execute()
                        )

                if getattr(res, "error", None):
                    print(
                        f"❌ Failed to upsert customer {customer.get('email')}: {res.error}"
                    )
        except Exception as e:
            print(f"❌ Error processing customer {customer.get('email')}: {str(e)}")


def main():
    """Main seeding function with proper order and error handling"""
    # Load all datasets
    datasets = {
        "customers": load_json("customers"),
        "warehouses": load_json("warehouses"),
        "vehicles": load_json("vehicles"),
        "packaging_types": load_json("packaging_types"),
        "orders": load_json("orders"),
        "shipments": load_json("shipments"),
        "inventory": load_json("inventory"),
        "fuel_prices": load_json("fuel_prices"),
        "vehicle_telemetry": load_json("vehicle_telemetry"),
        "documents": load_json("documents"),
    }

    print("\nSeeding base tables...")
    seed_customers(datasets["customers"])
    safe_upsert("warehouses", datasets["warehouses"], on_conflict="warehouse_id")
    safe_upsert("vehicles", datasets["vehicles"], on_conflict="vehicle_id")
    safe_upsert(
        "packaging_types", datasets["packaging_types"], on_conflict="packaging_id"
    )
    safe_upsert("fuel_prices", datasets["fuel_prices"], on_conflict="fuel_type")

    print("\nSeeding dependent tables...")
    safe_upsert("orders", datasets["orders"], on_conflict="order_id")
    safe_upsert("shipments", datasets["shipments"], on_conflict="shipment_id")
    safe_upsert("inventory", datasets["inventory"], on_conflict="inventory_id")

    print("\nSeeding telemetry and documents...")
    safe_upsert("vehicle_telemetry", datasets["vehicle_telemetry"])
    safe_upsert("documents", datasets["documents"], on_conflict="doc_id")

    print("\n✅ Supabase seeding complete!")


if __name__ == "__main__":
    main()
