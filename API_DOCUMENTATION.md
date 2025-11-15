# 🚲 Nomago Bike Monitor - Public API Documentation

Public API endpoint za dostop do podatkov o razpoložljivosti koles pri Four Points by Sheraton Ljubljana Mons.

---

## 🌐 Base URL

```
https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data
```

---

## 🔑 Authentication

API zahteva **ANON KEY** v Authorization header:

```bash
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhYXZyY3NncWVla2hqcGp4emx0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU1OTUyMzMsImV4cCI6MjA3MTE3MTIzM30.bgYTTOJIdeNSBTeA0KAluic328VzHCMzqlmqk9qw_UQ
```

---

## 📊 Endpoints

### GET `/get-bike-data`

Vrne zgodovino razpoložljivosti koles in trenutno stanje.

#### Query Parameters:

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `limit` | integer | 100 | Število zapisov (max 1000) |
| `offset` | integer | 0 | Offset za paginacijo |
| `since` | ISO 8601 | - | Samo podatki od tega datuma naprej |

#### Example Requests:

```bash
# Zadnjih 10 zapisov
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?limit=10" \
  -H "Authorization: Bearer YOUR_ANON_KEY"

# Podatki od določenega datuma
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?since=2025-11-15T00:00:00Z" \
  -H "Authorization: Bearer YOUR_ANON_KEY"

# Paginacija (preskočri prvih 20, vrni naslednjih 10)
curl "https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data?limit=10&offset=20" \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

#### Response Format:

```json
{
  "success": true,
  "station": {
    "id": 458645919,
    "name": "Four Points by Sheraton Ljubljana Mons",
    "location": {
      "lat": 46.052252,
      "lng": 14.45303
    }
  },
  "current": {
    "bikes": 2,
    "stands": 0,
    "total": 2,
    "status": "full"
  },
  "data": [
    {
      "id": 1,
      "timestamp": "2025-11-15T06:08:43.694+00:00",
      "available_bikes": 2,
      "available_stands": 0,
      "total_stands": 2,
      "station_id": 458645919,
      "created_at": "2025-11-15T06:08:43.883073+00:00"
    }
  ],
  "pagination": {
    "limit": 10,
    "offset": 0,
    "total": 1
  },
  "timestamp": "2025-11-15T06:12:11.209Z"
}
```

#### Response Fields:

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Ali je request uspel |
| `station` | object | Informacije o postaji |
| `station.id` | integer | ID postaje (458645919) |
| `station.name` | string | Ime postaje |
| `station.location` | object | GPS koordinate |
| `current` | object | **Trenutno stanje** |
| `current.bikes` | integer | Prosta kolesa zdaj |
| `current.stands` | integer | Prosta mesta zdaj |
| `current.total` | integer | Skupna kapaciteta |
| `current.status` | string | `empty`, `full`, ali `available` |
| `data` | array | Zgodovina meritev |
| `pagination` | object | Paginacija info |
| `timestamp` | string | ISO timestamp API klica |

#### Status Values:

| Status | Description |
|--------|-------------|
| `empty` | 0 koles - postaja prazna |
| `full` | 0 prostih mest - postaja polna |
| `available` | Kolesa in mesta na voljo |

---

## 💻 Code Examples

### JavaScript/TypeScript

```javascript
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const API_URL = 'https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data';

async function getBikeData(limit = 10) {
  const response = await fetch(`${API_URL}?limit=${limit}`, {
    headers: {
      'Authorization': `Bearer ${ANON_KEY}`
    }
  });

  const data = await response.json();

  if (data.success) {
    console.log('Current status:', data.current);
    console.log('History:', data.data);
  }

  return data;
}

// Usage
getBikeData(10).then(data => {
  console.log(`${data.current.bikes}/${data.current.total} bikes available`);
});
```

### Python

```python
import requests

ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
API_URL = 'https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data'

def get_bike_data(limit=10, since=None):
    params = {'limit': limit}
    if since:
        params['since'] = since

    headers = {
        'Authorization': f'Bearer {ANON_KEY}'
    }

    response = requests.get(API_URL, params=params, headers=headers)
    return response.json()

# Usage
data = get_bike_data(limit=10)
if data['success']:
    current = data['current']
    print(f"Status: {current['status']}")
    print(f"Bikes: {current['bikes']}/{current['total']}")
```

### cURL

```bash
#!/bin/bash
ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
API_URL="https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data"

# Get latest data
curl -s "${API_URL}?limit=10" \
  -H "Authorization: Bearer ${ANON_KEY}" | jq .

# Get current status only
curl -s "${API_URL}?limit=1" \
  -H "Authorization: Bearer ${ANON_KEY}" | jq '.current'
```

### PHP

```php
<?php
$anonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
$apiUrl = 'https://raavrcsgqeekhjpjxzlt.supabase.co/functions/v1/get-bike-data';

function getBikeData($limit = 10) {
    global $anonKey, $apiUrl;

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $apiUrl . '?limit=' . $limit);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Authorization: Bearer ' . $anonKey
    ]);

    $response = curl_exec($ch);
    curl_close($ch);

    return json_decode($response, true);
}

$data = getBikeData(10);
if ($data['success']) {
    $current = $data['current'];
    echo "Bikes: {$current['bikes']}/{$current['total']}\n";
    echo "Status: {$current['status']}\n";
}
?>
```

---

## 🔒 CORS Support

API podpira **CORS** in lahko deluje iz katerekoli domene (browser apps).

```
Access-Control-Allow-Origin: *
```

---

## ⚡ Rate Limiting

- Ni eksplicitnega rate limit-a
- Priporočeno: **Max 1 request/sekundo**
- Za večje obremenitve kontaktiraj maintainerja

---

## 🚨 Error Responses

### 401 Unauthorized

```json
{
  "code": 401,
  "message": "Missing authorization header"
}
```

**Fix:** Dodaj Authorization header z ANON KEY.

### 500 Internal Server Error

```json
{
  "success": false,
  "error": "Error message here"
}
```

---

## 📊 Use Cases

### Real-time Dashboard
```javascript
// Update every 30 seconds
setInterval(async () => {
  const data = await getBikeData(1);
  updateUI(data.current);
}, 30000);
```

### Historical Analysis
```python
# Get last 24 hours
import datetime
since = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
data = get_bike_data(limit=1000, since=since)

# Analyze trends
bikes_available = [record['available_bikes'] for record in data['data']]
avg_bikes = sum(bikes_available) / len(bikes_available)
print(f"Average bikes in last 24h: {avg_bikes:.1f}")
```

### Mobile App
```javascript
// React Native example
import React, { useState, useEffect } from 'react';

function BikeStatus() {
  const [current, setCurrent] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const data = await getBikeData(1);
      setCurrent(data.current);
    };

    fetchData();
    const interval = setInterval(fetchData, 60000); // Every minute

    return () => clearInterval(interval);
  }, []);

  if (!current) return <Text>Loading...</Text>;

  return (
    <View>
      <Text>{current.bikes}/{current.total} bikes available</Text>
      <Text>Status: {current.status}</Text>
    </View>
  );
}
```

---

## 🔗 Additional Resources

- **Supabase Dashboard:** https://supabase.com/dashboard/project/raavrcsgqeekhjpjxzlt
- **GitHub Repo:** https://github.com/Hopguides/nomago
- **Nomago Website:** https://www.nomago.si

---

## 📞 Support

Issues? Open a GitHub issue or contact the maintainer.

**Last Updated:** November 15, 2025
**API Version:** 1.0
**Station:** Four Points by Sheraton Ljubljana Mons
