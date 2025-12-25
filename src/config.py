import os


ABUSEIPDB_BASE_URL = "https://api.abuseipdb.com/api/v2/"
ABUSEIPDB_CHECK_ENDPOINT = f"{ABUSEIPDB_BASE_URL}/check"


MAX_AGE_DAY = int(os.getenv("MAX_AGE_DAY", 60))


HIGH_RISK_THRESHOLD = int(os.getenv("HIGH_RISK_THRESHOLD", "80"))
MEDIUM_RISK_THRESHOLD = int(os.getenv("MEDIUM_RISK_THRESHOLD", "30"))

LOG_FILE_PATH = os.getenv("LOG_FILE_PATH", "./logs/access.log")
IOC_DB_PATH = os.getenv("IOC_DB_PATH", "./data/iocs.db")
REPORTS_DIR = os.getenv("REPORTS_DIR", "./reports")