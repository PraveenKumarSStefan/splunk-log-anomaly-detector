from datetime import datetime, timedelta
class DedupCache:
    def __init__(self, ttl_minutes=30):
        self._cache = {}
        self._ttl = timedelta(minutes=ttl_minutes)
    def is_duplicate(self, key):
        if key in self._cache and datetime.now() - self._cache[key] < self._ttl: return True
        if key in self._cache: del self._cache[key]
        return False
    def mark(self, key): self._cache[key] = datetime.now()
