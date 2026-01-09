"""
Bulkowski Pattern Detection Helper Functions

Ported from Patternz FindPatterns.cs - these are the CRITICAL building blocks
that make professional pattern detection work.

All functions ported from Thomas Bulkowski's Patternz software (C#/.NET)
with algorithms from his Encyclopedia of Chart Patterns.
"""
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class PatternHelpers:
    """
    Core helper functions for pattern detection.
    Ported from Patternz FindPatterns.cs
    """
    
    def __init__(self):
        """Initialize helper with default settings"""
        self.strict_patterns = False  # Matches GlobalForm.StrictPatterns
        self.futures = False          # Matches GlobalForm.Futures
        self.near_futures = False     # Matches GlobalForm.NearFutures
        
    def find_all_tops(
        self, 
        highs: np.ndarray, 
        start_idx: int = 0, 
        end_idx: Optional[int] = None,
        trade_days: int = 3
    ) -> np.ndarray:
        """
        Find all local maxima (peaks) in price data.
        
        Ported from FindPatterns.cs lines 2399-2463
        
        Algorithm:
        1. Scan left-to-right looking for highs
        2. Track potential peak
        3. Only confirm peak after trade_days of lower highs
        4. Validate by checking trade_days backward window
        
        Args:
            highs: High prices array
            start_idx: Starting index
            end_idx: Ending index (None = end of array)
            trade_days: Validation window size (default 3)
            
        Returns:
            Array of indices where validated peaks occur
        """
        if end_idx is None:
            end_idx = len(highs) - 1
            
        tops = []
        countdown = trade_days
        current_top_idx = start_idx
        
        for i in range(start_idx, end_idx + 1):
            # Found a higher high - update potential top
            if highs[i] >= highs[current_top_idx]:
                current_top_idx = i
                countdown = trade_days - 1
                continue
                
            # Counting down validation window
            countdown -= 1
            
            # Validation window expired - confirm the top
            while countdown < 0:
                countdown = trade_days
                
                # Double-check by looking backward
                if current_top_idx - trade_days >= 0:
                    lookback_start = current_top_idx - trade_days
                    lookback_end = current_top_idx - 1
                    
                    # Verify all bars in lookback are lower
                    valid = True
                    for j in range(lookback_start, lookback_end + 1):
                        if highs[j] > highs[current_top_idx]:
                            valid = False
                            break
                    
                    if valid:
                        # Confirmed top!
                        tops.append(current_top_idx)
                        current_top_idx = i
                        break
                else:
                    # At start of data - accept as top
                    tops.append(current_top_idx)
                    current_top_idx = i
                    break
        
        return np.array(tops, dtype=np.int32)
    
    def find_all_bottoms(
        self, 
        lows: np.ndarray, 
        start_idx: int = 0, 
        end_idx: Optional[int] = None,
        trade_days: int = 3
    ) -> np.ndarray:
        """
        Find all local minima (troughs) in price data.
        
        Ported from FindPatterns.cs lines 1895-1950
        
        Algorithm:
        1. Scan left-to-right looking for lows
        2. Track potential bottom
        3. Only confirm bottom after trade_days of higher lows
        4. Validate by checking trade_days backward window
        
        Args:
            lows: Low prices array
            start_idx: Starting index
            end_idx: Ending index (None = end of array)
            trade_days: Validation window size (default 3)
            
        Returns:
            Array of indices where validated bottoms occur
        """
        if end_idx is None:
            end_idx = len(lows) - 1
            
        bottoms = []
        countdown = trade_days
        current_bottom_idx = start_idx
        
        for i in range(start_idx, end_idx + 1):
            # Found a lower low - update potential bottom
            if lows[i] <= lows[current_bottom_idx]:
                current_bottom_idx = i
                countdown = trade_days - 1
                continue
                
            # Counting down validation window
            countdown -= 1
            
            # Validation window expired - confirm the bottom
            while countdown < 0:
                countdown = trade_days
                
                # Double-check by looking backward
                if current_bottom_idx - trade_days >= 0:
                    lookback_start = current_bottom_idx - trade_days
                    lookback_end = current_bottom_idx - 1
                    
                    # Verify all bars in lookback are higher
                    valid = True
                    for j in range(lookback_start, lookback_end + 1):
                        if lows[j] < lows[current_bottom_idx]:
                            valid = False
                            break
                    
                    if valid:
                        # Confirmed bottom!
                        bottoms.append(current_bottom_idx)
                        current_bottom_idx = i
                        break
                else:
                    # At start of data - accept as bottom
                    bottoms.append(current_bottom_idx)
                    current_bottom_idx = i
                    break
        
        return np.array(bottoms, dtype=np.int32)
    
    def check_nearness(
        self, 
        point1: float, 
        point2: float, 
        percent: float = -1.0,
        price_vary: float = -1.0
    ) -> bool:
        """
        Check if two price points are "near" each other.
        
        Ported from FindPatterns.cs lines 1121-1170
        
        Two modes:
        1. Percentage-based: points within X% (e.g., 0.5% = 0.005)
        2. Price-based: points within $X (e.g., $0.25)
        
        Price-based mode auto-adjusts for stock price:
        - Stocks > $2500: divide tolerance by 2
        - Stocks > $5000: divide tolerance by 4
        - Futures: divide tolerance by 4
        
        Args:
            point1: First price point
            point2: Second price point
            percent: Percentage tolerance (e.g., 0.005 = 0.5%), -1 to disable
            price_vary: Price tolerance (e.g., 0.25 = $0.25), -1 to disable
            
        Returns:
            True if points are near, False otherwise
            
        Examples:
            # Check if bottoms within 0.5%
            check_nearness(100.0, 100.5, percent=0.005)  # True
            
            # Check if highs within $0.25
            check_nearness(50.25, 50.40, price_vary=0.25)  # True
            
            # Check resistance at $150 within $0.25 (auto-adjusted)
            check_nearness(150.0, 150.15, price_vary=0.25)  # True
        """
        # Both disabled
        if percent == -1.0 and price_vary == -1.0:
            return False
            
        # Zero prices
        if point1 == 0 or point2 == 0:
            return False
        
        # Method 1: Percentage-based
        if percent != -1.0:
            pct = abs(point1 - point2) / max(point1, point2)
            return pct <= percent
        
        # Method 2: Price-based with scaling
        if price_vary != -1.0:
            # Adjust for futures
            if self.futures:
                price_vary = price_vary / 4.0
            elif self.near_futures:
                price_vary = price_vary / 2.0
            
            # Adjust for high-priced stocks
            if point1 > 2500.0 or point2 > 2500.0:
                price_vary = price_vary / 2.0
            if point1 > 5000.0 or point2 > 5000.0:
                price_vary = price_vary / 2.0
            
            return abs(point1 - point2) <= price_vary
        
        return False
    
    def check_confirmation(
        self,
        opens: np.ndarray,
        highs: np.ndarray,
        lows: np.ndarray,
        closes: np.ndarray,
        start_idx: int,
        end_idx: int,
        bot_top: int = -1
    ) -> int:
        """
        Check if pattern has confirmed with breakout/breakdown.
        
        Ported from FindPatterns.cs lines 625-680
        
        Returns 3-state result:
        - 1: CONFIRMED (breakout occurred)
        - 0: PENDING (pattern valid but no breakout yet)
        - -1: FAILED (pattern invalidated by opposite move)
        
        Args:
            opens: Open prices
            highs: High prices
            lows: Low prices  
            closes: Close prices
            start_idx: Pattern start index
            end_idx: Pattern end index
            bot_top: Direction to check
                     -1 = bullish (check for upside breakout)
                      1 = bearish (check for downside breakdown)
                      
        Returns:
            1 = confirmed, 0 = pending, -1 = failed
            
        Example:
            # Double Bottom at bars 50-80, check for upside breakout
            result = check_confirmation(o, h, l, c, 50, 80, bot_top=-1)
            if result == 1:
                print("Pattern confirmed!")
            elif result == 0:
                print("Pattern pending confirmation")
            else:
                print("Pattern failed (broke down)")
        """
        # Find highest high and lowest low in pattern range
        pattern_high_idx = start_idx
        pattern_low_idx = start_idx
        
        for i in range(start_idx, end_idx + 1):
            if highs[i] > highs[pattern_high_idx]:
                pattern_high_idx = i
            if lows[i] < lows[pattern_low_idx] or lows[i] == 0:
                pattern_low_idx = i
        
        pattern_high = highs[pattern_high_idx]
        pattern_low = lows[pattern_low_idx]
        
        # Look AFTER pattern ends for confirmation
        for i in range(end_idx + 1, len(closes)):
            if bot_top == -1:
                # Looking for upside breakout
                if closes[i] > pattern_high:
                    return 1  # CONFIRMED
                if closes[i] < pattern_low:
                    return -1  # FAILED
            else:
                # Looking for downside breakdown  
                if closes[i] < pattern_low:
                    return 1  # CONFIRMED
                if closes[i] > pattern_high:
                    return -1  # FAILED
        
        return 0  # PENDING
    
    def find_bottom_spike_length(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        pattern_start: int,
        pattern_end: int
    ) -> Tuple[float, float]:
        """
        Measure spike characteristics at pattern extremes.
        
        Ported from FindPatterns.cs lines 399-436
        
        Calculates how much the lows "spike" below the pattern on left and right sides.
        Used to identify Adam vs Eve bottoms (spike = Adam, rounded = Eve).
        
        Args:
            highs: High prices
            lows: Low prices
            pattern_start: Pattern start index
            pattern_end: Pattern end index
            
        Returns:
            (left_spike, right_spike) as percentages (0-100)
            Spike > 30% = Adam (sharp V)
            Spike < 30% = Eve (rounded U)
        """
        left_spike = 0.0
        right_spike = 0.0
        
        # Left spike
        if pattern_start - 1 > 0:
            # Which side is lower?
            if lows[pattern_start - 1] < lows[pattern_start + 1]:
                spike_low = lows[pattern_start - 1]
            else:
                spike_low = lows[pattern_start + 1]
            
            # Calculate as percentage of bar range
            bar_range = highs[pattern_start] - lows[pattern_start]
            if bar_range != 0:
                left_spike = 100.0 * (spike_low - lows[pattern_start]) / bar_range
        
        # Right spike
        if pattern_end + 1 < len(lows):
            # Which side is lower?
            if lows[pattern_end - 1] < lows[pattern_end + 1]:
                spike_low = lows[pattern_end - 1]
            else:
                spike_low = lows[pattern_end + 1]
            
            # Calculate as percentage of bar range
            bar_range = highs[pattern_end] - lows[pattern_end]
            if bar_range != 0:
                right_spike = 100.0 * (spike_low - lows[pattern_end]) / bar_range
        
        return left_spike, right_spike
    
    def check_db_downtrend(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        bottom1_idx: int,
        bottom2_idx: int,
        slope_threshold: float = 0.2
    ) -> bool:
        """
        Check if there's a downtrend before double bottom.
        
        Validates that price was falling before the pattern (required for DB).
        
        Args:
            highs: High prices
            lows: Low prices
            bottom1_idx: First bottom index
            bottom2_idx: Second bottom index
            slope_threshold: Minimum downward slope (0.2 = 20%)
            
        Returns:
            True if valid downtrend exists, False otherwise
        """
        # Look at 21 bars before first bottom
        lookback = 21
        start = max(0, bottom1_idx - lookback)
        
        if start >= bottom1_idx:
            return False
        
        # Calculate slope of highs
        high_start = highs[start]
        high_end = highs[bottom1_idx]
        
        # Must be declining
        if high_end >= high_start:
            return False
        
        # Calculate percentage decline
        decline = (high_start - high_end) / high_start
        
        return decline >= slope_threshold

    def wide_range_average(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        end_idx: int,
        lookback: int = 22
    ) -> float:
        """
        Compute average high-low range over a lookback window.
        
        Ported from FindPatterns.cs FindWideRange() (lines 9440-9470)
        
        Args:
            highs: High price array
            lows: Low price array
            end_idx: Inclusive end index for the window
            lookback: Number of bars to include (default 22 to match Patternz)
            
        Returns:
            Average range over the window, or -1.0 if insufficient history
        """
        if end_idx < lookback - 1 or end_idx < 0:
            return -1.0
        
        start_idx = end_idx - (lookback - 1)
        window_highs = highs[start_idx:end_idx + 1]
        window_lows = lows[start_idx:end_idx + 1]
        ranges = window_highs - window_lows
        
        if len(ranges) == 0:
            return -1.0
        
        return float(np.mean(ranges))

    def hl_regression(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        end_idx: int,
        lookback: int = 5,
        use_closes: bool = False
    ) -> int:
        """
        Directional slope of highs/lows over a short window.
        
        Ported from FindPatterns.cs HLRegression() (lines 10319-10380)
        Returns:
            1 for upward bias, -1 for downward bias, 0 if flat/insufficient data
        """
        start_idx = end_idx - (lookback - 1)
        if start_idx < 0 or end_idx < 0:
            return 0
        
        if use_closes:
            series = highs[start_idx:end_idx + 1]
        else:
            series = (highs[start_idx:end_idx + 1] + lows[start_idx:end_idx + 1]) / 2.0
        
        n = len(series)
        if n == 0:
            return 0
        
        x = np.arange(1, n + 1, dtype=np.float64)
        sum_x = float(np.sum(x))
        sum_y = float(np.sum(series))
        sum_x2 = float(np.sum(x * x))
        sum_xy = float(np.sum(x * series))
        
        denom = n * sum_x2 - sum_x * sum_x
        slope = 0.0 if denom == 0 else (n * sum_xy - sum_x * sum_y) / denom
        
        direction = 0
        if slope < 0:
            direction = -1
        elif slope > 0:
            direction = 1
        
        # Recent pivot override to mimic Patternz behavior
        if end_idx + 1 < len(highs) and end_idx - 1 >= 0:
            if direction == -1 and highs[end_idx] < highs[end_idx + 1] and highs[end_idx - 1] < highs[end_idx]:
                direction = 1
            elif direction == 1 and highs[end_idx] > highs[end_idx + 1] and highs[end_idx - 1] > highs[end_idx]:
                direction = -1
        
        return direction


    def calculate_atr(self, high: np.ndarray, low: np.ndarray, close: np.ndarray, period: int = 14) -> np.ndarray:
        """
        Calculate Average True Range (ATR).
        """
        tr = np.maximum(high - low, np.abs(high - np.roll(close, 1)))
        tr[0] = high[0] - low[0]
        
        atr = np.zeros_like(tr)
        atr[0] = tr[0]
        
        # Simple Moving Average for first value? Or recursive?
        # Wilder's smoothing: ATR[i] = (ATR[i-1] * (n-1) + TR[i]) / n
        # For efficiency, we can use pandas ewm if available, but staying numpy here
        for i in range(1, len(tr)):
            atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period
            
        return atr

    def find_pivots_zigzag(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        atr: np.ndarray,
        threshold_factor: float = 1.5,
        min_bars_between_pivots: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Find pivots using ATR-based ZigZag method.
        
        Args:
            highs: High price array
            lows: Low price array
            atr: ATR array (same length)
            threshold_factor: Multiplier for ATR to trigger a pivot (e.g. 1.5 * ATR)
            min_bars_between_pivots: Minimum bars to confirm a new pivot
            
        Returns:
            List of dicts: {'idx': int, 'price': float, 'type': 'high'|'low'}
        """
        pivots = []
        if len(highs) < 10:
            return pivots

        # Initial direction
        trend = 0 # 1=up, -1=down
        last_pivot_idx = 0
        last_pivot_price = highs[0] # temporary
        
        # Initialize first pivot
        # Simple logic: look for first move > threshold
        for i in range(1, len(highs)):
            threshold = atr[i] * threshold_factor
            
            if trend == 0:
                if highs[i] > lows[0] + threshold:
                    trend = 1
                    last_pivot_idx = 0
                    last_pivot_price = lows[0]
                    pivots.append({'idx': 0, 'price': lows[0], 'type': 'low'})
                    last_pivot_idx = i
                    last_pivot_price = highs[i]
                elif lows[i] < highs[0] - threshold:
                    trend = -1
                    last_pivot_idx = 0
                    last_pivot_price = highs[0]
                    pivots.append({'idx': 0, 'price': highs[0], 'type': 'high'})
                    last_pivot_idx = i
                    last_pivot_price = lows[i]
                continue

            if trend == 1: # Upward trend, looking for highest high
                if highs[i] > last_pivot_price:
                    last_pivot_idx = i
                    last_pivot_price = highs[i]
                elif lows[i] < last_pivot_price - (atr[i] * threshold_factor):
                    # Reversal detected: Confirm previous high pivot
                    if i - last_pivot_idx >= min_bars_between_pivots:
                         pivots.append({'idx': last_pivot_idx, 'price': last_pivot_price, 'type': 'high'})
                         trend = -1
                         last_pivot_idx = i
                         last_pivot_price = lows[i]
            
            elif trend == -1: # Downward trend, looking for lowest low
                if lows[i] < last_pivot_price:
                    last_pivot_idx = i
                    last_pivot_price = lows[i]
                elif highs[i] > last_pivot_price + (atr[i] * threshold_factor):
                    # Reversal: Confirm previous low pivot
                     if i - last_pivot_idx >= min_bars_between_pivots:
                         pivots.append({'idx': last_pivot_idx, 'price': last_pivot_price, 'type': 'low'})
                         trend = 1
                         last_pivot_idx = i
                         last_pivot_price = highs[i]
                         
        # Add final pending pivot? Usually yes to capture valid current state
        if trend == 1:
             pivots.append({'idx': last_pivot_idx, 'price': last_pivot_price, 'type': 'high'})
        elif trend == -1:
             pivots.append({'idx': last_pivot_idx, 'price': last_pivot_price, 'type': 'low'})
             
        return pivots

    def is_volatility_contraction(self, pivots: List[Dict[str, Any]]) -> Tuple[bool, List[float]]:
        """
        Check if pivots show volatility contraction (VCP characteristics).
        
        Logic: Calculate depth of each swing (high to low). Check if successive depths decrease.
        Returns: (True/False, list of contraction %s)
        """
        if len(pivots) < 4:
            return False, []
            
        # Extract swings: High->Low sequences
        contractions = []
        
        # Iterate backwards? 
        # Pattern needs High -> Low -> Lower High -> Higher Low -> ...
        # VCP is about the depth of the pullback: High to subsequent Low
        
        # Simply find pairs of High->Low
        # Check last 3 High->Low pairs
        
        # We need a strict sequence? H L LH LL? No, VCP is usually H L H L H L where H-L ranges shrink.
        
        # Filter to just alternating pivots
        # Assuming pivots are alternating High/Low
        
        depths = []
        
        for i in range(len(pivots)-1):
            curr = pivots[i]
            next_p = pivots[i+1]
            
            if curr['type'] == 'high' and next_p['type'] == 'low':
                # Calculate depth %
                depth = (curr['price'] - next_p['price']) / curr['price']
                if depth > 0:
                    depths.append(depth)
                    
        if len(depths) < 2:
            return False, depths
            
        # Check for contraction (allow one anomaly? or strict?)
        # Strict: each subsequent depth is smaller (or at least not significantly larger)
        is_contracting = True
        last_depth = depths[0]
        
        # We want to see the sequence shrinking: e.g. 20%, 10%, 5%
        # So we check from earliest to latest
        
        for i in range(1, len(depths)):
            if depths[i] > last_depth * 1.1: # Allow 10% tolerance
                is_contracting = False
            last_depth = depths[i]
            
        return is_contracting, depths

    def measure_tightness(self, highs: np.ndarray, lows: np.ndarray, window: int = 10) -> float:
        """
        Measure price tightness as average daily range % over window.
        """
        if len(highs) < window:
            return 100.0 # Not tight
            
        ranges = (highs[-window:] - lows[-window:]) / lows[-window:]
        return float(np.mean(ranges))

    def check_volume_dryup(self, volumes: np.ndarray, window: int = 10, compare_window: int = 50) -> bool:
        """
        Check if recent volume is lower than historical average.
        """
        if len(volumes) < compare_window:
            return False
            
        recent_avg = np.mean(volumes[-window:])
        hist_avg = np.mean(volumes[-compare_window:])
        
        return recent_avg < (hist_avg * 0.7) # 30% drop



class PatternData:
    """
    Data structure for pattern detection.
    Matches Patternz nHLC array format for algorithm compatibility.
    """
    
    def __init__(
        self,
        opens: np.ndarray,
        highs: np.ndarray,
        lows: np.ndarray,
        closes: np.ndarray,
        volumes: np.ndarray,
        timestamps: Optional[np.ndarray] = None
    ):
        """
        Initialize pattern data in Patternz-compatible format.
        
        Converts from separate OHLCV arrays to nHLC[6, N] matrix format:
        - nHLC[0, i] = Open
        - nHLC[1, i] = High
        - nHLC[2, i] = Low
        - nHLC[3, i] = Close
        - nHLC[4, i] = Volume
        - nHLC[5, i] = Adjusted Close (same as close for now)
        """
        n = len(closes)
        
        # Validate
        assert len(opens) == n, "Opens length mismatch"
        assert len(highs) == n, "Highs length mismatch"
        assert len(lows) == n, "Lows length mismatch"
        assert len(volumes) == n, "Volumes length mismatch"
        
        # Create nHLC matrix (6 x N)
        self.nHLC = np.zeros((6, n), dtype=np.float64)
        self.nHLC[0, :] = opens
        self.nHLC[1, :] = highs
        self.nHLC[2, :] = lows
        self.nHLC[3, :] = closes
        self.nHLC[4, :] = volumes
        self.nHLC[5, :] = closes  # Adjusted close (same as close for now)
        
        self.timestamps = timestamps
        self.chart_start_index = 0
        self.chart_end_index = n - 1
        self.hlc_range = n - 1
    
    @property
    def opens(self) -> np.ndarray:
        """Get opens array"""
        return self.nHLC[0, :]
    
    @property
    def highs(self) -> np.ndarray:
        """Get highs array"""
        return self.nHLC[1, :]
    
    @property
    def lows(self) -> np.ndarray:
        """Get lows array"""
        return self.nHLC[2, :]
    
    @property
    def closes(self) -> np.ndarray:
        """Get closes array"""
        return self.nHLC[3, :]
    
    @property
    def volumes(self) -> np.ndarray:
        """Get volumes array"""
        return self.nHLC[4, :]
    
    def __len__(self) -> int:
        """Get number of bars"""
        return self.nHLC.shape[1]


# Singleton instance
_pattern_helpers = PatternHelpers()


def get_pattern_helpers() -> PatternHelpers:
    """Get shared pattern helpers instance"""
    return _pattern_helpers
