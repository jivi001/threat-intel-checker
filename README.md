# Threat Intel Checker

Lightweight Python tool to detect and report malicious IPs in web server logs using a local SQLite IOC database with optional live lookups via AbuseIPDB.

## Quick highlights
- Offline-first: fast local lookups via SQLite ([`iocstore.is_high_risk`](src/iocstore.py))
- Optional live enrichment from AbuseIPDB ([`abuseipdb.check_ip`](src/abuseipdb.py))
- Log scanning for common web server formats ([`log_scanner.scan_log_file`](src/log_scanner.py))
- CSV / JSON report generation (reports written to `./reports`)

## Requirements
- Python 3.8+
- See [requirements.txt](requirements.txt)

Install:
```sh
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration
Create a `.env` in the repo root with your API key:
```
ABUSEIPDB_API_KEY=your_api_key_here
```
Core configuration values live in [`src/config.py`](src/config.py).

## Initialize local DB
Create data dir and initialize the IOC DB:
```sh
python -c "from src.iocstore import init_db; init_db()"
```
See [`iocstore.init_db`](src/iocstore.py).

## Common workflows

- Download high-confidence IOCs from AbuseIPDB:
  ```sh
  python src/fetch_iocs.py
  ```
  (function: [`fetch_iocs.fetch_blacklist`](src/fetch_iocs.py))

- Check a single IP (offline + optional live):
  ```sh
  python check_ip.py 8.8.8.8         # offline lookup (local DB)
  python check_ip.py 8.8.8.8 --live  # also query AbuseIPDB
  ```
  (CLI entry: [`check_ip.main`](check_ip.py), live API: [`abuseipdb.check_ip`](src/abuseipdb.py))

- Scan a web server log for high-risk IPs:
  ```sh
  python src/log_scanner.py
  ```
  (core scanner: [`log_scanner.scan_log_file`](src/log_scanner.py); DB stats: [`iocstore.get_stats`](src/iocstore.py))

## Output
- CSV scan reports are written to `./reports` (configured via [`src/config.py`](src/config.py)).
- `check_ip.py --live` saves full JSON responses into `./reports`.

## Files of interest
- [src/log_scanner.py](src/log_scanner.py) — log parsing & scan workflow (`scan_log_file`)
- [src/iocstore.py](src/iocstore.py) — SQLite IO, lookups (`is_high_risk`, `get_stats`, `init_db`)
- [src/fetch_iocs.py](src/fetch_iocs.py) — downloads AbuseIPDB blacklist (`fetch_blacklist`)
- [src/abuseipdb.py](src/abuseipdb.py) — AbuseIPDB client (`check_ip`, `simple_verdict`)
- [check_ip.py](check_ip.py) — CLI wrapper for single-IP checks
- [requirements.txt](requirements.txt), [.gitignore](.gitignore)

## Tips
- Keep your `.env` out of version control (already in `.gitignore`).
- For production automation, run `src/fetch_iocs.py` regularly and scan logs on a schedule.
- Tune thresholds via [`src/config.py`](src/config.py): `HIGH_RISK_THRESHOLD`, `MAX_AGE_DAYS`.

## License
MIT — see [LICENSE](LICENSE)

