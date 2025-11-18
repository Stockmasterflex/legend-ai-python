"""
Advanced Multi-Timeframe Analyzer
Comprehensive MTF analysis with divergence detection, pattern alignment, and scoring
"""
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class TimeframeData:
    """Data structure for single timeframe analysis"""
    timeframe: str
    label: str  # Display label (e.g., "1D", "1W", "1M")
    weight: float  # Importance weight (0-1)

    # Price data
    current_price: float
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    ema_20: Optional[float] = None

    # Trend analysis
    trend_direction: str = "unknown"  # "up", "down", "sideways"
    trend_strength: float = 0.0  # 0-1
    price_position: str = "unknown"  # "above_sma", "below_sma", "between"

    # Momentum indicators
    rsi: Optional[float] = None
    rsi_trend: str = "neutral"  # "bullish", "bearish", "neutral"
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None

    # Volume
    volume_trend: str = "neutral"
    volume_strength: float = 0.0  # 0-1

    # Pattern detection
    pattern_detected: bool = False
    pattern_type: Optional[str] = None
    pattern_confidence: float = 0.0

    # Support/Resistance
    nearest_support: Optional[float] = None
    nearest_resistance: Optional[float] = None

    # Divergence flags
    bullish_divergence: bool = False
    bearish_divergence: bool = False
    divergence_type: Optional[str] = None  # "regular", "hidden"


@dataclass
class MTFDivergence:
    """Divergence detection across timeframes"""
    detected: bool
    divergence_type: str  # "bullish", "bearish", "none"
    timeframes_involved: List[str]
    severity: str  # "strong", "moderate", "weak"
    description: str

    # Price vs Indicator divergence
    price_trend: str
    indicator_trend: str
    confirmation_score: float  # 0-1


@dataclass
class MTFAlignment:
    """Alignment analysis across all timeframes"""
    is_aligned: bool
    alignment_score: float  # 0-10
    alignment_type: str  # "all_bullish", "all_bearish", "mixed", "neutral"

    # Timeframe agreement
    higher_tf_trend: str  # Trend on higher timeframes (Weekly, Monthly)
    lower_tf_trend: str   # Trend on lower timeframes (4H, 1H)
    trend_agreement: bool

    # Detailed breakdown
    bullish_timeframes: List[str]
    bearish_timeframes: List[str]
    neutral_timeframes: List[str]

    # Conflicts
    conflicts: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class MTFAnalysisResult:
    """Comprehensive MTF analysis result"""
    ticker: str
    timestamp: datetime

    # Overall scoring
    mtf_score: float  # 0-10 composite score
    signal_quality: str  # "Excellent", "Good", "Fair", "Poor"
    trade_recommendation: str  # "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"

    # Timeframe data
    timeframe_data: Dict[str, TimeframeData]

    # Alignment analysis
    alignment: MTFAlignment

    # Divergence detection
    divergences: List[MTFDivergence]

    # Entry/Exit recommendations
    optimal_entry_tf: str
    optimal_entry_price: Optional[float]
    stop_loss: Optional[float]
    take_profit: Optional[float]
    risk_reward_ratio: Optional[float]

    # Detailed insights
    key_insights: List[str]
    warnings: List[str]
    recommendations: List[str]


class MTFAnalyzer:
    """Advanced Multi-Timeframe Analyzer"""

    # Timeframe definitions with weights
    TIMEFRAMES = {
        "1month": {"label": "1M", "weight": 0.30, "interval": "1month"},
        "1week": {"label": "1W", "weight": 0.25, "interval": "1week"},
        "1day": {"label": "1D", "weight": 0.20, "interval": "1day"},
        "4hour": {"label": "4H", "weight": 0.15, "interval": "4hour"},
        "1hour": {"label": "1H", "weight": 0.10, "interval": "1hour"},
    }

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_timeframe(
        self,
        ticker: str,
        timeframe: str,
        data: pd.DataFrame
    ) -> TimeframeData:
        """
        Analyze a single timeframe

        Args:
            ticker: Stock symbol
            timeframe: Timeframe key (e.g., "1day")
            data: OHLCV DataFrame

        Returns:
            TimeframeData with complete analysis
        """
        tf_config = self.TIMEFRAMES.get(timeframe, {})
        label = tf_config.get("label", timeframe)
        weight = tf_config.get("weight", 0.1)

        if data is None or len(data) < 50:
            return TimeframeData(
                timeframe=timeframe,
                label=label,
                weight=weight,
                current_price=0.0,
                trend_direction="unknown"
            )

        # Current price
        current_price = float(data['close'].iloc[-1])

        # Calculate moving averages
        sma_50 = float(data['close'].rolling(50).mean().iloc[-1]) if len(data) >= 50 else None
        sma_200 = float(data['close'].rolling(200).mean().iloc[-1]) if len(data) >= 200 else None
        ema_20 = float(data['close'].ewm(span=20).mean().iloc[-1]) if len(data) >= 20 else None

        # Trend analysis
        trend_direction = self._calculate_trend(data)
        trend_strength = self._calculate_trend_strength(data)
        price_position = self._calculate_price_position(current_price, sma_50, sma_200)

        # RSI
        rsi = self._calculate_rsi(data)
        rsi_trend = self._classify_rsi_trend(rsi)

        # MACD
        macd, macd_signal, macd_hist = self._calculate_macd(data)

        # Volume analysis
        volume_trend = self._calculate_volume_trend(data)
        volume_strength = self._calculate_volume_strength(data)

        # Support/Resistance
        support, resistance = self._find_nearest_sr(data, current_price)

        # Divergence detection (price vs RSI)
        bullish_div, bearish_div, div_type = self._detect_divergence(data, rsi)

        return TimeframeData(
            timeframe=timeframe,
            label=label,
            weight=weight,
            current_price=current_price,
            sma_50=sma_50,
            sma_200=sma_200,
            ema_20=ema_20,
            trend_direction=trend_direction,
            trend_strength=trend_strength,
            price_position=price_position,
            rsi=rsi,
            rsi_trend=rsi_trend,
            macd=macd,
            macd_signal=macd_signal,
            macd_histogram=macd_hist,
            volume_trend=volume_trend,
            volume_strength=volume_strength,
            nearest_support=support,
            nearest_resistance=resistance,
            bullish_divergence=bullish_div,
            bearish_divergence=bearish_div,
            divergence_type=div_type
        )

    def analyze_alignment(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> MTFAlignment:
        """
        Analyze alignment across all timeframes

        Args:
            timeframe_data: Dictionary of TimeframeData for each timeframe

        Returns:
            MTFAlignment with detailed alignment analysis
        """
        bullish_tfs = []
        bearish_tfs = []
        neutral_tfs = []

        # Categorize each timeframe
        for tf_key, tf_data in timeframe_data.items():
            if tf_data.trend_direction == "up":
                bullish_tfs.append(tf_data.label)
            elif tf_data.trend_direction == "down":
                bearish_tfs.append(tf_data.label)
            else:
                neutral_tfs.append(tf_data.label)

        # Calculate alignment score (0-10)
        alignment_score = self._calculate_alignment_score(timeframe_data)

        # Determine alignment type
        num_bullish = len(bullish_tfs)
        num_bearish = len(bearish_tfs)
        total = len(timeframe_data)

        if num_bullish == total:
            alignment_type = "all_bullish"
            is_aligned = True
        elif num_bearish == total:
            alignment_type = "all_bearish"
            is_aligned = True
        elif num_bullish >= total * 0.8:
            alignment_type = "mostly_bullish"
            is_aligned = True
        elif num_bearish >= total * 0.8:
            alignment_type = "mostly_bearish"
            is_aligned = True
        elif num_bullish > num_bearish:
            alignment_type = "mixed_bullish"
            is_aligned = False
        elif num_bearish > num_bullish:
            alignment_type = "mixed_bearish"
            is_aligned = False
        else:
            alignment_type = "neutral"
            is_aligned = False

        # Higher vs Lower TF trends
        higher_tf_trend = self._get_higher_tf_trend(timeframe_data)
        lower_tf_trend = self._get_lower_tf_trend(timeframe_data)
        trend_agreement = (higher_tf_trend == lower_tf_trend)

        # Identify conflicts
        conflicts = []
        warnings = []

        if not trend_agreement:
            conflicts.append(f"Higher TF ({higher_tf_trend}) conflicts with Lower TF ({lower_tf_trend})")

        # Check for specific conflicts
        monthly = timeframe_data.get("1month")
        daily = timeframe_data.get("1day")

        if monthly and daily:
            if monthly.trend_direction == "down" and daily.trend_direction == "up":
                warnings.append("⚠️ Daily uptrend but Monthly downtrend - beware of reversal")
            elif monthly.trend_direction == "up" and daily.trend_direction == "down":
                warnings.append("⚠️ Daily downtrend but Monthly uptrend - may be pullback opportunity")

        return MTFAlignment(
            is_aligned=is_aligned,
            alignment_score=alignment_score,
            alignment_type=alignment_type,
            higher_tf_trend=higher_tf_trend,
            lower_tf_trend=lower_tf_trend,
            trend_agreement=trend_agreement,
            bullish_timeframes=bullish_tfs,
            bearish_timeframes=bearish_tfs,
            neutral_timeframes=neutral_tfs,
            conflicts=conflicts,
            warnings=warnings
        )

    def detect_mtf_divergences(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> List[MTFDivergence]:
        """
        Detect divergences across multiple timeframes

        Args:
            timeframe_data: Dictionary of TimeframeData

        Returns:
            List of detected divergences
        """
        divergences = []

        # Check for divergences in each timeframe
        for tf_key, tf_data in timeframe_data.items():
            if tf_data.bullish_divergence:
                divergences.append(MTFDivergence(
                    detected=True,
                    divergence_type="bullish",
                    timeframes_involved=[tf_data.label],
                    severity=self._assess_divergence_severity(tf_data),
                    description=f"Bullish {tf_data.divergence_type or 'regular'} divergence on {tf_data.label}",
                    price_trend="down",
                    indicator_trend="up",
                    confirmation_score=tf_data.trend_strength
                ))

            if tf_data.bearish_divergence:
                divergences.append(MTFDivergence(
                    detected=True,
                    divergence_type="bearish",
                    timeframes_involved=[tf_data.label],
                    severity=self._assess_divergence_severity(tf_data),
                    description=f"Bearish {tf_data.divergence_type or 'regular'} divergence on {tf_data.label}",
                    price_trend="up",
                    indicator_trend="down",
                    confirmation_score=tf_data.trend_strength
                ))

        # Check for cross-timeframe divergences
        # Example: Daily price rising but Weekly RSI falling
        daily = timeframe_data.get("1day")
        weekly = timeframe_data.get("1week")

        if daily and weekly:
            if (daily.trend_direction == "up" and
                weekly.rsi and weekly.rsi < 50 and
                daily.rsi and daily.rsi > weekly.rsi + 10):

                divergences.append(MTFDivergence(
                    detected=True,
                    divergence_type="bearish",
                    timeframes_involved=["1D", "1W"],
                    severity="strong",
                    description="Cross-timeframe divergence: Daily rally but Weekly momentum weakening",
                    price_trend="up",
                    indicator_trend="down",
                    confirmation_score=0.7
                ))

        return divergences

    def _calculate_trend(self, data: pd.DataFrame) -> str:
        """Calculate trend direction"""
        if len(data) < 20:
            return "unknown"

        # Compare recent price to older price
        recent_avg = data['close'].tail(10).mean()
        older_avg = data['close'].iloc[-30:-20].mean() if len(data) >= 30 else data['close'].iloc[:10].mean()

        change_pct = (recent_avg - older_avg) / older_avg

        if change_pct > 0.02:
            return "up"
        elif change_pct < -0.02:
            return "down"
        else:
            return "sideways"

    def _calculate_trend_strength(self, data: pd.DataFrame) -> float:
        """Calculate trend strength (0-1)"""
        if len(data) < 20:
            return 0.0

        # Use linear regression slope
        prices = data['close'].tail(20).values
        x = np.arange(len(prices))
        slope, _ = np.polyfit(x, prices, 1)

        # Normalize slope to 0-1 range
        avg_price = prices.mean()
        normalized_slope = abs(slope) / avg_price * 20  # Scale factor

        return min(1.0, normalized_slope)

    def _calculate_price_position(
        self,
        current_price: float,
        sma_50: Optional[float],
        sma_200: Optional[float]
    ) -> str:
        """Determine price position relative to moving averages"""
        if not sma_50 or not sma_200:
            return "unknown"

        if current_price > sma_50 and current_price > sma_200:
            return "above_both"
        elif current_price < sma_50 and current_price < sma_200:
            return "below_both"
        elif current_price > sma_50 and current_price < sma_200:
            return "between_ascending"
        else:
            return "between_descending"

    def _calculate_rsi(self, data: pd.DataFrame, period: int = 14) -> Optional[float]:
        """Calculate RSI"""
        if len(data) < period + 1:
            return None

        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        return float(rsi.iloc[-1]) if not pd.isna(rsi.iloc[-1]) else None

    def _classify_rsi_trend(self, rsi: Optional[float]) -> str:
        """Classify RSI as bullish, bearish, or neutral"""
        if rsi is None:
            return "neutral"

        if rsi > 60:
            return "bullish"
        elif rsi < 40:
            return "bearish"
        else:
            return "neutral"

    def _calculate_macd(
        self,
        data: pd.DataFrame,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Calculate MACD"""
        if len(data) < slow + signal:
            return None, None, None

        ema_fast = data['close'].ewm(span=fast).mean()
        ema_slow = data['close'].ewm(span=slow).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=signal).mean()
        histogram = macd_line - signal_line

        return (
            float(macd_line.iloc[-1]) if not pd.isna(macd_line.iloc[-1]) else None,
            float(signal_line.iloc[-1]) if not pd.isna(signal_line.iloc[-1]) else None,
            float(histogram.iloc[-1]) if not pd.isna(histogram.iloc[-1]) else None
        )

    def _calculate_volume_trend(self, data: pd.DataFrame) -> str:
        """Calculate volume trend"""
        if len(data) < 20:
            return "neutral"

        recent_vol = data['volume'].tail(10).mean()
        older_vol = data['volume'].iloc[-30:-20].mean() if len(data) >= 30 else data['volume'].iloc[:10].mean()

        if recent_vol > older_vol * 1.2:
            return "increasing"
        elif recent_vol < older_vol * 0.8:
            return "decreasing"
        else:
            return "neutral"

    def _calculate_volume_strength(self, data: pd.DataFrame) -> float:
        """Calculate volume strength (0-1)"""
        if len(data) < 20:
            return 0.0

        recent_vol = data['volume'].tail(10).mean()
        avg_vol = data['volume'].mean()

        ratio = recent_vol / avg_vol if avg_vol > 0 else 1.0

        # Normalize to 0-1 (1.5x average = 0.5, 2x average = 1.0)
        return min(1.0, (ratio - 1.0) * 2)

    def _find_nearest_sr(
        self,
        data: pd.DataFrame,
        current_price: float
    ) -> Tuple[Optional[float], Optional[float]]:
        """Find nearest support and resistance levels"""
        if len(data) < 50:
            return None, None

        # Use recent highs/lows
        highs = data['high'].tail(50)
        lows = data['low'].tail(50)

        # Find resistance (nearest high above current price)
        resistance_levels = highs[highs > current_price]
        resistance = float(resistance_levels.min()) if len(resistance_levels) > 0 else None

        # Find support (nearest low below current price)
        support_levels = lows[lows < current_price]
        support = float(support_levels.max()) if len(support_levels) > 0 else None

        return support, resistance

    def _detect_divergence(
        self,
        data: pd.DataFrame,
        rsi: Optional[float]
    ) -> Tuple[bool, bool, Optional[str]]:
        """
        Detect price/RSI divergence

        Returns:
            Tuple of (bullish_divergence, bearish_divergence, divergence_type)
        """
        if rsi is None or len(data) < 30:
            return False, False, None

        # Calculate RSI for last 30 bars
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi_series = 100 - (100 / (1 + rs))

        # Get recent data
        recent_prices = data['close'].tail(20).values
        recent_rsi = rsi_series.tail(20).values

        # Simple divergence detection: compare slopes
        price_slope = np.polyfit(np.arange(len(recent_prices)), recent_prices, 1)[0]
        rsi_slope = np.polyfit(np.arange(len(recent_rsi)), recent_rsi, 1)[0]

        # Bullish divergence: price falling, RSI rising
        bullish_div = (price_slope < 0 and rsi_slope > 0 and abs(price_slope) > abs(rsi_slope) * 0.1)

        # Bearish divergence: price rising, RSI falling
        bearish_div = (price_slope > 0 and rsi_slope < 0 and abs(rsi_slope) > abs(price_slope) * 0.1)

        div_type = "regular" if (bullish_div or bearish_div) else None

        return bullish_div, bearish_div, div_type

    def _calculate_alignment_score(
        self,
        timeframe_data: Dict[str, TimeframeData]
    ) -> float:
        """
        Calculate alignment score (0-10)

        10 = All timeframes bullish with strong trends
        5 = Mixed signals
        0 = All timeframes bearish with strong trends
        """
        total_score = 0.0
        total_weight = 0.0

        for tf_key, tf_data in timeframe_data.items():
            # Calculate individual TF score
            tf_score = 5.0  # Neutral baseline

            # Adjust for trend
            if tf_data.trend_direction == "up":
                tf_score = 5.0 + (tf_data.trend_strength * 5.0)
            elif tf_data.trend_direction == "down":
                tf_score = 5.0 - (tf_data.trend_strength * 5.0)

            # Apply weight
            weighted_score = tf_score * tf_data.weight
            total_score += weighted_score
            total_weight += tf_data.weight

        # Normalize to 0-10
        if total_weight > 0:
            final_score = total_score / total_weight
        else:
            final_score = 5.0

        return round(final_score, 2)

    def _get_higher_tf_trend(self, timeframe_data: Dict[str, TimeframeData]) -> str:
        """Get consensus trend from higher timeframes (Monthly, Weekly)"""
        higher_tfs = ["1month", "1week"]
        trends = []

        for tf_key in higher_tfs:
            if tf_key in timeframe_data:
                trends.append(timeframe_data[tf_key].trend_direction)

        if not trends:
            return "unknown"

        # Return most common trend
        up_count = trends.count("up")
        down_count = trends.count("down")

        if up_count > down_count:
            return "up"
        elif down_count > up_count:
            return "down"
        else:
            return "sideways"

    def _get_lower_tf_trend(self, timeframe_data: Dict[str, TimeframeData]) -> str:
        """Get consensus trend from lower timeframes (4H, 1H)"""
        lower_tfs = ["4hour", "1hour"]
        trends = []

        for tf_key in lower_tfs:
            if tf_key in timeframe_data:
                trends.append(timeframe_data[tf_key].trend_direction)

        if not trends:
            return "unknown"

        # Return most common trend
        up_count = trends.count("up")
        down_count = trends.count("down")

        if up_count > down_count:
            return "up"
        elif down_count > up_count:
            return "down"
        else:
            return "sideways"

    def _assess_divergence_severity(self, tf_data: TimeframeData) -> str:
        """Assess divergence severity based on timeframe and trend strength"""
        # Higher timeframes = more severe divergences
        if tf_data.timeframe in ["1month", "1week"]:
            return "strong"
        elif tf_data.timeframe == "1day":
            return "moderate"
        else:
            return "weak"
