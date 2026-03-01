from config.constants import (
    SCORE_LONG_DOMAIN, SCORE_LONG_LABEL, SCORE_HIGH_ENTROPY,
    SCORE_HIGH_RATE, SCORE_MANY_SUBDOMAINS, SCORE_ABUSE_QTYPE,
    DOMAIN_LENGTH_THRESHOLD, LABEL_LENGTH_THRESHOLD, ENTROPY_THRESHOLD,
    RATE_PER_MIN_THRESHOLD, UNIQUE_SUBDOMAIN_THRESHOLD, ABUSED_QTYPES,
)
from config.settings import SCORE_ALERT_THRESHOLD as THRESHOLD

def score_event(features: dict, rate_per_min: int = 0, unique_subdomains: int = 0) -> dict:
    score = 0
    reasons = []

    if features.get("domain_length", 0) > DOMAIN_LENGTH_THRESHOLD:
        score += SCORE_LONG_DOMAIN
        reasons.append(f"Long domain ({features['domain_length']} chars)")

    if features.get("max_label_length", 0) > LABEL_LENGTH_THRESHOLD:
        score += SCORE_LONG_LABEL
        reasons.append(f"Long label ({features['max_label_length']} chars)")

    if features.get("entropy", 0) > ENTROPY_THRESHOLD:
        score += SCORE_HIGH_ENTROPY
        reasons.append(f"High entropy ({features['entropy']:.2f})")

    if rate_per_min > RATE_PER_MIN_THRESHOLD:
        score += SCORE_HIGH_RATE
        reasons.append(f"High query rate ({rate_per_min}/min)")

    if unique_subdomains > UNIQUE_SUBDOMAIN_THRESHOLD:
        score += SCORE_MANY_SUBDOMAINS
        reasons.append(f"Many unique subdomains ({unique_subdomains}/min)")

    if features.get("qtype", "") in ABUSED_QTYPES:
        score += SCORE_ABUSE_QTYPE
        reasons.append(f"Abused qtype ({features['qtype']})")

    score = min(score, 100)
    is_alert = score >= THRESHOLD

    return {
        "score": score,
        "reasons": reasons,
        "is_alert": is_alert,
    }
