from datetime import datetime
from scapy.all import DNS, DNSQR, IP

QTYPE_MAP = {
    1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR",
    15: "MX", 16: "TXT", 28: "AAAA", 255: "ANY", 10: "NULL"
}

def normalize_packet(pkt) -> dict | None:
    try:
        dns = pkt[DNS]
        if dns.qdcount < 1 or not pkt.haslayer(DNSQR):
            return None

        qname_raw = pkt[DNSQR].qname
        if isinstance(qname_raw, bytes):
            qname = qname_raw.decode("utf-8", errors="replace").rstrip(".")
        else:
            qname = str(qname_raw).rstrip(".")

        qtype_int = pkt[DNSQR].qtype
        qtype = QTYPE_MAP.get(qtype_int, str(qtype_int))

        src_ip = pkt[IP].src if pkt.haslayer(IP) else "unknown"
        dst_ip = pkt[IP].dst if pkt.haslayer(IP) else "unknown"

        return {
            "ts": datetime.utcnow().isoformat(),
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "qname": qname,
            "qtype": qtype,
        }
    except Exception:
        return None
