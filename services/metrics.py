import time
from collections import defaultdict, deque
from config.constants import RATE_WINDOW_SECONDS
import tldextract

class RollingCounter:
    """Tracks counts within a sliding time window."""

    def __init__(self, window_seconds=RATE_WINDOW_SECONDS):
        self.window = window_seconds
        self._events: dict[str, deque] = defaultdict(deque)
        self._subdomains: dict[str, dict] = defaultdict(dict)

    def record(self, base_domain: str, qname: str):
        now = time.time()
        dq = self._events[base_domain]
        dq.append(now)
        while dq and dq[0] < now - self.window:
            dq.popleft()

        ext = tldextract.extract(qname)
        sub = ext.subdomain
        if sub:
            self._subdomains[base_domain][sub] = now

        self._subdomains[base_domain] = {
            s: t for s, t in self._subdomains[base_domain].items()
            if t >= now - self.window
        }

    def rate_per_min(self, base_domain: str) -> int:
        now = time.time()
        dq = self._events.get(base_domain, deque())
        recent = [t for t in dq if t >= now - 60]
        return len(recent)

    def unique_subdomains(self, base_domain: str) -> int:
        return len(self._subdomains.get(base_domain, {}))

metrics = RollingCounter()
