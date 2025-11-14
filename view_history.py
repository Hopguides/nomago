#!/usr/bin/env python3
"""
View historical data for Four Points station
"""

import csv
import os
from datetime import datetime
from collections import Counter

DATA_FILE = "four_points_history.csv"

def load_history():
    """Load historical data from CSV"""
    if not os.path.isfile(DATA_FILE):
        print(f"❌ Datoteka {DATA_FILE} ne obstaja")
        print("💡 Najprej zaženi: python3 monitor_four_points.py --once")
        return []

    records = []
    with open(DATA_FILE, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            records.append({
                'timestamp': row['timestamp'],
                'bikes': int(row['available_bikes']),
                'stands': int(row['available_stands']),
                'total': int(row['total_stands'])
            })

    return records

def display_statistics(records):
    """Display statistics from historical data"""
    if not records:
        print("📊 Ni zgodovinskih podatkov")
        return

    print("\n🚲 NOMAGO - Four Points by Sheraton (Zgodovinski podatki)")
    print("=" * 70)
    print()

    # Basic info
    print(f"📅 Obdobje:")
    print(f"   Od: {records[0]['timestamp']}")
    print(f"   Do: {records[-1]['timestamp']}")
    print(f"   Število meritev: {len(records)}")
    print()

    # Bike availability statistics
    bike_counts = [r['bikes'] for r in records]
    avg_bikes = sum(bike_counts) / len(bike_counts)
    min_bikes = min(bike_counts)
    max_bikes = max(bike_counts)

    print(f"📊 Statistika razpoložljivosti koles:")
    print(f"   Povprečje: {avg_bikes:.1f} koles")
    print(f"   Minimum: {min_bikes} koles")
    print(f"   Maksimum: {max_bikes} koles")
    print()

    # Frequency distribution
    bike_distribution = Counter(bike_counts)
    print(f"📈 Porazdelitev:")
    for bikes in sorted(bike_distribution.keys()):
        count = bike_distribution[bikes]
        percentage = (count / len(records)) * 100
        bar = "█" * int(percentage / 2)
        print(f"   {bikes} koles: {bar} {percentage:.1f}% ({count}x)")
    print()

    # Status distribution
    empty_count = sum(1 for r in records if r['bikes'] == 0)
    full_count = sum(1 for r in records if r['stands'] == 0)

    empty_pct = (empty_count / len(records)) * 100
    full_pct = (full_count / len(records)) * 100

    print(f"⚠️  Problematični dogodki:")
    print(f"   🔴 Prazna postaja (0 koles): {empty_count}x ({empty_pct:.1f}%)")
    print(f"   🟠 Polna postaja (0 mest): {full_count}x ({full_pct:.1f}%)")
    print()

def display_recent(records, limit=20):
    """Display recent entries"""
    print("\n⏱️  ZADNJIH MERITEV:")
    print("=" * 70)
    print(f"{'Čas':<20} {'Status':<12} {'Kolesa':<10} {'Mesta':<10}")
    print("-" * 70)

    for record in records[-limit:]:
        bikes = record['bikes']
        stands = record['stands']
        total = record['total']

        # Status
        if bikes == 0:
            status = "🔴 PRAZNO"
        elif stands == 0:
            status = "🟠 POLNO"
        elif bikes >= 2:
            status = "🟢 OK"
        else:
            status = "🟡 NIZKO"

        print(f"{record['timestamp']:<20} {status:<12} {bikes}/{total:<8} {stands}/{total:<8}")

    print()

def display_all(records):
    """Display all records"""
    print("\n📋 VSE MERITVE:")
    print("=" * 70)
    print(f"{'#':<5} {'Čas':<20} {'Kolesa':<10} {'Mesta':<10}")
    print("-" * 70)

    for idx, record in enumerate(records, 1):
        bikes = record['bikes']
        stands = record['stands']
        total = record['total']

        print(f"{idx:<5} {record['timestamp']:<20} {bikes}/{total:<8} {stands}/{total:<8}")

    print()

if __name__ == "__main__":
    import sys

    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    records = load_history()

    if records:
        display_statistics(records)

        if len(sys.argv) > 1 and sys.argv[1] == "--all":
            display_all(records)
        else:
            display_recent(records, limit=20)

            if len(records) > 20:
                print(f"💡 Za vse meritve uporabi: python3 view_history.py --all")
                print()
