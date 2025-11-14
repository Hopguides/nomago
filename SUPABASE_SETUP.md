# 🚲 Nomago Monitor - Supabase Setup

**100x lažje kot Railway!** ✅

---

## 🎯 Kaj Potrebuješ:

- ✅ Supabase projekt: **raavrcsgqeekhjpjxzlt**
- ✅ Supabase CLI (že imaš nameščen)
- ✅ Access token (že imaš v .env)

---

## 📋 SETUP V 4 KORAKIH:

### **KORAK 1: Ustvari Tabelo**

1. Pojdi na: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt
2. Klikni **"SQL Editor"** (leva stran)
3. **"New Query"**
4. **Kopiraj in prilepi** vsebino datoteke: `supabase-setup.sql`
5. Klikni **"Run"**

✅ Tabela `bike_history` ustvarjena!

---

### **KORAK 2: Deploy Edge Function**

V terminalu:

```bash
cd /Users/klemen_mac/Documents/nomago

# Prijava v Supabase
supabase login

# Link na projekt
supabase link --project-ref raavrcsgqeekhjpjxzlt

# Deploy funkcije
supabase functions deploy nomago-monitor
```

✅ Edge Function deployed!

---

### **KORAK 3: Testiraj Funkcijo**

```bash
# Test direktni klic
supabase functions invoke nomago-monitor
```

Pričakuješ:
```json
{
  "success": true,
  "station": "Four Points by Sheraton Ljubljana Mons",
  "bikes": 2,
  "stands": 0,
  "total": 2
}
```

---

### **KORAK 4: Nastavi Cron (Avtomatsko Spremljanje)**

1. Supabase Dashboard → **"Database"** → **"Cron Jobs"**
2. Klikni **"Create a new cron job"**
3. Name: `nomago-monitor`
4. Schedule: `*/10 * * * *` (vsakih 10 minut)
5. Function:
   ```sql
   SELECT
     net.http_post(
       url:='https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor',
       headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
     ) as request_id;
   ```

**ALI uporabi Supabase pg_cron:**

```sql
-- V SQL Editor
SELECT cron.schedule(
    'nomago-monitor-job',
    '*/10 * * * *', -- Vsakih 10 minut
    $$
    SELECT net.http_post(
        url:='https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor',
        headers:='{"Content-Type": "application/json", "Authorization": "Bearer YOUR_ANON_KEY"}'::jsonb
    );
    $$
);
```

✅ Avtomatsko spremljanje vsakih 10 minut!

---

## 🔍 Preveri Podatke:

### SQL Editor:
```sql
-- Zadnjih 10 meritev
SELECT * FROM bike_history
ORDER BY timestamp DESC
LIMIT 10;

-- Število vseh meritev
SELECT COUNT(*) FROM bike_history;

-- Statistika
SELECT
    AVG(available_bikes) as avg_bikes,
    MIN(available_bikes) as min_bikes,
    MAX(available_bikes) as max_bikes
FROM bike_history;
```

---

## 🌐 Ročni Klic Edge Function:

### Preko URL:
```bash
curl -X POST \
  https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

### Najdi ANON_KEY:
Supabase Dashboard → **Settings** → **API** → **Project API keys** → **anon/public**

---

## 📊 Dashboard Query Primer:

```sql
-- Prazna postaja (0 koles)
SELECT
    timestamp,
    available_bikes
FROM bike_history
WHERE available_bikes = 0
ORDER BY timestamp DESC;

-- Polna postaja (0 mest)
SELECT
    timestamp,
    available_stands
FROM bike_history
WHERE available_stands = 0
ORDER BY timestamp DESC;

-- Hourly trends
SELECT
    DATE_TRUNC('hour', timestamp) as hour,
    AVG(available_bikes) as avg_bikes
FROM bike_history
GROUP BY hour
ORDER BY hour DESC;
```

---

## ✅ PREDNOSTI SUPABASE:

| Feature | Supabase | Railway |
|---------|----------|---------|
| **Setup** | ✅ 4 koraki | ❌ 10+ korakov |
| **Variables** | ✅ Avtomatsko | ❌ Problemi z references |
| **Database** | ✅ Built-in PostgreSQL | ❌ Dodatna konfiguracija |
| **Cron** | ✅ pg_cron vgrajen | ❌ Potreben Procfile |
| **Logs** | ✅ Real-time dashboard | ⚠️ CLI required |
| **Free Tier** | ✅ 500MB DB | ✅ 500MB DB |

---

## 🔧 Troubleshooting:

### "Function not found"
```bash
supabase functions list
```

### "Database error"
Preveri da si zagnal `supabase-setup.sql`

### "Unauthorized"
Preveri da Edge Function uporablja `SUPABASE_SERVICE_ROLE_KEY`

---

## 📁 Datoteke:

```
nomago/
├── supabase/
│   └── functions/
│       └── nomago-monitor/
│           └── index.ts          # Edge Function
├── supabase-setup.sql            # Database schema
└── SUPABASE_SETUP.md            # Ta datoteka
```

---

## 🚀 Hitri Začetek:

```bash
# 1. Ustvari tabelo v SQL Editor (kopiraj supabase-setup.sql)

# 2. Deploy function
cd /Users/klemen_mac/Documents/nomago
supabase login
supabase link --project-ref raavrcsgqeekhjpjxzlt
supabase functions deploy nomago-monitor

# 3. Test
supabase functions invoke nomago-monitor

# 4. Nastavi cron v Supabase Dashboard

# 5. Profit! 🎉
```

---

**Verzija:** 1.0
**Datum:** November 2025
**Projekt:** raavrcsgqeekhjpjxzlt
