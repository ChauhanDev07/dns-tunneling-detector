import os
from dotenv import load_dotenv

load_dotenv()

INTERFACE = os.getenv("INTERFACE", None)

SCORE_ALERT_THRESHOLD = int(os.getenv("SCORE_ALERT_THRESHOLD", 70))

FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
SECRET_KEY = os.getenv("SECRET_KEY", "dns-tunnel-secret-key")

DB_PATH = os.getenv("DB_PATH", "storage/dns_events.db")
