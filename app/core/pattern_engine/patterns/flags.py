"""
Flag and Pennant Pattern Detection

Includes:
- High Tight Flag (HTF) - Explosive breakout pattern
- Bull Flags - Bullish continuation
- Bear Flags - Bearish continuation  
- Pennants - Symmetrical consolidation

Ported from FindPatterns.cs
"""
import numpy as np
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


def find_ht_flag(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    dates: Optional[np.ndarray] = None,
    helpers: Any = None,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Find High Tight Flag (HTF) patterns.
    
    This is one of the most explosive breakout patterns - occurs when a stock
    rallies 90%+ in a very short time (typically 2-8 weeks).
    
    Ported from FindPatterns.cs lines 6281-6358
    
    Pattern Recognition:
    1. Find a period with 90%+ price gain
    2. Gain must occur within ~2 months (varies by timeframe)
    3. Track from lowest low to highest high in window
    4. Pattern confirmed when breakout occurs
    
    Args:
        open_: Open prices
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        dates: Date array (optional, for timeframe validation)
        helpers: PatternHelpers instance
        strict: Use strict rules
        
    Returns:
        List of detected HTF patterns
    """
    patterns = []
    
    # Determine window size based on data characteristics
    # Daily: 42 bars (~2 months), Weekly: 8 bars, Intraday: 2 bars
    if len(close) < 10:
        return patterns
    
    # Estimate timeframe from data density
    window_size = 42  # Default to daily
    if len(close) > 1000:  # Likely intraday
        window_size = 2
    elif len(close) > 500:  # Likely weekly
        window_size = 8
    
    # Don't exceed available data
    if len(close) < window_size:
        window_size = len(close)
    
    # Scan through price data
    for i in range(len(close)):
        lowest_idx = -1
        highest_idx = -1
        
        # Calculate end of search window
        end_idx = min(i + window_size, len(close) - 1)
        
        # Track lowest low in current window
        for j in range(i, end_idx + 1):
            if lowest_idx == -1:
                lowest_idx = j
                highest_idx = j
            
            # Reset if we find a new low or invalid data
            if (low[j] <= low[lowest_idx] and low[j] > 0) or low[lowest_idx] == 0:
                lowest_idx = j
                highest_idx = j
                # Reset window from this point
                end_idx = min(j + window_size, len(close) - 1)
            
            # Track highest high
            if high[j] > high[highest_idx]:
                highest_idx = j
            
            # Check if we have invalid data or insufficient gain
            if low[lowest_idx] == 0:
                continue
            
            gain_pct = (high[highest_idx] - low[lowest_idx]) / low[lowest_idx]
            
            # HTF requirement: 90%+ gain
            if gain_pct < 0.90:
                continue
            
            # Check if still breaking to new highs
            if j + 1 <= len(high) - 1 and high[j + 1] > high[highest_idx]:
                continue
            
            # Validate timeframe if dates provided
            if dates is not None and len(dates) > highest_idx:
                # HTF should complete within ~2 months (60 days)
                try:
                    days_elapsed = (dates[highest_idx] - dates[lowest_idx]).days
                    if days_elapsed > 60:
                        continue
                except (AttributeError, TypeError):
                    # If date calculation fails, continue without date check
                    pass
            
            # Pattern confirmed!
            width = highest_idx - lowest_idx
            pattern_height = float(high[highest_idx] - low[lowest_idx])
            current_price = float(close[-1])
            
            # Entry: at highest high (breakout point) - NO BUFFER
            # Patternz: Entry = high[highest_idx] exactly
            entry = float(high[highest_idx])
            
            # Stop: Below midpoint of flag (50% retracement)
            # Patternz: Stop = low + (height * 0.5)
            midpoint = low[lowest_idx] + pattern_height * 0.5
            stop = float(midpoint)
            
            # Target: Measure move (100% extension)
            # Patternz: Target = entry + height
            target = entry + pattern_height
            
            # Risk/Reward
            risk = entry - stop
            reward = target - entry
            risk_reward = reward / risk if risk > 0 else 0
            
            # Confidence - HTF is high confidence when complete
            confidence = 0.85
            
            # Bonus: faster = stronger
            if width <= window_size // 2:
                confidence += 0.1
            
            # Bonus: explosive gain
            if gain_pct > 1.5:  # 150%+
                confidence += 0.05
            
            confidence = min(confidence, 1.0)
            score = confidence * 10
            
            patterns.append({
                'pattern': 'High Tight Flag',
                'type': 'HTF',
                'confidence': confidence,
                'score': score,
                'entry': entry,
                'stop': stop,
                'target': target,
                'risk_reward': risk_reward,
                'width': width,
                'height': pattern_height,
                'current_price': current_price,
                'confirmed': True,
                'metadata': {
                    'start': int(lowest_idx),
                    'end': int(highest_idx),
                    'gain_pct': float(gain_pct),
                    'start_price': float(low[lowest_idx]),
                    'end_price': float(high[highest_idx]),
                }
            })
            
            # Jump ahead to avoid overlapping patterns
            i = highest_idx
            break
    
    return patterns


def find_flags(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Find Bull and Bear Flag patterns.
    
    Ported from FindPatterns.cs lines 5307-5403
    
    Pattern Recognition:
    1. Identify strong directional move (flagpole)
    2. Find consolidation/correction (flag)
    3. Flag must not retrace too much of pole
    4. Validate flag shape with helpers
    
    Bull Flag: Up move -> tight consolidation -> breakout up
    Bear Flag: Down move -> tight consolidation -> breakdown
    
    Args:
        open_: Open prices
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        helpers: PatternHelpers instance
        strict: Use strict rules
        
    Returns:
        List of detected flag patterns (both bull and bear)
    """
    patterns = []
    
    # Tolerance for flag consolidation
    # Strict: 7.5%, Loose: 15%
    tolerance = 0.075 if strict else 0.15
    
    # Scan for consecutive price movements
    for i in range(1, len(close)):
        # Check for bullish or bearish trend start
        trend_direction = 0
        
        # Bullish start: both high and low move up
        if high[i - 1] < high[i] and low[i - 1] < low[i]:
            trend_direction = 1
        # Bearish start: both high and low move down  
        elif high[i - 1] > high[i] and low[i - 1] > low[i]:
            trend_direction = -1
        else:
            continue
        
        # Find extent of trend (flagpole)
        pole_end = i
        
        if trend_direction == 1:
            # Continue while uptrend persists
            for j in range(i, len(close)):
                if high[j - 1] < high[j] and low[j - 1] < low[j]:
                    pole_end = j
                else:
                    break
        else:
            # Continue while downtrend persists
            for j in range(i, len(close)):
                if high[j - 1] > high[j] and low[j - 1] > low[j]:
                    pole_end = j
                else:
                    break
        
        # Need at least 3 bars for pole
        pole_width = pole_end - i + 1
        if pole_width < 3:
            continue
        
        pole_start = i - 1
        
        if trend_direction == 1:
            # Bull flag: check consolidation doesn't gap up too much
            max_gap = 0.0
            for j in range(i, pole_end + 1):
                if low[j] > high[j - 1]:
                    gap = low[j] - high[j - 1]
                    if gap > max_gap:
                        max_gap = gap
            
            pole_height = high[pole_end] - low[pole_start]
            if pole_height <= 0:
                continue
            
            # Flag must be tight (gaps < tolerance of pole)
            if max_gap / pole_height >= tolerance:
                continue
            
            # Find flag consolidation portion
            flag_end = _find_flag_portion(
                high, low, pole_start, pole_end, trend_direction, helpers
            )
            
            if flag_end != -1:
                width = flag_end - pole_start
                current_price = float(close[-1])
                
                # Entry: breakout above flag high
                entry = float(high[pole_end])
                
                # Stop: below flag low
                stop = float(low[pole_end])
                
                # Target: pole height projected from breakout
                target = entry + pole_height
                
                # Risk/Reward
                risk = entry - stop
                reward = target - entry
                risk_reward = reward / risk if risk > 0 else 0
                
                # Confidence
                confidence = 0.75
                if pole_width >= 5:
                    confidence += 0.05  # Strong pole
                if max_gap / pole_height < tolerance / 2:
                    confidence += 0.1  # Very tight flag
                
                confidence = min(confidence, 1.0)
                score = confidence * 10
                
                patterns.append({
                    'pattern': 'Bull Flag',
                    'type': 'Flag',
                    'confidence': confidence,
                    'score': score,
                    'entry': entry,
                    'stop': stop,
                    'target': target,
                    'risk_reward': risk_reward,
                    'width': width,
                    'height': pole_height,
                    'current_price': current_price,
                    'confirmed': flag_end >= len(close) - 5,
                    'metadata': {
                        'pole_start': int(pole_start),
                        'pole_end': int(pole_end),
                        'flag_end': int(flag_end),
                        'direction': 'bullish',
                    }
                })
        
        else:
            # Bear flag: check consolidation doesn't gap down too much
            max_gap = 0.0
            for j in range(i, pole_end + 1):
                if high[j] < low[j - 1]:
                    gap = low[j - 1] - high[j]
                    if gap > max_gap:
                        max_gap = gap
            
            pole_height = high[pole_start] - low[pole_end]
            if pole_height <= 0:
                continue
            
            if max_gap / pole_height >= tolerance:
                continue
            
            # Find flag consolidation
            flag_end = _find_flag_portion(
                high, low, pole_start, pole_end, trend_direction, helpers
            )
            
            if flag_end != -1:
                width = flag_end - pole_start
                current_price = float(close[-1])
                
                # Entry: breakdown below flag low
                entry = float(low[pole_end])
                
                # Stop: above flag high
                stop = float(high[pole_end])
                
                # Target: pole height projected from breakdown
                target = entry - pole_height
                
                # Risk/Reward
                risk = stop - entry
                reward = entry - target
                risk_reward = reward / risk if risk > 0 else 0
                
                # Confidence
                confidence = 0.75
                if pole_width >= 5:
                    confidence += 0.05
                if max_gap / pole_height < tolerance / 2:
                    confidence += 0.1
                
                confidence = min(confidence, 1.0)
                score = confidence * 10
                
                patterns.append({
                    'pattern': 'Bear Flag',
                    'type': 'Flag',
                    'confidence': confidence,
                    'score': score,
                    'entry': entry,
                    'stop': stop,
                    'target': target,
                    'risk_reward': risk_reward,
                    'width': width,
                    'height': pole_height,
                    'current_price': current_price,
                    'confirmed': flag_end >= len(close) - 5,
                    'metadata': {
                        'pole_start': int(pole_start),
                        'pole_end': int(pole_end),
                        'flag_end': int(flag_end),
                        'direction': 'bearish',
                    }
                })
    
    return patterns


def _find_flag_portion(
    high: np.ndarray,
    low: np.ndarray,
    pole_start: int,
    pole_end: int,
    direction: int,
    helpers: Any
) -> int:
    """
    Find the consolidation portion after the flagpole.
    
    Returns the end index of the flag, or -1 if no valid flag found.
    """
    # Find tops and bottoms in the flag region
    tops = helpers.find_all_tops(high, start_idx=pole_end, trade_days=2)
    bottoms = helpers.find_all_bottoms(low, start_idx=pole_end, trade_days=2)
    
    if len(tops) < 2 or len(bottoms) < 2:
        return -1
    
    # Look for consolidation after pole
    # Flag should have at least 2 swings within narrow range
    flag_end = min(pole_end + 20, len(high) - 1)
    
    # Simple validation: check if we have alternating tops/bottoms
    if len(tops) >= 2 and len(bottoms) >= 2:
        # Ensure consolidation is tight
        flag_high = np.max(high[pole_end:flag_end+1])
        flag_low = np.min(low[pole_end:flag_end+1])
        flag_range = flag_high - flag_low
        
        pole_height = high[pole_end] - low[pole_start] if direction == 1 else high[pole_start] - low[pole_end]
        
        # Flag range should be < 50% of pole height
        if flag_range < pole_height * 0.5:
            return flag_end
    
    return -1


def find_pennants(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Find Pennant patterns (symmetrical triangular consolidation).
    
    Ported from FindPatterns.cs lines 6909-7036
    
    Pattern Recognition:
    1. Identify converging trendlines (symmetrical triangle)
    2. Must occur after strong directional move
    3. Converging highs and lows within specific timeframe
    4. Breakout expected in direction of prior trend
    
    Args:
        open_: Open prices
        high: High prices  
        low: Low prices
        close: Close prices
        volume: Volume data
        helpers: PatternHelpers instance
        strict: Use strict rules
        
    Returns:
        List of detected pennant patterns
    """
    patterns = []
    
    # Find all peaks and troughs
    bottoms = helpers.find_all_bottoms(low, trade_days=2)
    if len(bottoms) == 0:
        return patterns
    
    tops = helpers.find_all_tops(high, trade_days=2)
    if len(tops) == 0:
        return patterns
    
    # Scan for pennant formations
    for i in range(len(close) - 20):
        # Look ahead 20+ bars for pennant
        min_end = i + 3
        max_end = min(i + 20, len(close) - 1)
        
        for j in range(max_end, min_end - 1, -1):
            # Check if this forms a pennant shape
            if _is_pennant_shape(i, j, high, low):
                continue
            
            # Also check midpoint
            mid = int(i + (j - i) / 2)
            if _is_pennant_shape(mid, j, high, low):
                continue
            
            # Find the trend before pennant
            trend_start = _find_pennant_trend(i, j, bottoms, tops, high, low)
            
            if trend_start != 0:
                width = j - i
                pole_height = abs(high[i] - low[trend_start]) if trend_start < i else abs(high[trend_start] - low[i])
                current_price = float(close[-1])
                
                # Determine direction
                is_bullish = high[i] > high[trend_start] if trend_start < i else False
                
                if is_bullish:
                    entry = float(high[j])
                    stop = float(low[j])
                    target = entry + pole_height
                else:
                    entry = float(low[j])
                    stop = float(high[j])
                    target = entry - pole_height
                
                # Risk/Reward
                risk = abs(entry - stop)
                reward = abs(target - entry)
                risk_reward = reward / risk if risk > 0 else 0
                
                # Confidence
                confidence = 0.7
                if width >= 10:
                    confidence += 0.1
                
                confidence = min(confidence, 1.0)
                score = confidence * 10
                
                patterns.append({
                    'pattern': 'Pennant',
                    'type': 'PEN',
                    'confidence': confidence,
                    'score': score,
                    'entry': entry,
                    'stop': stop,
                    'target': target,
                    'risk_reward': risk_reward,
                    'width': width,
                    'height': pole_height,
                    'current_price': current_price,
                    'confirmed': j >= len(close) - 5,
                    'metadata': {
                        'trend_start': int(trend_start),
                        'pennant_start': int(i),
                        'pennant_end': int(j),
                        'direction': 'bullish' if is_bullish else 'bearish',
                    }
                })
                
                break
    
    return patterns


def _is_pennant_shape(start: int, end: int, high: np.ndarray, low: np.ndarray) -> bool:
    """
    Check if the price action forms a pennant (converging triangle).
    Returns False if it's a valid pennant, True if it breaks the pennant shape.
    """
    start_high = high[start]
    start_low = low[start]
    
    # Pennant should have converging highs and lows
    for i in range(start + 1, end + 1):
        # If price breaks above start high or below start low, not a pennant
        if high[i] >= start_high:
            return True
        if low[i] <= start_low:
            return True
    
    return False


def _find_pennant_trend(
    start: int,
    end: int,
    bottoms: np.ndarray,
    tops: np.ndarray,
    high: np.ndarray,
    low: np.ndarray
) -> int:
    """
    Find the prior trend that led to the pennant.
    Returns the index where the trend started, or 0 if no valid trend.
    """
    # Find highest and lowest points in pennant
    highest_idx = start
    lowest_idx = start
    
    for k in range(start + 1, end + 1):
        if high[k] > high[highest_idx]:
            highest_idx = k
        if low[k] < low[lowest_idx]:
            lowest_idx = k
    
    # Pennant range should be significant
    pennant_range = high[highest_idx] - low[lowest_idx]
    required_pole = pennant_range * 3  # Pole should be 3x pennant range
    
    # Look for prior trend in bottoms (bullish setup)
    for i in range(1, len(bottoms) - 1):
        bottom_idx = bottoms[i]
        
        # Find corresponding top
        for j in range(1, len(tops) - 1):
            top_idx = tops[j]
            
            # Check if this creates a valid pole
            if high[top_idx] <= low[bottom_idx]:
                continue
            
            # Top before bottom (bullish pole)
            if top_idx < bottom_idx:
                if bottom_idx != start and bottom_idx != start - 1:
                    continue
                
                # Check pole strength
                pole_height = high[top_idx] - low[bottom_idx]
                if pole_height >= required_pole:
                    return top_idx
    
    return 0

