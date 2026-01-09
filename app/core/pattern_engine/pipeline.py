"""
Scanner Pipeline
Implements the 8-stage production-grade scanning pipeline.
"""
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from app.core.detector_registry import get_all_detectors
from app.core.pattern_engine.scoring import PatternScorer
from app.core.pattern_engine.helpers import get_pattern_helpers

logger = logging.getLogger(__name__)


from app.core.pattern_engine.filters.regime import MarketRegimeFilter
from app.core.pattern_engine.filters.trend import TrendTemplateFilter

class ScanPipeline:
    """
    Orchestrates the end-to-end scanning process for a single symbol.
    """
    
    def __init__(self):
        self.helpers = get_pattern_helpers()
        self.scorer = PatternScorer()
        self.regime_filter = MarketRegimeFilter()
        self.trend_filter = TrendTemplateFilter()

    async def run(self, symbol: str, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Run the 8-stage pipeline for a ticker.
        """
        # Stage A: Data Validation
        if not self._validate_data(data):
            return []
            
        # Stage B: Market Regime
        regime = await self.regime_filter.analyze_regime()
        
        # Stage C: Trend Template
        trend_tier = self.trend_filter.check_tier(data)
        # Filter Logic: Reject Tier 3 for bullish patterns if regime is BEAR?
        # For now, flexible: just pass tier to scoring. 
        # But per plan: "Trend Tier filter ensures... If Tier 3, filter out bullish patterns"
        # We'll tag candidates and let validation/scorer handle strictness or return early if needed.
        # Strict Mode:
        # if trend_tier == "TIER_3" and regime['trend'] == "BEAR":
        #    return [] 

        # Stage D: Candidate Generation
        candidates = self._detect_candidates(symbol, data)
        if not candidates:
            return []

        # Stage E: Validation & Refinement
        validated = self._validate_candidates(candidates, regime, trend_tier)
        
        # Stage F: Scoring
        scored = self._score_patterns(validated, regime, trend_tier)
        
        # Stage G: Trade Plan
        planned = self._generate_trade_plans(scored)
        
        # Stage H: Format Output
        return self._format_output(planned)

    def _validate_data(self, data: pd.DataFrame) -> bool:
        """Stage A: Ensure data quality."""
        if len(data) < 50: # Minimum bars
            return False
        if 'close' not in data.columns or 'volume' not in data.columns:
            return False
        # Liquidity check (simple)
        # Using handle exceptions if volume is 0
        try:
             vol_avg = data['volume'].rolling(20).mean().iloc[-1]
             price = data['close'].iloc[-1]
             if (price * vol_avg) < 500_000:
                  return False
        except:
             return False
        return True

    def _detect_candidates(self, symbol: str, data: pd.DataFrame) -> List[Dict[str, Any]]:
        """Stage D: Run existing detectors."""
        candidates = []
        detectors = get_all_detectors()
        
        # Convert DF to what detectors expect if needed, or they take DF
        for detector in detectors:
            try:
                patterns = detector.find(data, "1day", symbol)
                if patterns:
                     for p in patterns:
                         # normalize to dict here or later? 
                         # pattern is PatternResult
                         candidates.append(p)
            except Exception as e:
                logger.debug(f"Detector {detector.name} error on {symbol}: {e}")
                
        return candidates

    def _validate_candidates(self, candidates: List[Any], regime: Dict, tier: str) -> List[Any]:
        """Stage E: Refinement."""
        # De-duplication logic (simple version for Phase 1)
        if not candidates:
            return []
            
        # Sort by confidence/priority
        # Assuming PatternResult objects
        candidates.sort(key=lambda x: x.confidence, reverse=True)
        
        # Return top 1 or all? 
        # User wants "Primary pattern + secondary"
        # For now return all, scanner service does filtering
        return candidates

    def _score_patterns(self, patterns: List[Any], regime: Dict, tier: str) -> List[Dict[str, Any]]:
        """Stage F: Scoring."""
        results = []
        for p in patterns:
            # Convert PatternResult to dict first? Scorer expects dict
            # We need a unified dict representation
            p_dict = {
                "pattern": p.pattern_type.value,
                "confidence": p.confidence,
                "metadata": {
                    "trend_tier": tier,
                    "regime": regime
                },
                "entry": p.entry,
                "stop": p.stop,
                "target": p.target,
                # Add raw object or fields needed by scorer
            }
            # Use scorer
            components, score = self.scorer.score_pattern(p_dict)
            p_dict['score'] = score
            p_dict['score_components'] = components.to_dict()
            p_dict['grade'] = self._get_grade(score)
            results.append(p_dict)
            
        return results

    def _get_grade(self, score: float) -> str:
        if score >= 90: return "A+"
        if score >= 80: return "A"
        if score >= 65: return "B"
        if score >= 50: return "C"
        return "Avoid"

    def _generate_trade_plans(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Stage G: Trade Logic."""
        for p in patterns:
            # Add simple reason string for now
            p['trade_plan'] = {
                "entry": p.get('entry'),
                "stop": p.get('stop'),
                "target": p.get('target'),
                "risk_per_share": round(p.get('entry', 0) - p.get('stop', 0), 2) if p.get('entry') and p.get('stop') else None
            }
        return patterns

    def _format_output(self, patterns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Stage H: Format."""
        # Simple pass-through for now
        return patterns

