"""
Multi-Timeframe Confirmation Service
Analyzes patterns across multiple timeframes (1D, 1W, 4H, 1H) for confluence
"""
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict

from app.core.pattern_detector import PatternDetector, PatternResult
from app.services.market_data import market_data_service

logger = logging.getLogger(__name__)


@dataclass
class TimeframeAnalysis:
    """Analysis result for a single timeframe"""
    timeframe: str
    pattern_detected: bool
    pattern_type: Optional[str]
    confidence: float
    trend_direction: str  # "up", "down", "sideways"
    trend_strength: str  # "strong", "medium", "weak"
    volume_trend: str  # "increasing", "decreasing", "neutral"
    entry: Optional[float]
    stop: Optional[float]
    target: Optional[float]


@dataclass
class MultiTimeframeResult:
    """Consolidated multi-timeframe analysis result"""
    ticker: str
    overall_confluence: float  # 0-1, higher = stronger confluence
    strong_signal: bool  # True if all timeframes align
    signal_quality: str  # "Excellent", "Good", "Fair", "Poor"

    # Per-timeframe results
    daily_1d: TimeframeAnalysis
    weekly_1w: TimeframeAnalysis
    four_hour_4h: TimeframeAnalysis
    one_hour_1h: TimeframeAnalysis

    # Confluence details
    alignment_details: Dict[str, Any]
    recommendations: List[str]


class MultiTimeframeConfirmation:
    """Service for multi-timeframe pattern analysis and confluence"""

    def __init__(self):
        self.detector = PatternDetector()
        self.timeframes = ["1day", "1week", "4hour", "1hour"]
        self.timeframe_labels = {"1day": "1D", "1week": "1W", "4hour": "4H", "1hour": "1H"}

    async def analyze_multi_timeframe(self, ticker: str) -> MultiTimeframeResult:
        """
        Analyze a ticker across multiple timeframes for confluence

        Args:
            ticker: Stock symbol to analyze

        Returns:
            Multi-timeframe analysis with confluence scoring
        """
        logger.info(f"📊 Analyzing {ticker} across multiple timeframes...")

        # Fetch data for all timeframes
        data_by_timeframe = {}
        for tf in self.timeframes:
            try:
                data = await market_data_service.get_time_series(
                    ticker=ticker,
                    interval=tf,
                    outputsize=500
                )
                data_by_timeframe[tf] = data
            except Exception as e:
                logger.warning(f"⚠️ Failed to fetch {tf} data for {ticker}: {e}")
                data_by_timeframe[tf] = None

        # Analyze each timeframe
        results = {}
        try:
            spy_data = await market_data_service.get_time_series("SPY", "1day", 500)
        except:
            spy_data = None

        for tf in self.timeframes:
            try:
                if data_by_timeframe[tf]:
                    analysis = await self.detector.analyze_ticker(
                        ticker, data_by_timeframe[tf], spy_data
                    )

                    if analysis:
                        results[tf] = TimeframeAnalysis(
                            timeframe=self.timeframe_labels[tf],
                            pattern_detected=analysis.score >= 0.60,
                            pattern_type=analysis.pattern if analysis.score >= 0.60 else None,
                            confidence=analysis.score,
                            trend_direction=self._get_trend(data_by_timeframe[tf]),
                            trend_strength=self._get_trend_strength(analysis.score),
                            volume_trend=self._get_volume_trend(data_by_timeframe[tf]),
                            entry=analysis.entry if analysis.score >= 0.60 else None,
                            stop=analysis.stop if analysis.score >= 0.60 else None,
                            target=analysis.target if analysis.score >= 0.60 else None,
                        )
                    else:
                        results[tf] = TimeframeAnalysis(
                            timeframe=self.timeframe_labels[tf],
                            pattern_detected=False,
                            pattern_type=None,
                            confidence=0.0,
                            trend_direction="unknown",
                            trend_strength="unknown",
                            volume_trend="unknown",
                            entry=None,
                            stop=None,
                            target=None,
                        )
            except Exception as e:
                logger.warning(f"⚠️ Error analyzing {tf}: {e}")
                results[tf] = TimeframeAnalysis(
                    timeframe=self.timeframe_labels[tf],
                    pattern_detected=False,
                    pattern_type=None,
                    confidence=0.0,
                    trend_direction="unknown",
                    trend_strength="unknown",
                    volume_trend="unknown",
                    entry=None,
                    stop=None,
                    target=None,
                )

        # Calculate confluence
        confluence_score, alignment, strong_signal = self._calculate_confluence(results)

        # Generate recommendations
        recommendations = self._generate_recommendations(results, confluence_score)

        # Determine signal quality
        if confluence_score >= 0.85:
            signal_quality = "Excellent"
        elif confluence_score >= 0.70:
            signal_quality = "Good"
        elif confluence_score >= 0.55:
            signal_quality = "Fair"
        else:
            signal_quality = "Poor"

        result = MultiTimeframeResult(
            ticker=ticker,
            overall_confluence=confluence_score,
            strong_signal=strong_signal,
            signal_quality=signal_quality,
            daily_1d=results.get("1day", TimeframeAnalysis("1D", False, None, 0, "unknown", "unknown", "unknown", None, None, None)),
            weekly_1w=results.get("1week", TimeframeAnalysis("1W", False, None, 0, "unknown", "unknown", "unknown", None, None, None)),
            four_hour_4h=results.get("4hour", TimeframeAnalysis("4H", False, None, 0, "unknown", "unknown", "unknown", None, None, None)),
            one_hour_1h=results.get("1hour", TimeframeAnalysis("1H", False, None, 0, "unknown", "unknown", "unknown", None, None, None)),
            alignment_details=alignment,
            recommendations=recommendations
        )

        logger.info(f"✅ {ticker} Multi-TF Analysis: {signal_quality} ({confluence_score:.1%} confluence)")

        return result

    def _get_trend(self, ohlcv_data) -> str:
        """Determine trend direction from OHLCV data"""
        if not ohlcv_data or len(ohlcv_data) < 2:
            return "unknown"

        # Get recent prices
        recent = ohlcv_data.tail(20)
        avg_price_recent = recent['close'].mean()
        avg_price_older = ohlcv_data.iloc[-50:-30]['close'].mean()

        if avg_price_recent > avg_price_older * 1.02:
            return "up"
        elif avg_price_recent < avg_price_older * 0.98:
            return "down"
        else:
            return "sideways"

    def _get_trend_strength(self, confidence: float) -> str:
        """Get trend strength based on pattern confidence"""
        if confidence >= 0.75:
            return "strong"
        elif confidence >= 0.60:
            return "medium"
        else:
            return "weak"

    def _get_volume_trend(self, ohlcv_data) -> str:
        """Determine volume trend"""
        if not ohlcv_data or len(ohlcv_data) < 20:
            return "unknown"

        recent_vol = ohlcv_data.tail(10)['volume'].mean()
        older_vol = ohlcv_data.iloc[-30:-20]['volume'].mean()

        if recent_vol > older_vol * 1.1:
            return "increasing"
        elif recent_vol < older_vol * 0.9:
            return "decreasing"
        else:
            return "neutral"

    def _calculate_confluence(self, results: Dict[str, TimeframeAnalysis]) -> tuple:
        """
        Calculate confluence score based on alignment across timeframes

        Returns:
            Tuple of (confluence_score, alignment_details, strong_signal)
        """
        # Score each timeframe
        scores = {}
        for tf, analysis in results.items():
            tf_score = analysis.confidence

            # Boost score if trend is uptrend on larger timeframe
            if analysis.trend_direction == "up" and tf in ["1day", "1week"]:
                tf_score = min(1.0, tf_score * 1.15)

            # Penalize if trend conflicts
            if analysis.trend_direction == "down" and tf in ["1day", "1week"]:
                tf_score = max(0.0, tf_score * 0.75)

            scores[tf] = tf_score

        # Calculate overall confluence
        # Daily is most important (50%), weekly (25%), 4H (15%), 1H (10%)
        confluence = (
            scores.get("1day", 0) * 0.50 +
            scores.get("1week", 0) * 0.25 +
            scores.get("4hour", 0) * 0.15 +
            scores.get("1hour", 0) * 0.10
        )

        # Check if all timeframes are aligned (strong signal)
        daily = results.get("1day")
        weekly = results.get("1week")
        four_h = results.get("4hour")

        strong_signal = (
            daily and daily.pattern_detected and
            weekly and weekly.trend_direction == "up" and
            four_h and four_h.trend_direction == "up"
        )

        # Build alignment details
        alignment = {
            "scores_by_timeframe": {
                "1D": scores.get("1day", 0),
                "1W": scores.get("1week", 0),
                "4H": scores.get("4hour", 0),
                "1H": scores.get("1hour", 0)
            },
            "daily_setup": f"{daily.pattern_type or 'None'} ({daily.confidence:.1%})" if daily else "No data",
            "weekly_trend": f"{weekly.trend_direction.upper()} ({weekly.confidence:.1%})" if weekly else "No data",
            "4h_alignment": f"{four_h.trend_direction.upper()} ({four_h.confidence:.1%})" if four_h else "No data",
            "overall": f"{confluence:.1%} confluence"
        }

        return confluence, alignment, strong_signal

    def _generate_recommendations(self, results: Dict[str, TimeframeAnalysis], confluence: float) -> List[str]:
        """Generate trading recommendations based on multi-TF analysis"""
        recommendations = []

        daily = results.get("1day")
        weekly = results.get("1week")
        four_h = results.get("4hour")

        # Pattern recommendations
        if daily and daily.pattern_detected:
            recommendations.append(f"✅ Daily setup confirmed: {daily.pattern_type}")
        else:
            recommendations.append("⚠️ No clear daily pattern - be cautious")

        # Trend alignment recommendations
        if weekly and weekly.trend_direction == "up":
            recommendations.append("✅ Weekly uptrend confirmed - bias favors LONGS")
        elif weekly and weekly.trend_direction == "down":
            recommendations.append("⚠️ Weekly downtrend - avoid long setups")
        else:
            recommendations.append("⚠️ Weekly trend unclear - wait for confirmation")

        # Confluence recommendations
        if confluence >= 0.85:
            recommendations.append("🎯 EXCELLENT CONFLUENCE - High probability trade")
            recommendations.append("💰 Risk is low, reward is high - ideal entry point")
        elif confluence >= 0.70:
            recommendations.append("✅ Good confluence across timeframes - trade-worthy setup")
        elif confluence >= 0.55:
            recommendations.append("⚠️ Fair confluence - wait for more confirmation")
        else:
            recommendations.append("❌ Poor confluence - skip this setup")

        # Volume recommendations
        if four_h and four_h.volume_trend == "increasing":
            recommendations.append("📈 Volume increasing on breakout - strong signal")
        elif four_h and four_h.volume_trend == "decreasing":
            recommendations.append("⚠️ Volume decreasing - weaker breakout potential")

        return recommendations


# Global instance
_multitf_service: Optional[MultiTimeframeConfirmation] = None


def get_multitf_service() -> MultiTimeframeConfirmation:
    """Get or create multi-timeframe service singleton"""
    global _multitf_service
    if _multitf_service is None:
        _multitf_service = MultiTimeframeConfirmation()
    return _multitf_service
