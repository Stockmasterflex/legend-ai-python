from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
import statistics
import math


@dataclass
class PatternResult:
    """Result of pattern detection analysis"""
    ticker: str
    pattern: str  # "VCP", "Cup & Handle", "Flat Base", "Breakout", "NONE"
    score: float  # 0-10 scale
    entry: float  # Entry price
    stop: float   # Stop loss price
    target: float # Target price
    risk_reward: float  # Risk/reward ratio
    criteria_met: List[str]  # List of satisfied criteria
    analysis: str  # Detailed analysis text
    timestamp: datetime

    # Additional metadata
    rs_rating: Optional[float] = None
    current_price: Optional[float] = None
    support_start: Optional[float] = None
    support_end: Optional[float] = None
    volume_increasing: Optional[bool] = None
    consolidation_days: Optional[int] = None
    chart_url: Optional[str] = None  # URL to chart image

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "ticker": self.ticker,
            "pattern": self.pattern,
            "score": round(self.score, 1),
            "entry": round(self.entry, 2),
            "stop": round(self.stop, 2),
            "target": round(self.target, 2),
            "risk_reward": round(self.risk_reward, 2),
            "criteria_met": self.criteria_met,
            "analysis": self.analysis,
            "timestamp": self.timestamp.isoformat(),
            "rs_rating": self.rs_rating,
            "current_price": self.current_price,
            "support_start": self.support_start,
            "support_end": self.support_end,
            "volume_increasing": self.volume_increasing,
            "consolidation_days": self.consolidation_days,
            "chart_url": self.chart_url,
        }


class PatternDetector:
    """
    Implements Mark Minervini's 8-Point Trend Template + Pattern Detection

    Based on analysis of Pattern_Detection_Engine_FINAL.json n8n workflow
    """

    def __init__(self):
        pass

    async def analyze_ticker(
        self,
        ticker: str,
        price_data: Dict[str, Any],
        spy_data: Optional[Dict[str, Any]] = None
    ) -> Optional[PatternResult]:
        """
        Analyze a ticker for pattern setups

        Args:
            ticker: Stock symbol
            price_data: OHLCV data from TwelveData/Yahoo
            spy_data: SPY data for RS calculation (optional)

        Returns:
            PatternResult if analysis successful, None if insufficient data
        """
        try:
            # Extract OHLCV data
            closes = price_data.get("c", [])
            highs = price_data.get("h", [])
            lows = price_data.get("l", [])
            volumes = price_data.get("v", [])

            # Validate minimum data requirements
            if len(closes) < 60:
                return self._create_insufficient_data_result(ticker, closes)

            # Calculate technical indicators
            metrics = self._compute_technical_metrics(closes, highs, lows, volumes)

            # Calculate RS rating if SPY data available
            rs_data = None
            if spy_data and "c" in spy_data:
                rs_data = self._calculate_rs_rating(closes, spy_data["c"])
                metrics["rs"] = rs_data["rs"]

            # Check if stock meets trend template
            trend_pass = self._check_trend_template(closes)

            # Detect patterns (only if trend template passes)
            patterns_found = []
            if trend_pass["pass"]:
                patterns_found = self._detect_patterns(closes, highs, lows, volumes, metrics)

            # Select best pattern
            if patterns_found:
                best_pattern = max(patterns_found, key=lambda x: x["score"])
                return self._create_pattern_result(ticker, best_pattern, closes, highs, lows, volumes, metrics, rs_data)
            else:
                return self._create_no_pattern_result(ticker, closes, highs, lows, volumes, metrics, rs_data)

        except Exception as e:
            print(f"Error analyzing {ticker}: {e}")
            return None

    def _compute_technical_metrics(self, closes: List[float], highs: List[float],
                                 lows: List[float], volumes: List[float]) -> Dict[str, Any]:
        """Compute technical indicators and metrics"""
        n = len(closes)
        current_price = closes[-1] if closes else 0

        # Moving averages
        sma_50 = self._sma(closes, 50)
        ema_21 = self._ema(closes, 21)
        sma_150 = self._sma(closes, 150)
        sma_200 = self._sma(closes, 200)
        ema_50 = self._ema(closes, 50)

        # Above MAs
        above_50 = n >= 50 and sma_50[-1] and current_price > sma_50[-1]
        above_200 = n >= 200 and sma_200[-1] and current_price > sma_200[-1]

        # 52-week high/low
        high_52w = max(highs[-252:]) if len(highs) >= 252 else max(highs)
        low_52w = min(lows[-252:]) if len(lows) >= 252 else min(lows)

        # Volume analysis
        volume_increasing = self._check_volume_increasing(volumes)
        volume_dry_up = self._check_volume_dry_up(volumes)

        # Volatility contractions
        contractions = self._analyze_volatility_contractions(closes)

        # Support levels
        support_start = min(closes[-30:]) if len(closes) >= 30 else min(closes)
        support_end = min(closes[-5:]) if len(closes) >= 5 else min(closes)

        return {
            "sma_50": sma_50,
            "sma_150": sma_150,
            "sma_200": sma_200,
            "ema_50": ema_50,
            "ema_21": ema_21,
            "above_50sma": above_50,
            "above_200sma": above_200,
            "high_52w": high_52w,
            "low_52w": low_52w,
            "volume_increasing": volume_increasing,
            "volume_dry_up": volume_dry_up,
            "contractions": contractions,
            "support_start": support_start,
            "support_end": support_end,
            "current_price": current_price,
            "rs": 0  # Will be set if SPY data available
        }

    def _check_trend_template(self, closes: List[float]) -> Dict[str, Any]:
        """Check Minervini's 8-point trend template"""
        n = len(closes)
        if n < 260:  # Need at least 260 days for full analysis
            return {"pass": False, "criteria": []}

        # Calculate moving averages
        sma_50 = self._sma(closes, 50)
        sma_150 = self._sma(closes, 150)
        sma_200 = self._sma(closes, 200)
        ema_50 = self._ema(closes, 50)

        price = closes[-1]

        # 52-week range
        high_52w = max(closes[-252:])
        low_52w = min(closes[-252:])

        criteria = []

        # Point 1: Price > 150 SMA & 200 SMA
        if price > sma_150[-1] and price > sma_200[-1]:
            criteria.append("✓ Price > 150 SMA & 200 SMA")

        # Point 2: 150 SMA > 200 SMA
        if sma_150[-1] > sma_200[-1]:
            criteria.append("✓ 150 SMA > 200 SMA")

        # Point 3: 200 SMA trending up (1+ months)
        if sma_200[-1] > sma_200[-22] and sma_200[-1] > sma_200[-88]:
            criteria.append("✓ 200 SMA trending up (1+ months)")

        # Point 4: 50 EMA > 150 SMA > 200 SMA
        if ema_50[-1] > sma_150[-1] and sma_150[-1] > sma_200[-1]:
            criteria.append("✓ 50 EMA > 150 SMA > 200 SMA")

        # Point 5: Price > 50 EMA
        if price > ema_50[-1]:
            criteria.append("✓ Price > 50 EMA")

        # Point 6: Price within 25% of 52w high
        pct_from_high = ((high_52w - price) / high_52w) * 100
        if pct_from_high <= 25:
            criteria.append("✓ Price within 25% of 52w high")

        # Point 7: Price > 30% above 52w low
        pct_above_low = ((price - low_52w) / low_52w) * 100
        if pct_above_low >= 30:
            criteria.append("✓ Price > 30% above 52w low")

        # Point 8: RS Rating > 70 (checked separately in pattern scoring)

        return {
            "pass": len(criteria) >= 7,  # Need 7 of 8 criteria (RS is separate)
            "criteria": criteria
        }

    def _detect_patterns(self, closes: List[float], highs: List[float],
                        lows: List[float], volumes: List[float],
                        metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Detect various chart patterns"""
        patterns = []

        # VCP Detection
        vcp = self._detect_vcp(closes, volumes, metrics)
        if vcp["hit"]:
            patterns.append(vcp)

        # Cup & Handle Detection
        cup_handle = self._detect_cup_handle(closes, highs, lows, volumes)
        if cup_handle["hit"]:
            patterns.append(cup_handle)

        # Flat Base Detection
        flat_base = self._detect_flat_base(closes)
        if flat_base["hit"]:
            patterns.append(flat_base)

        # Breakout Detection
        breakout = self._detect_breakout(closes, highs, volumes, metrics)
        if breakout["hit"]:
            patterns.append(breakout)

        rising_wedge = self._detect_wedge(highs, lows, direction="rising")
        if rising_wedge["hit"]:
            patterns.append(rising_wedge)

        falling_wedge = self._detect_wedge(highs, lows, direction="falling")
        if falling_wedge["hit"]:
            patterns.append(falling_wedge)

        ascending_triangle = self._detect_triangle(highs, lows, kind="ascending")
        if ascending_triangle["hit"]:
            patterns.append(ascending_triangle)

        symmetrical_triangle = self._detect_triangle(highs, lows, kind="symmetrical")
        if symmetrical_triangle["hit"]:
            patterns.append(symmetrical_triangle)

        head_shoulders = self._detect_head_shoulders(closes, inverted=False)
        if head_shoulders["hit"]:
            patterns.append(head_shoulders)

        inverse_head_shoulders = self._detect_head_shoulders(closes, inverted=True)
        if inverse_head_shoulders["hit"]:
            patterns.append(inverse_head_shoulders)

        ema_pullback = self._detect_ma_pullback(closes, metrics, length=21)
        if ema_pullback["hit"]:
            patterns.append(ema_pullback)

        sma_pullback = self._detect_ma_pullback(closes, metrics, length=50)
        if sma_pullback["hit"]:
            patterns.append(sma_pullback)

        return patterns

    def _detect_vcp(self, closes: List[float], volumes: List[float],
                   metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Volatility Contraction Pattern"""
        n = len(closes)
        if n < 120:
            return {"hit": False, "score": 0, "info": "Insufficient data"}

        contractions = metrics["contractions"]
        contraction_count = contractions["count"]
        if contraction_count < 2:
            return {"hit": False, "score": 0, "info": "Need 2+ contractions"}

        # Check if contractions are contracting (each smaller than previous)
        pulls = contractions["pulls"]
        contracting = True
        for i in range(1, len(pulls)):
            if pulls[i] > pulls[i-1] * 0.8:  # Not contracting enough
                contracting = False
                break

        volume_dry_up = metrics["volume_dry_up"]
        volume_increasing = metrics.get("volume_increasing")

        score = 4.0
        if contracting:
            score += 3.0
        else:
            score += 1.0
        if volume_dry_up:
            score += 1.5
        if contraction_count >= 3:
            score += 1.0
        if volume_increasing:
            score += 0.5

        top_pulls = [f"{x:.0f}%" for x in pulls[:4]] if pulls else []
        info_bits = [f"T={'/'.join(top_pulls)}" if top_pulls else "No pulls"]
        info_bits.append(f"dry-up={'yes' if volume_dry_up else 'no'}")

        return {
            "hit": score >= 6,
            "score": round(min(10.0, score), 1),
            "info": " · ".join(info_bits),
            "name": "VCP",
            "contractions": contraction_count,
            "volume_dry_up": volume_dry_up
        }

    def _detect_cup_handle(self, closes: List[float], highs: List[float],
                          lows: List[float], volumes: List[float]) -> Dict[str, Any]:
        """Detect Cup & Handle pattern - improved with stricter criteria"""
        n = len(closes)
        if n < 150:
            return {"hit": False, "score": 0, "info": "Need 150+ days data"}

        # Analyze last 200 days for cup formation
        window = closes[-200:]
        window_highs = highs[-200:]
        window_lows = lows[-200:]

        # Left rim (first 1/4 of window)
        left_quarter = window[:50]
        left_rim = max(left_quarter)

        # Bottom (middle section, 40-120 days back)
        middle_section = window[40:120]
        bottom = min(middle_section)
        bottom_idx = 40 + middle_section.index(bottom)

        # Right rim (last 1/4 of window, but should be before handle)
        right_section = window[100:160]
        right_rim = max(right_section) if right_section else closes[-1]

        # Cup depth check
        cup_depth = ((left_rim - bottom) / left_rim) * 100

        # Relaxed criteria for depth/length
        if cup_depth < 12 or cup_depth > 45:
            return {"hit": False, "score": 0, "info": f"Cup depth {cup_depth:.1f}% out of range"}

        # 2. Left and right rims should be similar (within 12%)
        rim_difference = abs(left_rim - right_rim) / left_rim * 100
        if rim_difference > 12:
            return {"hit": False, "score": 0, "info": f"Rims differ by {rim_difference:.1f}%"}

        # 3. Check handle formation (last 25 days)
        handle_window = closes[-25:]
        handle_high = max(handle_window)
        handle_low = min(handle_window)
        handle_depth = ((handle_high - handle_low) / handle_high) * 100

        # Handle must be shallow-ish
        if handle_depth < 2 or handle_depth > 15:
            return {"hit": False, "score": 0, "info": f"Handle depth {handle_depth:.1f}% invalid"}

        # 4. Handle should be above the cup bottom
        if handle_low < bottom * 1.005:
            return {"hit": False, "score": 0, "info": "Handle below cup bottom"}

        # 5. Recent price should be within 3% of the handle high (breakout zone)
        if closes[-1] < handle_high * 0.97:
            return {"hit": False, "score": 0, "info": "No breakout above handle"}

        # 6. Volume should increase on breakout (soft requirement)
        volume_increasing = bool(
            volumes[-5:] and len(volumes) >= 20 and volumes[-1] > statistics.mean(volumes[-20:-5]) * 1.1
        )

        # Scoring weights
        score = 7.5
        if rim_difference < 6:
            score += 0.5
        if handle_depth <= 8:
            score += 0.5
        if volume_increasing:
            score += 1
        score -= max(0, (cup_depth - 30) / 15)
        score = max(6.0, min(9.5, score))

        return {
            "hit": True,
            "score": round(score, 1),
            "info": f"Cup {cup_depth:.1f}%, handle {handle_depth:.1f}% · vol {'up' if volume_increasing else 'flat'}",
            "name": "Cup & Handle"
        }

    def _detect_flat_base(self, closes: List[float]) -> Dict[str, Any]:
        """Detect Flat Base pattern"""
        n = len(closes)
        if n < 50:
            return {"hit": False, "score": 0, "info": "Need 50+ days data"}

        # Look at last 35 days
        window = closes[-35:]
        high = max(window)
        low = min(window)
        depth = ((high - low) / high) * 100

        # Check tightness (low volatility in last 12 days)
        recent = window[-12:]
        if len(recent) < 12:
            return {"hit": False, "score": 0, "info": "Need more recent data"}

        try:
            stdev_recent = statistics.stdev(recent)
            avg_recent = statistics.mean(recent)
            tightness_ratio = stdev_recent / avg_recent if avg_recent > 0 else 1
            tight = tightness_ratio < 0.015
        except:
            tight = False

        depth_ok = depth <= 12 or (depth <= 15 and tight)
        if not depth_ok:
            return {"hit": False, "score": 0, "info": f"Depth {depth:.1f}% too wide"}

        score = 6.0
        score += max(0, (12 - min(depth, 12)) / 4)
        if tight:
            score += 1.0

        return {
            "hit": score >= 6,
            "score": round(min(9.0, score), 1),
            "info": f"Depth {depth:.1f}%, tight={tight}",
            "name": "Flat Base"
        }

    def _detect_breakout(self, closes: List[float], highs: List[float],
                        volumes: List[float], metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Detect Breakout pattern"""
        n = len(closes)
        if n < 160:
            return {"hit": False, "score": 0, "info": "Need 160+ days data"}

        # 52-week high
        high_52w = metrics["high_52w"]
        current_price = closes[-1]

        # Check breakout
        broke = current_price >= high_52w * 0.999  # Within 0.1% of 52w high
        near_high = current_price >= high_52w * 0.995

        # Volume spike (40% above 50-day average)
        if len(volumes) >= 50:
            recent_volume = volumes[-1]
            avg_volume_50 = sum(volumes[-50:]) / 50
            volume_spike = ((recent_volume - avg_volume_50) / avg_volume_50) * 100
        else:
            volume_spike = 0

        # Momentum (2%+ daily gain)
        momentum = 0
        if n >= 2:
            daily_return = (closes[-1] - closes[-2]) / closes[-2]
            if daily_return > 0.02:
                momentum = 1
        rs = metrics.get("rs", 0)

        score = 0
        if broke:
            score += 4.5
        elif near_high:
            score += 3.0
        if volume_spike >= 25:
            score += 2.5
        elif volume_spike >= 10:
            score += 1.0
        score += momentum
        if rs >= 60:
            score += 1.0

        return {
            "hit": score >= 6,
            "score": round(min(9.5, score), 1),
            "info": f"vol +{volume_spike:.0f}%, broke={broke}",
            "name": "Breakout"
        }

    def _detect_wedge(self, highs: List[float], lows: List[float], direction: str = "rising") -> Dict[str, Any]:
        """Detect rising/falling wedge formations."""
        window = 60
        if len(highs) < window or len(lows) < window:
            return {"hit": False, "score": 0, "info": "Need 60+ candles"}

        recent_highs = highs[-window:]
        recent_lows = lows[-window:]
        slope_high = self._linear_slope(recent_highs)
        slope_low = self._linear_slope(recent_lows)
        first_half_range = max(recent_highs[:window // 2]) - min(recent_lows[:window // 2])
        second_half_range = max(recent_highs[window // 2:]) - min(recent_lows[window // 2:])
        if first_half_range <= 0 or second_half_range <= 0:
            return {"hit": False, "score": 0, "info": "Range insufficient"}
        range_ratio = second_half_range / first_half_range

        if direction == "rising":
            if not (slope_high > 0 and slope_low > 0):
                return {"hit": False, "score": 0, "info": "No rising slopes"}
            if not (slope_low > slope_high * 0.8):
                return {"hit": False, "score": 0, "info": "No convergence"}
            if range_ratio > 0.85:
                return {"hit": False, "score": 0, "info": "Range not contracting"}
            info = f"slopeH {slope_high:.3f}, slopeL {slope_low:.3f}"
            score = 6.0 + (0.85 - range_ratio) * 5
            return {
                "hit": True,
                "score": round(min(9.5, score), 1),
                "info": info,
                "name": "Rising Wedge"
            }
        else:
            if not (slope_high < 0 and slope_low < 0):
                return {"hit": False, "score": 0, "info": "No falling slopes"}
            if not (abs(slope_high) > abs(slope_low) * 0.8):
                return {"hit": False, "score": 0, "info": "No convergence"}
            if range_ratio > 0.85:
                return {"hit": False, "score": 0, "info": "Range not contracting"}
            info = f"slopeH {slope_high:.3f}, slopeL {slope_low:.3f}"
            score = 6.0 + (0.85 - range_ratio) * 5
            return {
                "hit": True,
                "score": round(min(9.5, score), 1),
                "info": info,
                "name": "Falling Wedge"
            }

    def _detect_triangle(self, highs: List[float], lows: List[float], kind: str = "ascending") -> Dict[str, Any]:
        """Detect ascending or symmetrical triangle formations."""
        window = 70
        if len(highs) < window or len(lows) < window:
            return {"hit": False, "score": 0, "info": "Need 70+ candles"}

        recent_highs = highs[-window:]
        recent_lows = lows[-window:]
        slope_high = self._linear_slope(recent_highs)
        slope_low = self._linear_slope(recent_lows)
        first_half_range = max(recent_highs[:window // 2]) - min(recent_lows[:window // 2])
        second_half_range = max(recent_highs[window // 2:]) - min(recent_lows[window // 2:])
        if first_half_range <= 0 or second_half_range <= 0:
            return {"hit": False, "score": 0, "info": "Range insufficient"}
        range_ratio = second_half_range / first_half_range

        if kind == "ascending":
            flat_resistance = abs(slope_high) < abs(slope_low) * 0.3 and abs(slope_high) < 0.05
            rising_support = slope_low > 0.02
            if not (flat_resistance and rising_support):
                return {"hit": False, "score": 0, "info": "No flat top + rising base"}
            if range_ratio > 0.9:
                return {"hit": False, "score": 0, "info": "Range not contracting"}
            score = 6.2 + (0.9 - range_ratio) * 4
            return {
                "hit": True,
                "score": round(min(9.2, score), 1),
                "info": f"slopeL {slope_low:.3f}",
                "name": "Ascending Triangle"
            }

        # symmetrical
        descending_resistance = slope_high < -0.02
        rising_support = slope_low > 0.02
        if not (descending_resistance and rising_support):
            return {"hit": False, "score": 0, "info": "No converging trendlines"}
        if range_ratio > 0.92:
            return {"hit": False, "score": 0, "info": "Range not contracting"}
        score = 6.0 + (0.92 - range_ratio) * 4
        return {
            "hit": True,
            "score": round(min(9.0, score), 1),
            "info": f"slopeH {slope_high:.3f}, slopeL {slope_low:.3f}",
            "name": "Symmetrical Triangle"
        }

    def _detect_head_shoulders(self, closes: List[float], inverted: bool = False) -> Dict[str, Any]:
        """Detect (inverse) head & shoulders formations."""
        window = 110
        if len(closes) < window:
            return {"hit": False, "score": 0, "info": "Need 110+ candles"}
        segment = closes[-window:]
        mode = "min" if inverted else "max"
        extrema = self._find_local_extrema(segment, mode=mode)
        if len(extrema) < 3:
            return {"hit": False, "score": 0, "info": "Not enough pivots"}

        for i in range(len(extrema) - 2):
            p1, p2, p3 = extrema[i], extrema[i + 1], extrema[i + 2]
            if p2[0] - p1[0] < 5 or p3[0] - p2[0] < 5:
                continue
            shoulder_diff = abs(p1[1] - p3[1]) / max(p1[1], p3[1])
            if shoulder_diff > 0.05:
                continue
            if inverted:
                # Middle trough should be notably lower
                if not (p2[1] < min(p1[1], p3[1]) * 0.98):
                    continue
                name = "Inverse Head & Shoulders"
            else:
                if not (p2[1] > max(p1[1], p3[1]) * 1.02):
                    continue
                name = "Head & Shoulders"

            neckline = min(segment[p1[0]:p3[0] + 1]) if not inverted else max(segment[p1[0]:p3[0] + 1])
            span = p3[0] - p1[0]
            score = 6.5 + min(2.0, span / 30)
            info = f"shoulders Δ {shoulder_diff:.2%}, neckline {neckline:.2f}"
            return {
                "hit": True,
                "score": round(min(9.0, score), 1),
                "info": info,
                "name": name
            }

        return {"hit": False, "score": 0, "info": "Pattern not detected"}

    def _find_local_extrema(self, values: List[float], mode: str = "max") -> List[tuple]:
        """Return local maxima or minima indices/value pairs."""
        extrema = []
        for idx in range(2, len(values) - 2):
            window = values[idx - 2:idx + 3]
            center = window[2]
            if mode == "max":
                if center == max(window):
                    extrema.append((idx, center))
            else:
                if center == min(window):
                    extrema.append((idx, center))
        return extrema

    def _linear_slope(self, values: List[float]) -> float:
        """Compute slope via simple linear regression."""
        if not values or len(values) < 2:
            return 0.0
        n = len(values)
        mean_x = (n - 1) / 2
        mean_y = sum(values) / n
        numerator = 0.0
        denominator = 0.0
        for idx, val in enumerate(values):
            numerator += (idx - mean_x) * (val - mean_y)
            denominator += (idx - mean_x) ** 2
        if denominator == 0:
            return 0.0
        return numerator / denominator

    def _detect_ma_pullback(self, closes: List[float], metrics: Dict[str, Any], length: int = 21) -> Dict[str, Any]:
        """Detect constructive pullbacks to 21 EMA or 50 SMA."""
        if len(closes) < length + 10:
            return {"hit": False, "score": 0, "info": "Insufficient data"}

        if length == 21:
            ma_series = metrics.get("ema_21") or self._ema(closes, 21)
            label = "21 EMA Pullback"
            trend_guard = metrics.get("above_50sma", False)
            tolerance = 1.5
        else:
            ma_series = metrics.get("sma_50")
            label = "50 SMA Pullback"
            trend_guard = metrics.get("above_200sma", False)
            tolerance = 3.0

        if not ma_series or ma_series[-1] in (None, 0):
            return {"hit": False, "score": 0, "info": "MA unavailable"}

        ma_value = ma_series[-1]
        price = closes[-1]
        prev_close = closes[-2] if len(closes) >= 2 else price
        distance_pct = ((price - ma_value) / ma_value) * 100

        if distance_pct < -tolerance or distance_pct > tolerance:
            return {"hit": False, "score": 0, "info": f"Distance {distance_pct:.2f}%"}
        if price <= prev_close:
            return {"hit": False, "score": 0, "info": "No bounce confirmation"}
        if not trend_guard:
            return {"hit": False, "score": 0, "info": "Trend guard failed"}

        score = 6.5 + max(0, tolerance - abs(distance_pct)) * 0.4
        score = min(9.0, score)

        return {
            "hit": True,
            "score": round(score, 1),
            "info": f"Δ{distance_pct:.2f}% vs MA",
            "name": label
        }

    def _calculate_rs_rating(self, stock_closes: List[float], spy_closes: List[float]) -> Dict[str, float]:
        """Calculate Relative Strength vs SPY"""
        if len(spy_closes) < 61 or len(stock_closes) < 61:
            return {"rs": 0, "bonus": 0}

        # Compare 60-day performance
        stock_now = stock_closes[-1]
        stock_prev = stock_closes[-61]
        spy_now = spy_closes[-1]
        spy_prev = spy_closes[-61]

        stock_return = (stock_now - stock_prev) / stock_prev
        spy_return = (spy_now - spy_prev) / spy_prev
        relative = (stock_return - spy_return) * 100

        bonus = 2 if relative > 15 else 1 if relative > 5 else 0

        return {"rs": round(relative, 1), "bonus": bonus}

    def _analyze_volatility_contractions(self, closes: List[float]) -> Dict[str, Any]:
        """Analyze volatility contractions in price action"""
        if len(closes) < 20:
            return {"count": 0, "pulls": []}

        window = closes[-80:]  # Last 80 days
        highs = []
        lows = []

        # Find local highs and lows
        for i in range(2, len(window) - 2):
            if (window[i] > window[i-1] and window[i] > window[i-2] and
                window[i] > window[i+1] and window[i] > window[i+2]):
                highs.append(i)
            if (window[i] < window[i-1] and window[i] < window[i-2] and
                window[i] < window[i+1] and window[i] < window[i+2]):
                lows.append(i)

        pulls = []
        for low_idx in lows:
            # Find preceding high
            high_idx = None
            for h in reversed(highs):
                if h < low_idx:
                    high_idx = h
                    break

            if high_idx is not None:
                high_price = window[high_idx]
                low_price = window[low_idx]
                decline = ((high_price - low_price) / high_price) * 100
                if decline > 0:
                    pulls.append(decline)

        return {"count": len(pulls), "pulls": pulls}

    def _check_volume_increasing(self, volumes: List[float]) -> bool:
        """Check if volume is increasing"""
        if len(volumes) < 20:
            return False
        recent_5 = sum(volumes[-5:]) / 5
        prev_15 = sum(volumes[-20:-5]) / 15
        return recent_5 > prev_15

    def _check_volume_dry_up(self, volumes: List[float]) -> bool:
        """Check for volume dry-up on pullbacks"""
        if len(volumes) < 50:
            return False
        short_avg = sum(volumes[-10:]) / 10
        long_avg = sum(volumes[-50:]) / 50
        return short_avg < long_avg * 0.7  # 30% below normal

    def _calculate_entry_stop_target(self, pattern_type: str, closes: List[float],
                                   highs: List[float], lows: List[float]) -> tuple[float, float, float]:
        """Calculate entry, stop, and target prices"""
        current_price = closes[-1]

        # Entry: Recent high (last 10 days) or current price
        recent_high = max(highs[-10:]) if len(highs) >= 10 else max(highs)
        entry = recent_high if recent_high > current_price else current_price

        # Stop: Recent low (last 20 days) or 7% below entry
        recent_low = min(lows[-20:]) if len(lows) >= 20 else min(lows)
        stop = recent_low if recent_low < entry * 0.93 else entry * 0.93

        # Target: 15% above entry
        target = entry * 1.15

        return entry, stop, target

    def _sma(self, values: List[float], period: int) -> List[Optional[float]]:
        """Simple Moving Average"""
        result = []
        for i in range(len(values)):
            if i < period - 1:
                result.append(None)
            else:
                avg = sum(values[i-period+1:i+1]) / period
                result.append(avg)
        return result

    def _ema(self, values: List[float], period: int) -> List[float]:
        """Exponential Moving Average"""
        if not values:
            return []

        k = 2 / (period + 1)
        result = [values[0]]  # First EMA is just the first value

        for i in range(1, len(values)):
            ema = values[i] * k + result[-1] * (1 - k)
            result.append(ema)

        return result

    def _create_insufficient_data_result(self, ticker: str, closes: List[float]) -> PatternResult:
        """Create result for insufficient data"""
        current_price = closes[-1] if closes else 0
        recent_high = max(closes[-10:]) if len(closes) >= 10 else current_price
        recent_low = min(closes[-20:]) if len(closes) >= 20 else current_price * 0.93
        target = recent_high * 1.15 if recent_high > 0 else current_price * 1.15

        return PatternResult(
            ticker=ticker,
            pattern="NONE",
            score=0,
            entry=round(recent_high, 2),
            stop=round(recent_low, 2),
            target=round(target, 2),
            risk_reward=round((target - recent_high) / (recent_high - recent_low), 2) if recent_high > recent_low else 0,
            criteria_met=[],
            analysis=f"Insufficient price history (need ≥60 candles, have {len(closes)})",
            timestamp=datetime.now(),
            current_price=round(current_price, 2)
        )

    def _create_pattern_result(self, ticker: str, pattern_data: Dict[str, Any],
                              closes: List[float], highs: List[float], lows: List[float],
                              volumes: List[float], metrics: Dict[str, Any],
                              rs_data: Optional[Dict[str, Any]]) -> PatternResult:
        """Create PatternResult for detected pattern"""
        entry, stop, target = self._calculate_entry_stop_target(
            pattern_data["name"], closes, highs, lows
        )

        # Calculate risk/reward ratio
        risk = entry - stop
        reward = target - entry
        rr = reward / risk if risk > 0 else 0

        # Add RS bonus to score
        final_score = pattern_data["score"]
        if rs_data:
            final_score = min(10, final_score + rs_data["bonus"])

        # Generate criteria met list
        criteria = []
        if metrics["contractions"]["count"] >= 3:
            criteria.append(f"✓ {metrics['contractions']['count']} volatility contractions detected")
        if metrics["above_50sma"]:
            criteria.append("✓ Above 50-day SMA")
        if metrics["above_200sma"]:
            criteria.append("✓ Above 200-day SMA")
        if metrics["volume_dry_up"]:
            criteria.append("✓ Volume dry-up on pullbacks")
        if rs_data and rs_data["rs"] >= 70:
            criteria.append(f"✓ Strong RS rating ({rs_data['rs']})")
        if not criteria:
            criteria.append("✓ Pattern meets core criteria")

        return PatternResult(
            ticker=ticker,
            pattern=pattern_data["name"],
            score=round(final_score, 1),
            entry=round(entry, 2),
            stop=round(stop, 2),
            target=round(target, 2),
            risk_reward=round(rr, 2),
            criteria_met=criteria,
            analysis=pattern_data["info"],
            timestamp=datetime.now(),
            rs_rating=rs_data["rs"] if rs_data else None,
            current_price=round(metrics["current_price"], 2),
            support_start=round(metrics["support_start"], 2),
            support_end=round(metrics["support_end"], 2),
            volume_increasing=metrics["volume_increasing"],
            consolidation_days=metrics["contractions"]["count"] * 3
        )

    def _create_no_pattern_result(self, ticker: str, closes: List[float], highs: List[float],
                                 lows: List[float], volumes: List[float], metrics: Dict[str, Any],
                                 rs_data: Optional[Dict[str, Any]]) -> PatternResult:
        """Create PatternResult when no pattern detected"""
        entry, stop, target = self._calculate_entry_stop_target("NONE", closes, highs, lows)

        risk = entry - stop
        reward = target - entry
        rr = reward / risk if risk > 0 else 0

        # Generate reasons why no pattern
        reasons = []
        if not metrics["above_50sma"]:
            reasons.append("✗ Below 50-day SMA")
        if not metrics["above_200sma"]:
            reasons.append("✗ Below 200-day SMA")
        if metrics["contractions"]["count"] < 3:
            reasons.append(f"✗ Only {metrics['contractions']['count']} contraction(s) (need 3+)")
        if not metrics["volume_dry_up"]:
            reasons.append("✗ Volume not decreasing on pullbacks")
        if rs_data and rs_data["rs"] < 70:
            reasons.append(f"✗ RS rating below threshold ({rs_data['rs']})")
        if not reasons:
            reasons.append("No specific issues detected")

        return PatternResult(
            ticker=ticker,
            pattern="NONE",
            score=0,
            entry=round(entry, 2),
            stop=round(stop, 2),
            target=round(target, 2),
            risk_reward=round(rr, 2),
            criteria_met=reasons,
            analysis="No Minervini patterns detected",
            timestamp=datetime.now(),
            rs_rating=rs_data["rs"] if rs_data else None,
            current_price=round(metrics["current_price"], 2),
            support_start=round(metrics["support_start"], 2),
            support_end=round(metrics["support_end"], 2),
            volume_increasing=metrics["volume_increasing"],
            consolidation_days=metrics["contractions"]["count"] * 3
        )
