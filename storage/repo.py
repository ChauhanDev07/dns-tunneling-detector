import json
from storage.db import get_connection

def insert_event(event: dict, score: int):
    conn = get_connection()
    conn.execute("""
        INSERT INTO dns_events (ts, src_ip, dst_ip, qname, qtype, base_domain,
                                domain_length, max_label_length, entropy, score)
        VALUES (:ts, :src_ip, :dst_ip, :qname, :qtype, :base_domain,
                :domain_length, :max_label_length, :entropy, :score)
        INSERT INTO alerts (ts, src_ip, base_domain, qname, qtype, score, reasons)
        VALUES (:ts, :src_ip, :base_domain, :qname, :qtype, :score, :reasons)
        SELECT * FROM alerts ORDER BY ts DESC LIMIT ?
        SELECT * FROM dns_events ORDER BY ts DESC LIMIT ?
        SELECT base_domain, COUNT(*) as count, MAX(score) as max_score
        FROM alerts
        GROUP BY base_domain
        ORDER BY count DESC
        LIMIT ?
        SELECT src_ip, COUNT(*) as count, MAX(score) as max_score
        FROM alerts
        GROUP BY src_ip
        ORDER BY count DESC
        LIMIT ?
Returns per-minute query counts for the last N minutes."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT strftime('%Y-%m-%dT%H:%M:00', ts) as minute, COUNT(*) as count
        FROM dns_events
        WHERE ts >= datetime('now', ? || ' minutes')
        GROUP BY minute
        ORDER BY minute ASC
