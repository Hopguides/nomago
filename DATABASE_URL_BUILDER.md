# 🔧 Railway DATABASE_URL Builder

Če Railway reference variable `${{ Postgres.DATABASE_URL }}` ne dela, uporabi to metodo:

## Opcija 1: Direkten Copy-Paste

V **PostgreSQL servis → Variables** tab, kopiraj:
```
DATABASE_PRIVATE_URL
```

In ga prilepi kot **plain text** v **Worker servis → Variables → DATABASE_URL**

---

## Opcija 2: Sestavi iz Posameznih Delov

Če copy-paste ne dela, uporabi Railway "Raw Editor" v Worker Variables:

### V PostgreSQL Variables najdi:
- `PGUSER` (običajno: postgres)
- `PGPASSWORD` (dolg random string)
- `PGHOST` (postgres.railway.internal)
- `PGPORT` (5432)
- `PGDATABASE` (railway)

### V Worker Variables (Raw Editor) dodaj:

```env
DATABASE_URL=postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}
```

**POMEMBNO:** To so BASH-style environment variable substitutions, kar Railway podpira!

---

## Primer:

**Postgres Variables:**
```
PGUSER=postgres
PGPASSWORD=XokKPdBlMeUNgXOALpruNNsOlFaxAJXJ
PGHOST=postgres.railway.internal
PGPORT=5432
PGDATABASE=railway
```

**Worker Variable (Raw Editor):**
```env
DATABASE_URL=postgresql://${PGUSER}:${PGPASSWORD}@${PGHOST}:${PGPORT}/${PGDATABASE}
```

**Rezultat (Railway bo avtomatsko razširil):**
```
postgresql://postgres:XokKPdBlMeUNgXOALpruNNsOlFaxAJXJ@postgres.railway.internal:5432/railway
```

---

## Preverjanje:

Po deploymentu, v Worker Logs:

✅ **USPEH:**
```
DATABASE_URL: postgresql://post*** (length: 100+)
✅ [timestamp] Saved: 2/2 bikes
```

❌ **ŠE VEDNO NAPAKA:**
```
DATABASE_URL (length: 0)
⚠️  No DATABASE_URL - saving to JSON fallback
```
