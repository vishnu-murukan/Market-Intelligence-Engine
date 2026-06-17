import time
from typing import Any, Optional, Dict

class CacheService:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _make_key(self, industry_or_brand: str, key_type: str) -> str:
        return f"{industry_or_brand.lower().strip()}:{key_type.lower().strip()}"

    def get(self, industry_or_brand: str, key_type: str) -> Optional[Any]:
        key = self._make_key(industry_or_brand, key_type)
        if key in self._cache:
            entry = self._cache[key]
            # If TTL is 0 or -1, it means permanent/demo cache, never expires unless invalidated
            if entry["expires_at"] == -1 or time.time() < entry["expires_at"]:
                return entry["value"]
            else:
                del self._cache[key]  # Expired
        return None

    def set(self, industry_or_brand: str, key_type: str, value: Any, ttl_seconds: int):
        # Do not cache None, empty results, or error messages
        if value is None:
            return
        if isinstance(value, str) and any(err in value.lower() for err in ["error:", "exception:", "failed", "timed out"]):
            return
        if isinstance(value, dict) and "error" in value:
            return
        if isinstance(value, list) and len(value) == 0:
            return

        key = self._make_key(industry_or_brand, key_type)
        expires_at = -1 if ttl_seconds == -1 else (time.time() + ttl_seconds)
        self._cache[key] = {
            "value": value,
            "expires_at": expires_at
        }

    def invalidate(self, industry_or_brand: str, key_type: str):
        key = self._make_key(industry_or_brand, key_type)
        if key in self._cache:
            del self._cache[key]

    def clear(self):
        self._cache.clear()

# Global cache instance
cache_service = CacheService()
