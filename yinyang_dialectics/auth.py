"""
Authentication and API Key validation for Yin-Yang Dialectics.
"""

import hashlib
import secrets
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import json


class APIKeyValidator:
    """
    Validates API keys and manages licensing.
    
    In production, this would connect to a backend database.
    For now, it includes a local validation mechanism.
    """
    
    # Demo API keys for testing (remove in production)
    DEMO_KEYS = {
        "yd_sk_demo_free": {"tier": "free", "calls_limit": 100, "expires": None},
        "yd_sk_demo_pro": {"tier": "pro", "calls_limit": 10000, "expires": None},
    }
    
    def __init__(self):
        self.valid_keys: Dict[str, Dict] = self.DEMO_KEYS.copy()
        self.key_usage: Dict[str, int] = {}
    
    def generate_key(self, tier: str = "free") -> str:
        """
        Generate a new API key.
        
        In production, this would be called by the backend.
        """
        prefix = f"yd_sk_{tier}_"
        random_part = secrets.token_urlsafe(32)
        key = prefix + random_part
        return key
    
    def validate(self, api_key: str) -> bool:
        """
        Validate an API key.
        
        Returns True if valid, False otherwise.
        """
        if not api_key:
            return False
        
        # Check if key exists
        if api_key not in self.valid_keys:
            return False
        
        key_data = self.valid_keys[api_key]
        
        # Check expiration
        if key_data.get("expires"):
            expires = datetime.fromisoformat(key_data["expires"])
            if datetime.utcnow() > expires:
                return False
        
        return True
    
    def check_rate_limit(self, api_key: str) -> Tuple[bool, Dict[str, int]]:
        """
        Check if API key has exceeded rate limit.
        
        Returns (is_allowed, usage_info)
        """
        if not self.validate(api_key):
            return False, {"error": "Invalid API key"}
        
        key_data = self.valid_keys[api_key]
        current_usage = self.key_usage.get(api_key, 0)
        limit = key_data.get("calls_limit", 100)
        
        is_allowed = current_usage < limit
        
        return is_allowed, {
            "current_usage": current_usage,
            "limit": limit,
            "remaining": max(0, limit - current_usage),
            "tier": key_data.get("tier", "unknown")
        }
    
    def increment_usage(self, api_key: str) -> None:
        """
        Increment usage counter for an API key.
        
        In production, this would hit a database.
        """
        if api_key not in self.key_usage:
            self.key_usage[api_key] = 0
        self.key_usage[api_key] += 1
    
    def get_key_info(self, api_key: str) -> Optional[Dict]:
        """
        Get information about an API key.
        """
        if not self.validate(api_key):
            return None
        
        key_data = self.valid_keys[api_key].copy()
        key_data["current_usage"] = self.key_usage.get(api_key, 0)
        key_data["api_key"] = api_key
        
        return key_data


class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass


class RateLimitError(Exception):
    """Raised when rate limit is exceeded."""
    pass
