# Threat Intel Checker

Lightweight Python tool to detect and report malicious IPs in web server logs using a local SQLite IOC database with optional live lookups via AbuseIPDB.

**Supports: Windows, macOS, Linux**

## Quick highlights
- Offline-first: fast local lookups via SQLite ([`src/iocstore.is_high_risk`](src/iocstore.py))
- Optional live enrichment from AbuseIPDB ([`src/abuseipdb.check_ip`](src/abuseipdb.py))
- Log scanning for common web server formats ([`src/log_scanner.scan_log_file`](src/log_scanner.py))
- CSV / JSON report generation (reports written to `./reports`)
- **Cross-platform**: runs on Windows, macOS, and Linux

## Requirements
- Python 3.8+
- See [requirements.txt](requirements.txt)

## Installation

### Linux / macOS
```sh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows (PowerShell)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Windows (Command Prompt)
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Configuration
Create a `.env` in the repo root with your API key:
```
ABUSEIPDB_API_KEY=your_api_key_here
```
Core configuration values live in [`src/config.py`](src/config.py).

## Initialize local DB

### Linux / macOS
```sh
PYTHONPATH=./src python -c "from iocstore import init_db; init_db()"
```

### Windows (PowerShell)
```powershell
$env:PYTHONPATH="./src"; python -c "from iocstore import init_db; init_db()"
```

### Windows (Command Prompt)
```cmd
set PYTHONPATH=./src
python -c "from iocstore import init_db; init_db()"
```

See [`iocstore.init_db`](src/iocstore.py).

## Common workflows

### Download IOCs from AbuseIPDB

**Linux / macOS:**
```sh
PYTHONPATH=./src python src/fetch_iocs.py
```

**Windows (PowerShell):**
```powershell
$env:PYTHONPATH="./src"; python src/fetch_iocs.py
```

**Windows (Command Prompt):**
```cmd
set PYTHONPATH=./src
python src/fetch_iocs.py
```

### Check a single IP

**Linux / macOS (offline):**
```sh
PYTHONPATH=./src python check_ip.py 8.8.8.8
```

**Linux / macOS (with live lookup):**
```sh
PYTHONPATH=./src python check_ip.py 8.8.8.8 --live
```

**Windows PowerShell:**
```powershell
$env:PYTHONPATH="./src"; python check_ip.py 8.8.8.8 --live
```

**Windows Command Prompt:**
```cmd
set PYTHONPATH=./src
python check_ip.py 8.8.8.8 --live
```

### Scan a web server log

**Linux / macOS:**
```sh
PYTHONPATH=./src python src/log_scanner.py
```

**Windows:**
```cmd
set PYTHONPATH=./src
python src/log_scanner.py
```

## Output
- CSV scan reports are written to `./reports` (cross-platform compatible paths)
- `check_ip.py --live` saves full JSON responses into `./reports`
- Database file stored at `./data/iocs.db`

## Files of interest
- [src/log_scanner.py](src/log_scanner.py) — log parsing & scan workflow (`scan_log_file`)
- [src/iocstore.py](src/iocstore.py) — SQLite IO, lookups (`is_high_risk`, `get_stats`, `init_db`)
- [src/fetch_iocs.py](src/fetch_iocs.py) — downloads AbuseIPDB blacklist (`fetch_blacklist`)
- [src/abuseipdb.py](src/abuseipdb.py) — AbuseIPDB client (`check_ip`, `simple_verdict`)
- [check_ip.py](check_ip.py) — CLI wrapper for single-IP checks
- [src/config.py](src/config.py) — configuration (uses `pathlib` for cross-platform paths)
- [requirements.txt](requirements.txt), [.gitignore](.gitignore)

## Tips
- Keep your `.env` out of version control (already in `.gitignore`)
- For production automation, run `src/fetch_iocs.py` regularly and scan logs on a schedule
- Tune thresholds via [`src/config.py`](src/config.py): `HIGH_RISK_THRESHOLD`, `MAX_AGE_DAYS`
- All paths use `pathlib.Path` for automatic cross-platform support

## License
MIT — see [LICENSE](LICENSE)
