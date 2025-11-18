"""
MTF Alerts System
Monitors timeframe alignment and generates alerts when conditions are met
"""
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from app.core.mtf_analyzer import TimeframeData, MTFAlignment, MTFDivergence
from app.core.mtf_scoring import MTFScore
from app.core.mtf_entry_timing import EntrySignal

logger = logging.getLogger(__name__)


class AlertType(Enum):
    """Alert type classifications"""
    ALIGNMENT = "alignment"
    DIVERGENCE = "divergence"
    ENTRY_SIGNAL = "entry_signal"
    SCORE_CHANGE = "score_change"
    PATTERN = "pattern"
    BREAKOUT = "breakout"


class AlertSeverity(Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class MTFAlert:
    """Multi-Timeframe Alert"""
    alert_id: str
    ticker: str
    timestamp: datetime

    # Alert classification
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str

    # Context
    timeframes_affected: List[str]
    trigger_condition: str

    # Data
    current_price: float
    score: Optional[float] = None
    recommendation: Optional[str] = None

    # Actions
    suggested_action: Optional[str] = None
    expires_at: Optional[datetime] = None


class MTFAlertSystem:
    """
    MTF Alert System

    Monitors conditions and generates alerts for:
    - All timeframes aligned (bullish or bearish)
    - Divergence detection
    - Entry signal triggers
    - Score threshold crossings
    - Pattern confirmations
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def check_alignment_alerts(
        self,
        ticker: str,
        alignment: MTFAlignment,
        timeframe_data: Dict[str, TimeframeData],
        current_price: float
    ) -> List[MTFAlert]:
        """
        Check for alignment-based alerts

        Triggers when:
        - All timeframes align bullish
        - All timeframes align bearish
        - Transition from misaligned to aligned
        """
        alerts = []

        # Perfect alignment alerts
        if alignment.alignment_type == "all_bullish":
            alerts.append(MTFAlert(
                alert_id=f"{ticker}_ALL_BULLISH_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.ALIGNMENT,
                severity=AlertSeverity.CRITICAL,
                title="🎯 ALL TIMEFRAMES BULLISH",
                message=f"{ticker}: All timeframes ({', '.join(alignment.bullish_timeframes)}) aligned bullish. Strong buy signal!",
                timeframes_affected=alignment.bullish_timeframes,
                trigger_condition="all_timeframes_bullish",
                current_price=current_price,
                score=alignment.alignment_score,
                recommendation="STRONG BUY",
                suggested_action="Consider immediate long entry with tight stops"
            ))

        elif alignment.alignment_type == "all_bearish":
            alerts.append(MTFAlert(
                alert_id=f"{ticker}_ALL_BEARISH_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.ALIGNMENT,
                severity=AlertSeverity.HIGH,
                title="⚠️ ALL TIMEFRAMES BEARISH",
                message=f"{ticker}: All timeframes ({', '.join(alignment.bearish_timeframes)}) aligned bearish. Strong sell signal!",
                timeframes_affected=alignment.bearish_timeframes,
                trigger_condition="all_timeframes_bearish",
                current_price=current_price,
                score=alignment.alignment_score,
                recommendation="STRONG SELL",
                suggested_action="Consider exiting longs or initiating short position"
            ))

        # Strong alignment (80%+)
        elif alignment.alignment_type == "mostly_bullish":
            num_bullish = len(alignment.bullish_timeframes)
            total = num_bullish + len(alignment.bearish_timeframes) + len(alignment.neutral_timeframes)

            if num_bullish / total >= 0.8:
                alerts.append(MTFAlert(
                    alert_id=f"{ticker}_MOSTLY_BULLISH_{datetime.now().timestamp()}",
                    ticker=ticker,
                    timestamp=datetime.now(),
                    alert_type=AlertType.ALIGNMENT,
                    severity=AlertSeverity.HIGH,
                    title="📈 STRONG BULLISH ALIGNMENT",
                    message=f"{ticker}: {num_bullish}/{total} timeframes bullish ({', '.join(alignment.bullish_timeframes)}). High probability setup.",
                    timeframes_affected=alignment.bullish_timeframes,
                    trigger_condition="strong_bullish_alignment",
                    current_price=current_price,
                    score=alignment.alignment_score,
                    recommendation="BUY",
                    suggested_action="Look for entry on pullback to support"
                ))

        elif alignment.alignment_type == "mostly_bearish":
            num_bearish = len(alignment.bearish_timeframes)
            total = num_bearish + len(alignment.bullish_timeframes) + len(alignment.neutral_timeframes)

            if num_bearish / total >= 0.8:
                alerts.append(MTFAlert(
                    alert_id=f"{ticker}_MOSTLY_BEARISH_{datetime.now().timestamp()}",
                    ticker=ticker,
                    timestamp=datetime.now(),
                    alert_type=AlertType.ALIGNMENT,
                    severity=AlertSeverity.MEDIUM,
                    title="📉 STRONG BEARISH ALIGNMENT",
                    message=f"{ticker}: {num_bearish}/{total} timeframes bearish ({', '.join(alignment.bearish_timeframes)}). High probability downside.",
                    timeframes_affected=alignment.bearish_timeframes,
                    trigger_condition="strong_bearish_alignment",
                    current_price=current_price,
                    score=alignment.alignment_score,
                    recommendation="SELL",
                    suggested_action="Consider exiting or wait for oversold bounce to short"
                ))

        # Trend agreement between higher and lower TFs
        if alignment.trend_agreement and alignment.higher_tf_trend != "sideways":
            direction = alignment.higher_tf_trend.upper()

            alerts.append(MTFAlert(
                alert_id=f"{ticker}_TF_AGREEMENT_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.ALIGNMENT,
                severity=AlertSeverity.MEDIUM,
                title=f"✅ HIGHER/LOWER TF AGREEMENT: {direction}",
                message=f"{ticker}: Higher and lower timeframes agree on {direction} trend. Good confluence.",
                timeframes_affected=list(timeframe_data.keys()),
                trigger_condition=f"tf_agreement_{direction.lower()}",
                current_price=current_price,
                score=alignment.alignment_score,
                recommendation="BUY" if direction == "UP" else "SELL",
                suggested_action=f"Look for {direction} continuation patterns"
            ))

        return alerts

    def check_divergence_alerts(
        self,
        ticker: str,
        divergences: List[MTFDivergence],
        current_price: float
    ) -> List[MTFAlert]:
        """
        Check for divergence alerts

        Alerts for strong divergences that may signal reversals
        """
        alerts = []

        for div in divergences:
            if div.severity == "strong":
                severity = AlertSeverity.HIGH
            elif div.severity == "moderate":
                severity = AlertSeverity.MEDIUM
            else:
                severity = AlertSeverity.LOW

            if div.divergence_type == "bullish":
                title = "🔄 BULLISH DIVERGENCE DETECTED"
                suggested_action = "Watch for reversal setup - potential long entry"
            else:
                title = "🔄 BEARISH DIVERGENCE DETECTED"
                suggested_action = "Watch for reversal - consider taking profits or shorting"

            alerts.append(MTFAlert(
                alert_id=f"{ticker}_DIV_{div.divergence_type}_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.DIVERGENCE,
                severity=severity,
                title=title,
                message=f"{ticker}: {div.description}",
                timeframes_affected=div.timeframes_involved,
                trigger_condition=f"{div.divergence_type}_divergence_{div.severity}",
                current_price=current_price,
                score=div.confirmation_score,
                recommendation="WATCH",
                suggested_action=suggested_action
            ))

        return alerts

    def check_entry_signal_alerts(
        self,
        ticker: str,
        entry_signal: EntrySignal,
        current_price: float
    ) -> List[MTFAlert]:
        """
        Check for entry signal alerts

        Alerts when high-confidence entry signals appear
        """
        alerts = []

        # Only alert on high-confidence signals
        if entry_signal.confidence >= 0.7:
            if entry_signal.signal_type == "buy":
                severity = AlertSeverity.CRITICAL if entry_signal.confidence >= 0.8 else AlertSeverity.HIGH
                title = "🎯 LONG ENTRY SIGNAL"
                message = (
                    f"{ticker}: High-confidence LONG entry at ${entry_signal.entry_price:.2f}\n"
                    f"Stop: ${entry_signal.stop_loss:.2f} | Target: ${entry_signal.take_profit:.2f}\n"
                    f"R:R = {entry_signal.risk_reward_ratio:.2f} | Confidence: {entry_signal.confidence:.0%}"
                )
                recommendation = "BUY"

            elif entry_signal.signal_type == "sell":
                severity = AlertSeverity.CRITICAL if entry_signal.confidence >= 0.8 else AlertSeverity.HIGH
                title = "🎯 SHORT ENTRY SIGNAL"
                message = (
                    f"{ticker}: High-confidence SHORT entry at ${entry_signal.entry_price:.2f}\n"
                    f"Stop: ${entry_signal.stop_loss:.2f} | Target: ${entry_signal.take_profit:.2f}\n"
                    f"R:R = {entry_signal.risk_reward_ratio:.2f} | Confidence: {entry_signal.confidence:.0%}"
                )
                recommendation = "SELL"

            else:
                return alerts  # No alert for "wait" signals

            alerts.append(MTFAlert(
                alert_id=f"{ticker}_ENTRY_{entry_signal.signal_type.upper()}_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.ENTRY_SIGNAL,
                severity=severity,
                title=title,
                message=message,
                timeframes_affected=[entry_signal.entry_timeframe],
                trigger_condition=f"entry_signal_{entry_signal.signal_type}_confidence_{entry_signal.confidence:.0%}",
                current_price=current_price,
                score=entry_signal.confidence,
                recommendation=recommendation,
                suggested_action=f"Execute {entry_signal.signal_type.upper()} with planned risk management"
            ))

        return alerts

    def check_score_alerts(
        self,
        ticker: str,
        mtf_score: MTFScore,
        current_price: float,
        previous_score: Optional[float] = None
    ) -> List[MTFAlert]:
        """
        Check for score-based alerts

        Alerts on:
        - Score crossing into "Excellent" range (>= 8.5)
        - Score dropping below warning threshold (< 5.0)
        - Significant score changes
        """
        alerts = []

        score = mtf_score.overall_score

        # Excellent score alert
        if score >= 8.5:
            alerts.append(MTFAlert(
                alert_id=f"{ticker}_SCORE_EXCELLENT_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.SCORE_CHANGE,
                severity=AlertSeverity.HIGH,
                title="⭐ EXCELLENT SCORE ACHIEVED",
                message=f"{ticker}: MTF Score = {score}/10 ({mtf_score.category}). Premium setup!",
                timeframes_affected=[],
                trigger_condition="score_excellent",
                current_price=current_price,
                score=score,
                recommendation="STRONG BUY" if score >= 9.0 else "BUY",
                suggested_action="High-quality setup - consider position entry"
            ))

        # Warning score alert
        elif score < 4.0:
            alerts.append(MTFAlert(
                alert_id=f"{ticker}_SCORE_WARNING_{datetime.now().timestamp()}",
                ticker=ticker,
                timestamp=datetime.now(),
                alert_type=AlertType.SCORE_CHANGE,
                severity=AlertSeverity.MEDIUM,
                title="⚠️ LOW SCORE WARNING",
                message=f"{ticker}: MTF Score = {score}/10 ({mtf_score.category}). Poor setup quality.",
                timeframes_affected=[],
                trigger_condition="score_warning",
                current_price=current_price,
                score=score,
                recommendation="AVOID" if score < 3.0 else "HOLD",
                suggested_action="Wait for better setup or consider exiting"
            ))

        # Significant score change
        if previous_score is not None:
            score_change = score - previous_score

            if abs(score_change) >= 2.0:
                if score_change > 0:
                    title = "📈 SCORE IMPROVED SIGNIFICANTLY"
                    severity = AlertSeverity.MEDIUM
                else:
                    title = "📉 SCORE DETERIORATED"
                    severity = AlertSeverity.MEDIUM

                alerts.append(MTFAlert(
                    alert_id=f"{ticker}_SCORE_CHANGE_{datetime.now().timestamp()}",
                    ticker=ticker,
                    timestamp=datetime.now(),
                    alert_type=AlertType.SCORE_CHANGE,
                    severity=severity,
                    title=title,
                    message=f"{ticker}: Score changed from {previous_score:.1f} to {score:.1f} ({score_change:+.1f})",
                    timeframes_affected=[],
                    trigger_condition="score_significant_change",
                    current_price=current_price,
                    score=score,
                    recommendation="MONITOR",
                    suggested_action="Re-evaluate position based on new score"
                ))

        return alerts

    def generate_all_alerts(
        self,
        ticker: str,
        timeframe_data: Dict[str, TimeframeData],
        alignment: MTFAlignment,
        divergences: List[MTFDivergence],
        mtf_score: MTFScore,
        entry_signal: EntrySignal,
        current_price: float,
        previous_score: Optional[float] = None
    ) -> List[MTFAlert]:
        """
        Generate all alerts for current market conditions

        Args:
            ticker: Stock symbol
            timeframe_data: Dictionary of TimeframeData
            alignment: MTF alignment
            divergences: List of divergences
            mtf_score: MTF score
            entry_signal: Entry signal
            current_price: Current price
            previous_score: Previous MTF score (for comparison)

        Returns:
            List of all active alerts
        """
        all_alerts = []

        # Check each alert type
        all_alerts.extend(self.check_alignment_alerts(ticker, alignment, timeframe_data, current_price))
        all_alerts.extend(self.check_divergence_alerts(ticker, divergences, current_price))
        all_alerts.extend(self.check_entry_signal_alerts(ticker, entry_signal, current_price))
        all_alerts.extend(self.check_score_alerts(ticker, mtf_score, current_price, previous_score))

        # Sort by severity
        severity_order = {
            AlertSeverity.CRITICAL: 0,
            AlertSeverity.HIGH: 1,
            AlertSeverity.MEDIUM: 2,
            AlertSeverity.LOW: 3,
            AlertSeverity.INFO: 4
        }

        all_alerts.sort(key=lambda a: severity_order[a.severity])

        return all_alerts

    def format_alert(self, alert: MTFAlert) -> str:
        """Format alert as text for display"""
        severity_icons = {
            AlertSeverity.CRITICAL: "🔴",
            AlertSeverity.HIGH: "🟠",
            AlertSeverity.MEDIUM: "🟡",
            AlertSeverity.LOW: "🔵",
            AlertSeverity.INFO: "⚪"
        }

        icon = severity_icons.get(alert.severity, "")

        lines = [
            f"{icon} {alert.title}",
            f"Ticker: {alert.ticker}",
            f"Time: {alert.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Message: {alert.message}",
        ]

        if alert.timeframes_affected:
            lines.append(f"Timeframes: {', '.join(alert.timeframes_affected)}")

        if alert.recommendation:
            lines.append(f"Recommendation: {alert.recommendation}")

        if alert.suggested_action:
            lines.append(f"Action: {alert.suggested_action}")

        if alert.score is not None:
            lines.append(f"Score: {alert.score:.1%}" if alert.score <= 1.0 else f"Score: {alert.score:.1f}/10")

        return "\n".join(lines)
