"""
Wedge Pattern Detection

Includes:
- Rising Wedge (bearish reversal/continuation)
- Falling Wedge (bullish reversal/continuation)

Wedges are characterized by converging trendlines with both sloping
in the same direction, unlike triangles where they slope in opposite directions.

Ported from FindPatterns.cs lines 9356-9474
"""
import numpy as np
from typing import List, Dict, Any, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def find_wedges(
    open_: np.ndarray,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    volume: np.ndarray,
    helpers: Any,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Find both Rising and Falling Wedge patterns.
    
    Ported from FindPatterns.cs lines 9356-9474
    
    Pattern Recognition:
    1. Find two converging trendlines
    2. Both trendlines slope in same direction (up = rising, down = falling)
    3. Upper and lower lines must converge (get closer together)
    4. Validate wedge geometry and breakout direction
    
    Rising Wedge: Both lines slope up, typically bearish
    Falling Wedge: Both lines slope down, typically bullish
    
    Args:
        open_: Open prices
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        helpers: PatternHelpers instance
        strict: Use strict rules
        
    Returns:
        List of detected wedge patterns (both rising and falling)
    """
    patterns = []
    
    # Find rising wedges (Flag=92)
    rising_wedges = _find_wedge_type(
        high, low, close, helpers,
        wedge_type='rising',
        strict=strict
    )
    patterns.extend(rising_wedges)
    
    # Find falling wedges (Flag=96)
    falling_wedges = _find_wedge_type(
        high, low, close, helpers,
        wedge_type='falling',
        strict=strict
    )
    patterns.extend(falling_wedges)
    
    return patterns


def _find_wedge_type(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    helpers: Any,
    wedge_type: str,
    strict: bool
) -> List[Dict[str, Any]]:
    """
    Find wedges of a specific type (rising or falling).
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        helpers: PatternHelpers instance
        wedge_type: 'rising' or 'falling'
        strict: Use strict rules
        
    Returns:
        List of detected wedges
    """
    patterns = []
    
    # Slope tolerance
    # Strict: 6%, Loose: 1%
    min_slope = 0.06 if strict else 0.01
    
    # Direction: 1 for rising, -1 for falling
    direction = 1 if wedge_type == 'rising' else -1
    
    # Find trendlines on lows (support)
    lower_trendlines = _find_trendlines(
        low, high, helpers,
        line_type='support',
        direction=direction,
        min_slope=min_slope
    )
    
    if len(lower_trendlines) == 0:
        return patterns
    
    # Find trendlines on highs (resistance)
    upper_trendlines = _find_trendlines(
        low, high, helpers,
        line_type='resistance',
        direction=direction,
        min_slope=min_slope
    )
    
    if len(upper_trendlines) == 0:
        return patterns
    
    # Match upper and lower trendlines to form wedges
    for lower_tl in lower_trendlines:
        lower_start, lower_end, lower_slope = lower_tl
        
        for upper_tl in upper_trendlines:
            upper_start, upper_end, upper_slope = upper_tl
            
            # Verify both lines slope in same direction with minimum slope
            if wedge_type == 'rising':
                if upper_slope < 0.01 or lower_slope < 0.01:
                    continue
            else:
                if upper_slope > -min_slope or lower_slope > -min_slope:
                    continue
            
            # Calculate overlapping period
            wedge_start = max(lower_start, upper_start)
            wedge_end = min(lower_end, upper_end)
            
            # Wedge must have meaningful duration
            if wedge_end - wedge_start < 10:
                continue
            
            # Check if lines are converging
            if not _verify_convergence(
                lower_start, lower_end, upper_start, upper_end,
                lower_slope, upper_slope, direction
            ):
                continue
            
            # Validate wedge geometry
            if not _verify_wedge_geometry(
                wedge_start, wedge_end,
                lower_start, lower_end,
                upper_start, upper_end,
                high, low
            ):
                continue
            
            # Wedge confirmed!
            width = wedge_end - wedge_start
            pattern_height = float(np.max(high[wedge_start:wedge_end+1]) - np.min(low[wedge_start:wedge_end+1]))
            current_price = float(close[-1])
            
            # Entry and targets depend on wedge type
            if wedge_type == 'rising':
                # Rising wedge: bearish breakout expected (downward)
                entry = float(low[wedge_end])  # Break below support
                stop = float(high[wedge_end])  # Stop above resistance
                target = entry - pattern_height  # Target: full height downward
                
                pattern_name = 'Rising Wedge (Bearish)'
                
            else:
                # Falling wedge: bullish breakout expected (upward)
                entry = float(high[wedge_end])  # Break above resistance
                stop = float(low[wedge_end])  # Stop below support
                target = entry + pattern_height  # Target: full height upward
                
                pattern_name = 'Falling Wedge (Bullish)'
            
            # Risk/Reward
            risk = abs(entry - stop)
            reward = abs(target - entry)
            risk_reward = reward / risk if risk > 0 else 0
            
            # Confidence scoring
            confidence = 0.75
            
            # Bonus: longer wedge = more reliable
            if width > 20:
                confidence += 0.05
            
            # Bonus: strong convergence
            slope_ratio = abs(upper_slope / lower_slope) if lower_slope != 0 else 1
            if 0.8 < slope_ratio < 1.2:  # Similar slopes = better convergence
                confidence += 0.1
            
            # Bonus: good risk/reward
            if risk_reward > 2:
                confidence += 0.05
            
            confidence = min(confidence, 1.0)
            score = confidence * 10
            
            patterns.append({
                'pattern': pattern_name,
                'type': 'RW' if wedge_type == 'rising' else 'FW',
                'confidence': confidence,
                'score': score,
                'entry': entry,
                'stop': stop,
                'target': target,
                'risk_reward': risk_reward,
                'width': width,
                'height': pattern_height,
                'current_price': current_price,
                'confirmed': wedge_end >= len(close) - 5,
                'metadata': {
                    'wedge_start': int(wedge_start),
                    'wedge_end': int(wedge_end),
                    'lower_start': int(lower_start),
                    'lower_end': int(lower_end),
                    'upper_start': int(upper_start),
                    'upper_end': int(upper_end),
                    'lower_slope': float(lower_slope),
                    'upper_slope': float(upper_slope),
                    'direction': wedge_type,
                }
            })
    
    return patterns


def _find_trendlines(
    primary: np.ndarray,
    secondary: np.ndarray,
    helpers: Any,
    line_type: str,
    direction: int,
    min_slope: float
) -> List[Tuple[int, int, float]]:
    """
    Find trendlines in the data.
    
    Args:
        primary: Array to find trendline on (low for support, high for resistance)
        secondary: Array for context
        helpers: PatternHelpers instance
        line_type: 'support' or 'resistance'
        direction: 1 for rising, -1 for falling
        min_slope: Minimum slope required
        
    Returns:
        List of (start_idx, end_idx, slope) tuples
    """
    trendlines = []
    
    # Find pivot points
    if line_type == 'support':
        pivots = helpers.find_all_bottoms(primary, trade_days=3)
    else:
        pivots = helpers.find_all_tops(primary, trade_days=3)
    
    if len(pivots) < 2:
        return trendlines
    
    # Connect pivots to form trendlines
    for i in range(len(pivots) - 1):
        start_idx = pivots[i]
        
        for j in range(i + 1, len(pivots)):
            end_idx = pivots[j]
            
            # Need sufficient distance
            if end_idx - start_idx < 10:
                continue
            
            # Calculate slope
            price_change = primary[end_idx] - primary[start_idx]
            time_change = end_idx - start_idx
            
            if time_change == 0:
                continue
            
            slope = price_change / (primary[start_idx] * time_change) if primary[start_idx] != 0 else 0
            
            # Verify slope matches direction
            if direction == 1 and slope < min_slope:
                continue
            if direction == -1 and slope > -min_slope:
                continue
            
            # Validate trendline (price stays on correct side)
            valid = True
            tolerance = (secondary[end_idx] - primary[start_idx]) * 0.02  # 2% tolerance
            
            for k in range(start_idx, end_idx + 1):
                # Calculate expected price on trendline
                expected = primary[start_idx] + (k - start_idx) * (primary[end_idx] - primary[start_idx]) / (end_idx - start_idx)
                
                if line_type == 'support':
                    # Price shouldn't go too far below support
                    if primary[k] < expected - tolerance:
                        valid = False
                        break
                else:
                    # Price shouldn't go too far above resistance
                    if primary[k] > expected + tolerance:
                        valid = False
                        break
            
            if valid:
                trendlines.append((start_idx, end_idx, slope))
    
    return trendlines


def _verify_convergence(
    lower_start: int,
    lower_end: int,
    upper_start: int,
    upper_end: int,
    lower_slope: float,
    upper_slope: float,
    direction: int
) -> bool:
    """
    Verify that the trendlines are converging (getting closer together).
    
    Args:
        lower_start, lower_end: Lower trendline indices
        upper_start, upper_end: Upper trendline indices
        lower_slope, upper_slope: Trendline slopes
        direction: 1 for rising, -1 for falling
        
    Returns:
        True if lines are converging
    """
    # For convergence, the lines must get closer together
    # In a rising wedge, upper line slope should be less than lower line slope
    # In a falling wedge, lower line slope should be less than upper line slope (more negative)
    
    if direction == 1:
        # Rising wedge: upper slope < lower slope (upper line rises slower)
        return upper_slope < lower_slope * 0.9
    else:
        # Falling wedge: lower slope < upper slope (lower line falls faster)
        return lower_slope < upper_slope * 0.9


def _verify_wedge_geometry(
    wedge_start: int,
    wedge_end: int,
    lower_start: int,
    lower_end: int,
    upper_start: int,
    upper_end: int,
    high: np.ndarray,
    low: np.ndarray
) -> bool:
    """
    Verify the geometric properties of the wedge.
    
    Checks:
    1. Trendlines overlap sufficiently
    2. Range narrows over time (converging)
    3. Duration is reasonable
    
    Args:
        wedge_start, wedge_end: Overall wedge period
        lower_start, lower_end: Lower trendline period
        upper_start, upper_end: Upper trendline period
        high, low: Price arrays
        
    Returns:
        True if geometry is valid
    """
    # Calculate overlap
    lower_duration = lower_end - lower_start
    upper_duration = upper_end - upper_start
    wedge_duration = wedge_end - wedge_start
    
    # Require at least 57% overlap
    min_overlap = wedge_duration * 0.57
    
    if lower_duration < min_overlap and upper_duration < min_overlap:
        return False
    
    # Verify range narrows (width at start > width at end)
    start_range = high[wedge_start] - low[wedge_start]
    end_range = high[wedge_end] - low[wedge_end]
    
    # End range should be narrower (converging)
    if end_range >= start_range:
        return False
    
    # Convergence should be at least 30%
    convergence_pct = (start_range - end_range) / start_range if start_range > 0 else 0
    if convergence_pct < 0.3:
        return False
    
    return True

