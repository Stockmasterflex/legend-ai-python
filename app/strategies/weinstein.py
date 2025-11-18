"""
Stan Weinstein Trading Strategy Implementation

Implements Stan Weinstein's Stage Analysis methodology:
1. 4-Stage Cycle Analysis (Stages 1-4)
2. Stage 2 Breakout identification
3. 30-week Moving Average analysis
4. Mansfield Relative Strength
5. Volume analysis and confirmation

References:
- "Secrets for Profiting in Bull and Bear Markets" (1988)
- Stage Analysis methodology
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class WeinsteinStage(Enum):
    """Weinstein's 4 stages of stock price cycle"""
    STAGE_1_BASING = 1        # Accumulation/Base
    STAGE_2_ADVANCING = 2     # Markup/Uptrend
    STAGE_3_TOPPING = 3       # Distribution/Top
    STAGE_4_DECLINING = 4     # Markdown/Downtrend
    TRANSITION = 5            # Between stages
    UNKNOWN = 0


@dataclass
class StageAnalysisResult:
    """Stage analysis results"""
    stage: WeinsteinStage
    sub_stage: str  # e.g., "2A" (early stage 2), "2B" (late stage 2)
    confidence: float
    ma_30w: float
    ma_slope: str  # 'rising', 'flat', 'falling'
    price_vs_ma: str  # 'above', 'at', 'below'
    volume_trend: str  # 'increasing', 'flat', 'decreasing'
    details: Dict[str, Any]


@dataclass
class MansfieldRS:
    """Mansfield Relative Strength calculation"""
    current_value: float  # Current RS value
    crosses_zero_line: bool  # Recently crossed above/below zero
    direction: str  # 'rising', 'falling', 'flat'
    is_strong: bool  # RS > 0 and rising
    percentile_rank: float  # 0-100 ranking


@dataclass
class Stage2Breakout:
    """Stage 2 breakout signal"""
    symbol: str
    breakout_price: float
    entry_price: float
    stop_loss: float
    volume_confirmation: bool
    volume_vs_avg: float  # Multiple of 4-week average
    ma_30w: float
    mansfield_rs: float
    confidence: float
    reasons: List[str]


class WeinsteinStrategy:
    """
    Stan Weinstein's Stage Analysis Strategy

    Key Components:
    - 4-Stage Cycle: Identify current stage of price cycle
    - 30-Week MA: Primary trend indicator (on weekly charts)
    - Stage 2 Breakouts: Buy early Stage 2 with volume
    - Mansfield RS: Relative strength vs market
    - Risk Management: Exit on break below 30-week MA
    """

    def __init__(self,
                 use_weekly: bool = True,
                 min_volume_surge: float = 2.0,  # 2x 4-week average
                 ma_period: int = 30):            # 30-week MA (150-day on daily)
        """
        Initialize Weinstein Strategy

        Args:
            use_weekly: Use weekly data (True) or daily with 150-day MA (False)
            min_volume_surge: Minimum volume surge for breakout (2.0 = 2x average)
            ma_period: Moving average period (30 for weekly, 150 for daily)
        """
        self.use_weekly = use_weekly
        self.min_volume_surge = min_volume_surge
        self.ma_period = ma_period if use_weekly else 150

    def analyze_stage(self, ohlcv: pd.DataFrame) -> StageAnalysisResult:
        """
        Determine which of the 4 stages the stock is in

        Stage 1 (Basing):
        - Price oscillates above/below flat 30-week MA
        - Low volume, narrow range
        - MA is flat (neither rising nor falling)

        Stage 2 (Advancing):
        - Price breaks above resistance on heavy volume
        - Price stays above rising 30-week MA
        - Higher highs and higher lows
        - Volume expands on rallies

        Stage 3 (Topping):
        - Price moves sideways, MA flattens
        - Price crosses above/below MA frequently
        - Volume remains high (churning)

        Stage 4 (Declining):
        - Price breaks below 30-week MA on volume
        - Price makes lower lows and lower highs
        - MA turns down
        - Rallies are weak and brief

        Args:
            ohlcv: DataFrame with OHLCV data

        Returns:
            StageAnalysisResult with stage identification
        """
        if len(ohlcv) < self.ma_period + 20:
            return StageAnalysisResult(
                stage=WeinsteinStage.UNKNOWN,
                sub_stage="N/A",
                confidence=0,
                ma_30w=0,
                ma_slope='unknown',
                price_vs_ma='unknown',
                volume_trend='unknown',
                details={}
            )

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values
        volume = ohlcv['volume'].values

        # Calculate 30-week MA (or 150-day for daily)
        ma = pd.Series(close).rolling(self.ma_period).mean().values

        current_price = close[-1]
        current_ma = ma[-1]

        # Analyze MA slope
        ma_slope, slope_value = self._analyze_ma_slope(ma)

        # Price vs MA
        price_vs_ma = self._compare_price_to_ma(current_price, current_ma)

        # Volume trend
        volume_trend = self._analyze_volume_trend(volume)

        # Price action analysis
        higher_highs_lows = self._check_higher_highs_lows(high, low)
        lower_highs_lows = self._check_lower_highs_lows(high, low)

        # Crossing pattern (how often price crosses MA)
        crossings = self._count_ma_crossings(close, ma, lookback=20)

        # Determine stage
        stage, sub_stage, confidence = self._determine_stage(
            current_price, current_ma, ma_slope, slope_value,
            price_vs_ma, volume_trend, higher_highs_lows,
            lower_highs_lows, crossings, close, ma
        )

        details = {
            'current_price': current_price,
            'ma_value': current_ma,
            'ma_slope_value': slope_value,
            'price_pct_from_ma': ((current_price - current_ma) / current_ma * 100),
            'higher_highs_lows': higher_highs_lows,
            'lower_highs_lows': lower_highs_lows,
            'ma_crossings_20bars': crossings,
            'avg_volume_50': np.mean(volume[-50:]),
            'recent_volume': np.mean(volume[-10:])
        }

        return StageAnalysisResult(
            stage=stage,
            sub_stage=sub_stage,
            confidence=confidence,
            ma_30w=current_ma,
            ma_slope=ma_slope,
            price_vs_ma=price_vs_ma,
            volume_trend=volume_trend,
            details=details
        )

    def calculate_mansfield_rs(self,
                               stock_ohlcv: pd.DataFrame,
                               market_ohlcv: pd.DataFrame) -> MansfieldRS:
        """
        Calculate Mansfield Relative Strength

        Formula:
        MRS = ((Stock Price / Market Price) / 52-week MA of (Stock/Market)) - 1) * 100

        Or simplified:
        1. Calculate relative performance: RP = Stock Price / Market Price
        2. Calculate 52-week MA of RP
        3. MRS = ((RP / MA(RP, 52)) - 1) * 100

        Interpretation:
        - MRS > 0: Stock outperforming market
        - MRS < 0: Stock underperforming market
        - Crossing above 0: Bullish signal
        - Rising MRS: Strengthening relative performance

        Args:
            stock_ohlcv: Stock OHLCV data
            market_ohlcv: Market index OHLCV data (e.g., S&P 500)

        Returns:
            MansfieldRS calculation results
        """
        if len(stock_ohlcv) < 252 or len(market_ohlcv) < 252:
            return MansfieldRS(
                current_value=0,
                crosses_zero_line=False,
                direction='flat',
                is_strong=False,
                percentile_rank=50
            )

        # Align data
        min_len = min(len(stock_ohlcv), len(market_ohlcv))
        stock_close = stock_ohlcv['close'].values[-min_len:]
        market_close = market_ohlcv['close'].values[-min_len:]

        # Calculate relative performance
        rp = stock_close / market_close

        # Calculate 52-week (252-day) MA of RP
        rp_ma_52w = pd.Series(rp).rolling(252).mean().values

        # Calculate Mansfield RS
        mansfield_rs = ((rp / rp_ma_52w) - 1) * 100

        current_mrs = mansfield_rs[-1]

        # Check for zero-line cross
        crosses_zero_line = False
        if len(mansfield_rs) >= 10:
            # Check if crossed in last 10 periods
            recent_mrs = mansfield_rs[-10:]
            if any(recent_mrs[i] < 0 and recent_mrs[i+1] > 0 for i in range(len(recent_mrs)-1)):
                crosses_zero_line = True
            elif any(recent_mrs[i] > 0 and recent_mrs[i+1] < 0 for i in range(len(recent_mrs)-1)):
                crosses_zero_line = True

        # Determine direction
        if len(mansfield_rs) >= 20:
            slope = np.polyfit(range(20), mansfield_rs[-20:], 1)[0]
            if slope > 0.1:
                direction = 'rising'
            elif slope < -0.1:
                direction = 'falling'
            else:
                direction = 'flat'
        else:
            direction = 'flat'

        # Is strong (above zero and rising)
        is_strong = current_mrs > 0 and direction == 'rising'

        # Calculate percentile rank (simplified)
        if len(mansfield_rs) >= 252:
            percentile_rank = (
                (mansfield_rs[-1] > mansfield_rs[-252:]).sum() / 252 * 100
            )
        else:
            percentile_rank = 50

        return MansfieldRS(
            current_value=current_mrs,
            crosses_zero_line=crosses_zero_line,
            direction=direction,
            is_strong=is_strong,
            percentile_rank=percentile_rank
        )

    def identify_stage2_breakout(self,
                                 ohlcv: pd.DataFrame,
                                 symbol: str = 'UNKNOWN',
                                 market_ohlcv: Optional[pd.DataFrame] = None) -> Optional[Stage2Breakout]:
        """
        Identify Stage 2 breakout opportunities

        Stage 2 Breakout Criteria:
        1. Stock breaking above Stage 1 resistance
        2. 30-week MA turning up
        3. Price closing above 30-week MA
        4. Volume 2-3x 4-week average
        5. Mansfield RS turning positive (if market data available)
        6. Start of higher highs and higher lows

        Entry: Buy on breakout above resistance
        Stop: Below recent low or 30-week MA (whichever is higher)

        Args:
            ohlcv: Stock OHLCV data
            symbol: Stock symbol
            market_ohlcv: Optional market index data for Mansfield RS

        Returns:
            Stage2Breakout signal if valid setup exists
        """
        # Analyze stage
        stage_result = self.analyze_stage(ohlcv)

        # Must be in Stage 2 (or transitioning to Stage 2)
        if stage_result.stage not in [WeinsteinStage.STAGE_2_ADVANCING, WeinsteinStage.TRANSITION]:
            return None

        # For early Stage 2, we want substage 2A
        if stage_result.sub_stage not in ['2A', '2B', 'Transition_1_to_2']:
            return None

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values
        volume = ohlcv['volume'].values

        current_price = close[-1]
        ma_30w = stage_result.ma_30w

        # Find resistance level (highest high in Stage 1 base)
        # Look back 30-60 bars for base
        lookback = min(60, len(high) - 10)
        resistance = np.max(high[-lookback:-5])

        # Check if breaking out above resistance
        if current_price < resistance * 0.99:
            return None  # Not at breakout point yet

        # Check volume confirmation
        avg_volume_4w = np.mean(volume[-20:])  # 4-week average (20 bars)
        current_volume = volume[-1]
        volume_vs_avg = current_volume / avg_volume_4w if avg_volume_4w > 0 else 1

        volume_confirmation = volume_vs_avg >= self.min_volume_surge

        # Calculate Mansfield RS if market data provided
        mansfield_rs_value = 0
        if market_ohlcv is not None:
            mansfield_rs = self.calculate_mansfield_rs(ohlcv, market_ohlcv)
            mansfield_rs_value = mansfield_rs.current_value

        # Entry price: Just above resistance
        entry_price = resistance * 1.01

        # Stop loss: Below recent low or 30-week MA, whichever is higher
        recent_low = np.min(low[-20:])
        stop_loss = max(recent_low * 0.98, ma_30w * 0.97)

        # Risk check
        risk_pct = (entry_price - stop_loss) / entry_price
        if risk_pct > 0.15:  # More than 15% risk
            return None

        # Calculate confidence
        confidence = self._calculate_stage2_confidence(
            stage_result,
            volume_confirmation,
            volume_vs_avg,
            mansfield_rs_value
        )

        # Build reasons
        reasons = []
        reasons.append(f"Stage {stage_result.stage.value} {stage_result.sub_stage}")
        reasons.append(f"Breakout above ${resistance:.2f} resistance")
        if volume_confirmation:
            reasons.append(f"Volume: {volume_vs_avg:.1f}x average")
        if stage_result.ma_slope == 'rising':
            reasons.append("30-week MA rising")
        if mansfield_rs_value > 0:
            reasons.append(f"Mansfield RS: +{mansfield_rs_value:.1f}")

        return Stage2Breakout(
            symbol=symbol,
            breakout_price=resistance,
            entry_price=entry_price,
            stop_loss=stop_loss,
            volume_confirmation=volume_confirmation,
            volume_vs_avg=volume_vs_avg,
            ma_30w=ma_30w,
            mansfield_rs=mansfield_rs_value,
            confidence=confidence,
            reasons=reasons
        )

    # === Helper Methods ===

    def _analyze_ma_slope(self, ma: np.ndarray) -> Tuple[str, float]:
        """Analyze if MA is rising, flat, or falling"""
        if len(ma) < 20:
            return 'unknown', 0

        # Compare current MA to MA 20 bars ago
        current = ma[-1]
        prior = ma[-20]

        pct_change = (current - prior) / prior * 100

        if pct_change > 2:
            return 'rising', pct_change
        elif pct_change < -2:
            return 'falling', pct_change
        else:
            return 'flat', pct_change

    def _compare_price_to_ma(self, price: float, ma: float) -> str:
        """Compare price position relative to MA"""
        diff_pct = abs(price - ma) / ma * 100

        if diff_pct < 2:
            return 'at'
        elif price > ma:
            return 'above'
        else:
            return 'below'

    def _analyze_volume_trend(self, volume: np.ndarray) -> str:
        """Analyze if volume is increasing, flat, or decreasing"""
        if len(volume) < 50:
            return 'unknown'

        recent_vol = np.mean(volume[-20:])
        prior_vol = np.mean(volume[-50:-20])

        pct_change = (recent_vol - prior_vol) / prior_vol * 100

        if pct_change > 10:
            return 'increasing'
        elif pct_change < -10:
            return 'decreasing'
        else:
            return 'flat'

    def _check_higher_highs_lows(self, high: np.ndarray, low: np.ndarray, lookback: int = 30) -> bool:
        """Check if making higher highs and higher lows"""
        if len(high) < lookback:
            return False

        recent_high = np.max(high[-lookback//2:])
        prior_high = np.max(high[-lookback:-lookback//2])

        recent_low = np.min(low[-lookback//2:])
        prior_low = np.min(low[-lookback:-lookback//2])

        return recent_high > prior_high and recent_low > prior_low

    def _check_lower_highs_lows(self, high: np.ndarray, low: np.ndarray, lookback: int = 30) -> bool:
        """Check if making lower highs and lower lows"""
        if len(high) < lookback:
            return False

        recent_high = np.max(high[-lookback//2:])
        prior_high = np.max(high[-lookback:-lookback//2])

        recent_low = np.min(low[-lookback//2:])
        prior_low = np.min(low[-lookback:-lookback//2])

        return recent_high < prior_high and recent_low < prior_low

    def _count_ma_crossings(self, close: np.ndarray, ma: np.ndarray, lookback: int = 20) -> int:
        """Count how many times price crossed the MA"""
        if len(close) < lookback or len(ma) < lookback:
            return 0

        crossings = 0
        for i in range(-lookback, -1):
            # Check if crossed
            if (close[i-1] < ma[i-1] and close[i] > ma[i]) or \
               (close[i-1] > ma[i-1] and close[i] < ma[i]):
                crossings += 1

        return crossings

    def _determine_stage(self,
                        price: float,
                        ma: float,
                        ma_slope: str,
                        slope_value: float,
                        price_vs_ma: str,
                        volume_trend: str,
                        higher_highs_lows: bool,
                        lower_highs_lows: bool,
                        crossings: int,
                        close: np.ndarray,
                        ma_array: np.ndarray) -> Tuple[WeinsteinStage, str, float]:
        """Determine which stage based on all factors"""

        # Stage 2: Advancing/Uptrend
        if (ma_slope == 'rising' and
            price_vs_ma == 'above' and
            higher_highs_lows and
            crossings <= 2):

            # Determine sub-stage
            # 2A: Early stage 2 (just broke out, MA just turned up)
            if slope_value < 5 or len([1 for i in range(-30, 0) if close[i] > ma_array[i]]) < 20:
                sub_stage = '2A'
                confidence = 85
            # 2B: Late stage 2 (extended, MA steep)
            elif slope_value > 10:
                sub_stage = '2B'
                confidence = 70
            else:
                sub_stage = '2'
                confidence = 80

            return WeinsteinStage.STAGE_2_ADVANCING, sub_stage, confidence

        # Stage 4: Declining/Downtrend
        elif (ma_slope == 'falling' and
              price_vs_ma == 'below' and
              lower_highs_lows):

            # 4A: Early decline
            if slope_value > -5:
                sub_stage = '4A'
            # 4B: Extended decline
            else:
                sub_stage = '4B'

            confidence = 80
            return WeinsteinStage.STAGE_4_DECLINING, sub_stage, confidence

        # Stage 1: Basing/Accumulation
        elif (ma_slope == 'flat' and
              crossings >= 3 and
              not higher_highs_lows and
              not lower_highs_lows):

            sub_stage = '1'
            confidence = 75
            return WeinsteinStage.STAGE_1_BASING, sub_stage, confidence

        # Stage 3: Topping/Distribution
        elif (price_vs_ma in ['above', 'at'] and
              ma_slope in ['flat', 'falling'] and
              crossings >= 3):

            sub_stage = '3'
            confidence = 70
            return WeinsteinStage.STAGE_3_TOPPING, sub_stage, confidence

        # Transition states
        else:
            # Transitioning from 1 to 2
            if ma_slope == 'rising' and price_vs_ma == 'above':
                sub_stage = 'Transition_1_to_2'
                confidence = 65
                return WeinsteinStage.TRANSITION, sub_stage, confidence

            # Transitioning from 2 to 3
            elif price_vs_ma == 'above' and ma_slope == 'flat':
                sub_stage = 'Transition_2_to_3'
                confidence = 60
                return WeinsteinStage.TRANSITION, sub_stage, confidence

            # Unknown
            else:
                sub_stage = 'Unknown'
                confidence = 30
                return WeinsteinStage.UNKNOWN, sub_stage, confidence

    def _calculate_stage2_confidence(self,
                                    stage_result: StageAnalysisResult,
                                    volume_confirmation: bool,
                                    volume_surge: float,
                                    mansfield_rs: float) -> float:
        """Calculate confidence for Stage 2 breakout (0-100)"""
        confidence = 0.0

        # Stage confidence (0-40 points)
        confidence += (stage_result.confidence / 100) * 40

        # Volume (0-30 points)
        if volume_confirmation:
            if volume_surge >= 3.0:
                confidence += 30
            elif volume_surge >= 2.0:
                confidence += 25
            else:
                confidence += 15
        else:
            confidence += 5

        # MA slope (0-15 points)
        if stage_result.ma_slope == 'rising':
            confidence += 15
        elif stage_result.ma_slope == 'flat':
            confidence += 5

        # Mansfield RS (0-15 points)
        if mansfield_rs > 5:
            confidence += 15
        elif mansfield_rs > 0:
            confidence += 10
        elif mansfield_rs > -5:
            confidence += 5

        return min(100, confidence)
