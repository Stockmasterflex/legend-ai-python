"""
William O'Neil Trading Strategy Implementation

Implements William O'Neil's CAN SLIM methodology:
1. CAN SLIM criteria (7-point system)
2. Cup & Handle pattern detection
3. Breakout identification with volume
4. Follow-Through Day (FTD) detection
5. Pivot point analysis

References:
- "How to Make Money in Stocks" (2009)
- IBD (Investor's Business Daily) methodology
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class MarketCondition(Enum):
    """Market direction states"""
    CONFIRMED_UPTREND = 1
    UPTREND_UNDER_PRESSURE = 2
    MARKET_CORRECTION = 3
    UNKNOWN = 0


@dataclass
class CANSLIMScore:
    """CAN SLIM criteria evaluation results"""
    passes: bool
    total_score: float  # 0-7
    criteria: Dict[str, bool]
    details: Dict[str, Any]
    recommendation: str


@dataclass
class CupHandlePattern:
    """Cup & Handle pattern details"""
    found: bool
    cup_depth_pct: float
    cup_length_bars: int
    handle_depth_pct: float
    pivot_price: float
    buy_point: float
    ideal_buy_zone_high: float  # Buy point + 5%
    is_valid: bool
    quality_score: float


@dataclass
class BreakoutSignal:
    """Breakout entry signal"""
    symbol: str
    buy_point: float
    stop_loss: float
    volume_surge_pct: float
    pattern_type: str  # 'cup_handle', 'flat_base', 'double_bottom', etc.
    market_condition: MarketCondition
    confidence: float
    reasons: List[str]


@dataclass
class FollowThroughDay:
    """Follow-Through Day analysis"""
    is_ftd: bool
    day_number: int  # Day of rally attempt
    index_gain_pct: float
    volume_vs_prior: float  # Volume increase vs prior day
    is_valid: bool
    details: str


class ONeilStrategy:
    """
    William O'Neil's CAN SLIM and IBD methodology

    Key Components:
    - CAN SLIM: 7 criteria for stock selection
    - Chart Patterns: Cup & Handle, Flat Base, etc.
    - Breakouts: 40-50%+ volume surge on breakout
    - Market Timing: Follow-Through Days
    - Risk Management: 7-8% stop losses
    """

    def __init__(self,
                 min_volume_surge: float = 0.40,  # 40% volume increase
                 max_stop_loss: float = 0.08,     # 8% max stop
                 min_rs_rating: float = 80):       # Min RS rating
        """
        Initialize O'Neil Strategy

        Args:
            min_volume_surge: Minimum volume increase for breakout (0.40 = 40%)
            max_stop_loss: Maximum stop loss percentage
            min_rs_rating: Minimum relative strength rating (0-100)
        """
        self.min_volume_surge = min_volume_surge
        self.max_stop_loss = max_stop_loss
        self.min_rs_rating = min_rs_rating

    def evaluate_canslim(self,
                        ohlcv: pd.DataFrame,
                        fundamentals: Optional[Dict[str, Any]] = None) -> CANSLIMScore:
        """
        Evaluate stock against CAN SLIM criteria

        C = Current quarterly earnings (up 25%+ YoY)
        A = Annual earnings growth (25%+ over 3 years)
        N = New (product, management, price high)
        S = Supply & Demand (shares outstanding, volume)
        L = Leader or Laggard (RS rating 80+)
        I = Institutional sponsorship
        M = Market direction (confirmed uptrend)

        Args:
            ohlcv: DataFrame with OHLCV data
            fundamentals: Optional dict with fundamental data

        Returns:
            CANSLIMScore with evaluation results
        """
        criteria = {}
        details = {}
        score = 0.0

        close = ohlcv['close'].values
        volume = ohlcv['volume'].values
        high = ohlcv['high'].values

        # C - Current Quarterly Earnings (requires fundamental data)
        if fundamentals and 'eps_growth_qoq' in fundamentals:
            c_earnings = fundamentals['eps_growth_qoq'] >= 25
            criteria['C_current_earnings'] = c_earnings
            details['eps_growth_qoq'] = fundamentals.get('eps_growth_qoq', 0)
            score += 1 if c_earnings else 0
        else:
            criteria['C_current_earnings'] = None
            details['eps_growth_qoq'] = 'N/A'

        # A - Annual Earnings Growth (requires fundamental data)
        if fundamentals and 'eps_growth_3yr' in fundamentals:
            a_annual = fundamentals['eps_growth_3yr'] >= 25
            criteria['A_annual_earnings'] = a_annual
            details['eps_growth_3yr'] = fundamentals.get('eps_growth_3yr', 0)
            score += 1 if a_annual else 0
        else:
            criteria['A_annual_earnings'] = None
            details['eps_growth_3yr'] = 'N/A'

        # N - New (check if stock is within 25% of 52-week high)
        if len(high) >= 252:
            week_52_high = np.max(high[-252:])
            current_price = close[-1]
            distance_from_high = (week_52_high - current_price) / week_52_high
            n_new = distance_from_high <= 0.25

            criteria['N_new_high'] = n_new
            details['distance_from_52w_high_pct'] = distance_from_high * 100
            score += 1 if n_new else 0
        else:
            criteria['N_new_high'] = False
            details['distance_from_52w_high_pct'] = 100

        # S - Supply & Demand (volume characteristics)
        avg_volume = np.mean(volume[-50:])
        recent_volume = np.mean(volume[-10:])
        volume_increasing = recent_volume > avg_volume * 1.1

        # Check for reasonable float (if provided)
        shares_outstanding = fundamentals.get('shares_outstanding', 0) if fundamentals else 0
        reasonable_float = True
        if shares_outstanding > 0:
            # Prefer < 25M shares for small-cap growth
            reasonable_float = shares_outstanding < 25_000_000 or shares_outstanding < 200_000_000

        s_supply = volume_increasing and reasonable_float
        criteria['S_supply_demand'] = s_supply
        details['avg_volume'] = avg_volume
        details['volume_increasing'] = volume_increasing
        details['shares_outstanding'] = shares_outstanding
        score += 1 if s_supply else 0

        # L - Leader or Laggard (RS Rating 80+)
        rs_rating = self._calculate_rs_rating(close)
        l_leader = rs_rating >= self.min_rs_rating

        criteria['L_leader'] = l_leader
        details['rs_rating'] = rs_rating
        score += 1 if l_leader else 0

        # I - Institutional Sponsorship (requires ownership data)
        if fundamentals and 'institutional_ownership_pct' in fundamentals:
            inst_own = fundamentals['institutional_ownership_pct']
            # Want increasing institutional ownership, but not excessive
            i_institutional = 10 <= inst_own <= 70
            criteria['I_institutional'] = i_institutional
            details['institutional_ownership_pct'] = inst_own
            score += 1 if i_institutional else 0
        else:
            criteria['I_institutional'] = None
            details['institutional_ownership_pct'] = 'N/A'

        # M - Market Direction (simplified - check major indices)
        # In practice, check S&P 500 or NASDAQ for FTD
        market_condition = self._assess_market_condition(ohlcv)
        m_market = market_condition == MarketCondition.CONFIRMED_UPTREND

        criteria['M_market_direction'] = m_market
        details['market_condition'] = market_condition.name
        score += 1 if m_market else 0

        # Determine if passes (need at least 5-6 of 7)
        known_criteria = sum(1 for v in criteria.values() if v is not None)
        passes = score >= max(5, known_criteria * 0.75)

        # Recommendation
        if score >= 6:
            recommendation = "STRONG BUY - Meets CAN SLIM criteria"
        elif score >= 5:
            recommendation = "BUY - Good CAN SLIM setup"
        elif score >= 4:
            recommendation = "HOLD - Partial CAN SLIM criteria met"
        else:
            recommendation = "AVOID - Does not meet CAN SLIM criteria"

        return CANSLIMScore(
            passes=passes,
            total_score=score,
            criteria=criteria,
            details=details,
            recommendation=recommendation
        )

    def detect_cup_and_handle(self, ohlcv: pd.DataFrame) -> CupHandlePattern:
        """
        Detect Cup & Handle pattern (O'Neil's most important pattern)

        Cup Criteria:
        - Prior uptrend of at least 30%
        - Cup depth: 12-33% (max 50% in bear market)
        - Cup length: 7-65 weeks (prefer 3-6 months)
        - Rounded bottom (U-shape, not V-shape)
        - Left and right sides at similar heights

        Handle Criteria:
        - Forms in upper half of cup
        - Depth: 8-12% (max 15%)
        - Length: 1-4 weeks minimum
        - Downward or sideways drift
        - Volume dries up in handle

        Args:
            ohlcv: DataFrame with OHLCV data

        Returns:
            CupHandlePattern with pattern details
        """
        if len(ohlcv) < 100:
            return CupHandlePattern(
                found=False, cup_depth_pct=0, cup_length_bars=0,
                handle_depth_pct=0, pivot_price=0, buy_point=0,
                ideal_buy_zone_high=0, is_valid=False, quality_score=0
            )

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values
        volume = ohlcv['volume'].values

        # Find potential cup (look for major low point)
        lookback = min(150, len(close) - 20)

        best_pattern = None
        best_score = 0

        for cup_bottom_idx in range(30, len(close) - 20):
            # Define cup region
            cup_start_idx = max(0, cup_bottom_idx - 60)

            # Find left peak (before cup)
            left_high_idx = cup_start_idx + np.argmax(high[cup_start_idx:cup_bottom_idx])
            left_peak = high[left_high_idx]

            # Cup bottom
            cup_low = low[cup_bottom_idx]

            # Calculate cup depth
            cup_depth_pct = (left_peak - cup_low) / left_peak * 100

            # Check if depth is reasonable (12-50%)
            if not (12 <= cup_depth_pct <= 50):
                continue

            # Find right peak (after cup)
            right_search_end = min(len(close), cup_bottom_idx + 50)
            right_high_idx = cup_bottom_idx + np.argmax(high[cup_bottom_idx:right_search_end])
            right_peak = high[right_high_idx]

            # Check if right side approaches left peak (within 5%)
            peak_diff_pct = abs(right_peak - left_peak) / left_peak * 100
            if peak_diff_pct > 5:
                continue

            # Cup length
            cup_length = right_high_idx - left_high_idx
            if cup_length < 30:  # At least 30 bars
                continue

            # Check for handle (pullback from right peak)
            handle_start_idx = right_high_idx
            handle_end_idx = min(len(close) - 1, handle_start_idx + 20)

            if handle_end_idx <= handle_start_idx + 5:
                continue  # Handle too short

            handle_low = np.min(low[handle_start_idx:handle_end_idx+1])
            handle_depth_pct = (right_peak - handle_low) / right_peak * 100

            # Handle should be shallow (8-15%)
            if not (3 <= handle_depth_pct <= 15):
                continue

            # Handle should be in upper half of cup
            cup_midpoint = (left_peak + cup_low) / 2
            if handle_low < cup_midpoint:
                continue

            # Check volume dry-up in handle
            handle_volume = np.mean(volume[handle_start_idx:handle_end_idx+1])
            prior_volume = np.mean(volume[max(0, handle_start_idx-20):handle_start_idx])
            volume_dryup = handle_volume < prior_volume * 0.8

            # Calculate quality score
            quality_score = self._score_cup_handle(
                cup_depth_pct, handle_depth_pct, cup_length, volume_dryup
            )

            if quality_score > best_score:
                best_score = quality_score

                # Buy point is just above right peak
                buy_point = right_peak * 1.001
                ideal_buy_zone_high = buy_point * 1.05  # Within 5% of buy point

                best_pattern = CupHandlePattern(
                    found=True,
                    cup_depth_pct=cup_depth_pct,
                    cup_length_bars=cup_length,
                    handle_depth_pct=handle_depth_pct,
                    pivot_price=right_peak,
                    buy_point=buy_point,
                    ideal_buy_zone_high=ideal_buy_zone_high,
                    is_valid=quality_score >= 60,
                    quality_score=quality_score
                )

        if best_pattern:
            return best_pattern

        return CupHandlePattern(
            found=False, cup_depth_pct=0, cup_length_bars=0,
            handle_depth_pct=0, pivot_price=0, buy_point=0,
            ideal_buy_zone_high=0, is_valid=False, quality_score=0
        )

    def identify_breakout(self,
                         ohlcv: pd.DataFrame,
                         symbol: str = 'UNKNOWN') -> Optional[BreakoutSignal]:
        """
        Identify valid breakout with O'Neil's criteria

        Breakout Rules:
        - Break above pivot point (resistance)
        - Volume surge: 40-50%+ above average
        - Close in upper portion of day's range
        - Market in confirmed uptrend (ideally)
        - Buy within 5% of buy point

        Args:
            ohlcv: DataFrame with OHLCV data
            symbol: Stock symbol

        Returns:
            BreakoutSignal if valid breakout exists
        """
        if len(ohlcv) < 100:
            return None

        close = ohlcv['close'].values
        high = ohlcv['high'].values
        low = ohlcv['low'].values
        volume = ohlcv['volume'].values

        current_price = close[-1]
        current_volume = volume[-1]

        # Check for cup & handle
        cup_handle = self.detect_cup_and_handle(ohlcv)

        if cup_handle.found and cup_handle.is_valid:
            # Check if breaking out
            buy_point = cup_handle.buy_point

            # Check if price is at or near buy point
            if current_price >= buy_point * 0.99:
                # Check volume surge
                avg_volume_50 = np.mean(volume[-50:-1])
                volume_surge_pct = (current_volume / avg_volume_50 - 1) * 100

                if volume_surge_pct >= self.min_volume_surge * 100:
                    # Valid breakout!

                    # Stop loss: 7-8% below buy point
                    stop_loss = buy_point * 0.93

                    # Market condition
                    market_condition = self._assess_market_condition(ohlcv)

                    # Confidence score
                    confidence = self._calculate_breakout_confidence(
                        cup_handle.quality_score,
                        volume_surge_pct,
                        market_condition
                    )

                    reasons = [
                        f"Cup & Handle breakout (quality: {cup_handle.quality_score:.0f})",
                        f"Volume surge: +{volume_surge_pct:.0f}% vs average",
                        f"Buy point: ${buy_point:.2f}",
                        f"Market: {market_condition.name}"
                    ]

                    return BreakoutSignal(
                        symbol=symbol,
                        buy_point=buy_point,
                        stop_loss=stop_loss,
                        volume_surge_pct=volume_surge_pct,
                        pattern_type='cup_handle',
                        market_condition=market_condition,
                        confidence=confidence,
                        reasons=reasons
                    )

        # Check for other patterns (flat base, double bottom, etc.)
        # For now, return None if no cup & handle breakout
        return None

    def detect_follow_through_day(self, index_ohlcv: pd.DataFrame) -> FollowThroughDay:
        """
        Detect Follow-Through Day (FTD) - market bottom signal

        FTD Criteria:
        - Occurs on day 4-7 (or up to day 12) of rally attempt
        - Major index (S&P 500, NASDAQ) gains 1.25%+ (some say 1.7%+)
        - Volume higher than previous day
        - Preferably higher than 50-day average volume
        - Should not undercut rally-attempt day low afterward

        Args:
            index_ohlcv: DataFrame with major index OHLCV data

        Returns:
            FollowThroughDay analysis
        """
        if len(index_ohlcv) < 20:
            return FollowThroughDay(
                is_ftd=False, day_number=0, index_gain_pct=0,
                volume_vs_prior=0, is_valid=False,
                details="Insufficient data"
            )

        close = index_ohlcv['close'].values
        volume = index_ohlcv['volume'].values
        low = index_ohlcv['low'].values

        # Find rally attempt start (lowest low in recent period)
        lookback = min(30, len(close) - 10)
        rally_start_idx = len(close) - lookback + np.argmin(low[-lookback:-3])

        # Check days 4-12 after rally start
        for day in range(4, min(13, len(close) - rally_start_idx)):
            idx = rally_start_idx + day

            if idx >= len(close):
                break

            # Calculate gain from prior day
            gain_pct = (close[idx] / close[idx-1] - 1) * 100

            # Calculate volume vs prior day
            volume_vs_prior = volume[idx] / volume[idx-1] if volume[idx-1] > 0 else 1

            # Check criteria
            strong_gain = gain_pct >= 1.25
            volume_higher = volume_vs_prior >= 1.0

            # Check if volume is above 50-day average
            avg_volume = np.mean(volume[max(0, idx-50):idx])
            volume_above_avg = volume[idx] > avg_volume

            if strong_gain and volume_higher:
                # Check if rally low has been undercut
                rally_low = low[rally_start_idx]
                undercut = np.any(low[idx:] < rally_low) if idx < len(low) - 1 else False

                is_valid = not undercut and volume_above_avg

                return FollowThroughDay(
                    is_ftd=True,
                    day_number=day,
                    index_gain_pct=gain_pct,
                    volume_vs_prior=volume_vs_prior,
                    is_valid=is_valid,
                    details=f"Day {day} FTD: +{gain_pct:.2f}% on {volume_vs_prior:.0%} volume"
                )

        return FollowThroughDay(
            is_ftd=False, day_number=0, index_gain_pct=0,
            volume_vs_prior=0, is_valid=False,
            details="No FTD detected in recent rally attempt"
        )

    # === Helper Methods ===

    def _calculate_rs_rating(self, close: np.ndarray) -> float:
        """
        Calculate RS (Relative Strength) rating similar to IBD
        Compares price performance to market
        """
        if len(close) < 252:
            return 50

        # Calculate performance over multiple periods
        perf_qtrs = [
            (close[-1] / close[-63] - 1) * 100 if len(close) >= 63 else 0,   # 3m
            (close[-1] / close[-126] - 1) * 100 if len(close) >= 126 else 0,  # 6m
            (close[-1] / close[-189] - 1) * 100 if len(close) >= 189 else 0,  # 9m
            (close[-1] / close[-252] - 1) * 100 if len(close) >= 252 else 0   # 12m
        ]

        # Weighted: 40% recent quarter, 20% each for others
        weighted_perf = (
            perf_qtrs[0] * 0.40 +
            perf_qtrs[1] * 0.20 +
            perf_qtrs[2] * 0.20 +
            perf_qtrs[3] * 0.20
        )

        # Normalize to 0-100 (assume market average ~10% annual)
        rs_rating = min(100, max(0, 50 + weighted_perf * 2))

        return rs_rating

    def _assess_market_condition(self, ohlcv: pd.DataFrame) -> MarketCondition:
        """Assess overall market condition (simplified)"""
        if len(ohlcv) < 50:
            return MarketCondition.UNKNOWN

        close = ohlcv['close'].values
        ma_50 = pd.Series(close).rolling(50).mean().values

        current_price = close[-1]

        # Simple check: price vs 50-day MA
        if current_price > ma_50[-1] * 1.02:
            return MarketCondition.CONFIRMED_UPTREND
        elif current_price > ma_50[-1] * 0.98:
            return MarketCondition.UPTREND_UNDER_PRESSURE
        else:
            return MarketCondition.MARKET_CORRECTION

    def _score_cup_handle(self,
                         cup_depth: float,
                         handle_depth: float,
                         cup_length: int,
                         volume_dryup: bool) -> float:
        """Score cup & handle pattern quality (0-100)"""
        score = 0.0

        # Cup depth score (ideal: 15-33%)
        if 15 <= cup_depth <= 33:
            score += 30
        elif 12 <= cup_depth <= 40:
            score += 20
        else:
            score += 10

        # Handle depth score (ideal: 8-12%)
        if 8 <= handle_depth <= 12:
            score += 30
        elif 5 <= handle_depth <= 15:
            score += 20
        else:
            score += 10

        # Cup length score (ideal: 30-150 bars)
        if 30 <= cup_length <= 150:
            score += 20
        elif 20 <= cup_length <= 200:
            score += 15
        else:
            score += 5

        # Volume dry-up
        if volume_dryup:
            score += 20
        else:
            score += 5

        return score

    def _calculate_breakout_confidence(self,
                                      pattern_quality: float,
                                      volume_surge: float,
                                      market_condition: MarketCondition) -> float:
        """Calculate breakout confidence (0-100)"""
        confidence = 0.0

        # Pattern quality (0-40 points)
        confidence += (pattern_quality / 100) * 40

        # Volume surge (0-30 points)
        if volume_surge >= 100:  # 100%+ surge
            confidence += 30
        elif volume_surge >= 50:  # 50%+ surge
            confidence += 25
        elif volume_surge >= 40:  # 40%+ surge
            confidence += 20
        else:
            confidence += 10

        # Market condition (0-30 points)
        if market_condition == MarketCondition.CONFIRMED_UPTREND:
            confidence += 30
        elif market_condition == MarketCondition.UPTREND_UNDER_PRESSURE:
            confidence += 15
        else:
            confidence += 5

        return min(100, confidence)
