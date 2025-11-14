# 🚀 Quick Start Guide

## 📋 What You Have

Two monitoring systems for Nomago Four Points station:

| System | Storage | Use Case |
|--------|---------|----------|
| **Railway Monitor** | PostgreSQL (cloud) | Production, 24/7 monitoring |
| **Local Monitor** | CSV (local files) | Testing, offline use |

---

## 🚂 Railway Deployment (Production)

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```

### 2. Login to Railway
```bash
railway login
```

### 3. Create Project
1. Go to [railway.app](https://railway.app)
2. Create new project
3. Add PostgreSQL database (auto-creates `DATABASE_URL`)

### 4. Deploy
```bash
cd /Users/klemen_mac/Documents/nomago
railway link   # Connect to your Railway project
railway up     # Deploy the code
```

### 5. Monitor
```bash
railway logs           # View logs
railway status         # Check status
railway connect postgres  # Access database
```

**That's it!** The monitor will run every 10 minutes automatically.

---

## 💻 Local Usage (Testing)

### Option 1: One-time check (JSON)
```bash
python3 monitor.py
```
Saves to `nomago_history.json`

### Option 2: Continuous monitoring (CSV)
```bash
python3 monitor_four_points.py
```
Saves to `four_points_history.csv` every 5 minutes

### Option 3: View history
```bash
python3 view_history.py
```

---

## 🛠️ Helper Script

Use the deployment helper for common tasks:

```bash
./deploy.sh
```

**Options:**
1. Test locally (JSON fallback)
2. Test with local PostgreSQL
3. Deploy to Railway
4. View Railway logs
5. Connect to Railway PostgreSQL
6. Check Railway status

---

## 📊 Check Your Data

### Railway (PostgreSQL)
```bash
railway connect postgres
```
Then:
```sql
SELECT * FROM bike_history ORDER BY timestamp DESC LIMIT 10;
```

### Local (JSON)
```bash
cat nomago_history.json
```

### Local (CSV)
```bash
python3 view_history.py
```

---

## 🔧 Files Explained

**Railway Deployment:**
- `monitor.py` - Main script (PostgreSQL + JSON fallback)
- `requirements.txt` - Python dependencies
- `Procfile` - Railway process definition
- `railway.json` - Railway configuration
- `RAILWAY_README.md` - Full Railway docs

**Local Monitoring:**
- `monitor_four_points.py` - CSV-based monitor
- `view_history.py` - Display CSV statistics
- `README.md` - Local monitoring docs

**Data:**
- `nomago-bikes.json` - All 168 stations
- `ljubljana-postaje.txt` - Ljubljana stations list

**Helper:**
- `deploy.sh` - Deployment helper script

---

## 🎯 Next Steps

### For Production (Railway):
1. ✅ Deploy to Railway
2. ✅ Verify PostgreSQL connection
3. ✅ Check logs after 10-20 minutes
4. ✅ Query database to see data

### For Local Development:
1. ✅ Run `python3 monitor.py` once
2. ✅ Check `nomago_history.json`
3. ✅ Run `python3 monitor_four_points.py` for continuous monitoring
4. ✅ Use `python3 view_history.py` to see statistics

---

## ⚠️ Troubleshooting

**"Railway CLI not found"**
```bash
npm install -g @railway/cli
```

**"psycopg2 import error" (locally)**
```bash
pip install psycopg2-binary
```

**"requests not found"**
```bash
pip install requests
```

**"SSL certificate error"**
→ Already fixed in `monitor.py` (uses requests library)

**"No data in database"**
```bash
# Check Railway logs
railway logs --tail 50

# Verify DATABASE_URL exists
railway variables
```

---

## 📞 Resources

- **Railway Docs:** https://docs.railway.app
- **Full Railway Guide:** `RAILWAY_README.md`
- **Local Monitor Guide:** `README.md`
- **API Endpoint:** https://api.ontime.si/api/v1/nomago-bike/

---

**Ready to go!** 🚀

Choose Railway for 24/7 cloud monitoring or local scripts for testing.
