import os
import requests
from dotenv import load_dotenv

from config import ABUSEIPDB_API_URL, MAX_AGE_DAYS

load_dotenv()

API_KEY = os.getenv("ABUSEIPDB_API_KEY")
if not API_KEY:
    raise RuntimeError("ABUSEIPDB_API_KEY not set in environment/.env")

SESSION = requests.Session()
SESSION.headers.update({
    "Key": API_KEY,
    "Accept": "application/json",
})


def check_ip(ip_address: str, max_age_days: int | None = None) -> dict:
    params = {
        "ipAddress": ip_address,
        "maxAgeInDays": max_age_days or MAX_AGE_DAYS,
        "verbose": True,
    }

    resp = SESSION.get(ABUSEIPDB_API_URL, params=params, timeout=15)
    resp.raise_for_status()
    payload = resp.json()

    # AbuseIPDB puts the useful info inside the 'data' key.
    return payload.get("data", {})


def simple_verdict(ip_data: dict) -> str:
    score = ip_data.get("abuseConfidenceScore", 0)
    total_reports = ip_data.get("totalReports", 0)
    last_seen = ip_data.get("lastReportedAt", "N/A")
    country = ip_data.get("countryCode", "N/A")

    if score >= 80:
        label = "HIGH RISK"
    elif score >= 30:
        label = "SUSPICIOUS"
    else:
        label = "LOW RISK"

    return (
        f"{label} | score={score}, reports={total_reports}, "
        f"last_seen={last_seen}, country={country}"
    )
