#!/usr/bin/env python3
"""
Nomago Four Points Station Monitor
Real-time monitoring with historical data storage
"""

import json
import csv
import time
from datetime import datetime
import subprocess
import sys
import os

# Configuration
API_URL = "https://api.ontime.si/api/v1/nomago-bike/"
STATION_NAME = "Four Points by Sheraton Ljubljana Mons"
DATA_FILE = "four_points_history.csv"
INTERVAL = 300  # 5 minutes (in seconds)

def fetch_station_data():
    """Fetch current station data from API"""
    try:
        result = subprocess.run(
            ['curl', '-s', API_URL],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)

            # Find Four Points station
            for station in data['results']:
                if STATION_NAME in station['location_name']:
                    return station

        return None
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def save_to_history(station_data):
    """Save station data to CSV file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Check if file exists to write header
    file_exists = os.path.isfile(DATA_FILE)

    with open(DATA_FILE, 'a', newline='') as csvfile:
        fieldnames = ['timestamp', 'available_bikes', 'available_stands', 'total_stands', 'api_timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            'timestamp': timestamp,
            'available_bikes': station_data['available_bikes'],
            'available_stands': station_data['available_stands'],
            'total_stands': station_data['total_stands'],
            'api_timestamp': station_data['created_date']
        })

def display_status(station_data):
    """Display current station status"""
    bikes = station_data['available_bikes']
    stands = station_data['available_stands']
    total = station_data['total_stands']

    # Status indicator
    if bikes == 0:
        status = "🔴 PRAZNO"
    elif stands == 0:
        status = "🟠 POLNO"
    elif bikes >= 5:
        status = "🟢 ODLIČNO"
    elif bikes >= 2:
        status = "🟡 ZMERNO"
    else:
        status = "🟡 NIZKO"

    timestamp = datetime.now().strftime("%H:%M:%S")

    print(f"[{timestamp}] {status} | 🚲 Kolesa: {bikes}/{total} | 🅿️ Mesta: {stands}/{total}")

def monitor_continuous():
    """Continuously monitor station"""
    print("🚲 NOMAGO MONITOR - Four Points by Sheraton Ljubljana Mons")
    print("=" * 70)
    print(f"📊 Interval: {INTERVAL} sekund ({INTERVAL//60} minut)")
    print(f"💾 Zgodovina: {DATA_FILE}")
    print("⏹️  Ustavi: Ctrl+C")
    print("=" * 70)
    print()

    try:
        while True:
            station = fetch_station_data()

            if station:
                display_status(station)
                save_to_history(station)
            else:
                print(f"❌ [{datetime.now().strftime('%H:%M:%S')}] Napaka pri pridobivanju podatkov")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n\n✅ Spremljanje ustavljeno")
        print(f"📁 Zgodovinski podatki: {DATA_FILE}")

def monitor_once():
    """Single check of station status"""
    print("🚲 NOMAGO POSTAJA - Four Points by Sheraton Ljubljana Mons")
    print("=" * 70)

    station = fetch_station_data()

    if station:
        print()
        display_status(station)
        save_to_history(station)
        print()
        print(f"✅ Podatki shranjeni v: {DATA_FILE}")
    else:
        print("❌ Napaka pri pridobivanju podatkov")

    print()

if __name__ == "__main__":
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) > 1 and sys.argv[1] == "--once":
        monitor_once()
    else:
        monitor_continuous()
