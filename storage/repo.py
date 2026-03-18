import json
from storage.db import get_connection

<<<<<<< HEAD
=======

>>>>>>> 05ab3fa (updated API logic)
def insert_event(event: dict, score: int):
    conn = get_connection()
    conn.execute("""
        INSERT INTO dns_events (ts, src_ip, dst_ip, qname, qtype, base_domain,
                                domain_length, max_label_length, entropy, score)
        VALUES (:ts, :src_ip, :dst_ip, :qname, :qtype, :base_domain,
                :domain_length, :max_label_length, :entropy, :score)
<<<<<<< HEAD
        INSERT INTO alerts (ts, src_ip, base_domain, qname, qtype, score, reasons)
        VALUES (:ts, :src_ip, :base_domain, :qname, :qtype, :score, :reasons)
        SELECT * FROM alerts ORDER BY ts DESC LIMIT ?
        SELECT * FROM dns_events ORDER BY ts DESC LIMIT ?
=======
    """, {**event, "score": score})
    conn.commit()


def insert_alert(event: dict, score: int, reasons: list):
    conn = get_connection()
    conn.execute("""
        INSERT INTO alerts (ts, src_ip, base_domain, qname, qtype, score, reasons)
        VALUES (:ts, :src_ip, :base_domain, :qname, :qtype, :score, :reasons)
    """, {**event, "score": score, "reasons": json.dumps(reasons)})
    conn.commit()


def get_recent_alerts(limit=50):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM alerts ORDER BY ts DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_recent_events(limit=100):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM dns_events ORDER BY ts DESC LIMIT ?", (limit,)
    ).fetchall()
    return [dict(r) for r in rows]


def get_top_suspicious_domains(limit=10):
    conn = get_connection()
    rows = conn.execute("""
>>>>>>> 05ab3fa (updated API logic)
        SELECT base_domain, COUNT(*) as count, MAX(score) as max_score
        FROM alerts
        GROUP BY base_domain
        ORDER BY count DESC
        LIMIT ?
<<<<<<< HEAD
=======
    """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_top_suspicious_ips(limit=10):
    conn = get_connection()
    rows = conn.execute("""
>>>>>>> 05ab3fa (updated API logic)
        SELECT src_ip, COUNT(*) as count, MAX(score) as max_score
        FROM alerts
        GROUP BY src_ip
        ORDER BY count DESC
        LIMIT ?
<<<<<<< HEAD
Returns per-minute query counts for the last N minutes."""
=======
    """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def get_query_rate_timeline(minutes=10):
    """Returns per-minute query counts for the last N minutes."""
>>>>>>> 05ab3fa (updated API logic)
    conn = get_connection()
    rows = conn.execute("""
        SELECT strftime('%Y-%m-%dT%H:%M:00', ts) as minute, COUNT(*) as count
        FROM dns_events
        WHERE ts >= datetime('now', ? || ' minutes')
        GROUP BY minute
        ORDER BY minute ASC
<<<<<<< HEAD
=======
    """, (f"-{minutes}",)).fetchall()
    return [dict(r) for r in rows]


def get_stats_summary():
    """Return high-level aggregate stats."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM dns_events").fetchone()[0]
    alerts = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    unique_domains = conn.execute("SELECT COUNT(DISTINCT base_domain) FROM dns_events").fetchone()[0]
    unique_ips = conn.execute("SELECT COUNT(DISTINCT src_ip) FROM dns_events").fetchone()[0]
    avg_score = conn.execute("SELECT ROUND(AVG(score), 1) FROM dns_events").fetchone()[0] or 0
    max_score = conn.execute("SELECT MAX(score) FROM dns_events").fetchone()[0] or 0
    return {
        "total_queries": total,
        "total_alerts": alerts,
        "unique_domains": unique_domains,
        "unique_ips": unique_ips,
        "avg_score": avg_score,
        "max_score": max_score,
    }


def get_qtype_distribution():
    """Return query type counts."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT qtype, COUNT(*) as count
        FROM dns_events
        GROUP BY qtype
        ORDER BY count DESC
        LIMIT 10
    """).fetchall()
    return [dict(r) for r in rows]


def search_events(query: str, min_score: int = 0, limit: int = 50):
    """Full-text search across qname, src_ip, base_domain."""
    conn = get_connection()
    like = f"%{query}%"
    rows = conn.execute("""
        SELECT * FROM dns_events
        WHERE (qname LIKE ? OR src_ip LIKE ? OR base_domain LIKE ?)
          AND score >= ?
        ORDER BY ts DESC
        LIMIT ?
    """, (like, like, like, min_score, limit)).fetchall()
    return [dict(r) for r in rows]


def clear_alerts():
    """Delete all alert records and return count deleted."""
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) FROM alerts").fetchone()[0]
    conn.execute("DELETE FROM alerts")
    conn.commit()
    return count
>>>>>>> 05ab3fa (updated API logic)
