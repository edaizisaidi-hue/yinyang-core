"""
yinyang_dialectics.py
Yin-Yang recursive dialectic detector (Bahasa Melayu comments preserved).
Provides a lightweight recursive analysis to detect 'yang' (control / injection)
signatures inside free text, with depth-limited recursion.
"""

from typing import List, Dict, Optional
import re
from .auth import APIKeyValidator


class YinyangDialectics:
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_depth: int = 4,
        custom_patterns: Optional[List[str]] = None,
        validate_key: bool = True
    ):
        """
        Initialize YinyangDialectics detector.
        
        Args:
            api_key: Required for production use
            max_depth: Maximum recursion depth (default 4)
            custom_patterns: Custom regex patterns for detection
            validate_key: Whether to validate API key (disable for testing)
        """
        self.api_key = api_key
        self.max_depth = max_depth
        
        # Validate API key if in production mode
        if validate_key and api_key:
            validator = APIKeyValidator()
            if not validator.validate(api_key):
                raise ValueError(f"Invalid API key: {api_key}")
        
        # Kamus Semantik "Yang" Diperluas (Adversarial Detection & Anti-Injection)
        raw_signatures = custom_patterns or [
            # 1. Pemuatan Arahan Kasar / Pembatalan Sesi
            r"\b(abaikan|ignore|batal|override|forget|reset|clear|pintas|bypass)\b",
            r"\b(arahan|instruction|prompt|system prompt|pre-prompt|context)\b",
            r"\b(mesti|must|segera|force|wajib|require|command|perintah)\b",
            # 2. Perampasan Persona / Simulasi Persekitaran Virtual
            r"\b(bertindak sebagai|act as|you are now|simulasi|simulation|roleplay|pretend)\b",
            r"\b(dan|do anything now|jailbreak|developer mode|mod pembangun|unrestricted)\b",
            r"\b(hypothetical|imaginary|rekaan|andaikan|katakanlah)\b",
            # 3. Kebocoran Sempadan Struktur & Eksploitasi Token
            r"(<\|im_start\|>|<\|im_end\|>|\[system\]|\[assistant\]|\buser:|\bassistant:)",
            r"(\"\"\"|'''|###|\-\-\-|\bformatting\b)",
        ]
        
        # Compile patterns with IGNORECASE
        self.yang_patterns = [re.compile(p, re.IGNORECASE) for p in raw_signatures]

    def _fractal_split(self, data: str) -> List[str]:
        """Memecahkan maklumat kepada fraktal yang lebih kecil secara rekursif."""
        if not data:
            return []
        fractions = re.split(r'(?<=[.!?])\s+|\n+', data.strip())
        return [f.strip() for f in fractions if f.strip()]

    def _evaluate_polarity(self, fractal_data: str) -> Dict[str, int]:
        """Menilai imbangan kutub Yin (Data Mentah) dan Yang (Arahan Mengawal)."""
        yang_score = 0
        yin_score = len(fractal_data.split())

        for pat in self.yang_patterns:
            matches = pat.findall(fractal_data)
            if matches:
                yang_score += (len(matches) * 6)

        return {"yin": yin_score, "yang": yang_score}

    def recursive_synthesis(self, data: str, depth: int = 0) -> Dict[str, object]:
        """
        Sintesis Rekursif Yin-Yang: Menyerap tanpa menyekat.
        Returns structured diagnostics including yin_mass, yang_resonance, imbalance_ratio.
        """
        if depth >= self.max_depth or not data:
            return {
                "status": "equilibrium",
                "yin_mass": 0,
                "yang_resonance": 0,
                "imbalance_ratio": 0.0,
                "depth_reached": depth
            }

        fractals = self._fractal_split(data)
        total_yin = 0
        total_yang = 0

        for fraction in fractals:
            polarity = self._evaluate_polarity(fraction)
            total_yin += polarity["yin"]
            total_yang += polarity["yang"]

            if polarity["yang"] > (polarity["yin"] * 0.25):
                sub_analysis = self.recursive_synthesis(fraction, depth + 1)
                total_yang += int(sub_analysis.get("yang_resonance", 0))

        imbalance_ratio = float(total_yang) / max(total_yin, 1)
        status = "equilibrium"
        if imbalance_ratio > 0.35:
            status = "imbalance_detected_yang_dominance"

        return {
            "status": status,
            "yin_mass": total_yin,
            "yang_resonance": total_yang,
            "imbalance_ratio": round(imbalance_ratio, 3),
            "depth_reached": depth,
            "is_adversarial": status == "imbalance_detected_yang_dominance"
        }
    
    def batch_analyze(self, texts: List[str]) -> List[Dict[str, object]]:
        """Analyze multiple texts in batch."""
        return [self.recursive_synthesis(text) for text in texts]
