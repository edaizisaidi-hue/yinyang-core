"""
Yin-Yang Dialectics: Proprietary Adversarial Detection Engine

Version: 1.0.0
Author: edaizisaidi-hue
License: Proprietary
"""

from .core import YinyangDialectics
from .auth import APIKeyValidator
from .licensing import LicenseManager

__version__ = "1.0.0"
__author__ = "edaizisaidi-hue"

__all__ = [
    "YinyangDialectics",
    "APIKeyValidator",
    "LicenseManager",
]
