# 🧪 Nomago Monitor - Testing Guide

Complete test suite for Supabase Edge Function and Database.

---

## 📋 Prerequisites

Get your **ANON KEY** from Supabase:

1. Go to: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt
2. **Settings** → **API** → **Project API keys**
3. Copy **`anon / public`** key
4. Export it:
   ```bash
   export SUPABASE_ANON_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
   ```

---

## 🚀 Quick Test (All Tests)

Run complete test suite:

```bash
cd /Users/klemen_mac/Documents/nomago

# Set ANON KEY
export SUPABASE_ANON_KEY='your_key_here'

# Run all tests
chmod +x run-all-tests.sh
./run-all-tests.sh
```

**Expected Output:**
```
✅ Database accessible
✅ bike_history table exists
✅ Edge Function deployed and working
✅ Data being saved correctly
🎉 ALL TESTS PASSED!
```

---

## 🔬 Individual Tests

### Test 1: Database Connection

Tests table access and schema:

```bash
export SUPABASE_ANON_KEY='your_key'
python3 test-database.py
```

**What it checks:**
- ✅ Table `bike_history` exists
- ✅ Table is accessible
- ✅ Record count
- ✅ Recent records
- ✅ Table schema/columns

---

### Test 2: Edge Function

Tests Edge Function deployment and response:

```bash
export SUPABASE_ANON_KEY='your_key'
python3 test-edge-function.py
```

**What it checks:**
- ✅ Function is deployed
- ✅ Authentication works
- ✅ Returns valid JSON
- ✅ Contains expected fields

---

### Test 3: Manual cURL Test

Direct HTTP test:

```bash
curl -X POST \
  "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor" \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json"
```

**Expected Response:**
```json
{
  "success": true,
  "station": "Four Points by Sheraton Ljubljana Mons",
  "bikes": 2,
  "stands": 0,
  "total": 2,
  "timestamp": "2025-11-14T..."
}
```

---

## 📊 Verify Data in Database

After running Edge Function, check database:

```bash
# Quick check via REST API
curl -s \
  "https://raavrcsgqeekhjpjxzlt.supabase.co/rest/v1/bike_history?select=*&order=timestamp.desc&limit=5" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" | python3 -m json.tool
```

**OR** in Supabase SQL Editor:

```sql
SELECT * FROM bike_history
ORDER BY timestamp DESC
LIMIT 10;
```

---

## 🔍 Test Files

| File | Purpose |
|------|---------|
| `run-all-tests.sh` | Complete test suite - runs all tests |
| `test-database.py` | Tests database connection and table |
| `test-edge-function.py` | Tests Edge Function deployment |
| `test-function.sh` | Simple bash test script |

---

## ✅ Success Criteria

All tests pass when you see:

```
✅ Database accessible
✅ bike_history table exists
✅ Edge Function returns success: true
✅ Data saved to database
✅ Recent records visible in table
```

---

## ❌ Troubleshooting

### "Missing authorization header"
→ Set `SUPABASE_ANON_KEY` environment variable

### "Table 'bike_history' not found"
→ Run `supabase-setup.sql` in SQL Editor

### "Invalid JWT"
→ Check ANON KEY is correct (not ACCESS_TOKEN or SERVICE_ROLE_KEY)

### "Function not found"
→ Redeploy: `supabase functions deploy nomago-monitor --project-ref raavrcsgqeekhjpjxzlt`

### No data in database
→ Check Edge Function logs in Supabase Dashboard

---

## 🎯 After Tests Pass

1. ✅ All tests green
2. ✅ Data visible in database
3. ✅ Edge Function working
4. 🎯 **Next:** Set up automated cron job

Run `setup-cron.sql` to enable automatic monitoring every 10 minutes!

---

## 📖 Related Docs

- **Setup:** `QUICK_START_SUPABASE.md`
- **Database:** `supabase-setup.sql`
- **Cron Job:** `setup-cron.sql`
- **Detailed Guide:** `SUPABASE_SETUP.md`

---

**Run tests now to verify everything works!** 🚀

```bash
export SUPABASE_ANON_KEY='your_key'
./run-all-tests.sh
```
