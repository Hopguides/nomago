# 🚀 Nomago Monitor - Supabase Quick Start

## ✅ Kaj Si Že Naredil:

- [x] **KORAK 1:** Tabela ustvarjena (`bike_history`) ✅
- [x] **KORAK 2:** Edge Function deployed (`nomago-monitor`) ✅
- [ ] **KORAK 3:** Test funkcije
- [ ] **KORAK 4:** Nastavi avtomatsko spremljanje

---

## 🧪 KORAK 3: Testiraj Funkcijo

### Metoda A: Ročni HTTP Test

1. **Pridobi ANON KEY:**
   - Pojdi na: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt
   - **Settings** → **API**
   - **Project API keys** → Kopiraj **`anon` / `public`** key
   - Izgleda nekako tako: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

2. **Test s curl:**
   ```bash
   curl -X POST \
     "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor" \
     -H "Authorization: Bearer YOUR_ANON_KEY" \
     -H "Content-Type: application/json"
   ```

3. **ALI uporabi test script:**
   ```bash
   cd /Users/klemen_mac/Documents/nomago
   ./test-function.sh
   ```

### Metoda B: Supabase Dashboard

1. Pojdi na: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/functions
2. Klikni na **`nomago-monitor`**
3. Klikni **"Invoke function"** gumb
4. Poglej response

### Pričakovan Response:

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

## 🤖 KORAK 4: Nastavi Avtomatsko Spremljanje (Cron)

### Metoda A: SQL Editor (Priporočeno)

1. **Pridobi ANON KEY** (glej zgoraj)

2. **Odpri `setup-cron.sql`** in zamenjaj `YOUR_ANON_KEY` s pravim key-em

3. **Izvedi v SQL Editor:**
   - Pojdi na: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/sql
   - **New Query**
   - Kopiraj in prilepi celotno `setup-cron.sql`
   - **Run** ▶️

4. **Preveri:**
   ```sql
   SELECT * FROM cron.job;
   ```
   Moral bi videti `nomago-monitor-job`

### Metoda B: Database Cron UI (Če obstaja)

1. Supabase Dashboard → **Database** → **Cron Jobs**
2. **Create new cron job**
3. Name: `nomago-monitor`
4. Schedule: `*/10 * * * *`
5. SQL:
   ```sql
   SELECT net.http_post(
       url:='https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/nomago-monitor',
       headers:=jsonb_build_object(
           'Content-Type', 'application/json',
           'Authorization', 'Bearer YOUR_ANON_KEY'
       )
   );
   ```

---

## 📊 Preveri Podatke

### SQL Query:

```sql
-- Zadnjih 10 meritev
SELECT * FROM bike_history
ORDER BY timestamp DESC
LIMIT 10;

-- Število vseh zapisov
SELECT COUNT(*) as total_records FROM bike_history;

-- Statistika
SELECT
    MIN(timestamp) as first_record,
    MAX(timestamp) as last_record,
    COUNT(*) as total_records,
    AVG(available_bikes) as avg_bikes
FROM bike_history;
```

### Dashboard:

1. Pojdi na: https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/editor
2. **Table Editor** → **bike_history**
3. Poglej podatke v tabeli

---

## 🔍 Logs

### Edge Function Logs:

1. https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/functions/nomago-monitor
2. Tab **"Logs"**
3. Vidiš vsakič ko se funkcija izvede

### Pričakovani Log:

```
🚲 Nomago Monitor - Starting...
📊 Found station: Four Points by Sheraton Ljubljana Mons
🚲 Bikes: 2/2
✅ Saved to database: 2/2 bikes
```

---

## ⚠️ Troubleshooting

### "Invalid JWT" napaka:
→ Uporabi ANON KEY, ne ACCESS TOKEN

### "Function not found":
→ Preveri da je deployed: `supabase functions deploy nomago-monitor --project-ref raavrcsgqeekhjpjxzlt`

### "Table doesn't exist":
→ Zaženi `supabase-setup.sql` v SQL Editor

### Cron ne deluje:
→ Preveri da si zamenjal `YOUR_ANON_KEY` s pravim keyem

---

## 📁 Datoteke

| Datoteka | Namen |
|----------|-------|
| `supabase-setup.sql` | Ustvari tabelo (že done ✅) |
| `setup-cron.sql` | Nastavi avtomatski cron job |
| `test-function.sh` | Test script za funkcijo |
| `SUPABASE_SETUP.md` | Podrobna navodila |
| `QUICK_START_SUPABASE.md` | Ta datoteka - hitri začetek |

---

## ✅ Naslednji Koraki:

1. **Testiraj funkcijo** (KORAK 3)
2. **Nastavi cron** (KORAK 4)
3. **Preveri podatke** čez 10-20 minut
4. **Profitaj!** 🎉

---

## 🔗 Hitre Povezave:

- **Dashboard:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt
- **SQL Editor:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/sql
- **Functions:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/functions
- **Table Editor:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/editor
- **API Settings:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt/settings/api

---

**Nadaljuj s KORAKOM 3 - testiraj funkcijo!** 🚀
