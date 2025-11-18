"""
Options-Pattern Integration Layer
Enhances pattern detection with options flow analysis
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd

from app.config import get_settings
from app.services.cache import get_cache_service
from app.services.options_data import get_options_service
from app.services.options_screener import get_options_screener
from app.core.detector_base import PatternResult

logger = logging.getLogger(__name__)


class OptionsPatternEnhancer:
    """
    Enhance pattern detection with options flow analysis

    Features:
    - Add options flow confirmation to patterns
    - Detect divergences (bullish pattern + bearish options flow)
    - Score patterns based on options activity
    - Generate alerts for unusual options activity
    """

    def __init__(self):
        self.settings = get_settings()
        self.cache = get_cache_service()
        self.options_service = get_options_service()
        self.screener = get_options_screener()

    async def enhance_pattern(
        self,
        symbol: str,
        pattern_result: Dict[str, Any],
        include_strategies: bool = False
    ) -> Dict[str, Any]:
        """
        Enhance a pattern result with options flow analysis

        Args:
            symbol: Stock ticker
            pattern_result: Pattern detection result
            include_strategies: Include strategy suggestions

        Returns:
            Enhanced pattern with options data
        """
        cache_key = f"enhanced_pattern:{symbol}:{pattern_result.get('pattern_type', 'unknown')}"

        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        try:
            # Run options analysis in parallel
            options_tasks = [
                self.screener.comprehensive_scan(symbol),
                self.options_service.get_put_call_ratio(symbol),
                self.options_service.get_unusual_activity(symbol),
            ]

            results = await asyncio.gather(*options_tasks, return_exceptions=True)
            comprehensive_scan, pc_ratio, unusual_activity = results

            # Extract key metrics
            options_sentiment = self._determine_options_sentiment(
                comprehensive_scan if isinstance(comprehensive_scan, dict) else {},
                pc_ratio if isinstance(pc_ratio, dict) else {},
                unusual_activity if isinstance(unusual_activity, list) else []
            )

            # Check for pattern-options alignment
            pattern_type = pattern_result.get("pattern_type", "unknown")
            pattern_sentiment = self._get_pattern_sentiment(pattern_type, pattern_result)

            alignment = self._check_alignment(pattern_sentiment, options_sentiment)

            # Build enhanced result
            enhanced = {
                **pattern_result,
                "options_analysis": {
                    "sentiment": options_sentiment,
                    "put_call_ratio": pc_ratio.get("volume_pc_ratio") if isinstance(pc_ratio, dict) else None,
                    "unusual_activity_count": len(unusual_activity) if isinstance(unusual_activity, list) else 0,
                    "activity_score": comprehensive_scan.get("activity_score", 0) if isinstance(comprehensive_scan, dict) else 0,
                    "alignment_with_pattern": alignment,
                    "confirmation_strength": self._calculate_confirmation_strength(
                        alignment,
                        comprehensive_scan if isinstance(comprehensive_scan, dict) else {},
                        unusual_activity if isinstance(unusual_activity, list) else []
                    )
                },
                "alerts": self._generate_alerts(
                    symbol,
                    pattern_type,
                    pattern_sentiment,
                    options_sentiment,
                    alignment,
                    unusual_activity if isinstance(unusual_activity, list) else []
                ),
                "options_flow_summary": self._generate_flow_summary(
                    comprehensive_scan if isinstance(comprehensive_scan, dict) else {},
                    pc_ratio if isinstance(pc_ratio, dict) else {},
                    unusual_activity if isinstance(unusual_activity, list) else []
                )
            }

            # Add strategy suggestions if requested
            if include_strategies:
                enhanced["suggested_strategies"] = await self._suggest_strategies(
                    symbol,
                    pattern_type,
                    pattern_sentiment,
                    options_sentiment,
                    pattern_result
                )

            # Adjust pattern score based on options confirmation
            original_score = pattern_result.get("score", 50)
            confirmation_boost = self._calculate_score_boost(alignment, comprehensive_scan if isinstance(comprehensive_scan, dict) else {})
            enhanced["adjusted_score"] = min(100, original_score + confirmation_boost)

            await self.cache.set(cache_key, enhanced, ttl=300)
            return enhanced

        except Exception as e:
            logger.error(f"Error enhancing pattern for {symbol}: {e}")
            return pattern_result  # Return original on error

    def _determine_options_sentiment(
        self,
        comprehensive_scan: Dict[str, Any],
        pc_ratio: Dict[str, Any],
        unusual_activity: List[Dict[str, Any]]
    ) -> str:
        """Determine overall options sentiment"""
        bullish_signals = 0
        bearish_signals = 0

        # Put/Call ratio
        pc_ratio_value = pc_ratio.get("volume_pc_ratio", 1.0)
        if pc_ratio_value < 0.7:
            bullish_signals += 2
        elif pc_ratio_value > 1.3:
            bearish_signals += 2

        # Unusual activity
        for activity in unusual_activity:
            if activity.get("sentiment") == "bullish":
                bullish_signals += 1
            elif activity.get("sentiment") == "bearish":
                bearish_signals += 1

        # Activity score
        activity_score = comprehensive_scan.get("activity_score", 0)
        if activity_score > 60:
            # High activity - check sentiment from summary
            summary = comprehensive_scan.get("summary", "")
            if "bullish" in summary.lower():
                bullish_signals += 1
            elif "bearish" in summary.lower():
                bearish_signals += 1

        # Determine overall sentiment
        if bullish_signals > bearish_signals + 1:
            return "bullish"
        elif bearish_signals > bullish_signals + 1:
            return "bearish"
        else:
            return "neutral"

    def _get_pattern_sentiment(self, pattern_type: str, pattern_result: Dict[str, Any]) -> str:
        """Determine pattern sentiment"""
        # Bullish patterns
        bullish_patterns = [
            "vcp", "cup_handle", "ascending_triangle", "falling_wedge",
            "inverse_head_shoulders", "double_bottom", "channel_up", "50_sma_pullback"
        ]

        # Bearish patterns
        bearish_patterns = [
            "head_shoulders", "double_top", "rising_wedge", "descending_triangle",
            "channel_down"
        ]

        pattern_lower = pattern_type.lower()

        for bullish in bullish_patterns:
            if bullish in pattern_lower:
                return "bullish"

        for bearish in bearish_patterns:
            if bearish in pattern_lower:
                return "bearish"

        return "neutral"

    def _check_alignment(self, pattern_sentiment: str, options_sentiment: str) -> str:
        """Check if pattern and options flow are aligned"""
        if pattern_sentiment == options_sentiment:
            return "confirmed"
        elif pattern_sentiment == "neutral" or options_sentiment == "neutral":
            return "neutral"
        else:
            return "divergence"

    def _calculate_confirmation_strength(
        self,
        alignment: str,
        comprehensive_scan: Dict[str, Any],
        unusual_activity: List[Dict[str, Any]]
    ) -> str:
        """Calculate how strong the confirmation is"""
        if alignment == "divergence":
            return "conflicting"

        activity_score = comprehensive_scan.get("activity_score", 0)
        unusual_count = len(unusual_activity)

        if alignment == "confirmed":
            if activity_score > 70 and unusual_count > 3:
                return "very_strong"
            elif activity_score > 50 and unusual_count > 1:
                return "strong"
            elif activity_score > 30:
                return "moderate"
            else:
                return "weak"
        else:  # neutral
            return "neutral"

    def _calculate_score_boost(
        self,
        alignment: str,
        comprehensive_scan: Dict[str, Any]
    ) -> int:
        """Calculate score boost/penalty based on options confirmation"""
        if alignment == "confirmed":
            activity_score = comprehensive_scan.get("activity_score", 0)
            if activity_score > 70:
                return 15
            elif activity_score > 50:
                return 10
            elif activity_score > 30:
                return 5
            else:
                return 0
        elif alignment == "divergence":
            # Penalize divergence
            return -10
        else:
            return 0

    def _generate_alerts(
        self,
        symbol: str,
        pattern_type: str,
        pattern_sentiment: str,
        options_sentiment: str,
        alignment: str,
        unusual_activity: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate alerts based on pattern-options analysis"""
        alerts = []

        # Confirmation alert
        if alignment == "confirmed":
            alerts.append({
                "type": "confirmation",
                "severity": "high",
                "message": f"Options flow confirms {pattern_type} pattern ({pattern_sentiment})",
                "timestamp": datetime.now().isoformat()
            })

        # Divergence alert
        if alignment == "divergence":
            alerts.append({
                "type": "divergence",
                "severity": "warning",
                "message": f"Options flow diverges from pattern: {pattern_type} is {pattern_sentiment} but options are {options_sentiment}",
                "timestamp": datetime.now().isoformat()
            })

        # Unusual call buying on bullish pattern
        if pattern_sentiment == "bullish":
            call_buying = [a for a in unusual_activity if a.get("type") == "call"]
            if len(call_buying) > 0:
                total_premium = sum(a.get("premium", 0) for a in call_buying)
                alerts.append({
                    "type": "unusual_call_buying",
                    "severity": "high",
                    "message": f"Unusual call buying detected: ${total_premium:,.0f} in premium",
                    "details": call_buying[:3],  # Top 3 trades
                    "timestamp": datetime.now().isoformat()
                })

        # Smart money flow (large blocks/sweeps)
        large_trades = [a for a in unusual_activity if a.get("premium", 0) > 100000]
        if len(large_trades) > 0:
            alerts.append({
                "type": "smart_money",
                "severity": "high",
                "message": f"{len(large_trades)} large institutional-sized options trades detected",
                "details": large_trades[:2],
                "timestamp": datetime.now().isoformat()
            })

        return alerts

    def _generate_flow_summary(
        self,
        comprehensive_scan: Dict[str, Any],
        pc_ratio: Dict[str, Any],
        unusual_activity: List[Dict[str, Any]]
    ) -> str:
        """Generate human-readable options flow summary"""
        parts = []

        # Put/Call ratio
        pc_value = pc_ratio.get("volume_pc_ratio")
        if pc_value:
            pc_sentiment = pc_ratio.get("sentiment", "neutral")
            parts.append(f"P/C Ratio: {pc_value:.2f} ({pc_sentiment})")

        # Activity level
        activity_score = comprehensive_scan.get("activity_score", 0)
        activity_level = comprehensive_scan.get("activity_level", "low")
        parts.append(f"Activity: {activity_level} ({activity_score}/100)")

        # Unusual activity
        if unusual_activity:
            total_premium = sum(a.get("premium", 0) for a in unusual_activity)
            parts.append(f"{len(unusual_activity)} unusual trades (${total_premium:,.0f})")

        # Summary from comprehensive scan
        summary = comprehensive_scan.get("summary")
        if summary:
            parts.append(summary)

        return " | ".join(parts) if parts else "No significant options activity"

    async def _suggest_strategies(
        self,
        symbol: str,
        pattern_type: str,
        pattern_sentiment: str,
        options_sentiment: str,
        pattern_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Suggest options strategies based on pattern and flow"""
        from app.services.options_strategy import get_strategy_builder

        strategies = []
        strategy_builder = get_strategy_builder()

        try:
            # For bullish patterns with confirmation
            if pattern_sentiment == "bullish" and options_sentiment in ["bullish", "neutral"]:
                # Suggest covered calls for existing longs
                strategies.append({
                    "name": "Covered Call",
                    "description": "Generate income on existing long position",
                    "risk_level": "low",
                    "ideal_for": "Existing long positions looking for income",
                    "note": "Consider 30-45 DTE, 0.30 delta strikes"
                })

                # Suggest bull call spreads for new positions
                strategies.append({
                    "name": "Bull Call Spread",
                    "description": "Defined-risk bullish play on breakout",
                    "risk_level": "moderate",
                    "ideal_for": "High-probability breakout plays",
                    "note": "Enter on breakout confirmation with volume"
                })

            # For bearish patterns
            elif pattern_sentiment == "bearish" and options_sentiment in ["bearish", "neutral"]:
                # Suggest protective puts for existing longs
                strategies.append({
                    "name": "Protective Put",
                    "description": "Hedge existing long positions",
                    "risk_level": "low",
                    "ideal_for": "Portfolio protection during breakdown",
                    "note": "Consider ATM or slightly OTM puts"
                })

                # Suggest bear put spreads
                strategies.append({
                    "name": "Bear Put Spread",
                    "description": "Defined-risk bearish play",
                    "risk_level": "moderate",
                    "ideal_for": "High-probability breakdown plays"
                })

            # For high IV situations
            pc_ratio = await self.options_service.get_put_call_ratio(symbol)
            iv_data = await self.options_service.get_iv_percentile(symbol)

            if isinstance(iv_data, dict) and iv_data.get("iv_rank", 0) > 70:
                if pattern_sentiment == "neutral":
                    strategies.append({
                        "name": "Iron Condor",
                        "description": "Profit from high IV and range-bound movement",
                        "risk_level": "moderate",
                        "ideal_for": "High IV with expected consolidation",
                        "note": f"IV Rank: {iv_data.get('iv_rank', 0):.0f}% - excellent for premium selling"
                    })

            return strategies

        except Exception as e:
            logger.error(f"Error suggesting strategies: {e}")
            return []

    async def batch_enhance_patterns(
        self,
        patterns: List[Dict[str, Any]],
        include_strategies: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Enhance multiple patterns with options data

        Args:
            patterns: List of pattern results
            include_strategies: Include strategy suggestions

        Returns:
            List of enhanced patterns
        """
        tasks = []
        for pattern in patterns:
            symbol = pattern.get("symbol", "")
            if symbol:
                tasks.append(self.enhance_pattern(symbol, pattern, include_strategies))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        enhanced_patterns = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error enhancing pattern {i}: {result}")
                enhanced_patterns.append(patterns[i])  # Use original
            else:
                enhanced_patterns.append(result)

        return enhanced_patterns

    async def get_pattern_options_divergences(
        self,
        symbols: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Scan for pattern-options divergences across multiple symbols

        Divergences can signal:
        - False breakouts (bullish pattern + bearish flow)
        - Hidden opportunities (bearish pattern + bullish flow)

        Args:
            symbols: List of symbols to scan

        Returns:
            List of divergences
        """
        # This would integrate with the pattern scanner
        # For now, return structure
        return []


# Singleton instance
_enhancer: Optional[OptionsPatternEnhancer] = None


def get_pattern_enhancer() -> OptionsPatternEnhancer:
    """Get or create pattern enhancer singleton"""
    global _enhancer
    if _enhancer is None:
        _enhancer = OptionsPatternEnhancer()
    return _enhancer
