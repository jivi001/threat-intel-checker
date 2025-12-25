import os
import csv
import requests
from datetime import datetime
from dotenv import load_dotenv

from config import (
    ABUSEIPDB_BASE_URL,
    MAX_AGE_DAYS,
    HIGH_RISK_THRESHOLD,
    REPORTS_DIR,
)

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
if not API_KEY:
    raise RuntimeError("ABUSEIPDB_API_KEY not set in environment/.env")

SESSION = requests.Session()
SESSION.headers.update({
    "Key": API_KEY,
    "Accept": "application/json",
})


def fetch_blacklist():
    """Fetch high-confidence blacklist from AbuseIPDB."""
    url = f"{ABUSEIPDB_BASE_URL}/blacklist"
    params = {
        "confidenceMinimum": HIGH_RISK_THRESHOLD,
        "limit": 10000,
    }

    resp = SESSION.get(url, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    # expected: {"data": [{"ipAddress": "...", "abuseConfidenceScore": 100, ...}, ...]}
    return data.get("data", [])


def save_to_csv(iocs):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    ts = datetime.utcnow().strftime("%d%m%Y_%H%M%S")
    out_path = os.path.join(REPORTS_DIR, f"abuseipdb_iocs_{ts}.csv")

    fieldnames = ["ipAddress", "abuseConfidenceScore", "lastReportedAt", "countryCode"]

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in iocs:
            writer.writerow({
                "ipAddress": item.get("ipAddress"),
                "abuseConfidenceScore": item.get("abuseConfidenceScore"),
                "lastReportedAt": item.get("lastReportedAt"),
                "countryCode": item.get("countryCode"),
            })

    print(f"Saved {len(iocs)} IOCs to {out_path}")


def main():
    print("Fetching high‑risk IPs from AbuseIPDB...")
    iocs = fetch_blacklist()
    print(f"Fetched {len(iocs)} records")
    save_to_csv(iocs)


if __name__ == "__main__":
    main()
