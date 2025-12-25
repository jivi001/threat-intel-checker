🛡️ Threat Intel Checker

Threat Intel Checker is a Python-based threat intelligence enrichment engine that scans web server logs and IP addresses against high-confidence abuse data from AbuseIPDB.
It enables real-time attacker detection, offline IOC lookups, and SOC-ready reporting using a high-performance local SQLite database.

Built for cybersecurity analysts, blue-team engineers, and security students.

🎯 Key Capabilities

🔍 Live Threat Intelligence Enrichment via AbuseIPDB API

💾 Local SQLite IOC Cache for ultra-fast offline lookups

📊 Apache / Nginx / Common Log Format Parsing

🚨 Real-Time Threat Detection & Alerts

📈 CSV & JSON Reports (SOC-friendly)

🖥️ Cross-Platform (Linux, Windows, macOS)

⚡ Low API Usage with intelligent caching

🧠 Use Cases

SOC log monitoring & triage

Blue-team threat hunting

Incident response enrichment

Honeypot & lab analysis

Cybersecurity academic projects

Lightweight threat-intel automation

🖥️ Sample Output
🛡️  Threat Intel Log Scanner
DB stats: {'total': 12543, 'high_risk': 892}
🔴 HIT: 45.146.166.149 (score=95, country=RU)
🚨 Found 1 high-risk IPs!
💾 Saved to ./reports/log_scan_hits_20251225_155200.csv

🚀 Installation & Usage
Prerequisites

Python 3.8+

Free AbuseIPDB API Key

Step 1: Clone & Environment Setup
Linux / macOS
git clone https://github.com/jivi001/threat-intel-checker
cd threat-intel-checker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

Windows (PowerShell)
git clone https://github.com/jivi001/threat-intel-checker
cd threat-intel-checker
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt

Windows (Command Prompt)
git clone https://github.com/jivi001/threat-intel-checker
cd threat-intel-checker
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt

Step 2: Configure API Key
# Get your key from https://www.abuseipdb.com/dashboard/api
echo "ABUSEIPDB_API_KEY=your_actual_key_here" > .env


🔐 .env is git-ignored. API keys are never committed.

Step 3: Initialize Local Database
mkdir -p data logs reports      # Linux/macOS
mkdir data logs reports         # Windows

python -c "from iocstore import init_db; init_db()"

Step 4: Full Demo
# Download threat intelligence (12k+ IOCs)
python fetch_iocs.py

# Check a single IP (local DB)
python check_ip.py 8.8.8.8

# Live API check (rate-limited)
python check_ip.py 8.8.8.8 --live

# Create sample log & scan
echo '45.146.166.149 - - [$(date)] "GET /" 200' > logs/access.log
python log_scanner.py

🛠️ Command Reference
Command	Description
python fetch_iocs.py	Download threat IOCs
python log_scanner.py	Scan logs for malicious IPs
python check_ip.py <IP>	Local DB lookup
python check_ip.py <IP> --live	Live AbuseIPDB check
📁 Project Structure
threat-intel-checker/
├── config.py          # Configuration
├── abuseipdb.py       # AbuseIPDB API client
├── iocstore.py        # SQLite IOC storage engine
├── fetch_iocs.py      # IOC downloader
├── log_scanner.py     # Log analysis engine
├── check_ip.py        # CLI IP checker
├── data/iocs.db       # Local threat database
├── logs/access.log    # Sample logs
├── reports/           # CSV / JSON outputs
├── requirements.txt   # Dependencies
└── .env               # API key (ignored)

📊 Outputs Generated

data/iocs.db → Local threat database

reports/abuseipdb_iocs_*.csv → Raw IOC feeds

reports/log_scan_hits_*.csv → Detected attacks

reports/check_*.json → Detailed IP intelligence

🛡️ Risk Scoring Model
Score	Verdict	Recommended Action
0–29	LOW RISK	Allow
30–79	SUSPICIOUS	Monitor
80–100	HIGH RISK	Block
🔄 Production Deployment
Linux / macOS (Cron)
# Daily IOC refresh (09:00)
0 9 * * * cd /path/to/project && source venv/bin/activate && python fetch_iocs.py

# Hourly log scan
0 * * * * cd /path/to/project && source venv/bin/activate && python log_scanner.py

Windows (Task Scheduler)

Program: venv\Scripts\python.exe

Argument: log_scanner.py

Trigger: Hourly / Daily

🔐 Security Notes

API keys stored securely using .env

No outbound traffic unless --live is used

Offline mode works without internet access

SQLite database is local-only

🤝 Contributing

Fork the repository

Create a feature branch

git checkout -b feature/your-feature


Commit changes

git commit -m "Add feature"


Push & open a Pull Request

📄 License

MIT License — see LICENSE file.

🙏 Acknowledgments

AbuseIPDB for open threat intelligence

Built with ❤️ for cybersecurity analysts

⚡ One-Line Demo
python fetch_iocs.py && echo '45.146.166.149 - - [$(date)] "GET /" 200' > logs/access.log && python log_scanner.py

⭐ If this project helps your threat hunting, consider starring the repo
🐛 Found an issue? Open a GitHub ticket