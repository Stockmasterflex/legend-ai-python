"""
Cup & Handle Pattern Detection

Ported from Patternz FindPatterns.cs FindCup() method (lines 4506-4587)
"""
import numpy as np
from typing import List, Dict, Any
import logging

from app.core.pattern_engine.helpers import PatternData, PatternHelpers

logger = logging.getLogger(__name__)


def find_cup(
    data: PatternData,
    helpers: PatternHelpers,
    strict: bool = False
) -> List[Dict[str, Any]]:
    """
    Find Cup & Handle patterns.
    
    Ported from FindPatterns.cs lines 4506-4587
    
    Pattern characteristics:
    - Two peaks (rims) separated by 35-325 days
    - U-shaped bottom between peaks
    - Left and right rims at similar heights (80-120% of depth)
    - Handle forms after right rim (< 1/4 of cup width)
    - Breakout above right rim with volume
    
    Args:
        data: PatternData with OHLCV
        helpers: PatternHelpers instance
        strict: Use strict pattern rules (Patternz StrictPatterns flag)
        
    Returns:
        List of detected cup patterns with metadata
    """
    patterns = []
    
    # Find peaks (rims)
    trade_days = 20 if strict else 10
    tops = helpers.find_all_tops(
        data.highs,
        data.chart_start_index,
        data.chart_end_index,
        trade_days
    )
    
    if len(tops) < 2:
        logger.debug(f"Not enough tops for cup detection: {len(tops)}")
        return patterns
    
    # Check each pair of tops as potential cup rims
    for i in range(len(tops) - 1, 0, -1):
        right_rim_idx = tops[i]
        
        for j in range(i - 1, -1, -1):
            left_rim_idx = tops[j]
            
            # Cup width must be 35-325 days
            cup_width = right_rim_idx - left_rim_idx
            if cup_width > 325 or cup_width < 35:
                if cup_width > 325:
                    break  # Too wide, earlier tops will be even wider
                continue
            
            # Find the bottom (lowest low between rims)
            bottom_idx = left_rim_idx + 1
            for k in range(left_rim_idx + 2, right_rim_idx):
                if data.lows[k] < data.lows[bottom_idx]:
                    bottom_idx = k
            
            left_rim_high = data.highs[left_rim_idx]
            right_rim_high = data.highs[right_rim_idx]
            bottom_low = data.lows[bottom_idx]
            
            # Calculate cup depth
            cup_depth = left_rim_high - bottom_low
            if cup_depth <= 0:
                continue
            
            # Right rim must be 80-120% of left rim height
            # (measured from bottom)
            min_rim_height = bottom_low + 0.8 * cup_depth
            max_rim_height = bottom_low + 1.2 * cup_depth
            
            if right_rim_high > max_rim_height or right_rim_high < min_rim_height:
                continue
            
            # Validate U-shape: price shouldn't break above certain thresholds in middle
            # Divide cup into 5 sections and check each
            section_width = cup_width // 5
            
            # Sections: 
            # [0-20%] left rim area
            # [20-40%] left descent
            # [40-60%] bottom area (most critical)
            # [60-80%] right ascent  
            # [80-100%] right rim area
            
            # Upper threshold: 60% of depth (bottom + 60% of rise to rim)
            upper_threshold = bottom_low + 0.6 * cup_depth
            
            # Middle threshold: 40% of depth (stricter for middle section)
            middle_threshold = bottom_low + 0.4 * cup_depth
            
            invalid_shape = False
            
            for k in range(left_rim_idx + section_width, right_rim_idx):
                # Determine which section we're in
                progress = (k - left_rim_idx) / cup_width
                
                # Middle 20-80% should stay below upper threshold
                if 0.2 <= progress <= 0.8:
                    if data.closes[k] > upper_threshold:
                        invalid_shape = True
                        break
                
                # Critical middle 40-60% should stay below middle threshold
                if 0.4 <= progress <= 0.6:
                    if data.closes[k] > middle_threshold:
                        invalid_shape = True
                        break
            
            if invalid_shape:
                continue
            
            # Look for handle formation and breakout after right rim
            handle_found = False
            handle_end_idx = right_rim_idx
            confirmed = False
            
            for k in range(right_rim_idx + 1, min(len(data.closes), data.chart_end_index + 1)):
                # Handle dips below upper threshold
                if data.lows[k] < (middle_threshold + upper_threshold) / 2:
                    # Breaking too low invalidates pattern
                    break
                
                # Breakout above right rim
                if data.closes[k] > right_rim_high and k - right_rim_idx > 5:
                    # Handle width must be < 1/4 of cup width
                    handle_width = k - right_rim_idx
                    if handle_width < cup_width / 4:
                        handle_found = True
                        handle_end_idx = k
                        confirmed = True
                        
                        # Calculate target (measure move)
                        target = right_rim_high + cup_depth
                        
                        patterns.append({
                            'pattern': 'Cup',
                            'start_idx': left_rim_idx,
                            'mid_idx': right_rim_idx,
                            'end_idx': handle_end_idx,
                            'left_rim': left_rim_high,
                            'right_rim': right_rim_high,
                            'bottom': bottom_low,
                            'bottom_idx': bottom_idx,
                            'cup_width': cup_width,
                            'cup_depth': cup_depth,
                            'handle_width': handle_width,
                            'target': target,
                            'confirmed': True,
                            'confidence': _calculate_cup_confidence(
                                cup_width, cup_depth, 
                                abs(left_rim_high - right_rim_high) / left_rim_high,
                                handle_width, cup_width
                            )
                        })
                    break
            
            # Pattern exists but not yet broken out
            if not confirmed and not invalid_shape:
                # Still a valid pending cup pattern
                target = right_rim_high + cup_depth
                
                patterns.append({
                    'pattern': 'Cup?',
                    'start_idx': left_rim_idx,
                    'mid_idx': right_rim_idx,
                    'end_idx': min(len(data.closes) - 1, right_rim_idx + cup_width // 4),
                    'left_rim': left_rim_high,
                    'right_rim': right_rim_high,
                    'bottom': bottom_low,
                    'bottom_idx': bottom_idx,
                    'cup_width': cup_width,
                    'cup_depth': cup_depth,
                    'handle_width': 0,
                    'target': target,
                    'confirmed': False,
                    'confidence': _calculate_cup_confidence(
                        cup_width, cup_depth,
                        abs(left_rim_high - right_rim_high) / left_rim_high,
                        0, cup_width
                    ) * 0.7  # Reduce confidence for unconfirmed
                })
    
    logger.info(f"Found {len(patterns)} cup patterns")
    return patterns


def _calculate_cup_confidence(
    cup_width: int,
    cup_depth: float,
    rim_diff_pct: float,
    handle_width: int,
    max_handle_width: int
) -> float:
    """Calculate confidence score for cup pattern"""
    confidence = 0.6  # Base confidence
    
    # Width factor: 50-150 days is ideal
    if 50 <= cup_width <= 150:
        confidence += 0.15
    elif 35 <= cup_width <= 200:
        confidence += 0.1
    
    # Rim similarity: closer is better
    if rim_diff_pct < 0.03:  # Within 3%
        confidence += 0.1
    elif rim_diff_pct < 0.06:  # Within 6%
        confidence += 0.05
    
    # Handle compactness: smaller is better
    if handle_width > 0:
        handle_ratio = handle_width / max_handle_width
        if handle_ratio < 0.15:
            confidence += 0.1
        elif handle_ratio < 0.25:
            confidence += 0.05
    
    # Depth factor: 15-40% is ideal
    # (depth as % of left rim price)
    # Note: we don't have rim price here, but larger absolute depths are better
    if cup_depth > 5.0:  # Significant depth
        confidence += 0.05
    
    return min(1.0, confidence)
