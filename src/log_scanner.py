import re
import os
import csv
from datetime import datetime
from collections import Counter

from config import LOG_FILE_PATH, HIGH_RISK_THRESHOLD, REPORTS_DIR
from iocstore import is_high_risk, get_stats
from abuseipdb import check_ip, simple_verdict

# Regex to extract IP addresses from common log formats
IP_REGEX = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")


def scan_log_file(log_path: str) -> list:
    """Scan log file, extract unique IPs, check against IOC DB.
    Returns list of hits with details.
    """
    if not os.path.exists(log_path):
        print(f"Log file not found: {log_path}")
        return []

    hits = []
    unique_ips = set()

    print(f"Scanning {log_path}...")

    with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_num, line in enumerate(f, 1):
            # Extract all IPs from this log line
            ips = IP_REGEX.findall(line)
            for ip in ips:
                unique_ips.add(ip)

    print(f"Found {len(unique_ips)} unique IPs in log")

    # Check each unique IP against local IOC database
    for ip in unique_ips:
        risk_data = is_high_risk(ip)
        if risk_data:
            hits.append({
                "ip": ip,
                "score": risk_data.get("abuse_confidence_score"),
                "reports": risk_data.get("total_reports"),
                "country": risk_data.get("country_code"),
                "source": "local_db",
            })
            print(f"🔴 HIT: {ip} (score={risk_data.get('abuse_confidence_score')})")

    return hits


def save_hits_report(hits: list):
    """Save scan results to timestamped CSV."""
    if not hits:
        print("No hits found.")
        return

    os.makedirs(REPORTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"log_scan_hits_{ts}.csv")

    fieldnames = ["ip", "score", "reports", "country", "source", "scan_time"]

    with open(report_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for hit in hits:
            row = {**hit, "scan_time": datetime.now().isoformat()}
            writer.writerow(row)

    print(f"💾 Saved {len(hits)} hits to {report_path}")


def main():
    """Main scanning workflow."""
    print("🛡️  Threat Intel Log Scanner")
    print(f"DB stats: {get_stats()}")

    hits = scan_log_file(LOG_FILE_PATH)

    if hits:
        print(f"\n🚨 Found {len(hits)} high-risk IPs!")
        save_hits_report(hits)
    else:
        print("\n✅ No high-risk IPs detected.")


if __name__ == "__main__":
    main()
