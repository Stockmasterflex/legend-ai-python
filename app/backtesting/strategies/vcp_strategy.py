"""
VCP (Volatility Contraction Pattern) Strategy
Based on Mark Minervini's VCP pattern
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
import pandas as pd
import sys
import os

# Add parent directory to path to import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from app.backtesting.strategy import Strategy, Signal, SignalType


class VCPStrategy(Strategy):
    """
    VCP Strategy Implementation

    Entry: When VCP pattern completes and price breaks above pivot
    Exit: Stop loss or profit target
    Position Sizing: Based on ATR risk
    """

    def __init__(self, name: str = "VCP Strategy", parameters: Optional[Dict[str, Any]] = None):
        """Initialize VCP strategy"""
        default_params = {
            "min_score": 70.0,  # Minimum VCP score
            "risk_per_trade": 0.02,  # 2% risk per trade
            "reward_ratio": 3.0,  # 3R profit target
            "stop_multiplier": 2.0,  # Stop loss: 2x ATR below entry
            "volume_confirm": True,  # Require volume confirmation
            "min_consolidation_days": 15,  # Minimum consolidation period
        }

        if parameters:
            default_params.update(parameters)

        super().__init__(name, default_params)

    async def on_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        timestamp: datetime,
        portfolio_value: float,
        cash: float,
    ) -> List[Signal]:
        """Generate trading signals based on VCP pattern"""
        signals = []

        # Need at least 60 bars for VCP analysis
        if len(data) < 60:
            return signals

        # Update indicators
        self.update_indicators(ticker, data)

        # Get current price
        current_price = data.iloc[-1]["close"]
        prev_close = data.iloc[-2]["close"] if len(data) > 1 else current_price

        # Check for VCP pattern
        vcp_detected, vcp_score = self._detect_vcp(ticker, data)

        # Entry logic: VCP pattern + breakout
        if ticker not in self.current_positions:
            if vcp_detected and vcp_score >= self.get_parameter("min_score"):
                # Check for breakout (price breaking above recent high)
                pivot_high = data["high"].rolling(20).max().iloc[-1]

                if current_price > pivot_high and prev_close <= pivot_high:
                    # Volume confirmation
                    volume_ok = True
                    if self.get_parameter("volume_confirm"):
                        avg_volume = data["volume"].rolling(20).mean().iloc[-1]
                        volume_ok = data.iloc[-1]["volume"] > avg_volume * 1.5

                    if volume_ok:
                        # Calculate stop loss and take profit
                        atr = self._calculate_atr(data, period=14)
                        stop_multiplier = self.get_parameter("stop_multiplier")
                        reward_ratio = self.get_parameter("reward_ratio")

                        stop_loss = current_price - (atr * stop_multiplier)
                        risk = current_price - stop_loss
                        take_profit = current_price + (risk * reward_ratio)

                        signal = Signal(
                            type=SignalType.BUY,
                            ticker=ticker,
                            timestamp=timestamp,
                            price=current_price,
                            stop_loss=stop_loss,
                            take_profit=take_profit,
                            confidence=vcp_score / 100.0,
                            reason=f"VCP breakout (score: {vcp_score:.1f})",
                            metadata={"vcp_score": vcp_score, "atr": atr},
                        )
                        signals.append(signal)

        # Exit logic
        else:
            position = self.current_positions[ticker]

            # Trail stop loss if in profit
            if current_price > position["entry_price"] * 1.1:  # 10% profit
                # Trailing stop at entry (breakeven)
                signal = Signal(
                    type=SignalType.CLOSE,
                    ticker=ticker,
                    timestamp=timestamp,
                    price=current_price,
                    reason="Trailing stop triggered",
                )
                signals.append(signal)

        return signals

    async def calculate_position_size(
        self,
        signal: Signal,
        portfolio_value: float,
        cash: float,
        current_price: float,
    ) -> int:
        """Calculate position size based on risk management"""
        risk_pct = self.get_parameter("risk_per_trade")

        if signal.stop_loss:
            # Calculate shares based on fixed risk amount
            risk_amount = portfolio_value * risk_pct
            risk_per_share = abs(current_price - signal.stop_loss)

            if risk_per_share > 0:
                shares = int(risk_amount / risk_per_share)
            else:
                shares = 0
        else:
            # No stop loss defined, use 10% of portfolio
            max_position_value = portfolio_value * 0.1
            shares = int(max_position_value / current_price)

        # Cap by available cash
        max_shares_by_cash = int(cash / current_price)
        shares = min(shares, max_shares_by_cash)

        return max(0, shares)

    def _detect_vcp(self, ticker: str, data: pd.DataFrame) -> tuple:
        """
        Detect VCP pattern
        Returns (is_vcp, score)
        """
        # Simplified VCP detection
        # In production, integrate with existing VCPDetector from app/core/detectors/vcp_detector.py

        score = 0.0

        # 1. Check for uptrend (50+ higher than 200 SMA)
        sma_50 = data["close"].rolling(50).mean().iloc[-1]
        sma_200 = data["close"].rolling(200).mean().iloc[-1]

        if sma_50 > sma_200:
            score += 25

        # 2. Check for contracting volatility
        volatility_20 = data["close"].rolling(20).std()
        volatility_decreasing = volatility_20.iloc[-1] < volatility_20.iloc[-20]

        if volatility_decreasing:
            score += 25

        # 3. Check for tight consolidation
        recent_range = (data["high"].iloc[-20:].max() - data["low"].iloc[-20:].min())
        price_range_pct = (recent_range / data["close"].iloc[-1]) * 100

        if price_range_pct < 15:  # Less than 15% range
            score += 25

        # 4. Check for volume dry-up
        avg_volume_early = data["volume"].iloc[-60:-20].mean()
        avg_volume_recent = data["volume"].iloc[-20:].mean()

        if avg_volume_recent < avg_volume_early * 0.7:  # 30% reduction
            score += 25

        is_vcp = score >= self.get_parameter("min_score")

        return is_vcp, score

    def _calculate_atr(self, data: pd.DataFrame, period: int = 14) -> float:
        """Calculate Average True Range"""
        high = data["high"]
        low = data["low"]
        close = data["close"]

        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(period).mean().iloc[-1]

        return atr

    def update_indicators(self, ticker: str, data: pd.DataFrame):
        """Calculate indicators for VCP strategy"""
        super().update_indicators(ticker, data)

        if ticker not in self.indicators:
            self.indicators[ticker] = {}

        # SMAs
        self.indicators[ticker]["sma_50"] = data["close"].rolling(50).mean()
        self.indicators[ticker]["sma_200"] = data["close"].rolling(200).mean()

        # Volume
        self.indicators[ticker]["volume_avg_20"] = data["volume"].rolling(20).mean()

        # Volatility
        self.indicators[ticker]["volatility_20"] = data["close"].rolling(20).std()
