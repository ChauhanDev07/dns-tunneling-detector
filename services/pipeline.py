from detector.features import extract_features
from detector.scorer import score_event
from storage.repo import insert_event, insert_alert
from services.metrics import metrics

_socketio = None

def set_socketio(sio):
    global _socketio
    _socketio = sio

def process_event(raw_event: dict):
    """Called for every DNS event captured by the collector."""
    features = extract_features(raw_event)
    base = features.get("base_domain", "")

    metrics.record(base, features["qname"])
    rate = metrics.rate_per_min(base)
    unique_subs = metrics.unique_subdomains(base)

    result = score_event(features, rate_per_min=rate, unique_subdomains=unique_subs)
    score = result["score"]
    reasons = result["reasons"]
    is_alert = result["is_alert"]

    insert_event(features, score)
    if is_alert:
        insert_alert(features, score, reasons)

    if _socketio:
        event_payload = {
            "ts": features["ts"],
            "src_ip": features.get("src_ip", ""),
            "qname": features.get("qname", ""),
            "qtype": features.get("qtype", ""),
            "base_domain": base,
            "score": score,
            "entropy": features.get("entropy", 0),
        }
        _socketio.emit("dns_event", event_payload, namespace="/")

        if is_alert:
            alert_payload = {**event_payload, "reasons": reasons}
            _socketio.emit("alert", alert_payload, namespace="/")
