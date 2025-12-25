import sqlite3
import csv
import os
from typing import List, Dict, Optional
from datetime import datetime

from config import IOC_DB_PATH, HIGH_RISK_THRESHOLD

DB_PATH = IOC_DB_PATH

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iocs (
            ip_address TEXT PRIMARY KEY,
            abuse_confidence_score INTEGER,
            total_reports INTEGER,
            country_code TEXT,
            last_reported_at TEXT,
            usage_type TEXT,
            fetched_at TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def load_from_csv(csv_path: str) -> List[Dict]:
    iocs = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            iocs.append({
                "ip_address": row["ipAddress"],
                "abuse_confidence_score": int(row["abuseConfidenceScore"]),
                "total_reports": int(row.get("totalReports", 0)),
                "country_code": row.get("countryCode", ""),
                "last_reported_at": row.get("lastReportedAt", ""),
                "usage_type": row.get("usageType", ""),
            })
    return iocs

def save_iocs(iocs: List[Dict]):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.utcnow().isoformat()
    
    for ioc in iocs:
        cursor.execute("""
            INSERT OR REPLACE INTO iocs 
            (ip_address, abuse_confidence_score, total_reports, country_code, 
             last_reported_at, usage_type, fetched_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            ioc["ip_address"],
            ioc["abuse_confidence_score"],
            ioc["total_reports"],
            ioc["country_code"],
            ioc["last_reported_at"],
            ioc["usage_type"],
            now,
        ))
    
    conn.commit()
    conn.close()
    print(f"Saved {len(iocs)} IOCs to {DB_PATH}")

def is_high_risk(ip_address: str) -> Optional[Dict]:
    """Fast lookup: is this IP in our local high-risk list?"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM iocs WHERE ip_address = ? AND abuse_confidence_score >= ?",
        (ip_address, HIGH_RISK_THRESHOLD)
    )
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            "ip_address": row[0],
            "abuse_confidence_score": row[1],
            "total_reports": row[2],
            "country_code": row[3],
            "last_reported_at": row[4],
            "usage_type": row[5],
        }
    return None

def get_stats() -> Dict:
    """Return DB stats: total IOCs, high-risk count."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM iocs")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM iocs WHERE abuse_confidence_score >= ?", 
                   (HIGH_RISK_THRESHOLD,))
    high_risk = cursor.fetchone()[0]
    
    conn.close()
    return {"total": total, "high_risk": high_risk}
