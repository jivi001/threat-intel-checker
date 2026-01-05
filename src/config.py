import os
from pathlib import Path

# Cross-platform base directory
BASE_DIR = Path(__file__).parent.parent

# Database path (works on Windows/Mac/Linux)
DATA_DIR = BASE_DIR / "data"
IOC_DB_PATH = str(DATA_DIR / "iocs.db")

# Reports directory
REPORTS_DIR = str(BASE_DIR / "reports")

# AbuseIPDB settings
HIGH_RISK_THRESHOLD = 50
MAX_AGE_DAYS = 90
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"


# Load API key from environment
ABUSEIPDB_API_KEY = os.getenv("ABUSEIPDB_API_KEY", "")
