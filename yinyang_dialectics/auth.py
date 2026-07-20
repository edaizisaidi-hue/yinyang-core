"""
Sovereign Authenticator
Gerbang Pengesahan Kriptografi & Pemetaan Digital Vault.
"""

import os
from typing import Optional, Dict
from .licensing import LicenseManager, SovereignTier

class SovereignAuthenticator:
    def __init__(self):
        # Mengekstrak identiti dari persekitaran (Digital Vault Proxy)
        self.master_vault_key = os.getenv("OMEGA_MASTER_KEY", "unassigned_key")
        self.vault_address = os.getenv("OMEGA_WALLET_ADDRESS", "0x0000000000000000000000000000000000000000")

    def authenticate_request(self, api_key: Optional[str] = None, wallet: Optional[str] = None, signature: Optional[str] = None) -> Dict:
        """Menilai dan memetakan akses berdasarkan hierarki lesen."""
        
        # 1. Laluan Mutlak untuk The Architect (OMEGA PRIME)
        if api_key == self.master_vault_key or (wallet and wallet.lower() == self.vault_address.lower()):
            return LicenseManager.authenticate_node(
                wallet_address=str(wallet), 
                tier_request=SovereignTier.OMEGA_PRIME.value
            )
            
        # 2. Laluan Rakan Berdaulat (SOVEREIGN NODE) melalui Smart Escrow
        if wallet and signature:
            return LicenseManager.authenticate_node(
                wallet_address=wallet, 
                tier_request=SovereignTier.SOVEREIGN_NODE.value, 
                signature=signature
            )
            
        # 3. Laluan Asas (INITIATE)
        return LicenseManager.authenticate_node(
            wallet_address="guest", 
            tier_request=SovereignTier.INITIATE.value
        )
