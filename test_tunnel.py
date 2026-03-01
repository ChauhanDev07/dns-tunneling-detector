import sys
sys.path.insert(0, '.')
from storage.db import init_db
from services.pipeline import process_event, set_socketio

class FakeSIO:
    def emit(self, *a, **k): pass

set_socketio(FakeSIO())
init_db()

process_event({
    "ts": "2026-01-01T12:00:00",
    "src_ip": "192.168.1.99",
    "dst_ip": "8.8.8.8",
    "qname": "ajd92kdkd9dkkd9d9d9d9aabbccdd112233.evil-c2.com",
    "qtype": "TXT",
})

print("Done — check dashboard at http://localhost:5000")
