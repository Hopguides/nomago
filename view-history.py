#!/usr/bin/env python3
"""
View Bike History from Supabase
"""

import requests
import json
from datetime import datetime

ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"
API_URL = "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data"

def get_all_history(limit=1000):
    """Get all bike history"""
    response = requests.get(
        API_URL,
        params={'limit': limit},
        headers={'Authorization': f'Bearer {ANON_KEY}'}
    )
    return response.json()

def display_history():
    """Display bike history with statistics"""
    print("🚲 NOMAGO BIKE HISTORY - Four Points by Sheraton")
    print("=" * 70)

    data = get_all_history()

    if not data.get('success'):
        print(f"❌ Error: {data.get('error')}")
        return

    records = data.get('data', [])
    current = data.get('current')

    print(f"\n📊 CURRENT STATUS:")
    print(f"   Bikes: {current['bikes']}/{current['total']}")
    print(f"   Stands: {current['stands']}/{current['total']}")
    print(f"   Status: {current['status'].upper()}")

    if not records:
        print("\n⚠️  No historical records yet")
        return

    print(f"\n📈 STATISTICS:")
    print(f"   Total Records: {len(records)}")

    bikes = [r['available_bikes'] for r in records]
    print(f"   Average Bikes: {sum(bikes)/len(bikes):.1f}")
    print(f"   Min Bikes: {min(bikes)}")
    print(f"   Max Bikes: {max(bikes)}")

    empty = sum(1 for r in records if r['available_bikes'] == 0)
    full = sum(1 for r in records if r['available_stands'] == 0)

    print(f"\n⚠️  EVENTS:")
    print(f"   Empty Station (0 bikes): {empty} times ({empty/len(records)*100:.1f}%)")
    print(f"   Full Station (0 stands): {full} times ({full/len(records)*100:.1f}%)")

    print(f"\n⏱️  RECENT RECORDS (Last 10):")
    print("-" * 70)
    print(f"{'Timestamp':<25} {'Bikes':<10} {'Stands':<10} {'Status':<10}")
    print("-" * 70)

    for record in records[:10]:
        ts = datetime.fromisoformat(record['timestamp'].replace('Z', '+00:00'))
        ts_local = ts.strftime('%Y-%m-%d %H:%M:%S')

        bikes = record['available_bikes']
        stands = record['available_stands']

        if bikes == 0:
            status = "🔴 EMPTY"
        elif stands == 0:
            status = "🟠 FULL"
        else:
            status = "🟢 OK"

        print(f"{ts_local:<25} {bikes}/2        {stands}/2        {status}")

    print("-" * 70)
    print(f"\n📅 Period:")
    first = datetime.fromisoformat(records[-1]['timestamp'].replace('Z', '+00:00'))
    last = datetime.fromisoformat(records[0]['timestamp'].replace('Z', '+00:00'))
    print(f"   From: {first.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   To:   {last.strftime('%Y-%m-%d %H:%M:%S')}")

    duration = last - first
    print(f"   Duration: {duration}")

if __name__ == "__main__":
    display_history()
