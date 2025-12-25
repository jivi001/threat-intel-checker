"""
Simple CLI tool to check any IP's reputation via AbuseIPDB.
Usage: python3 check_ip.py 8.8.8.8
"""

import sys
import argparse
from datetime import datetime

from config import REPORTS_DIR
from abuseipdb import check_ip, simple_verdict
from iocstore import is_high_risk

def main():
    parser = argparse.ArgumentParser(description="Check IP reputation")
    parser.add_argument("ip", help="IP address to check")
    parser.add_argument("--live", action="store_true", help="Check live API (not just local DB)")
    args = parser.parse_args()
    
    ip = args.ip.strip()
    
    print(f"🔍 Checking {ip}...")
    print("=" * 50)
    
    # Always check local DB first (fast)
    local_hit = is_high_risk(ip)
    if local_hit:
        print("📊 LOCAL DB HIT:")
        print(f"   Score: {local_hit['abuse_confidence_score']}")
        print(f"   Reports: {local_hit['total_reports']}")
        print(f"   Country: {local_hit['country_code']}")
        print()
    
    # Optional live API check
    if args.live:
        print("🌐 Live API check...")
        try:
            data = check_ip(ip)
            verdict = simple_verdict(data)
            print(f"   Verdict: {verdict}")
            
            # Save detailed result
            save_detailed_report(ip, data)
            
        except Exception as e:
            print(f"   ❌ API error: {e}")
    
    else:
        print("💡 Run with --live for fresh API data")

def save_detailed_report(ip: str, data: dict):
    """Save full API response to reports folder."""
    import json
    import os
    
    os.makedirs(REPORTS_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = os.path.join(REPORTS_DIR, f"check_{ip}_{ts}.json")
    
    full_report = {
        "ip": ip,
        "checked_at": datetime.now().isoformat(),
        "api_data": data
    }
    
    with open(report_path, "w") as f:
        json.dump(full_report, f, indent=2)
    
    print(f"💾 Full report saved: {report_path}")

if __name__ == "__main__":
    main()
