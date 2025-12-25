# Threat Intel Checker

Threat Intel Checker is a Python-based threat intelligence enrichment tool that detects malicious IP addresses in web server logs using curated abuse data from **AbuseIPDB**.
It supports fast offline lookups via a local SQLite database with optional live intelligence checks for up-to-date threat context.

Designed for SOC workflows, blue-team operations, and cybersecurity research.

---

## Features

* Threat intelligence enrichment using AbuseIPDB
* High-speed local SQLite IOC database
* Apache, Nginx, and Common Log Format parsing
* Real-time detection of high-risk IP addresses
* CSV and JSON report generation
* Offline-first design with optional live API checks
* Cross-platform support (Linux, Windows, macOS)

---

## Use Cases

* Security Operations Center (SOC) log analysis
* Incident response and alert enrichment
* Threat hunting and investigation
* Honeypot and lab log analysis
* Cybersecurity academic and portfolio projects

---

## Sample Output

```text
Threat Intel Log Scanner
-----------------------
IOC Database:
  Total indicators : 12,543
  High-risk IPs    : 892

[ALERT] Malicious IP detected
IP Address : 45.146.166.149
Risk Score : 95
Country    : RU
Verdict    : HIGH RISK (BLOCK)

Report saved to:
./reports/log_scan_hits_20251225_155200.csv
```

---

## Requirements

* Python 3.8 or later
* Free AbuseIPDB API key

---

## Installation

### Clone Repository

```bash
git clone https://github.com/jivi001/threat-intel-checker
cd threat-intel-checker
```

### Virtual Environment Setup

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```env
ABUSEIPDB_API_KEY=your_api_key_here
```

> The `.env` file is excluded from version control.

---

## Initialization

```bash
mkdir data logs reports
python -c "from iocstore import init_db; init_db()"
```

---

## Usage

### Download Threat Indicators

```bash
python fetch_iocs.py
```

### Check a Single IP (Offline)

```bash
python check_ip.py 8.8.8.8
```

### Live Threat Intelligence Lookup

```bash
python check_ip.py 8.8.8.8 --live
```

### Scan Web Server Logs

```bash
python log_scanner.py
```

---

## Command Reference

| Command                   | Description                           |
| ------------------------- | ------------------------------------- |
| `fetch_iocs.py`           | Download and update threat indicators |
| `log_scanner.py`          | Scan logs for malicious IPs           |
| `check_ip.py <IP>`        | Offline IOC database lookup           |
| `check_ip.py <IP> --live` | Live AbuseIPDB lookup                 |

---

## Project Structure

```text
threat-intel-checker/
├── abuseipdb.py        # Threat intelligence client
├── iocstore.py         # SQLite IOC storage engine
├── fetch_iocs.py       # IOC downloader
├── log_scanner.py      # Log analysis engine
├── check_ip.py         # CLI interface
├── config.py           # Configuration
├── data/
│   └── iocs.db         # Local threat database
├── logs/
│   └── access.log      # Sample log file
├── reports/            # Generated reports
├── requirements.txt
└── .env                # API key (ignored)
```

---

## Risk Scoring Model

| Score Range | Classification | Recommended Action |
| ----------- | -------------- | ------------------ |
| 0–29        | Low Risk       | Allow              |
| 30–79       | Suspicious     | Monitor            |
| 80–100      | High Risk      | Block              |

---

## Automation (Production Use)

### Linux / macOS (Cron)

```bash
# Daily IOC refresh
0 9 * * * python fetch_iocs.py

# Hourly log scan
0 * * * * python log_scanner.py
```

### Windows (Task Scheduler)

* Program: `venv\Scripts\python.exe`
* Arguments: `log_scanner.py`
* Trigger: Hourly or daily

---

## Security Notes

* API keys stored securely using environment variables
* No outbound network traffic unless live mode is enabled
* Local SQLite database only (no external exposure)
* Suitable for offline and restricted environments

---

## License

MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

Threat intelligence data provided by AbuseIPDB.

---

## One-Line Demo

```bash
python fetch_iocs.py && echo '45.146.166.149 - - [GET / HTTP/1.1] 200' > logs/access.log && python log_scanner.py
```

