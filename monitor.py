import requests
import json
import os
from datetime import datetime

# Railway PostgreSQL connection
# Try multiple possible environment variable names
DATABASE_URL = (
    os.environ.get('DATABASE_URL') or
    os.environ.get('DATABASE_PRIVATE_URL') or
    os.environ.get('POSTGRES_URL')
)

def fetch_nomago_data():
    """Fetch current bike availability"""
    url = "https://api.ontime.si/api/v1/nomago-bike/"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Find Four Points station (ID: 458645919)
        # API returns data in 'results' array
        results = data.get('results', [])
        station = next((s for s in results if s.get('station_id') == 458645919), None)

        if station:
            return {
                'timestamp': datetime.now().isoformat(),
                'available_bikes': station.get('available_bikes', 0),
                'available_stands': station.get('available_stands', 0),
                'total_stands': station.get('total_stands', 2),
                'station_id': station.get('station_id')
            }
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return None

def save_to_db(data):
    """Save to PostgreSQL"""
    if not DATABASE_URL:
        print("⚠️  No DATABASE_URL - saving to JSON fallback")
        save_to_json(data)
        return

    import psycopg2

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create table if not exists
        cur.execute('''
            CREATE TABLE IF NOT EXISTS bike_history (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                available_bikes INTEGER,
                available_stands INTEGER,
                total_stands INTEGER,
                station_id BIGINT
            )
        ''')

        # Insert data
        cur.execute('''
            INSERT INTO bike_history
            (timestamp, available_bikes, available_stands, total_stands, station_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (
            data['timestamp'],
            data['available_bikes'],
            data['available_stands'],
            data['total_stands'],
            data['station_id']
        ))

        conn.commit()
        cur.close()
        conn.close()

        print(f"✅ [{data['timestamp']}] Saved: {data['available_bikes']}/{data['total_stands']} bikes")

    except Exception as e:
        print(f"❌ DB Error: {e}")
        save_to_json(data)

def save_to_json(data):
    """Fallback: save to JSON file"""
    filename = 'nomago_history.json'

    try:
        # Read existing data
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                history = json.load(f)
        else:
            history = []

        # Append new data
        history.append(data)

        # Write back
        with open(filename, 'w') as f:
            json.dump(history, f, indent=2)

        print(f"✅ [{data['timestamp']}] Saved to JSON: {data['available_bikes']}/{data['total_stands']} bikes")

    except Exception as e:
        print(f"❌ JSON Error: {e}")

if __name__ == "__main__":
    print("🚲 NOMAGO Monitor - Railway")
    print("=" * 50)

    # Debug: Check environment variables
    print(f"\n🔍 DEBUG INFO:")
    print(f"DATABASE_URL exists: {'Yes' if DATABASE_URL else 'No'}")
    if DATABASE_URL:
        # Show masked URL for security
        masked_url = DATABASE_URL[:20] + "***" + DATABASE_URL[-10:] if len(DATABASE_URL) > 30 else "***"
        print(f"DATABASE_URL value: {masked_url}")

    # Check individual variables
    print(f"\nChecking specific variables:")
    for var in ['DATABASE_URL', 'DATABASE_PRIVATE_URL', 'POSTGRES_URL']:
        val = os.environ.get(var)
        if val:
            val_preview = val[:15] + "***" if len(val) > 15 else val
            print(f"  {var}: {val_preview} (length: {len(val)})")
        else:
            print(f"  {var}: NOT SET")

    # Show all DATABASE* env vars (masked)
    db_vars = {k: v for k, v in os.environ.items() if k.startswith('DATABASE') or k.startswith('PG') or k.startswith('POSTGRES')}
    print(f"\nFound {len(db_vars)} database-related env variables:")
    for key, value in db_vars.items():
        val_len = len(value) if value else 0
        print(f"  - {key} (length: {val_len})")

    print("=" * 50)
    print()

    data = fetch_nomago_data()
    if data:
        save_to_db(data)
    else:
        print("❌ Failed to fetch data")
