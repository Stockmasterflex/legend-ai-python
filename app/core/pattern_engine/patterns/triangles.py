"""
Triangle Pattern Detection

Ported from Patternz FindPatterns.cs
- FindAscendingTriangle() (lines 4605-4780)
- FindDescendingTriangle() (lines 4605-4780)
- FindSymTriangle() (lines 10375-10630)
"""
import numpy as np
from typing import List, Dict, Any, Tuple
import logging

from app.core.pattern_engine.helpers import PatternData, PatternHelpers

logger = logging.getLogger(__name__)


def find_ascending_triangle(
    data: PatternData,
    helpers: PatternHelpers
) -> List[Dict[str, Any]]:
    """
    Find Ascending Triangle patterns.
    
    Pattern characteristics:
    - Flat/horizontal resistance (multiple touches at same high)
    - Rising support (higher lows)
    - Typically 3+ touches on each trendline
    - Breakout above resistance confirms pattern
    
    Args:
        data: PatternData with OHLCV
        helpers: PatternHelpers instance
        
    Returns:
        List of detected ascending triangle patterns
    """
    patterns = []
    
    # Find trendlines
    tl_resistance, tl_support = _find_triangle_trendlines(
        data, helpers, triangle_type="ascending"
    )
    
    # Match resistance and support lines to form triangles
    for resist in tl_resistance:
        for support in tl_support:
            # Support must start before or at resistance start
            if support['start_idx'] > resist['start_idx']:
                continue
            
            # Lines should end around the same time
            if abs(support['end_idx'] - resist['end_idx']) > 20:
                continue
            
            # Verify convergence (support rising toward resistance)
            start_gap = resist['level'] - _get_tl_price(support, support['start_idx'])
            end_gap = resist['level'] - _get_tl_price(support, resist['end_idx'])
            
            if end_gap >= start_gap * 0.8:  # Not converging enough
                continue
            
            # Check confirmation (breakout above resistance)
            confirmation = 0
            breakout_idx = resist['end_idx']
            
            for k in range(resist['end_idx'] + 1, min(len(data.closes), resist['end_idx'] + 30)):
                if data.closes[k] > resist['level']:
                    confirmation = 1
                    breakout_idx = k
                    break
                elif data.closes[k] < _get_tl_price(support, k):
                    confirmation = -1  # Broke down
                    break
            
            if confirmation == -1:
                continue
            
            # Calculate target
            height = resist['level'] - _get_tl_price(support, support['start_idx'])
            target = resist['level'] + height
            
            pattern_name = "Ascending Triangle"
            if confirmation == 0:
                pattern_name += "?"
            
            patterns.append({
                'pattern': pattern_name,
                'start_idx': support['start_idx'],
                'mid_idx': resist['end_idx'],
                'end_idx': breakout_idx,
                'resistance': resist['level'],
                'support_start': _get_tl_price(support, support['start_idx']),
                'support_end': _get_tl_price(support, resist['end_idx']),
                'height': height,
                'target': target,
                'touches_resistance': resist['touches'],
                'touches_support': support['touches'],
                'confirmed': confirmation == 1,
                'confidence': _calculate_triangle_confidence(
                    resist['touches'], support['touches'], 
                    resist['end_idx'] - support['start_idx'],
                    confirmation == 1
                )
            })
    
    logger.info(f"Found {len(patterns)} ascending triangle patterns")
    return patterns


def find_descending_triangle(
    data: PatternData,
    helpers: PatternHelpers
) -> List[Dict[str, Any]]:
    """
    Find Descending Triangle patterns.
    
    Pattern characteristics:
    - Flat/horizontal support (multiple touches at same low)
    - Descending resistance (lower highs)
    - Typically 3+ touches on each trendline
    - Breakdown below support confirms pattern
    
    Args:
        data: PatternData with OHLCV
        helpers: PatternHelpers instance
        
    Returns:
        List of detected descending triangle patterns
    """
    patterns = []
    
    # Find trendlines
    tl_resistance, tl_support = _find_triangle_trendlines(
        data, helpers, triangle_type="descending"
    )
    
    # Match resistance and support lines to form triangles
    for support in tl_support:
        for resist in tl_resistance:
            # Resistance must start before or at support start
            if resist['start_idx'] > support['start_idx']:
                continue
            
            # Lines should end around the same time
            if abs(resist['end_idx'] - support['end_idx']) > 20:
                continue
            
            # Verify convergence (resistance falling toward support)
            start_gap = _get_tl_price(resist, resist['start_idx']) - support['level']
            end_gap = _get_tl_price(resist, support['end_idx']) - support['level']
            
            if end_gap >= start_gap * 0.8:  # Not converging enough
                continue
            
            # Check confirmation (breakdown below support)
            confirmation = 0
            breakout_idx = support['end_idx']
            
            for k in range(support['end_idx'] + 1, min(len(data.closes), support['end_idx'] + 30)):
                if data.closes[k] < support['level']:
                    confirmation = 1
                    breakout_idx = k
                    break
                elif data.closes[k] > _get_tl_price(resist, k):
                    confirmation = -1  # Broke up
                    break
            
            if confirmation == -1:
                continue
            
            # Calculate target
            height = _get_tl_price(resist, resist['start_idx']) - support['level']
            target = support['level'] - height
            
            pattern_name = "Descending Triangle"
            if confirmation == 0:
                pattern_name += "?"
            
            patterns.append({
                'pattern': pattern_name,
                'start_idx': resist['start_idx'],
                'mid_idx': support['end_idx'],
                'end_idx': breakout_idx,
                'support': support['level'],
                'resistance_start': _get_tl_price(resist, resist['start_idx']),
                'resistance_end': _get_tl_price(resist, support['end_idx']),
                'height': height,
                'target': target,
                'touches_support': support['touches'],
                'touches_resistance': resist['touches'],
                'confirmed': confirmation == 1,
                'confidence': _calculate_triangle_confidence(
                    support['touches'], resist['touches'],
                    support['end_idx'] - resist['start_idx'],
                    confirmation == 1
                )
            })
    
    logger.info(f"Found {len(patterns)} descending triangle patterns")
    return patterns


def find_sym_triangle(
    data: PatternData,
    helpers: PatternHelpers
) -> List[Dict[str, Any]]:
    """
    Find Symmetrical Triangle patterns.
    
    Pattern characteristics:
    - Descending resistance (lower highs)
    - Rising support (higher lows)
    - Both lines converge at similar rates
    - Breakout in either direction confirms
    
    Args:
        data: PatternData with OHLCV
        helpers: PatternHelpers instance
        
    Returns:
        List of detected symmetrical triangle patterns
    """
    patterns = []
    
    # Find all tops and bottoms
    tops = helpers.find_all_tops(data.highs, data.chart_start_index, data.chart_end_index, trade_days=3)
    bottoms = helpers.find_all_bottoms(data.lows, data.chart_start_index, data.chart_end_index, trade_days=3)
    
    if len(tops) < 2 or len(bottoms) < 2:
        return patterns
    
    # Find descending resistance lines
    resistance_lines = _find_descending_trendlines(data, helpers, tops, min_touches=2)
    
    # Find ascending support lines
    support_lines = _find_ascending_trendlines(data, helpers, bottoms, min_touches=2)
    
    # Match lines to form symmetrical triangles
    for resist in resistance_lines:
        for support in support_lines:
            # Lines must overlap significantly
            overlap_start = max(resist['start_idx'], support['start_idx'])
            overlap_end = min(resist['end_idx'], support['end_idx'])
            
            if overlap_end - overlap_start < 20:  # Need at least 20 bars overlap
                continue
            
            # Check convergence: resistance falling, support rising at similar rates
            resist_start = _get_tl_price(resist, overlap_start)
            resist_end = _get_tl_price(resist, overlap_end)
            support_start = _get_tl_price(support, overlap_start)
            support_end = _get_tl_price(support, overlap_end)
            
            start_gap = resist_start - support_start
            end_gap = resist_end - support_end
            
            if start_gap <= 0 or end_gap <= 0:
                continue
            
            convergence_rate = end_gap / start_gap
            
            # Should converge significantly (end gap < 40% of start gap)
            if convergence_rate > 0.6:
                continue
            
            # Check for breakout in either direction
            confirmation = 0
            breakout_idx = overlap_end
            breakout_direction = None
            
            for k in range(overlap_end + 1, min(len(data.closes), overlap_end + 30)):
                resist_price = _get_tl_price(resist, k)
                support_price = _get_tl_price(support, k)
                
                if data.closes[k] > resist_price:
                    confirmation = 1
                    breakout_idx = k
                    breakout_direction = "up"
                    break
                elif data.closes[k] < support_price:
                    confirmation = 1
                    breakout_idx = k
                    breakout_direction = "down"
                    break
            
            # Calculate target
            height = start_gap
            if breakout_direction == "up":
                target = _get_tl_price(resist, overlap_end) + height
            elif breakout_direction == "down":
                target = _get_tl_price(support, overlap_end) - height
            else:
                target = (_get_tl_price(resist, overlap_end) + _get_tl_price(support, overlap_end)) / 2
            
            pattern_name = "Symmetrical Triangle"
            if confirmation == 0:
                pattern_name += "?"
            
            patterns.append({
                'pattern': pattern_name,
                'start_idx': overlap_start,
                'mid_idx': overlap_end,
                'end_idx': breakout_idx,
                'resistance_start': resist_start,
                'resistance_end': resist_end,
                'support_start': support_start,
                'support_end': support_end,
                'height': height,
                'target': target,
                'convergence_rate': convergence_rate,
                'breakout_direction': breakout_direction,
                'confirmed': confirmation == 1,
                'confidence': _calculate_triangle_confidence(
                    resist['touches'], support['touches'],
                    overlap_end - overlap_start,
                    confirmation == 1
                )
            })
    
    logger.info(f"Found {len(patterns)} symmetrical triangle patterns")
    return patterns


def _find_triangle_trendlines(
    data: PatternData,
    helpers: PatternHelpers,
    triangle_type: str
) -> Tuple[List[Dict], List[Dict]]:
    """Find trendlines for triangle patterns"""
    tops = helpers.find_all_tops(data.highs, data.chart_start_index, data.chart_end_index, trade_days=3)
    bottoms = helpers.find_all_bottoms(data.lows, data.chart_start_index, data.chart_end_index, trade_days=3)
    
    resistance_lines = []
    support_lines = []
    
    if triangle_type == "ascending":
        # Flat resistance: find tops at similar heights
        resistance_lines = _find_horizontal_levels(data, helpers, tops, data.highs, is_high=True)
        # Rising support: find ascending line through bottoms
        support_lines = _find_ascending_trendlines(data, helpers, bottoms, min_touches=2)
    
    elif triangle_type == "descending":
        # Flat support: find bottoms at similar depths
        support_lines = _find_horizontal_levels(data, helpers, bottoms, data.lows, is_high=False)
        # Falling resistance: find descending line through tops
        resistance_lines = _find_descending_trendlines(data, helpers, tops, min_touches=2)
    
    return resistance_lines, support_lines


def _find_horizontal_levels(
    data: PatternData,
    helpers: PatternHelpers,
    pivots: np.ndarray,
    prices: np.ndarray,
    is_high: bool,
    min_touches: int = 3
) -> List[Dict]:
    """Find horizontal resistance or support levels"""
    levels = []
    
    for i in range(len(pivots) - min_touches + 1):
        touches = [pivots[i]]
        base_price = prices[pivots[i]]
        
        # Find other pivots near this level
        for j in range(i + 1, len(pivots)):
            if pivots[j] - pivots[i] > 126:  # Max pattern width
                break
            
            if helpers.check_nearness(base_price, prices[pivots[j]], price_vary=0.25):
                touches.append(pivots[j])
        
        if len(touches) >= min_touches:
            levels.append({
                'level': base_price,
                'start_idx': touches[0],
                'end_idx': touches[-1],
                'touches': len(touches),
                'touch_indices': touches
            })
    
    return levels


def _find_ascending_trendlines(
    data: PatternData,
    helpers: PatternHelpers,
    pivots: np.ndarray,
    min_touches: int = 2
) -> List[Dict]:
    """Find ascending trendlines through pivots"""
    lines = []
    
    for i in range(len(pivots) - 1):
        for j in range(i + 1, len(pivots)):
            if pivots[j] - pivots[i] > 126:
                break
            
            # Calculate slope
            price1 = data.lows[pivots[i]]
            price2 = data.lows[pivots[j]]
            slope = (price2 - price1) / (pivots[j] - pivots[i])
            
            # Must be ascending
            if slope <= 0:
                continue
            
            # Find touches
            touches = [pivots[i], pivots[j]]
            
            for k in range(i + 1, j):
                expected = price1 + slope * (pivots[k] - pivots[i])
                if helpers.check_nearness(expected, data.lows[pivots[k]], price_vary=0.25):
                    touches.append(pivots[k])
            
            if len(touches) >= min_touches:
                lines.append({
                    'start_idx': pivots[i],
                    'end_idx': pivots[j],
                    'start_price': price1,
                    'end_price': price2,
                    'slope': slope,
                    'touches': len(touches),
                    'touch_indices': sorted(touches)
                })
    
    return lines


def _find_descending_trendlines(
    data: PatternData,
    helpers: PatternHelpers,
    pivots: np.ndarray,
    min_touches: int = 2
) -> List[Dict]:
    """Find descending trendlines through pivots"""
    lines = []
    
    for i in range(len(pivots) - 1):
        for j in range(i + 1, len(pivots)):
            if pivots[j] - pivots[i] > 126:
                break
            
            # Calculate slope
            price1 = data.highs[pivots[i]]
            price2 = data.highs[pivots[j]]
            slope = (price2 - price1) / (pivots[j] - pivots[i])
            
            # Must be descending
            if slope >= 0:
                continue
            
            # Find touches
            touches = [pivots[i], pivots[j]]
            
            for k in range(i + 1, j):
                expected = price1 + slope * (pivots[k] - pivots[i])
                if helpers.check_nearness(expected, data.highs[pivots[k]], price_vary=0.25):
                    touches.append(pivots[k])
            
            if len(touches) >= min_touches:
                lines.append({
                    'start_idx': pivots[i],
                    'end_idx': pivots[j],
                    'start_price': price1,
                    'end_price': price2,
                    'slope': slope,
                    'touches': len(touches),
                    'touch_indices': sorted(touches)
                })
    
    return lines


def _get_tl_price(trendline: Dict, idx: int) -> float:
    """Get price at index for a trendline"""
    if 'level' in trendline:
        # Horizontal line
        return trendline['level']
    else:
        # Sloped line
        return trendline['start_price'] + trendline['slope'] * (idx - trendline['start_idx'])


def _calculate_triangle_confidence(
    touches1: int,
    touches2: int,
    width: int,
    confirmed: bool
) -> float:
    """Calculate confidence score for triangle pattern"""
    confidence = 0.60  # Base
    
    # Touches: more is better
    total_touches = touches1 + touches2
    if total_touches >= 6:
        confidence += 0.12
    elif total_touches >= 5:
        confidence += 0.08
    elif total_touches >= 4:
        confidence += 0.05
    
    # Width: 30-80 days ideal
    if 30 <= width <= 80:
        confidence += 0.10
    elif 20 <= width <= 100:
        confidence += 0.06
    
    # Confirmation
    if confirmed:
        confidence += 0.13
    
    return min(1.0, confidence)
