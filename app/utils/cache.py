import time

class SimpleCache:
    def __init__(self):
        self._cache = {}

    def get(self, key: str):
        item = self._cache.get(key)
        if item:
            expiry, value = item
            if time.time() < expiry:
                return value
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value, ttl_seconds: int = 3600):
        expiry = time.time() + ttl_seconds
        self._cache[key] = (expiry, value)

    def clear(self):
        self._cache = {}

# Global cache instance
cache_instance = SimpleCache()
