"""
MTF Dashboard Generator
Creates comprehensive multi-timeframe dashboard with charts, indicators, and patterns
"""
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import pandas as pd

from app.core.mtf_analyzer import TimeframeData, MTFAlignment, MTFDivergence
from app.core.mtf_scoring import MTFScore
from app.core.mtf_entry_timing import EntryTiming

logger = logging.getLogger(__name__)


@dataclass
class MTFIndicatorRow:
    """Single row in the indicator table"""
    timeframe: str
    price: float
    sma_50: Optional[float]
    sma_200: Optional[float]
    rsi: Optional[float]
    macd: Optional[str]  # "Bullish" / "Bearish"
    trend: str
    volume: str
    pattern: Optional[str]


@dataclass
class MTFPatternSummary:
    """Pattern summary across timeframes"""
    timeframe: str
    pattern_type: Optional[str]
    confidence: float
    entry: Optional[float]
    stop: Optional[float]
    target: Optional[float]
    status: str  # "Active", "Completed", "None"


@dataclass
class MTFDashboard:
    """Complete MTF Dashboard data"""
    ticker: str
    timestamp: datetime
    current_price: float

    # Overall assessment
    mtf_score: MTFScore
    alignment: MTFAlignment
    entry_timing: EntryTiming

    # Data tables
    indicator_table: List[MTFIndicatorRow]
    pattern_summary: List[MTFPatternSummary]
    divergence_alerts: List[str]

    # Recommendations
    recommendation: str
    key_levels: Dict[str, Any]
    action_items: List[str]

    # Visual data (for chart rendering)
    chart_data: Dict[str, Any]


class MTFDashboardGenerator:
    """Generates comprehensive MTF dashboards"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def generate_dashboard(
        self,
        ticker: str,
        timeframe_data: Dict[str, TimeframeData],
        data_by_timeframe: Dict[str, pd.DataFrame],
        alignment: MTFAlignment,
        divergences: List[MTFDivergence],
        mtf_score: MTFScore,
        entry_timing: EntryTiming
    ) -> MTFDashboard:
        """
        Generate comprehensive MTF dashboard

        Args:
            ticker: Stock symbol
            timeframe_data: Dictionary of TimeframeData
            data_by_timeframe: Dictionary of OHLCV DataFrames
            alignment: MTF alignment analysis
            divergences: List of divergences
            mtf_score: MTF score
            entry_timing: Entry timing analysis

        Returns:
            MTFDashboard with all visualization data
        """
        # Get current price
        current_price = self._get_current_price(timeframe_data)

        # Build indicator table
        indicator_table = self._build_indicator_table(timeframe_data)

        # Build pattern summary
        pattern_summary = self._build_pattern_summary(timeframe_data)

        # Build divergence alerts
        divergence_alerts = self._build_divergence_alerts(divergences)

        # Generate recommendation
        recommendation = self._generate_recommendation(
            mtf_score, alignment, entry_timing
        )

        # Identify key levels
        key_levels = self._identify_key_levels(timeframe_data, current_price)

        # Generate action items
        action_items = self._generate_action_items(
            mtf_score, alignment, entry_timing, divergences
        )

        # Build chart data
        chart_data = self._build_chart_data(
            ticker, timeframe_data, data_by_timeframe
        )

        return MTFDashboard(
            ticker=ticker,
            timestamp=datetime.now(),
            current_price=current_price,
            mtf_score=mtf_score,
            alignment=alignment,
            entry_timing=entry_timing,
            indicator_table=indicator_table,
            pattern_summary=pattern_summary,
            divergence_alerts=divergence_alerts,
            recommendation=recommendation,
            key_levels=key_levels,
            action_items=action_items,
            chart_data=chart_data
        )

    def format_dashboard_text(self, dashboard: MTFDashboard) -> str:
        """
        Format dashboard as text for display

        Returns:
            Formatted text dashboard
        """
        lines = []

        # Header
        lines.append("=" * 80)
        lines.append(f"MTF DASHBOARD: {dashboard.ticker}")
        lines.append(f"Generated: {dashboard.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Current Price: ${dashboard.current_price:.2f}")
        lines.append("=" * 80)
        lines.append("")

        # Overall Score
        lines.append("📊 OVERALL ASSESSMENT")
        lines.append("-" * 80)
        lines.append(f"MTF Score: {dashboard.mtf_score.overall_score}/10 ({dashboard.mtf_score.category})")
        lines.append(f"Recommendation: {dashboard.recommendation}")
        lines.append(f"Alignment: {dashboard.alignment.alignment_type.replace('_', ' ').title()}")
        lines.append("")

        # Score Breakdown
        lines.append("📈 SCORE BREAKDOWN")
        lines.append("-" * 80)
        for component, score in dashboard.mtf_score.score_breakdown.items():
            lines.append(f"  {component}: {score:.1f}/10")
        lines.append("")

        # Indicator Table
        lines.append("📋 INDICATOR TABLE (All Timeframes)")
        lines.append("-" * 80)
        lines.append(f"{'TF':<6} {'Price':<10} {'SMA50':<10} {'SMA200':<10} {'RSI':<8} {'MACD':<10} {'Trend':<10} {'Volume':<12} {'Pattern':<15}")
        lines.append("-" * 80)

        for row in dashboard.indicator_table:
            lines.append(
                f"{row.timeframe:<6} "
                f"${row.price:<9.2f} "
                f"${row.sma_50 or 0:<9.2f} "
                f"${row.sma_200 or 0:<9.2f} "
                f"{row.rsi or 0:<7.1f} "
                f"{row.macd or 'N/A':<10} "
                f"{row.trend:<10} "
                f"{row.volume:<12} "
                f"{row.pattern or 'None':<15}"
            )
        lines.append("")

        # Pattern Summary
        lines.append("📐 PATTERN SUMMARY (All Timeframes)")
        lines.append("-" * 80)
        lines.append(f"{'TF':<6} {'Pattern':<20} {'Confidence':<12} {'Entry':<10} {'Stop':<10} {'Target':<10} {'Status':<10}")
        lines.append("-" * 80)

        for pattern in dashboard.pattern_summary:
            lines.append(
                f"{pattern.timeframe:<6} "
                f"{pattern.pattern_type or 'None':<20} "
                f"{pattern.confidence:.0%}{'':>7} "
                f"${pattern.entry or 0:<9.2f} "
                f"${pattern.stop or 0:<9.2f} "
                f"${pattern.target or 0:<9.2f} "
                f"{pattern.status:<10}"
            )
        lines.append("")

        # Divergence Alerts
        if dashboard.divergence_alerts:
            lines.append("⚠️ DIVERGENCE ALERTS")
            lines.append("-" * 80)
            for alert in dashboard.divergence_alerts:
                lines.append(f"  {alert}")
            lines.append("")

        # Alignment Analysis
        lines.append("🎯 ALIGNMENT ANALYSIS")
        lines.append("-" * 80)
        lines.append(f"Bullish Timeframes: {', '.join(dashboard.alignment.bullish_timeframes) or 'None'}")
        lines.append(f"Bearish Timeframes: {', '.join(dashboard.alignment.bearish_timeframes) or 'None'}")
        lines.append(f"Neutral Timeframes: {', '.join(dashboard.alignment.neutral_timeframes) or 'None'}")
        lines.append(f"Higher TF Trend: {dashboard.alignment.higher_tf_trend.upper()}")
        lines.append(f"Lower TF Trend: {dashboard.alignment.lower_tf_trend.upper()}")
        lines.append(f"Trend Agreement: {'✅ YES' if dashboard.alignment.trend_agreement else '❌ NO'}")
        lines.append("")

        if dashboard.alignment.conflicts:
            lines.append("⚠️ Conflicts:")
            for conflict in dashboard.alignment.conflicts:
                lines.append(f"  {conflict}")
            lines.append("")

        # Entry Timing
        lines.append("⏰ ENTRY TIMING")
        lines.append("-" * 80)
        lines.append(f"Optimal Entry TF: {dashboard.entry_timing.optimal_entry_tf}")
        signal = dashboard.entry_timing.current_signal
        lines.append(f"Signal Type: {signal.signal_type.upper()}")
        lines.append(f"Confidence: {signal.confidence:.0%}")

        if signal.signal_type != "wait":
            lines.append(f"Entry Price: ${signal.entry_price:.2f}")
            lines.append(f"Stop Loss: ${signal.stop_loss:.2f}")
            lines.append(f"Take Profit: ${signal.take_profit:.2f}")
            lines.append(f"Risk:Reward: {signal.risk_reward_ratio:.2f}")
            lines.append(f"Reason: {signal.entry_reason}")
        else:
            lines.append(f"Reason: {signal.entry_reason}")

        lines.append("")

        if dashboard.entry_timing.timing_notes:
            lines.append("📝 Timing Notes:")
            for note in dashboard.entry_timing.timing_notes:
                lines.append(f"  {note}")
            lines.append("")

        if dashboard.entry_timing.wait_for:
            lines.append("⏳ Wait For:")
            for condition in dashboard.entry_timing.wait_for:
                lines.append(f"  • {condition}")
            lines.append("")

        # Key Levels
        lines.append("🎯 KEY LEVELS")
        lines.append("-" * 80)
        for level_name, level_value in dashboard.key_levels.items():
            if isinstance(level_value, (int, float)):
                lines.append(f"  {level_name}: ${level_value:.2f}")
            else:
                lines.append(f"  {level_name}: {level_value}")
        lines.append("")

        # Action Items
        lines.append("✅ ACTION ITEMS")
        lines.append("-" * 80)
        for i, action in enumerate(dashboard.action_items, 1):
            lines.append(f"  {i}. {action}")
        lines.append("")

        # Scoring Notes
        lines.append("💡 SCORING NOTES")
        lines.append("-" * 80)
        for note in dashboard.mtf_score.scoring_notes:
            lines.append(f"  {note}")
        lines.append("")

        lines.append("=" * 80)

        return "\n".join(lines)

    def _get_current_price(self, timeframe_data: Dict[str, TimeframeData]) -> float:
        """Get current price from timeframe data"""
        # Prefer 1hour for most recent price
        for tf_key in ["1hour", "4hour", "1day"]:
            if tf_key in timeframe_data:
                return timeframe_data[tf_key].current_price

        # Fallback to any available
        if timeframe_data:
            return list(timeframe_data.values())[0].current_price

        return 0.0

    def _build_indicator_table(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> List[MTFIndicatorRow]:
        """Build indicator table showing all indicators across all timeframes"""
        rows = []

        # Sort timeframes by importance
        tf_order = ["1month", "1week", "1day", "4hour", "1hour"]

        for tf_key in tf_order:
            if tf_key not in timeframe_data:
                continue

            tf_data = timeframe_data[tf_key]

            # MACD signal
            macd_signal = "N/A"
            if tf_data.macd_histogram is not None:
                macd_signal = "Bullish" if tf_data.macd_histogram > 0 else "Bearish"

            rows.append(MTFIndicatorRow(
                timeframe=tf_data.label,
                price=tf_data.current_price,
                sma_50=tf_data.sma_50,
                sma_200=tf_data.sma_200,
                rsi=tf_data.rsi,
                macd=macd_signal,
                trend=tf_data.trend_direction.upper(),
                volume=tf_data.volume_trend.title(),
                pattern=tf_data.pattern_type
            ))

        return rows

    def _build_pattern_summary(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> List[MTFPatternSummary]:
        """Build pattern summary table"""
        summaries = []

        tf_order = ["1month", "1week", "1day", "4hour", "1hour"]

        for tf_key in tf_order:
            if tf_key not in timeframe_data:
                continue

            tf_data = timeframe_data[tf_key]

            status = "Active" if tf_data.pattern_detected else "None"

            summaries.append(MTFPatternSummary(
                timeframe=tf_data.label,
                pattern_type=tf_data.pattern_type,
                confidence=tf_data.pattern_confidence,
                entry=None,  # Would come from pattern detector
                stop=tf_data.nearest_support,
                target=tf_data.nearest_resistance,
                status=status
            ))

        return summaries

    def _build_divergence_alerts(
        self,
        divergences: List[MTFDivergence]
    ) -> List[str]:
        """Build divergence alert messages"""
        alerts = []

        for div in divergences:
            severity_emoji = "🔴" if div.severity == "strong" else "🟡" if div.severity == "moderate" else "🟢"
            alerts.append(f"{severity_emoji} {div.description} (Confidence: {div.confirmation_score:.0%})")

        return alerts

    def _generate_recommendation(
        self,
        mtf_score: MTFScore,
        alignment: MTFAlignment,
        entry_timing: EntryTiming
    ) -> str:
        """Generate overall trading recommendation"""
        score = mtf_score.overall_score

        if score >= 8.5:
            return "🟢 STRONG BUY - Excellent setup with high confidence"
        elif score >= 7.0:
            return "🟢 BUY - Good setup with favorable alignment"
        elif score >= 5.5:
            return "🟡 HOLD - Fair setup, wait for better confirmation"
        elif score >= 4.0:
            return "🟡 NEUTRAL - Mixed signals, no clear direction"
        elif score >= 3.0:
            return "🔴 SELL - Poor setup, consider exiting"
        else:
            return "🔴 STRONG SELL - Very poor setup, avoid or short"

    def _identify_key_levels(
        self,
        timeframe_data: Dict[str, TimeframeData],
        current_price: float
    ) -> Dict[str, Any]:
        """Identify key support/resistance levels across timeframes"""
        levels = {}

        # Collect support/resistance from all timeframes
        supports = []
        resistances = []

        for tf_data in timeframe_data.values():
            if tf_data.nearest_support:
                supports.append(tf_data.nearest_support)
            if tf_data.nearest_resistance:
                resistances.append(tf_data.nearest_resistance)

        # Key support (strongest support below price)
        valid_supports = [s for s in supports if s < current_price]
        if valid_supports:
            levels["Key Support"] = max(valid_supports)

        # Key resistance (strongest resistance above price)
        valid_resistances = [r for r in resistances if r > current_price]
        if valid_resistances:
            levels["Key Resistance"] = min(valid_resistances)

        # Add SMA levels from daily
        daily = timeframe_data.get("1day")
        if daily:
            if daily.sma_50:
                levels["Daily SMA 50"] = daily.sma_50
            if daily.sma_200:
                levels["Daily SMA 200"] = daily.sma_200

        return levels

    def _generate_action_items(
        self,
        mtf_score: MTFScore,
        alignment: MTFAlignment,
        entry_timing: EntryTiming,
        divergences: List[MTFDivergence]
    ) -> List[str]:
        """Generate actionable items for trader"""
        actions = []

        signal = entry_timing.current_signal

        if signal.signal_type == "buy":
            actions.append(f"Consider LONG entry at ${signal.entry_price:.2f}")
            actions.append(f"Set stop loss at ${signal.stop_loss:.2f}")
            actions.append(f"Set take profit at ${signal.take_profit:.2f}")
            actions.append(f"Position size based on R:R of {signal.risk_reward_ratio:.2f}")

        elif signal.signal_type == "sell":
            actions.append(f"Consider SHORT entry at ${signal.entry_price:.2f}")
            actions.append(f"Set stop loss at ${signal.stop_loss:.2f}")
            actions.append(f"Set take profit at ${signal.take_profit:.2f}")
            actions.append(f"Position size based on R:R of {signal.risk_reward_ratio:.2f}")

        else:
            actions.append("Wait for better entry setup")
            if entry_timing.wait_for:
                actions.append(f"Monitor: {', '.join(entry_timing.wait_for[:2])}")

        # Divergence actions
        for div in divergences:
            if div.severity == "strong":
                if div.divergence_type == "bullish":
                    actions.append("Watch for bullish reversal opportunity")
                else:
                    actions.append("Watch for bearish reversal or take profits")

        # Alignment actions
        if not alignment.trend_agreement:
            actions.append("Monitor for higher/lower TF alignment before committing")

        if mtf_score.overall_score < 5.0:
            actions.append("Consider staying in cash until score improves")

        return actions

    def _build_chart_data(
        self,
        ticker: str,
        timeframe_data: Dict[str, TimeframeData],
        data_by_timeframe: Dict[str, pd.DataFrame]
    ) -> Dict[str, Any]:
        """
        Build chart data for visualization

        Returns structured data for charting libraries
        """
        chart_data = {
            "ticker": ticker,
            "timeframes": {}
        }

        for tf_key, tf_data in timeframe_data.items():
            ohlcv = data_by_timeframe.get(tf_key)

            if ohlcv is not None and len(ohlcv) > 0:
                # Get last 100 bars for charting
                chart_ohlcv = ohlcv.tail(100)

                chart_data["timeframes"][tf_data.label] = {
                    "ohlcv": chart_ohlcv.to_dict('records'),
                    "sma_50": tf_data.sma_50,
                    "sma_200": tf_data.sma_200,
                    "support": tf_data.nearest_support,
                    "resistance": tf_data.nearest_resistance,
                    "current_price": tf_data.current_price
                }

        return chart_data
