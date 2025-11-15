# 🚀 Public API - Quick Start

**Public endpoint za dostop do podatkov o Nomago kolesih pri Four Points hotelu.**

---

## 🌐 API Endpoint

```
https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data
```

---

## 🔑 Authentication

Potrebuješ ANON KEY v Authorization header:

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ
```

---

## ⚡ Quick Examples

### cURL (Command Line)

```bash
# Current status
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?limit=1" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ"
```

### JavaScript/Fetch

```javascript
fetch('https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?limit=10', {
  headers: {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ'
  }
})
.then(res => res.json())
.then(data => {
  console.log('Current bikes:', data.current.bikes);
  console.log('Status:', data.current.status);
});
```

### Python

```python
import requests

response = requests.get(
    'https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data',
    params={'limit': 10},
    headers={
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ'
    }
)

data = response.json()
print(f"Bikes: {data['current']['bikes']}/{data['current']['total']}")
```

---

## 📊 Response Example

```json
{
  "success": true,
  "station": {
    "name": "Four Points by Sheraton Ljubljana Mons",
    "location": {"lat": 46.052252, "lng": 14.45303}
  },
  "current": {
    "bikes": 2,
    "stands": 0,
    "total": 2,
    "status": "full"
  },
  "data": [...],
  "pagination": {...}
}
```

---

## 🔧 Query Parameters

| Parameter | Example | Description |
|-----------|---------|-------------|
| `limit` | `?limit=10` | Število zapisov (default: 100) |
| `offset` | `?offset=20` | Offset za paginacijo |
| `since` | `?since=2025-11-15T00:00:00Z` | Samo od tega datuma naprej |

---

## ✅ Status Values

- **`empty`** - 0 koles (postaja prazna)
- **`full`** - 0 mest (postaja polna)
- **`available`** - Kolesa in mesta na voljo

---

## 📖 Full Documentation

Za podrobno dokumentacijo glej: **`API_DOCUMENTATION.md`**

- Vsi query parametri
- Error handling
- Code examples (JS, Python, PHP, cURL)
- Use cases
- CORS details

---

## 🧪 Test It Now

```bash
cd /Users/klemen_mac/Documents/nomago
./test-public-api.sh
```

---

## 🔗 Links

- **API Docs:** `API_DOCUMENTATION.md`
- **GitHub:** https://github.com/Hopguides/nomago
- **Supabase Dashboard:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt

---

**Last Updated:** November 15, 2025
**Endpoint Status:** 🟢 LIVE
