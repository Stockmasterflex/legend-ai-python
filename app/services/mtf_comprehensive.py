"""
Comprehensive MTF Service
Integrates all MTF components: analysis, scoring, timing, dashboard, and alerts
"""
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from datetime import datetime

from app.services.market_data import market_data_service
from app.core.mtf_analyzer import MTFAnalyzer, TimeframeData, MTFAlignment, MTFDivergence
from app.core.mtf_scoring import MTFScoringEngine, MTFScore
from app.core.mtf_entry_timing import MTFEntryTimingOptimizer, EntryTiming
from app.core.mtf_dashboard import MTFDashboardGenerator, MTFDashboard
from app.core.mtf_alerts import MTFAlertSystem, MTFAlert

logger = logging.getLogger(__name__)


@dataclass
class ComprehensiveMTFResult:
    """Complete MTF analysis result with all components"""
    ticker: str
    timestamp: datetime

    # Core analysis
    timeframe_data: Dict[str, TimeframeData]
    alignment: MTFAlignment
    divergences: List[MTFDivergence]

    # Scoring
    mtf_score: MTFScore
    trade_recommendation: str

    # Entry timing
    entry_timing: EntryTiming

    # Dashboard
    dashboard: MTFDashboard

    # Alerts
    alerts: List[MTFAlert]

    # Summary
    summary: Dict[str, any]


class ComprehensiveMTFService:
    """
    Comprehensive Multi-Timeframe Trading System

    Integrates:
    1. Timeframe Alignment - Daily, Weekly, Monthly analysis
    2. MTF Dashboard - Charts, indicators, patterns
    3. MTF Scoring - 0-10 scale with alignment logic
    4. Entry Timing - Lower TF for entries, higher TF for direction
    5. Alerts - Alignment and divergence notifications
    """

    def __init__(self):
        self.analyzer = MTFAnalyzer()
        self.scoring_engine = MTFScoringEngine()
        self.entry_optimizer = MTFEntryTimingOptimizer()
        self.dashboard_generator = MTFDashboardGenerator()
        self.alert_system = MTFAlertSystem()

        self.logger = logging.getLogger(__name__)

    async def analyze_comprehensive(
        self,
        ticker: str,
        previous_score: Optional[float] = None
    ) -> ComprehensiveMTFResult:
        """
        Perform comprehensive MTF analysis

        Args:
            ticker: Stock symbol
            previous_score: Previous MTF score (for delta alerts)

        Returns:
            Complete MTF analysis with all components
        """
        self.logger.info(f"🔍 Starting comprehensive MTF analysis for {ticker}...")

        # Step 1: Fetch data for all timeframes
        self.logger.info(f"📊 Fetching multi-timeframe data...")
        data_by_timeframe = await self._fetch_all_timeframes(ticker)

        # Step 2: Analyze each timeframe
        self.logger.info(f"📈 Analyzing individual timeframes...")
        timeframe_data = {}

        for tf_key, tf_config in self.analyzer.TIMEFRAMES.items():
            ohlcv = data_by_timeframe.get(tf_key)

            if ohlcv is not None:
                tf_data = self.analyzer.analyze_timeframe(ticker, tf_key, ohlcv)
                timeframe_data[tf_key] = tf_data
                self.logger.info(
                    f"  {tf_data.label}: {tf_data.trend_direction.upper()} "
                    f"(strength: {tf_data.trend_strength:.1%})"
                )

        # Step 3: Analyze alignment
        self.logger.info(f"🎯 Analyzing timeframe alignment...")
        alignment = self.analyzer.analyze_alignment(timeframe_data)
        self.logger.info(
            f"  Alignment: {alignment.alignment_type} "
            f"(score: {alignment.alignment_score:.1f}/10)"
        )

        # Step 4: Detect divergences
        self.logger.info(f"🔄 Detecting divergences...")
        divergences = self.analyzer.detect_mtf_divergences(timeframe_data)
        self.logger.info(f"  Found {len(divergences)} divergence(s)")

        # Step 5: Calculate MTF score
        self.logger.info(f"📊 Calculating MTF score...")
        mtf_score = self.scoring_engine.calculate_mtf_score(
            timeframe_data, alignment, divergences
        )
        self.logger.info(
            f"  MTF Score: {mtf_score.overall_score}/10 ({mtf_score.category})"
        )

        # Get trade recommendation
        trade_recommendation = self.scoring_engine.get_trade_recommendation(mtf_score)

        # Step 6: Optimize entry timing
        self.logger.info(f"⏰ Optimizing entry timing...")
        entry_timing = self.entry_optimizer.optimize_entry(
            ticker, timeframe_data, data_by_timeframe
        )
        self.logger.info(
            f"  Entry Signal: {entry_timing.current_signal.signal_type.upper()} "
            f"on {entry_timing.optimal_entry_tf} "
            f"(confidence: {entry_timing.current_signal.confidence:.0%})"
        )

        # Step 7: Generate dashboard
        self.logger.info(f"📋 Generating MTF dashboard...")
        dashboard = self.dashboard_generator.generate_dashboard(
            ticker, timeframe_data, data_by_timeframe,
            alignment, divergences, mtf_score, entry_timing
        )

        # Step 8: Generate alerts
        self.logger.info(f"🔔 Generating alerts...")
        alerts = self.alert_system.generate_all_alerts(
            ticker, timeframe_data, alignment, divergences,
            mtf_score, entry_timing.current_signal,
            dashboard.current_price, previous_score
        )
        self.logger.info(f"  Generated {len(alerts)} alert(s)")

        # Step 9: Build summary
        summary = self._build_summary(
            ticker, timeframe_data, alignment, mtf_score,
            entry_timing, alerts
        )

        self.logger.info(f"✅ Comprehensive MTF analysis complete for {ticker}")

        return ComprehensiveMTFResult(
            ticker=ticker,
            timestamp=datetime.now(),
            timeframe_data=timeframe_data,
            alignment=alignment,
            divergences=divergences,
            mtf_score=mtf_score,
            trade_recommendation=trade_recommendation,
            entry_timing=entry_timing,
            dashboard=dashboard,
            alerts=alerts,
            summary=summary
        )

    async def _fetch_all_timeframes(self, ticker: str) -> Dict[str, any]:
        """Fetch data for all timeframes"""
        data_by_timeframe = {}

        for tf_key, tf_config in self.analyzer.TIMEFRAMES.items():
            interval = tf_config["interval"]

            try:
                data = await market_data_service.get_time_series(
                    ticker=ticker,
                    interval=interval,
                    outputsize=500  # Get enough data for all indicators
                )
                data_by_timeframe[tf_key] = data
                self.logger.debug(f"  Fetched {len(data) if data is not None else 0} bars for {tf_config['label']}")

            except Exception as e:
                self.logger.warning(f"  ⚠️ Failed to fetch {tf_config['label']} data: {e}")
                data_by_timeframe[tf_key] = None

        return data_by_timeframe

    def _build_summary(
        self,
        ticker: str,
        timeframe_data: Dict[str, TimeframeData],
        alignment: MTFAlignment,
        mtf_score: MTFScore,
        entry_timing: EntryTiming,
        alerts: List[MTFAlert]
    ) -> Dict[str, any]:
        """Build concise summary"""
        signal = entry_timing.current_signal

        # Count critical/high alerts
        high_priority_alerts = [
            a for a in alerts
            if a.severity.value in ["critical", "high"]
        ]

        return {
            "ticker": ticker,
            "overall_score": f"{mtf_score.overall_score}/10",
            "category": mtf_score.category,
            "alignment_type": alignment.alignment_type.replace("_", " ").title(),
            "is_aligned": alignment.is_aligned,
            "trend_agreement": alignment.trend_agreement,
            "higher_tf_trend": alignment.higher_tf_trend.upper(),
            "lower_tf_trend": alignment.lower_tf_trend.upper(),
            "entry_signal": signal.signal_type.upper(),
            "entry_confidence": f"{signal.confidence:.0%}",
            "optimal_entry_tf": entry_timing.optimal_entry_tf,
            "total_alerts": len(alerts),
            "high_priority_alerts": len(high_priority_alerts),
            "divergences_detected": len([
                tf for tf in timeframe_data.values()
                if tf.bullish_divergence or tf.bearish_divergence
            ]),
            "bullish_timeframes": len(alignment.bullish_timeframes),
            "bearish_timeframes": len(alignment.bearish_timeframes),
            "neutral_timeframes": len(alignment.neutral_timeframes)
        }

    def format_comprehensive_report(
        self,
        result: ComprehensiveMTFResult,
        include_dashboard: bool = True
    ) -> str:
        """
        Format comprehensive report as text

        Args:
            result: MTF analysis result
            include_dashboard: Include full dashboard (can be verbose)

        Returns:
            Formatted text report
        """
        lines = []

        # Header
        lines.append("=" * 100)
        lines.append(f"COMPREHENSIVE MTF ANALYSIS: {result.ticker}")
        lines.append(f"Generated: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 100)
        lines.append("")

        # Executive Summary
        lines.append("📊 EXECUTIVE SUMMARY")
        lines.append("-" * 100)
        lines.append(f"MTF Score: {result.mtf_score.overall_score}/10 ({result.mtf_score.category})")
        lines.append(f"Recommendation: {result.trade_recommendation}")
        lines.append(f"Alignment: {result.alignment.alignment_type.replace('_', ' ').title()}")
        lines.append(f"Entry Signal: {result.entry_timing.current_signal.signal_type.upper()} "
                    f"(Confidence: {result.entry_timing.current_signal.confidence:.0%})")
        lines.append(f"Alerts: {len(result.alerts)} active")
        lines.append("")

        # Critical Alerts (if any)
        critical_alerts = [a for a in result.alerts if a.severity.value in ["critical", "high"]]
        if critical_alerts:
            lines.append("🚨 CRITICAL ALERTS")
            lines.append("-" * 100)
            for alert in critical_alerts[:5]:  # Show top 5
                lines.append(self.alert_system.format_alert(alert))
                lines.append("")

        # Score Breakdown
        lines.append("📈 SCORE BREAKDOWN")
        lines.append("-" * 100)
        for note in result.mtf_score.scoring_notes:
            lines.append(f"  {note}")
        lines.append("")

        # Alignment Details
        lines.append("🎯 ALIGNMENT DETAILS")
        lines.append("-" * 100)
        lines.append(f"Bullish TFs: {', '.join(result.alignment.bullish_timeframes) or 'None'}")
        lines.append(f"Bearish TFs: {', '.join(result.alignment.bearish_timeframes) or 'None'}")
        lines.append(f"Neutral TFs: {', '.join(result.alignment.neutral_timeframes) or 'None'}")
        lines.append(f"Higher TF Trend: {result.alignment.higher_tf_trend.upper()}")
        lines.append(f"Lower TF Trend: {result.alignment.lower_tf_trend.upper()}")
        lines.append(f"Trend Agreement: {'✅ YES' if result.alignment.trend_agreement else '❌ NO'}")
        lines.append("")

        # Divergences
        if result.divergences:
            lines.append("🔄 DIVERGENCES DETECTED")
            lines.append("-" * 100)
            for div in result.divergences:
                lines.append(f"  • {div.description} (Severity: {div.severity})")
            lines.append("")

        # Entry Timing
        lines.append("⏰ ENTRY TIMING")
        lines.append("-" * 100)
        signal = result.entry_timing.current_signal
        lines.append(f"Signal: {signal.signal_type.upper()}")
        lines.append(f"Optimal Entry TF: {result.entry_timing.optimal_entry_tf}")

        if signal.signal_type != "wait":
            lines.append(f"Entry Price: ${signal.entry_price:.2f}")
            lines.append(f"Stop Loss: ${signal.stop_loss:.2f}")
            lines.append(f"Take Profit: ${signal.take_profit:.2f}")
            lines.append(f"Risk:Reward: {signal.risk_reward_ratio:.2f}")
            lines.append(f"Confidence: {signal.confidence:.0%}")

        for note in result.entry_timing.timing_notes:
            lines.append(f"  {note}")

        if result.entry_timing.wait_for:
            lines.append("")
            lines.append("  Wait for:")
            for condition in result.entry_timing.wait_for:
                lines.append(f"    • {condition}")

        lines.append("")

        # Full Dashboard (optional)
        if include_dashboard:
            lines.append(self.dashboard_generator.format_dashboard_text(result.dashboard))

        # Summary
        lines.append("=" * 100)
        lines.append("END OF REPORT")
        lines.append("=" * 100)

        return "\n".join(lines)


# Global instance
_comprehensive_mtf_service: Optional[ComprehensiveMTFService] = None


def get_comprehensive_mtf_service() -> ComprehensiveMTFService:
    """Get or create comprehensive MTF service singleton"""
    global _comprehensive_mtf_service
    if _comprehensive_mtf_service is None:
        _comprehensive_mtf_service = ComprehensiveMTFService()
    return _comprehensive_mtf_service
