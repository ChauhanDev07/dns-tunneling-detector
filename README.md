# 🛡 DNS Tunnel Detector — Real-Time Traffic Monitoring Dashboard

A university-grade Python project that captures live DNS traffic, detects DNS tunneling using rule-based scoring, and visualizes suspicious activity on a live web dashboard.

---

## 📋 What It Does

| Layer | What happens |
|-------|-------------|
| **Collector** | Captures DNS packets on UDP/TCP port 53 using `scapy` |
| **Detector** | Extracts features (length, entropy, query rate) and scores each event |
| **Storage** | Saves events and alerts to SQLite |
| **Dashboard** | Flask + Socket.IO web dashboard with live updates |

---

## 🚀 Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

**Windows extra step:** Install [Npcap](https://npcap.com/) (required for packet capture).

### 2. Configure (optional)

```bash
cp .env.example .env
# Edit INTERFACE= to match your network card name
```

### 3. Run the dashboard + capture

```bash
# Linux
sudo python run.py

# Windows (run terminal as Administrator)
python run.py
```

Open your browser: **http://localhost:5000**

### 4. Demo without real packets (simulation)

```bash
# In a separate terminal (dashboard must be running)
python simulate_traffic.py
```

This generates 80% normal + 20% tunneling-pattern events so you can see the dashboard in action without needing admin access.

---

## 🔍 Detection Rules

| Rule | Score | Threshold |
|------|-------|-----------|
| Domain length | +25 | > 80 characters |
| Max label length | +25 | > 50 characters |
| Shannon entropy | +25 | > 4.2 (random-looking) |
| Query rate | +15 | > 30 queries/min to same domain |
| Unique subdomains | +15 | > 25 unique subdomains/min |
| Abused qtype | +10 | TXT or NULL record type |

**Score ≥ 70 → ALERT**

---

## 🗂 Project Structure

```
dns-tunnel-detector/
├── collector/
│   ├── sniff_dns.py     # Packet capture (scapy, cross-platform)
│   └── normalize.py     # Raw packet → standard event dict
├── detector/
│   ├── features.py      # Length, entropy, label analysis
│   └── scorer.py        # Rule-based score 0–100 + reasons
├── storage/
│   ├── db.py            # SQLite init
│   └── repo.py          # Insert / query functions
├── services/
│   ├── pipeline.py      # capture → features → score → store → push
│   └── metrics.py       # Rolling window rate counters
├── dashboard/
│   ├── app.py           # Flask + Socket.IO app
│   ├── routes.py        # REST API endpoints
│   └── templates/
│       └── index.html   # Live dashboard UI
├── config/
│   ├── settings.py      # .env-based config
│   └── constants.py     # Detection thresholds
├── simulate_traffic.py  # Demo traffic generator
└── run.py               # Entry point
```

---

## 💻 OS-Specific Notes

| Item | Windows | Linux |
|------|---------|-------|
| Packet capture driver | Npcap (install from npcap.com) | libpcap (usually pre-installed) |
| Permissions | Run as Administrator | `sudo python run.py` |
| Interface name | "Ethernet", "Wi-Fi" | "eth0", "ens33", "wlan0" |
| Python version | 3.10+ | 3.10+ |

---

## 📊 Dashboard Features

- **Live DNS query feed** — scrolling table, color-coded by risk score
- **🚨 Alert panel** — reason tags for each flagged event
- **Query rate timeline** — 10-minute rolling line chart
- **Score distribution** — bar chart of risk score buckets
- **Top suspicious domains** — ranked with bar indicators
- **Top suspicious IPs** — ranked with bar indicators
- **Detection rules panel** — scoring weights at a glance

---

## 🧪 Testing

Simulate tunneling by running `simulate_traffic.py` which generates:
- Normal queries to google.com, github.com, etc.
- Tunneling-pattern queries with 40–70 char random subdomains, TXT/NULL types

---

## 📚 Technologies Used

- **Python 3.10+** — core language
- **scapy** — packet capture
- **Flask + Flask-SocketIO** — web server + live push
- **SQLite** — lightweight storage
- **tldextract** — domain parsing
- **Chart.js** — dashboard charts (via CDN)
- **Socket.IO JS** — live WebSocket updates

---

*Built as a university security monitoring project. For educational use only.*
