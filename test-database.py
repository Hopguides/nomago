#!/usr/bin/env python3
"""
Test Supabase Database Connection
Verifies bike_history table exists and can be queried
"""

import requests
import json
import os
import sys

# Configuration
PROJECT_REF = "raavrcsgqeekhjpjxzlt"
SUPABASE_URL = f"https://{PROJECT_REF}.supabase.co"
REST_API_URL = f"{SUPABASE_URL}/rest/v1/bike_history"

def test_database():
    """Test database access and table structure"""
    print("🗄️  Testing Supabase Database")
    print("=" * 60)

    anon_key = os.environ.get('SUPABASE_ANON_KEY')

    if not anon_key:
        print("\n❌ SUPABASE_ANON_KEY not set")
        print("\n📋 Get ANON KEY from:")
        print("   https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/settings/api")
        print("\n🔧 Then run:")
        print("   SUPABASE_ANON_KEY=your_key python3 test-database.py")
        return

    print(f"\n✅ Using ANON KEY from environment")
    print(f"📍 API URL: {REST_API_URL}")

    headers = {
        'apikey': anon_key,
        'Authorization': f'Bearer {anon_key}',
        'Content-Type': 'application/json'
    }

    # Test 1: Check table access
    print("\n" + "=" * 60)
    print("TEST 1: Table Access")
    print("=" * 60)

    try:
        response = requests.get(
            f"{REST_API_URL}?select=*&limit=1",
            headers=headers,
            timeout=10
        )

        print(f"Status: {response.status_code}")

        if response.status_code == 200:
            print("✅ Table accessible")

            data = response.json()
            if data:
                print(f"✅ Table has data ({len(data)} record(s) returned)")
                print(f"\nSample record:")
                print(json.dumps(data[0], indent=2, default=str))
            else:
                print("⚠️  Table is empty (no records yet)")

        elif response.status_code == 401:
            print("❌ Unauthorized - check ANON KEY")
        elif response.status_code == 404:
            print("❌ Table 'bike_history' not found - run supabase-setup.sql")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"❌ Request failed: {e}")

    # Test 2: Count records
    print("\n" + "=" * 60)
    print("TEST 2: Record Count")
    print("=" * 60)

    try:
        response = requests.get(
            f"{REST_API_URL}?select=count",
            headers={**headers, 'Prefer': 'count=exact'},
            timeout=10
        )

        if response.status_code == 200:
            count = response.headers.get('Content-Range', '0').split('/')[-1]
            print(f"✅ Total records: {count}")

    except Exception as e:
        print(f"❌ Count failed: {e}")

    # Test 3: Recent records
    print("\n" + "=" * 60)
    print("TEST 3: Recent Records (Last 5)")
    print("=" * 60)

    try:
        response = requests.get(
            f"{REST_API_URL}?select=timestamp,available_bikes,available_stands,total_stands&order=timestamp.desc&limit=5",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data:
                print(f"✅ Found {len(data)} recent records:\n")
                for record in data:
                    print(f"   {record['timestamp']}: {record['available_bikes']}/{record['total_stands']} bikes")
            else:
                print("⚠️  No records found")

    except Exception as e:
        print(f"❌ Query failed: {e}")

    # Test 4: Table schema
    print("\n" + "=" * 60)
    print("TEST 4: Table Schema")
    print("=" * 60)

    try:
        # Get one record to see all columns
        response = requests.get(
            f"{REST_API_URL}?select=*&limit=1",
            headers=headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            if data:
                print("✅ Table columns:")
                for key in data[0].keys():
                    print(f"   - {key}")
            else:
                print("⚠️  Cannot verify schema (no records)")
                print("   Expected columns:")
                print("   - id, timestamp, available_bikes, available_stands")
                print("   - total_stands, station_id, created_at")

    except Exception as e:
        print(f"❌ Schema check failed: {e}")

    print("\n" + "=" * 60)
    print("✅ Database tests complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_database()
