import threading
from scapy.all import sniff, DNS, DNSQR, IP

from collector.normalize import normalize_packet
from config.settings import INTERFACE

_callback = None

def set_callback(fn):
   
    global _callback
    _callback = fn

def _packet_handler(pkt):
    if not pkt.haslayer(DNS) or not pkt.haslayer(DNSQR):
        return
    event = normalize_packet(pkt)
    if event and _callback:
        _callback(event)

def list_interfaces():
    
    return get_if_list()

def start_sniffing(iface=INTERFACE):
    """Start sniffing in a background daemon thread."""
    def _run():
        kwargs = {"filter": "udp port 53 or tcp port 53", "prn": _packet_handler, "store": False}
        if iface:
            kwargs["iface"] = iface
        print(f"[Collector] Sniffing on interface: {iface or 'default'}")
        sniff(**kwargs)

    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return t
