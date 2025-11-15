# 📊 Nomago History - Kako Videti Vse Podatke

## 🤖 KAJ DELA CRON JOB:

**Avtomatsko spremljanje vsakih 10 minut:**

```
Vsake 10 minut:
  1. Kliče Nomago API
  2. Pridobi podatke za Four Points postajo
  3. Shrani v Supabase bazo

Rezultat: 144 zapisov/dan, ~4,320/mesec
```

**Primer zapisa:**
```json
{
  "timestamp": "2025-11-15 07:08:43",
  "available_bikes": 2,
  "available_stands": 0,
  "total_stands": 2
}
```

---

## 📊 KAKO VIDETI ZGODOVINO:

### 1️⃣ **Supabase Table Editor (Najlažje)**

**Direktni link:**
👉 https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/editor/29410

**Kaj vidiš:**
- Celotna tabela `bike_history`
- Vsi zapisi z timestamp
- Filter & sort možnosti
- Vizualni pregled

---

### 2️⃣ **SQL Editor (Za Query-je)**

**Direktni link:**
👉 https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/sql/new

**Uporabni SQL-ji:**

```sql
-- Vse (zadnji najprej)
SELECT * FROM bike_history
ORDER BY timestamp DESC;

-- Zadnjih 100
SELECT * FROM bike_history
ORDER BY timestamp DESC
LIMIT 100;

-- Statistika
SELECT
    COUNT(*) as total_records,
    MIN(timestamp) as first_record,
    MAX(timestamp) as last_record,
    AVG(available_bikes) as avg_bikes
FROM bike_history;

-- Kdaj je bila prazna
SELECT timestamp, available_bikes
FROM bike_history
WHERE available_bikes = 0
ORDER BY timestamp DESC;

-- Kdaj je bila polna
SELECT timestamp, available_stands
FROM bike_history
WHERE available_stands = 0
ORDER BY timestamp DESC;

-- Po urah
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(available_bikes) as avg_bikes,
    COUNT(*) as readings
FROM bike_history
GROUP BY hour
ORDER BY hour DESC;
```

---

### 3️⃣ **Python Script (Terminal)**

```bash
cd /Users/klemen_mac/Documents/nomago
python3 view-history.py
```

**Prikaže:**
```
📊 CURRENT STATUS
📈 STATISTICS (avg, min, max)
⚠️  EVENTS (empty/full times)
⏱️  RECENT RECORDS (zadnjih 10)
📅 PERIOD (časovno obdobje)
```

---

### 4️⃣ **Public API (Za Aplikacije)**

**Get zadnjih 100 zapisov:**
```bash
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?limit=100" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"
```

**Od danes:**
```bash
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?since=2025-11-15T00:00:00Z" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"
```

---

## 🔗 QUICK LINKS:

| Link | Purpose |
|------|---------|
| [Table Editor](https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/editor/29410) | Vizualni pregled podatkov |
| [SQL Editor](https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/sql/new) | SQL queries |
| [Functions](https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/functions) | Edge Functions logs |
| [Cron Jobs](https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/database/cron-jobs) | Cron job status |

---

## 📈 STATISTIKA EXAMPLES:

### Python (JavaScript podobno):
```python
import requests

response = requests.get(
    'https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data',
    params={'limit': 1000},
    headers={'Authorization': 'Bearer YOUR_KEY'}
)

data = response.json()
records = data['data']

# Analiza
bikes = [r['available_bikes'] for r in records]
avg = sum(bikes) / len(bikes)
print(f"Average bikes: {avg:.1f}")

# Kdaj je bila prazna
empty_times = [r for r in records if r['available_bikes'] == 0]
print(f"Empty {len(empty_times)} times")
```

---

## ⏰ CRON JOB STATUS:

**Preveri da teče:**
```sql
SELECT * FROM cron.job WHERE jobname = 'nomago-monitor';
```

**Zgodovina izvajanj:**
```sql
SELECT * FROM cron.job_run_details
WHERE jobname = 'nomago-monitor'
ORDER BY start_time DESC
LIMIT 20;
```

**Direct link:**
👉 https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/database/cron-jobs

---

## 📊 PRIČAKOVANI RAST PODATKOV:

| Obdobje | Zapisi | Velikost |
|---------|--------|----------|
| 1 dan | 144 | ~14 KB |
| 1 teden | 1,008 | ~100 KB |
| 1 mesec | 4,320 | ~430 KB |
| 1 leto | 52,560 | ~5 MB |

---

## 🎯 NAJPOGOSTEJŠI USE CASE-i:

### 1. Trenutno stanje:
```bash
python3 view-history.py
```

### 2. Vsi podatki (vizualno):
👉 https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/editor/29410

### 3. Custom analiza:
```sql
-- V SQL Editor
SELECT * FROM bike_history WHERE available_bikes = 0;
```

---

**Last Updated:** November 15, 2025
**Total Records:** ~1 (narašča vsakih 10 min)
