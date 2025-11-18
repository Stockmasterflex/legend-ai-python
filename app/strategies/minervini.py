"""
Mark Minervini Trading Strategy Implementation

Implements Mark Minervini's proven methodologies:
1. SEPA (Specific Entry Point Analysis)
2. VCP (Volatility Contraction Pattern)
3. Stage Analysis (Stage 2 Uptrend identification)
4. Trend Template (8-point checklist)
5. Position Sizing & Risk Management

References:
- "Trade Like a Stock Market Wizard" (2013)
- "Think & Trade Like a Champion" (2017)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class Stage(Enum):
    """Stock price stages"""
    STAGE_1_BASING = 1
    STAGE_2_UPTREND = 2
    STAGE_3_TOPPING = 3
    STAGE_4_DOWNTREND = 4
    UNKNOWN = 0


@dataclass
class TrendTemplateResult:
    """Results from Minervini Trend Template analysis"""
    passes: bool
    score: float  # 0-8 (number of criteria met)
    criteria: Dict[str, bool]
    stage: Stage
    details: Dict[str, Any]


@dataclass
class SEPASignal:
    """SEPA entry signal"""
    symbol: str
    entry_price: float
    stop_loss: float
    initial_target: float
    risk_reward_ratio: float
    position_size_pct: float
    entry_type: str  # 'breakout' or 'pullback'
    confidence: float
    reasons: List[str]


@dataclass
class VCPAnalysis:
    """VCP pattern analysis results"""
    is_vcp: bool
    num_contractions: int
    contraction_sequence: List[float]  # % declines
    final_contraction_pct: float
    volume_declining: bool
    breakout_imminent: bool
    pivot_price: float


class MinerviniStrategy:
    """
    Mark Minervini's complete trading strategy implementation

    Key Components:
    - Trend Template: 8-point checklist for Stage 2 stocks
    - SEPA: Precise entry point identification
    - VCP: Volatility contraction pattern detection
    - Position Sizing: Risk-based position sizing (1% risk rule)
    - Risk Management: 7-10% stop losses, trailing stops
    """

    def __init__(self,
                 risk_per_trade: float = 0.01,  # 1% risk per trade
                 max_stop_loss: float = 0.10,   # 10% max stop
                 min_rs_rating: float = 70,      # Min relative strength
                 account_size: float = 100000):  # Portfolio size
        """
        Initialize Minervini Strategy

        Args:
            risk_per_trade: Max risk per trade as decimal (0.01 = 1%)
            max_stop_loss: Maximum stop loss percentage (0.10 = 10%)
            min_rs_rating: Minimum relative strength rating (0-100)
            account_size: Total portfolio value
        """
        self.risk_per_trade = risk_per_trade
        self.max_stop_loss = max_stop_loss
        self.min_rs_rating = min_rs_rating
        self.account_size = account_size

    def check_trend_template(self, ohlcv: pd.DataFrame) -> TrendTemplateResult:
        """
        Minervini's 8-Point Trend Template

        Criteria:
        1. Current price > 150-day & 200-day MA
        2. 150-day MA > 200-day MA
        3. 200-day MA trending up for at least 1 month
        4. 50-day MA > 150-day MA > 200-day MA
        5. Current price > 50-day MA
        6. Current price at least 30% above 52-week low
        7. Current price within 25% of 52-week high
        8. Relative Strength (RS) rating >= 70

        Args:
            ohlcv: DataFrame with OHLCV data (minimum 200 days)

        Returns:
            TrendTemplateResult with pass/fail and details
        """
        if len(ohlcv) < 200:
            return TrendTemplateResult(
                passes=False, score=0, criteria={},
                stage=Stage.UNKNOWN, details={}
            )

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values

        # Calculate moving averages
        ma_50 = pd.Series(close).rolling(50).mean().values
        ma_150 = pd.Series(close).rolling(150).mean().values
        ma_200 = pd.Series(close).rolling(200).mean().values

        current_price = close[-1]

        # Calculate 52-week high/low
        week_52_high = np.max(high[-252:])  # ~252 trading days = 1 year
        week_52_low = np.min(low[-252:])

        # Criterion 1: Price > 150-day & 200-day MA
        c1 = current_price > ma_150[-1] and current_price > ma_200[-1]

        # Criterion 2: 150-day MA > 200-day MA
        c2 = ma_150[-1] > ma_200[-1]

        # Criterion 3: 200-day MA trending up (higher than 1 month ago)
        ma_200_month_ago = ma_200[-22] if len(ma_200) > 22 else ma_200[0]
        c3 = ma_200[-1] > ma_200_month_ago

        # Criterion 4: 50 > 150 > 200 MA
        c4 = ma_50[-1] > ma_150[-1] and ma_150[-1] > ma_200[-1]

        # Criterion 5: Price > 50-day MA
        c5 = current_price > ma_50[-1]

        # Criterion 6: Price at least 30% above 52-week low
        c6 = current_price >= week_52_low * 1.30

        # Criterion 7: Price within 25% of 52-week high
        distance_from_high = (week_52_high - current_price) / week_52_high
        c7 = distance_from_high <= 0.25

        # Criterion 8: RS Rating >= 70 (requires market data - using proxy)
        # Proxy: Calculate price performance vs initial price
        rs_proxy = self._calculate_rs_proxy(close)
        c8 = rs_proxy >= self.min_rs_rating

        criteria = {
            '1_price_above_150_200ma': c1,
            '2_ma150_above_ma200': c2,
            '3_ma200_trending_up': c3,
            '4_ma_alignment_50_150_200': c4,
            '5_price_above_50ma': c5,
            '6_price_30pct_above_52w_low': c6,
            '7_price_within_25pct_52w_high': c7,
            '8_rs_rating_above_70': c8
        }

        score = sum(criteria.values())
        passes = score >= 7  # Must meet at least 7 of 8 criteria

        # Determine stage
        stage = self._determine_stage(
            current_price, ma_50[-1], ma_150[-1], ma_200[-1], close
        )

        details = {
            'current_price': current_price,
            'ma_50': ma_50[-1],
            'ma_150': ma_150[-1],
            'ma_200': ma_200[-1],
            '52_week_high': week_52_high,
            '52_week_low': week_52_low,
            'distance_from_high_pct': distance_from_high * 100,
            'distance_from_low_pct': ((current_price - week_52_low) / week_52_low) * 100,
            'rs_proxy': rs_proxy
        }

        return TrendTemplateResult(
            passes=passes,
            score=score,
            criteria=criteria,
            stage=stage,
            details=details
        )

    def analyze_vcp(self, ohlcv: pd.DataFrame) -> VCPAnalysis:
        """
        Analyze for Volatility Contraction Pattern (VCP)

        VCP Characteristics:
        - Series of price contractions (pullbacks) getting tighter
        - Each pullback is smaller than the previous (e.g., 20%, 12%, 8%, 4%)
        - Volume decreases during each contraction
        - Typically 3-6 contractions before breakout
        - Final contraction usually 5-15% or less
        - "T" formations (tight price action) near pivot

        Args:
            ohlcv: DataFrame with OHLCV data

        Returns:
            VCPAnalysis with pattern details
        """
        if len(ohlcv) < 100:
            return VCPAnalysis(
                is_vcp=False, num_contractions=0,
                contraction_sequence=[], final_contraction_pct=0,
                volume_declining=False, breakout_imminent=False,
                pivot_price=0
            )

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values
        volume = ohlcv['volume'].values

        # Find swing highs and lows
        pivots = self._find_pivots(high, low, close)

        if len(pivots) < 6:
            return VCPAnalysis(
                is_vcp=False, num_contractions=0,
                contraction_sequence=[], final_contraction_pct=0,
                volume_declining=False, breakout_imminent=False,
                pivot_price=close[-1]
            )

        # Identify contractions (high to low sequences)
        contractions = self._identify_contractions(pivots, high, low)

        if len(contractions) < 3:
            return VCPAnalysis(
                is_vcp=False, num_contractions=len(contractions),
                contraction_sequence=[c['decline_pct'] for c in contractions],
                final_contraction_pct=0,
                volume_declining=False, breakout_imminent=False,
                pivot_price=close[-1]
            )

        # Check if contractions are shrinking
        is_shrinking = self._check_shrinking_contractions(contractions)

        # Check volume pattern (should decline)
        volume_declining = self._check_volume_decline(volume, contractions)

        # Get final contraction size
        final_contraction_pct = contractions[-1]['decline_pct'] * 100

        # Check for tight price action (potential breakout)
        recent_range = (np.max(high[-10:]) - np.min(low[-10:])) / close[-1]
        breakout_imminent = recent_range < 0.05  # Less than 5% range

        # Determine pivot price (resistance to break)
        pivot_price = np.max(high[-30:])

        is_vcp = (
            len(contractions) >= 3 and
            is_shrinking and
            final_contraction_pct <= 15  # Last pullback < 15%
        )

        return VCPAnalysis(
            is_vcp=is_vcp,
            num_contractions=len(contractions),
            contraction_sequence=[c['decline_pct'] * 100 for c in contractions],
            final_contraction_pct=final_contraction_pct,
            volume_declining=volume_declining,
            breakout_imminent=breakout_imminent,
            pivot_price=pivot_price
        )

    def generate_sepa_signal(self,
                            ohlcv: pd.DataFrame,
                            symbol: str = 'UNKNOWN',
                            fundamental_score: Optional[float] = None) -> Optional[SEPASignal]:
        """
        Generate SEPA (Specific Entry Point Analysis) signal

        SEPA combines:
        1. Trend Template confirmation
        2. VCP or other setup pattern
        3. Precise entry point (breakout or pullback)
        4. Defined risk (stop loss)
        5. Risk/reward calculation

        Entry Types:
        - Breakout: Buy as stock breaks above pivot/resistance
        - Pullback: Buy on pullback to support (50-day MA)

        Args:
            ohlcv: DataFrame with OHLCV data
            symbol: Stock symbol
            fundamental_score: Optional fundamental rating (0-100)

        Returns:
            SEPASignal if valid setup exists, None otherwise
        """
        # Step 1: Check Trend Template
        trend_result = self.check_trend_template(ohlcv)

        if not trend_result.passes or trend_result.stage != Stage.STAGE_2_UPTREND:
            return None  # Must be in Stage 2 uptrend

        # Step 2: Analyze for VCP
        vcp = self.analyze_vcp(ohlcv)

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values

        current_price = close[-1]
        ma_50 = pd.Series(close).rolling(50).mean().values[-1]

        # Step 3: Determine entry type and price
        entry_type = None
        entry_price = None
        stop_loss = None

        # Breakout entry (VCP with tight action near pivot)
        if vcp.is_vcp and vcp.breakout_imminent:
            entry_type = 'breakout'
            entry_price = vcp.pivot_price * 1.001  # Just above pivot

            # Stop loss: Below recent low or 7-10% below entry
            recent_low = np.min(low[-20:])
            stop_loss_1 = recent_low * 0.98  # 2% below recent low
            stop_loss_2 = entry_price * 0.93  # 7% below entry
            stop_loss = max(stop_loss_1, stop_loss_2)

        # Pullback entry (to 50-day MA in uptrend)
        elif current_price <= ma_50 * 1.02 and current_price >= ma_50 * 0.98:
            # Price near 50-day MA
            entry_type = 'pullback'
            entry_price = current_price

            # Stop loss: Below 50-day MA or 7% below entry
            stop_loss = min(ma_50 * 0.97, entry_price * 0.93)

        if not entry_type:
            return None  # No valid entry setup

        # Step 4: Calculate risk and position size
        risk_per_share = entry_price - stop_loss
        risk_pct = risk_per_share / entry_price

        if risk_pct > self.max_stop_loss:
            return None  # Risk too high

        # Position sizing: Risk 1% of account
        risk_amount = self.account_size * self.risk_per_trade
        shares = int(risk_amount / risk_per_share)
        position_value = shares * entry_price
        position_size_pct = (position_value / self.account_size) * 100

        # Initial target: 4:1 risk/reward minimum
        initial_target = entry_price + (risk_per_share * 4)
        risk_reward_ratio = 4.0

        # Step 5: Calculate confidence score
        confidence = self._calculate_sepa_confidence(
            trend_result, vcp, entry_type, risk_pct, fundamental_score
        )

        # Generate entry reasons
        reasons = []
        reasons.append(f"Stage 2 uptrend (Trend Template: {trend_result.score}/8)")
        if vcp.is_vcp:
            reasons.append(f"VCP pattern: {vcp.num_contractions} contractions")
        if trend_result.details['rs_proxy'] >= 80:
            reasons.append(f"Strong RS rating: {trend_result.details['rs_proxy']:.0f}")
        if entry_type == 'breakout':
            reasons.append("Breakout above pivot point")
        else:
            reasons.append("Pullback to 50-day MA support")

        return SEPASignal(
            symbol=symbol,
            entry_price=entry_price,
            stop_loss=stop_loss,
            initial_target=initial_target,
            risk_reward_ratio=risk_reward_ratio,
            position_size_pct=position_size_pct,
            entry_type=entry_type,
            confidence=confidence,
            reasons=reasons
        )

    def calculate_position_size(self,
                               entry_price: float,
                               stop_loss: float,
                               account_size: Optional[float] = None) -> Dict[str, Any]:
        """
        Calculate position size using 1% risk rule

        Minervini's Rule: Never risk more than 1% of capital on a single trade

        Args:
            entry_price: Planned entry price
            stop_loss: Stop loss price
            account_size: Account size (uses self.account_size if None)

        Returns:
            Dict with shares, position_value, risk_amount, etc.
        """
        if account_size is None:
            account_size = self.account_size

        risk_per_share = entry_price - stop_loss
        risk_pct = (risk_per_share / entry_price) * 100

        # Calculate shares based on 1% risk
        risk_amount = account_size * self.risk_per_trade
        shares = int(risk_amount / risk_per_share)

        position_value = shares * entry_price
        position_pct = (position_value / account_size) * 100

        return {
            'shares': shares,
            'position_value': position_value,
            'position_pct': position_pct,
            'risk_per_share': risk_per_share,
            'risk_pct': risk_pct,
            'risk_amount': risk_amount,
            'max_loss': shares * risk_per_share
        }

    # === Helper Methods ===

    def _calculate_rs_proxy(self, close: np.ndarray) -> float:
        """
        Calculate relative strength proxy
        (In production, use actual RS rating from data provider)
        """
        if len(close) < 252:
            return 50

        # Calculate price performance over various periods
        perf_1m = (close[-1] / close[-22] - 1) * 100 if len(close) >= 22 else 0
        perf_3m = (close[-1] / close[-63] - 1) * 100 if len(close) >= 63 else 0
        perf_6m = (close[-1] / close[-126] - 1) * 100 if len(close) >= 126 else 0
        perf_12m = (close[-1] / close[-252] - 1) * 100 if len(close) >= 252 else 0

        # Weighted average (more weight on recent performance)
        rs = (perf_1m * 0.4 + perf_3m * 0.3 + perf_6m * 0.2 + perf_12m * 0.1)

        # Normalize to 0-100 scale (assuming market avg is 10% annual return)
        rs_normalized = min(100, max(0, 50 + rs))

        return rs_normalized

    def _determine_stage(self,
                        price: float,
                        ma_50: float,
                        ma_150: float,
                        ma_200: float,
                        close_history: np.ndarray) -> Stage:
        """Determine which stage the stock is in"""

        # Stage 2: Uptrend
        if (price > ma_50 > ma_150 > ma_200 and
            ma_200 > close_history[-30]):  # MA200 rising
            return Stage.STAGE_2_UPTREND

        # Stage 4: Downtrend
        if (price < ma_50 < ma_150 < ma_200):
            return Stage.STAGE_4_DOWNTREND

        # Stage 1: Basing (price oscillating around flat MA200)
        ma_200_flat = abs(ma_200 - close_history[-30]) / ma_200 < 0.02
        if ma_200_flat and abs(price - ma_200) / ma_200 < 0.10:
            return Stage.STAGE_1_BASING

        # Stage 3: Topping
        if price > ma_200 and ma_50 < ma_150:
            return Stage.STAGE_3_TOPPING

        return Stage.UNKNOWN

    def _find_pivots(self,
                    high: np.ndarray,
                    low: np.ndarray,
                    close: np.ndarray,
                    lookback: int = 5) -> List[Dict[str, Any]]:
        """Find swing high and low pivot points"""
        pivots = []

        for i in range(lookback, len(close) - lookback):
            # Swing high
            if high[i] == max(high[i-lookback:i+lookback+1]):
                pivots.append({
                    'index': i,
                    'price': high[i],
                    'type': 'high'
                })
            # Swing low
            elif low[i] == min(low[i-lookback:i+lookback+1]):
                pivots.append({
                    'index': i,
                    'price': low[i],
                    'type': 'low'
                })

        return pivots

    def _identify_contractions(self,
                              pivots: List[Dict[str, Any]],
                              high: np.ndarray,
                              low: np.ndarray) -> List[Dict[str, Any]]:
        """Identify contraction sequences (high-to-low pullbacks)"""
        contractions = []

        for i in range(len(pivots) - 1):
            if pivots[i]['type'] == 'high':
                # Find next low
                for j in range(i + 1, len(pivots)):
                    if pivots[j]['type'] == 'low':
                        high_price = pivots[i]['price']
                        low_price = pivots[j]['price']
                        decline_pct = (high_price - low_price) / high_price

                        if decline_pct > 0.03:  # At least 3% decline
                            contractions.append({
                                'high_idx': pivots[i]['index'],
                                'low_idx': pivots[j]['index'],
                                'high_price': high_price,
                                'low_price': low_price,
                                'decline_pct': decline_pct
                            })
                        break

        return contractions

    def _check_shrinking_contractions(self, contractions: List[Dict[str, Any]]) -> bool:
        """Check if contraction sizes are decreasing"""
        if len(contractions) < 2:
            return False

        for i in range(1, len(contractions)):
            if contractions[i]['decline_pct'] >= contractions[i-1]['decline_pct']:
                return False  # Not shrinking

        return True

    def _check_volume_decline(self,
                             volume: np.ndarray,
                             contractions: List[Dict[str, Any]]) -> bool:
        """Check if volume is declining during contractions"""
        if len(contractions) < 2:
            return False

        avg_volumes = []
        for c in contractions:
            start_idx = c['high_idx']
            end_idx = c['low_idx']
            avg_vol = np.mean(volume[start_idx:end_idx+1])
            avg_volumes.append(avg_vol)

        # Check if generally declining
        return avg_volumes[-1] < avg_volumes[0]

    def _calculate_sepa_confidence(self,
                                  trend_result: TrendTemplateResult,
                                  vcp: VCPAnalysis,
                                  entry_type: str,
                                  risk_pct: float,
                                  fundamental_score: Optional[float]) -> float:
        """Calculate confidence score for SEPA signal (0-100)"""
        score = 0.0

        # Trend Template score (0-40 points)
        score += (trend_result.score / 8.0) * 40

        # VCP quality (0-20 points)
        if vcp.is_vcp:
            score += 15
            if vcp.breakout_imminent:
                score += 5

        # Entry type (0-15 points)
        if entry_type == 'breakout':
            score += 15
        elif entry_type == 'pullback':
            score += 10

        # Risk (0-15 points)
        if risk_pct <= 0.05:  # 5% or less
            score += 15
        elif risk_pct <= 0.07:  # 7% or less
            score += 10
        elif risk_pct <= 0.10:  # 10% or less
            score += 5

        # Fundamentals (0-10 points) - if provided
        if fundamental_score is not None:
            score += (fundamental_score / 100) * 10
        else:
            score += 5  # Neutral if not provided

        return min(100, score)
