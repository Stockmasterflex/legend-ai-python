
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Tuple
import numpy as np

@dataclass
class ScoreComponents:
    """
    Breakdown of the Calibrated Scoring Framework.
    Max Score: 100
    Quality (50) + Readiness (30) - Risk (upto 30)
    """
    # Quality (Max 50)
    trend_quality: float = 0.0          # Max 15
    structure_tightness: float = 0.0    # Max 15
    volume_characteristics: float = 0.0 # Max 10
    pattern_maturity: float = 0.0       # Max 10
    
    # Readiness (Max 30)
    breakout_proximity: float = 0.0     # Max 10
    relative_strength: float = 0.0      # Max 10
    moving_average_stack: float = 0.0   # Max 10
    
    # Risk/Penalties (Negative values)
    risk_overhead: float = 0.0          # Max -10
    risk_volatility: float = 0.0        # Max -10
    risk_regime: float = 0.0            # Max -10

    def total_score(self) -> float:
        total = (
            self.trend_quality +
            self.structure_tightness +
            self.volume_characteristics +
            self.pattern_maturity +
            self.breakout_proximity +
            self.relative_strength +
            self.moving_average_stack +
            self.risk_overhead +
            self.risk_volatility +
            self.risk_regime
        )
        return float(np.clip(total, 0, 100))

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


class PatternScorer:
    """
    Calibrated Scoring System.
    Evaluates patterns based on Quality, Readiness, and Risk.
    """

    def score_pattern(self, pattern: Dict[str, Any]) -> Tuple[ScoreComponents, float]:
        """
        Score a single pattern.
        Pattern dict should contain 'metadata' populated by pipeline.
        """
        metadata = pattern.get("metadata") or {}
        # Extract inputs
        regime = metadata.get("regime", {})
        tier = metadata.get("trend_tier", "TIER_3")
        
        # --- Quality (0-50) ---
        q_trend = self._score_trend_quality(pattern, metadata, tier) # Max 15
        q_structure = self._score_structure(pattern, metadata)       # Max 15
        q_volume = self._score_volume(pattern, metadata)             # Max 10
        q_maturity = self._score_maturity(pattern, metadata)         # Max 10
        
        # --- Readiness (0-30) ---
        r_prox = self._score_proximity(pattern)                      # Max 10
        r_rs = self._score_relative_strength(pattern, metadata)      # Max 10
        r_ma = self._score_ma_stack(pattern, metadata)               # Max 10
        
        # --- Risk (Negative) ---
        risk_overhead = self._score_overhead(pattern, metadata)      # Max -10
        risk_vol = self._score_volatility_risk(pattern, metadata)    # Max -10
        risk_regime = self._score_regime_drag(regime)                # Max -10
        
        components = ScoreComponents(
            trend_quality=q_trend,
            structure_tightness=q_structure,
            volume_characteristics=q_volume,
            pattern_maturity=q_maturity,
            breakout_proximity=r_prox,
            relative_strength=r_rs,
            moving_average_stack=r_ma,
            risk_overhead=risk_overhead,
            risk_volatility=risk_vol,
            risk_regime=risk_regime
        )
        
        return components, components.total_score()

    def score_patterns(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score multiple patterns."""
        scored = []
        for p in patterns:
            components, score = self.score_pattern(p)
            p['score'] = score
            p['score_components'] = components.to_dict()
            scored.append(p)
        scored.sort(key=lambda x: x['score'], reverse=True)
        return scored

    # --- Helpers ---

    def _score_trend_quality(self, pattern: Dict, metadata: Dict, tier: str) -> float:
        # Max 15
        score = 0.0
        # Tier 1 = 10 pts, Tier 2 = 5 pts
        if tier == "TIER_1": score += 10
        elif tier == "TIER_2": score += 5
        
        # Trend strength / coherence
        conf = pattern.get("confidence", 0.0)
        score += conf * 5 # Add up to 5 points based on detector confidence
        
        return min(15.0, score)

    def _score_structure(self, pattern: Dict, metadata: Dict) -> float:
        # Max 15. Tightness, logic.
        # VCP logic: if 'vcp' in pattern, 15?
        name = pattern.get("pattern", "")
        if "VCP" in name:
            return 15.0
        if "Cup" in name:
            return 12.0
        if "Flag" in name:
            return 10.0
        return 5.0 # Generic

    def _score_volume(self, pattern: Dict, metadata: Dict) -> float:
        # Max 10. Dry up?
        # If we have volume trend info
        slope = metadata.get("volume_trend_slope") or 0.0
        if slope < 0: return 10.0 # Decreasing volume
        return 5.0

    def _score_maturity(self, pattern: Dict, metadata: Dict) -> float:
        # Max 10.
        # Prefer 4-8 weeks?
        # Assuming metadata has 'duration'
        return 5.0 # Default

    def _score_proximity(self, pattern: Dict) -> float:
        # Max 10. Near pivot?
        # If current price is within 2% of pivot
        pivot = pattern.get("entry") or pattern.get("pivot_price")
        # current price from metadata? Or assume pattern has it?
        # We need current price. 
        # Assume it's passed or calculable.
        return 5.0 # Placeholder

    def _score_relative_strength(self, pattern: Dict, metadata: Dict) -> float:
        # Max 10.
        # RS Rating > 85 = 10 pts
        # RS Rating > 70 = 5 pts
        return 5.0

    def _score_ma_stack(self, pattern: Dict, metadata: Dict) -> float:
        # Max 10.
        # Price > 20 > 50 > 200
        return 5.0

    def _score_overhead(self, pattern: Dict, metadata: Dict) -> float:
        # Negative. Max -10.
        return 0.0

    def _score_volatility_risk(self, pattern: Dict, metadata: Dict) -> float:
        # Negative.
        # If ATR high or loose action
        return 0.0

    def _score_regime_drag(self, regime: Dict) -> float:
        # Negative.
        # If Bear market, -10.
        trend = regime.get("trend", "NEUTRAL")
        if trend == "BEAR": return -10.0
        if trend == "CORRECTION": return -5.0
        return 0.0

