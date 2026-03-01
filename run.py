import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from storage.db import init_db
from collector.sniff_dns import start_sniffing, list_interfaces, set_callback
from services.pipeline import process_event, set_socketio
from dashboard.app import app, socketio, get_socketio
from config.settings import FLASK_HOST, FLASK_PORT

def main():
    print("=" * 60)
    print("  DNS Tunnel Detector  - Real-Time Monitor")
    print("=" * 60)

    init_db()

    try:
        ifaces = list_interfaces()
        print(f"[Collector] Available interfaces: {ifaces}")
    except Exception as e:
        print(f"[Collector] Could not list interfaces: {e}")

    sio = get_socketio()
    set_socketio(sio)

    set_callback(process_event)

    try:
        start_sniffing()
        print("[Collector] Packet capture started.")
    except Exception as e:
        print(f"[Collector] Capture failed: {e}")
        print("            Run as Administrator for real packet capture.")
        print("            Use simulate_traffic.py to demo without capture.")

    print(f"\n[Dashboard] Open browser: http://localhost:{FLASK_PORT}")
    print("=" * 60)
    socketio.run(app, host=FLASK_HOST, port=FLASK_PORT,
                 debug=False, allow_unsafe_werkzeug=True)

if __name__ == "__main__":
    main()
