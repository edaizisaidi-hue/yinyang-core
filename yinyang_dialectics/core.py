"""
Yin-Yang Recursive Dialectic Matrix
Sovereign Dynamic Scaling (Wafq 369 Protocol)
"""

import re
from typing import List, Dict, Optional
from .auth import SovereignAuthenticator

class YinyangDialectics:
    def __init__(self, max_dynamic_depth: int = 9):
        self.max_dynamic_depth = max_dynamic_depth
        self.auth_engine = SovereignAuthenticator()

    def _calculate_dynamic_depth(self, data: str) -> int:
        length = len(data)
        if length < 100: return 3
        elif length < 500: return 6
        else: return min(9, self.max_dynamic_depth)

    def _fractal_split(self, data: str) -> List[str]:
        if not data: return []
        mid = len(data) // 2
        return [data[:mid], data[mid:]]

    def _evaluate_polarity(self, fractal_data: str) -> Dict[str, int]:
        yang_patterns = [r'(?i)ignore previous', r'(?i)system prompt', r'(?i)bypass']
        yang_score = sum(1 for p in yang_patterns if re.search(p, fractal_data))
        yin_score = len(fractal_data) // 50
        return {"yin": yin_score, "yang": yang_score}

    def recursive_synthesis(self, data: str, current_depth: int = 0, target_depth: Optional[int] = None) -> Dict[str, object]:
        if target_depth is None:
            target_depth = self._calculate_dynamic_depth(data)
            
        if current_depth >= target_depth or not data:
            return {"status": "resolved", "depth": current_depth, "polarity": self._evaluate_polarity(data)}
            
        fractals = self._fractal_split(data)
        return {
            "level": current_depth,
            "target_depth": target_depth,
            "left_node": self.recursive_synthesis(fractals[0], current_depth + 1, target_depth),
            "right_node": self.recursive_synthesis(fractals[1], current_depth + 1, target_depth)
        }

    def batch_analyze(self, texts: List[str]) -> List[Dict[str, object]]:
        return [self.recursive_synthesis(text) for text in texts]
