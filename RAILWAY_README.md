# 🚲 Nomago Railway Monitor

Real-time monitoring of Nomago bike station at **Four Points by Sheraton Ljubljana Mons** with PostgreSQL storage on Railway.

## 🎯 Overview

This service automatically fetches bike availability data every 10 minutes and stores it in a PostgreSQL database for historical tracking and analysis.

**Monitored Station:**
- **Name:** Four Points by Sheraton Ljubljana Mons
- **Station ID:** 458645919
- **Location:** 46.052252, 14.45303
- **Capacity:** 2 bikes

## 🚂 Railway Deployment

### Prerequisites
1. Railway account ([railway.app](https://railway.app))
2. GitHub repository with this code

### Setup Instructions

#### 1. Create New Project on Railway
```bash
railway login
railway init
```

#### 2. Add PostgreSQL Database
1. Go to your Railway project dashboard
2. Click **"New"** → **"Database"** → **"PostgreSQL"**
3. Railway will auto-create `DATABASE_URL` environment variable

#### 3. Deploy the Service
```bash
# Link to Railway project
railway link

# Deploy
railway up
```

#### 4. Configure Cron Job
Railway doesn't have built-in cron, so use one of these options:

**Option A: Railway Cron Service (Recommended)**
1. Create `railway.json`:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. Create `Procfile`:
```
worker: while true; do python3 monitor.py; sleep 600; done
```

**Option B: External Cron Service**
Use [cron-job.org](https://cron-job.org) or similar to trigger:
```
*/10 * * * * curl https://your-railway-app.up.railway.app/trigger
```

**Option C: GitHub Actions**
Create `.github/workflows/cron.yml`:
```yaml
name: Nomago Monitor Cron
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
  workflow_dispatch:

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests psycopg2-binary
      - name: Run monitor
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: python3 monitor.py
```

## 📊 Database Schema

The `bike_history` table is auto-created on first run:

```sql
CREATE TABLE bike_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    available_bikes INTEGER,
    available_stands INTEGER,
    total_stands INTEGER,
    station_id BIGINT
);
```

### Sample Data
```sql
SELECT * FROM bike_history ORDER BY timestamp DESC LIMIT 5;
```

| id  | timestamp           | available_bikes | available_stands | total_stands | station_id |
|-----|---------------------|-----------------|------------------|--------------|------------|
| 123 | 2025-11-14 15:08:21 | 2               | 0                | 2            | 458645919  |
| 122 | 2025-11-14 15:00:00 | 1               | 1                | 2            | 458645919  |
| 121 | 2025-11-14 14:50:00 | 0               | 2                | 2            | 458645919  |

## 🔧 Environment Variables

| Variable | Description | Auto-set by Railway |
|----------|-------------|---------------------|
| `DATABASE_URL` | PostgreSQL connection string | ✅ Yes (when PostgreSQL added) |

**Format:**
```
postgresql://user:password@host:port/database
```

## 📦 Dependencies

Create `requirements.txt`:
```
requests==2.31.0
psycopg2-binary==2.9.9
```

Install locally:
```bash
pip install -r requirements.txt
```

## 🧪 Local Testing

### Without Database (JSON fallback)
```bash
python3 monitor.py
```
Data will be saved to `nomago_history.json`

### With Local PostgreSQL
```bash
# Install PostgreSQL locally
brew install postgresql  # macOS
# or
sudo apt install postgresql  # Linux

# Create database
createdb nomago

# Set DATABASE_URL
export DATABASE_URL="postgresql://localhost/nomago"

# Run monitor
python3 monitor.py
```

## 📈 Querying Historical Data

### Total Records
```sql
SELECT COUNT(*) FROM bike_history;
```

### Average Availability
```sql
SELECT
    AVG(available_bikes) as avg_bikes,
    MIN(available_bikes) as min_bikes,
    MAX(available_bikes) as max_bikes
FROM bike_history;
```

### Empty Station Frequency
```sql
SELECT
    COUNT(*) as times_empty,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM bike_history), 2) as percentage
FROM bike_history
WHERE available_bikes = 0;
```

### Full Station Frequency
```sql
SELECT
    COUNT(*) as times_full,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM bike_history), 2) as percentage
FROM bike_history
WHERE available_stands = 0;
```

### Hourly Trends
```sql
SELECT
    EXTRACT(HOUR FROM timestamp) as hour,
    AVG(available_bikes) as avg_bikes,
    COUNT(*) as readings
FROM bike_history
GROUP BY hour
ORDER BY hour;
```

### Last 24 Hours
```sql
SELECT
    timestamp,
    available_bikes,
    available_stands
FROM bike_history
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;
```

## 🔍 Monitoring & Debugging

### Check Railway Logs
```bash
railway logs
```

### Test Monitor Script
```bash
# On Railway
railway run python3 monitor.py

# Locally
python3 monitor.py
```

### Connect to Railway PostgreSQL
```bash
# Get DATABASE_URL
railway variables

# Connect with psql
railway connect postgres
```

## 🛠️ File Structure

```
nomago/
├── monitor.py                    # Main Railway monitor script
├── requirements.txt              # Python dependencies
├── railway.json                  # Railway config (optional)
├── Procfile                      # Railway process definition
├── RAILWAY_README.md            # This file
│
├── monitor_four_points.py       # Alternative: Local CSV monitor
├── view_history.py              # CSV history viewer
├── nomago-bikes.json            # All 168 stations data
└── ljubljana-postaje.txt        # Ljubljana stations list
```

## 🚀 API Reference

**Endpoint:** `https://api.ontime.si/api/v1/nomago-bike/`

**Response:**
```json
{
  "count": 168,
  "next": null,
  "previous": null,
  "results": [
    {
      "station_id": 458645919,
      "location_name": "Four Points by Sheraton Ljubljana Mons",
      "created_date": "2025-11-14T14:48:10.370896+01:00",
      "lat": 46.052252,
      "lng": 14.45303,
      "available_bikes": 2,
      "available_stands": 0,
      "total_stands": 2
    }
  ]
}
```

## ⚠️ Known Issues & Solutions

### Issue: SSL Certificate Error
**Solution:** Use `requests.get()` with proper SSL verification (already implemented)

### Issue: API Rate Limiting
**Solution:** Monitor runs every 10 minutes (144 requests/day) - well within limits

### Issue: Database Connection Timeout
**Solution:** Script includes retry logic and JSON fallback

### Issue: Missing Data Points
**Solution:** Check Railway logs for errors:
```bash
railway logs --tail 100
```

## 📊 Expected Data Volume

- **Per Record:** ~100 bytes
- **Per Day:** 144 records × 100 bytes = ~14 KB
- **Per Month:** ~420 KB
- **Per Year:** ~5 MB

Railway's free tier PostgreSQL should handle this easily.

## 🔐 Security

- `DATABASE_URL` stored as Railway environment variable (encrypted)
- No API keys required (public API)
- Read-only access to Nomago API
- Database credentials never committed to git

## 📞 Support & Resources

- **Railway Docs:** https://docs.railway.app
- **Nomago Website:** https://www.nomago.si
- **API Provider:** https://ontime.si
- **PostgreSQL Docs:** https://www.postgresql.org/docs

## 📝 License

Personal project for monitoring bike availability.

---

**Last Updated:** November 14, 2025
**Version:** 1.0.0
**Python:** 3.11+
**Database:** PostgreSQL 15+
