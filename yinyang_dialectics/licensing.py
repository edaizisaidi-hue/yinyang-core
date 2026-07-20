"""
Licensing and subscription management for Yin-Yang Dialectics.
"""

from typing import Dict, List
from enum import Enum
from datetime import datetime, timedelta


class TierType(str, Enum):
    """Subscription tiers."""
    FREE = "free"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class SubscriptionTier:
    """
    Represents a subscription tier with its limits and features.
    """
    
    def __init__(
        self,
        name: str,
        monthly_price: float,
        monthly_api_calls: int,
        max_recursion_depth: int,
        custom_patterns: bool = False,
        webhook_support: bool = False,
        priority_support: bool = False,
    ):
        self.name = name
        self.monthly_price = monthly_price
        self.monthly_api_calls = monthly_api_calls
        self.max_recursion_depth = max_recursion_depth
        self.custom_patterns = custom_patterns
        self.webhook_support = webhook_support
        self.priority_support = priority_support
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "monthly_price": self.monthly_price,
            "monthly_api_calls": self.monthly_api_calls,
            "max_recursion_depth": self.max_recursion_depth,
            "features": {
                "custom_patterns": self.custom_patterns,
                "webhook_support": self.webhook_support,
                "priority_support": self.priority_support,
            }
        }


class LicenseManager:
    """
    Manages licensing tiers and subscription information.
    """
    
    # Define subscription tiers
    TIERS = {
        TierType.FREE: SubscriptionTier(
            name="Free",
            monthly_price=0.0,
            monthly_api_calls=100,
            max_recursion_depth=2,
            custom_patterns=False,
            webhook_support=False,
            priority_support=False,
        ),
        TierType.PRO: SubscriptionTier(
            name="Pro",
            monthly_price=19.99,
            monthly_api_calls=10000,
            max_recursion_depth=4,
            custom_patterns=True,
            webhook_support=True,
            priority_support=False,
        ),
        TierType.ENTERPRISE: SubscriptionTier(
            name="Enterprise",
            monthly_price=0.0,  # Custom pricing
            monthly_api_calls=1000000,  # Unlimited
            max_recursion_depth=8,
            custom_patterns=True,
            webhook_support=True,
            priority_support=True,
        ),
    }
    
    @classmethod
    def get_tier(cls, tier_type: str) -> SubscriptionTier:
        """
        Get a subscription tier by type.
        """
        return cls.TIERS.get(tier_type, cls.TIERS[TierType.FREE])
    
    @classmethod
    def list_tiers(cls) -> Dict[str, Dict]:
        """
        Get all available tiers.
        """
        return {tier: tier_obj.to_dict() for tier, tier_obj in cls.TIERS.items()}
    
    @classmethod
    def validate_usage(cls, tier_type: str, current_usage: int) -> bool:
        """
        Check if current usage is within tier limits.
        """
        tier = cls.get_tier(tier_type)
        return current_usage <= tier.monthly_api_calls
