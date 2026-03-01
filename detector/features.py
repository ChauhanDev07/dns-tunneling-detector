import math
import tldextract

def get_base_domain(qname: str) -> str:
    """Extract base domain (e.g., 'evil.com' from 'abc.xyz.evil.com')."""
    ext = tldextract.extract(qname)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return qname

def get_labels(qname: str) -> list[str]:
    return qname.split(".")

def domain_length(qname: str) -> int:
    return len(qname)

def max_label_length(qname: str) -> int:
    labels = get_labels(qname)
    return max((len(l) for l in labels), default=0)

def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((count / n) * math.log2(count / n) for count in freq.values())

def subdomain_entropy(qname: str) -> float:
    """Entropy of the subdomain portion only (most random part)."""
    ext = tldextract.extract(qname)
    subdomain = ext.subdomain
    return shannon_entropy(subdomain) if subdomain else 0.0

def extract_features(event: dict) -> dict:
    qname = event.get("qname", "")
    qtype = event.get("qtype", "A")
    base = get_base_domain(qname)

    features = {
        **event,
        "base_domain": base,
        "domain_length": domain_length(qname),
        "max_label_length": max_label_length(qname),
        "entropy": round(subdomain_entropy(qname), 4),
        "qtype": qtype,
    }
    return features
