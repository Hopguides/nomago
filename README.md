# 🚲 Nomago Four Points Station Monitor

Spremljanje razpoložljivosti Nomago koles pri Four Points by Sheraton Ljubljana Mons v realnem času s shranjevanjem zgodovinskih podatkov.

## 📋 Datoteke

```
nomago/
├── monitor_four_points.py      # Glavna skripta za spremljanje
├── view_history.py              # Prikaz zgodovinskih podatkov
├── four_points_history.csv      # Zgodovina meritev (auto-generated)
├── nomago-bikes.json            # Celoten seznam postaj
└── ljubljana-postaje.txt        # Seznam ljubljanskih postaj
```

## 🚀 Uporaba

### 1. Enkratna meritev
Pridobi in shrani trenutno stanje postaje:

```bash
python3 monitor_four_points.py --once
```

**Izpis:**
```
🚲 NOMAGO POSTAJA - Four Points by Sheraton Ljubljana Mons
======================================================================

[14:54:56] 🟠 POLNO | 🚲 Kolesa: 2/2 | 🅿️ Mesta: 0/2

✅ Podatki shranjeni v: four_points_history.csv
```

### 2. Neprekinjeno spremljanje
Spremljaj postajo vsakih 5 minut:

```bash
python3 monitor_four_points.py
```

**Izpis:**
```
🚲 NOMAGO MONITOR - Four Points by Sheraton Ljubljana Mons
======================================================================
📊 Interval: 300 sekund (5 minut)
💾 Zgodovina: four_points_history.csv
⏹️  Ustavi: Ctrl+C
======================================================================

[14:54:56] 🟠 POLNO | 🚲 Kolesa: 2/2 | 🅿️ Mesta: 0/2
[15:00:00] 🟢 OK | 🚲 Kolesa: 1/2 | 🅿️ Mesta: 1/2
[15:05:00] 🔴 PRAZNO | 🚲 Kolesa: 0/2 | 🅿️ Mesta: 2/2
...
```

**Ustavitev:** Pritisni `Ctrl+C`

### 3. Prikaz zgodovine
Prikaži statistiko in zadnjih 20 meritev:

```bash
python3 view_history.py
```

**Izpis:**
```
🚲 NOMAGO - Four Points by Sheraton (Zgodovinski podatki)
======================================================================

📅 Obdobje:
   Od: 2025-11-14 14:54:56
   Do: 2025-11-14 17:30:12
   Število meritev: 33

📊 Statistika razpoložljivosti koles:
   Povprečje: 1.2 koles
   Minimum: 0 koles
   Maksimum: 2 koles

📈 Porazdelitev:
   0 koles: ████████████████ 30.3% (10x)
   1 koles: ████████████████████████ 45.5% (15x)
   2 koles: ████████████ 24.2% (8x)

⚠️  Problematični dogodki:
   🔴 Prazna postaja (0 koles): 10x (30.3%)
   🟠 Polna postaja (0 mest): 8x (24.2%)

⏱️  ZADNJIH MERITEV:
======================================================================
Čas                  Status       Kolesa     Mesta
----------------------------------------------------------------------
...
```

### 4. Prikaz celotne zgodovine
Prikaži vse meritve:

```bash
python3 view_history.py --all
```

## 📊 Statusi postaje

| Status | Ikona | Opis |
|--------|-------|------|
| **PRAZNO** | 🔴 | 0 koles - ni možnosti izposoje |
| **POLNO** | 🟠 | 0 mest - ni možnosti vračila |
| **NIZKO** | 🟡 | 1 kolo - nizka razpoložljivost |
| **OK** | 🟢 | 2+ kolesi - normalna razpoložljivost |

## ⚙️ Konfiguracija

Uredi `monitor_four_points.py`:

```python
# Spremeni interval spremljanja (v sekundah)
INTERVAL = 300  # 5 minut (privzeto)
INTERVAL = 60   # 1 minuta (pogostejše)
INTERVAL = 900  # 15 minut (redkejše)

# Spremeni ime datoteke za zgodovino
DATA_FILE = "four_points_history.csv"
```

## 📈 Struktura CSV datoteke

```csv
timestamp,available_bikes,available_stands,total_stands,api_timestamp
2025-11-14 14:54:56,2,0,2,2025-11-14T14:48:10.370896+01:00
2025-11-14 15:00:00,1,1,2,2025-11-14T14:53:22.123456+01:00
2025-11-14 15:05:00,0,2,2,2025-11-14T14:58:45.789012+01:00
```

**Stolpci:**
- `timestamp` - Čas meritve (lokalni)
- `available_bikes` - Prosta kolesa
- `available_stands` - Prosta mesta
- `total_stands` - Skupna kapaciteta
- `api_timestamp` - API timestamp

## 🔧 Zahteve

- **Python 3** (brez dodatnih paketov)
- **curl** (že nameščen na macOS)
- Internet povezava za dostop do API-ja

## 📍 Podatki o postaji

**Lokacija:** Four Points by Sheraton Ljubljana Mons
**Naslov:** Tržaška cesta, Ljubljana
**GPS:** 46.052252, 14.45303
**Kapaciteta:** 2 kolesi (najmanjša v sistemu)
**ID:** 458645919

[📍 Oglej si na Google Maps](https://maps.google.com/?q=46.052252,14.45303)

## 💡 Napredne uporabe

### Avtomatično spremljanje 24/7
Uporabi `nohup` za zagon v ozadju:

```bash
nohup python3 monitor_four_points.py > monitor.log 2>&1 &
```

Preveri proces:
```bash
ps aux | grep monitor_four_points
```

Ustavi proces:
```bash
pkill -f monitor_four_points
```

### Cron job (periodično spremljanje)
Dodaj v crontab za zagon vsako uro:

```bash
crontab -e
```

Dodaj vrstico:
```
0 * * * * cd /Users/klemen_mac/Documents/nomago && python3 monitor_four_points.py --once
```

### Izvoz podatkov za analizo
Zgodovino lahko uvozit v Excel, Numbers, ali programsko analiziraš:

```python
import pandas as pd

df = pd.read_csv('four_points_history.csv')
print(df.describe())
```

## 🌐 API vir

Podatki iz: **Ontime.si API**
Endpoint: `https://api.ontime.si/api/v1/nomago-bike/`
Sistem: **Nomago bike-sharing Ljubljana**

## 📝 Opombe

- Postaja Four Points ima samo **2 kolesi** (najmanjša v sistemu)
- Podatki se posodabljajo ~vsake 5 minut na API-ju
- CSV datoteka raste s časom - redna arhivacija priporočena
- Meritve se shranjujejo lokalno - brez povezave z oblačnimi storitvami

## 🆘 Težave

**SSL Certificate Error:**
```
[SSL: CERTIFICATE_VERIFY_FAILED]
```
→ Skripta uporablja `curl` namesto `urllib`, kar rešuje SSL težave na macOS

**No data error:**
```
❌ Napaka pri pridobivanju podatkov
```
→ Preveri internet povezavo ali API dostopnost

**File not found:**
```
❌ Datoteka four_points_history.csv ne obstaja
```
→ Zaženi najprej `python3 monitor_four_points.py --once`

---

**Verzija:** 1.0
**Datum:** November 2025
**Avtor:** Klemen
