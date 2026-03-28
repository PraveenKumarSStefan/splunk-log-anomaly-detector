from datetime import datetime, timedelta
class DedupCache:
    def __init__(self, ttl=30):
        self._cache={}; self._ttl=timedelta(minutes=ttl)
    def is_duplicate(self, k):
        if k in self._cache and datetime.now()-self._cache[k]<self._ttl: return True
        if k in self._cache: del self._cache[k]
        return False
    def mark(self, k): self._cache[k]=datetime.now()
