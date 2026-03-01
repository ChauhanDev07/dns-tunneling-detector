import time
import random
import string
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dashboard.app import app, socketio
from services.pipeline import process_event, set_socketio
from storage.db import init_db

set_socketio(socketio)
init_db()

def rand_str(n):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=n))

NORMAL_DOMAINS = [
    "google.com", "cloudflare.com", "facebook.com",
    "github.com", "youtube.com", "microsoft.com",
    "amazon.com", "twitter.com", "reddit.com",
]

def normal_event():
    sub = random.choice(["www", "mail", "cdn", "api", "static"])
    domain = random.choice(NORMAL_DOMAINS)
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "src_ip": f"192.168.1.{random.randint(2, 20)}",
        "dst_ip": "8.8.8.8",
        "qname": f"{sub}.{domain}",
        "qtype": "A",
    }

def tunnel_event():
    base = random.choice(["evil-c2.com", "tunnel.net", "exfil-data.io", "badactor.xyz"])
    sub = rand_str(random.randint(40, 70))
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "src_ip": f"192.168.1.{random.randint(100, 110)}",
        "dst_ip": "1.2.3.4",
        "qname": f"{sub}.{base}",
        "qtype": random.choice(["TXT", "NULL", "A"]),
    }

print("[Simulator] Starting — open http://localhost:5000 in browser")
print("[Simulator] Press Ctrl+C to stop\n")

count = 0
with app.app_context():
    try:
        while True:
            is_tunnel = random.random() < 0.25
            event = tunnel_event() if is_tunnel else normal_event()
            process_event(event)
            tag = "TUNNEL" if is_tunnel else "normal"
            print(f"  [{tag}]  {event['src_ip']:15s}  {event['qname'][:60]}")
            count += 1
            time.sleep(random.uniform(0.2, 0.6))
    except KeyboardInterrupt:
        print(f"\n[Simulator] Stopped. Sent {count} events.")
