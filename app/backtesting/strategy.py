"""
Strategy Builder Framework
Defines base classes and interfaces for creating backtestable strategies
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List
import pandas as pd


class SignalType(Enum):
    """Trading signal types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    EXIT = "exit"


class PositionSizingMethod(Enum):
    """Position sizing methods"""
    FIXED_SHARES = "fixed_shares"  # Fixed number of shares
    FIXED_DOLLARS = "fixed_dollars"  # Fixed dollar amount
    PERCENT_CAPITAL = "percent_capital"  # Percentage of available capital
    RISK_BASED = "risk_based"  # Based on risk per trade (2% rule)
    KELLY_CRITERION = "kelly"  # Kelly criterion


class ExitReason(Enum):
    """Reasons for exiting a trade"""
    TARGET_HIT = "target"
    STOP_LOSS = "stop_loss"
    SIGNAL = "signal"  # Exit signal from strategy
    TIME_BASED = "time_based"  # Max holding period reached
    END_OF_PERIOD = "end_of_period"  # Backtest ended


@dataclass
class StrategySignal:
    """Trading signal with entry/exit details"""
    signal_type: SignalType
    timestamp: datetime
    price: float
    ticker: str

    # Entry signals
    stop_loss: Optional[float] = None
    target_price: Optional[float] = None
    confidence: float = 1.0  # 0-1 confidence score
    reason: str = ""
    metadata: Dict[str, Any] = None

    # Position sizing
    position_size: Optional[int] = None  # Shares to trade
    position_value: Optional[float] = None  # Dollar value

    # Exit signals
    exit_reason: Optional[ExitReason] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RiskManagementRules:
    """Risk management configuration"""
    max_position_size: float = 0.2  # Max 20% of portfolio per position
    max_portfolio_risk: float = 0.06  # Max 6% total portfolio risk
    risk_per_trade: float = 0.02  # 2% risk per trade
    max_correlation: float = 0.7  # Max correlation between positions
    max_sector_exposure: float = 0.3  # Max 30% in single sector
    use_trailing_stop: bool = False
    trailing_stop_percent: float = 0.05  # 5% trailing stop
    max_open_positions: int = 10
    min_risk_reward: float = 2.0  # Minimum 2:1 risk/reward ratio


class Strategy(ABC):
    """
    Base class for all trading strategies

    Strategies must implement:
    - generate_signals(): Analyze data and generate trading signals
    - calculate_position_size(): Determine position sizing
    """

    def __init__(
        self,
        name: str,
        description: str = "",
        position_sizing_method: PositionSizingMethod = PositionSizingMethod.RISK_BASED,
        risk_rules: Optional[RiskManagementRules] = None
    ):
        self.name = name
        self.description = description
        self.position_sizing_method = position_sizing_method
        self.risk_rules = risk_rules or RiskManagementRules()
        self.parameters: Dict[str, Any] = {}

    @abstractmethod
    def generate_signals(
        self,
        data: pd.DataFrame,
        ticker: str,
        current_positions: Dict[str, Any]
    ) -> List[StrategySignal]:
        """
        Generate trading signals from price data

        Args:
            data: OHLCV DataFrame with datetime index
            ticker: Stock ticker symbol
            current_positions: Dictionary of currently open positions

        Returns:
            List of StrategySignal objects
        """
        pass

    def calculate_position_size(
        self,
        signal: StrategySignal,
        current_capital: float,
        current_price: float,
        account_risk_pct: float = 0.02
    ) -> int:
        """
        Calculate position size based on strategy rules

        Args:
            signal: The trading signal
            current_capital: Available capital
            current_price: Current stock price
            account_risk_pct: Risk percentage (default 2%)

        Returns:
            Number of shares to trade
        """
        if self.position_sizing_method == PositionSizingMethod.FIXED_SHARES:
            return self.parameters.get("fixed_shares", 100)

        elif self.position_sizing_method == PositionSizingMethod.FIXED_DOLLARS:
            fixed_amount = self.parameters.get("fixed_dollars", 10000)
            return int(fixed_amount / current_price)

        elif self.position_sizing_method == PositionSizingMethod.PERCENT_CAPITAL:
            pct = self.parameters.get("capital_percent", 0.1)  # 10% default
            return int((current_capital * pct) / current_price)

        elif self.position_sizing_method == PositionSizingMethod.RISK_BASED:
            # Calculate position size based on risk per trade
            if signal.stop_loss is None:
                # Default to 5% stop if not provided
                stop_loss = current_price * 0.95
            else:
                stop_loss = signal.stop_loss

            risk_per_share = abs(current_price - stop_loss)
            if risk_per_share == 0:
                return 0

            dollar_risk = current_capital * account_risk_pct
            shares = int(dollar_risk / risk_per_share)

            # Apply max position size limit
            max_shares = int((current_capital * self.risk_rules.max_position_size) / current_price)
            return min(shares, max_shares)

        elif self.position_sizing_method == PositionSizingMethod.KELLY_CRITERION:
            # Simplified Kelly: f = (p*b - q) / b
            # where p = win rate, q = 1-p, b = avg_win/avg_loss
            win_rate = self.parameters.get("win_rate", 0.5)
            avg_win = self.parameters.get("avg_win", 0.1)
            avg_loss = self.parameters.get("avg_loss", 0.05)

            if avg_loss == 0:
                return 0

            b = avg_win / avg_loss
            kelly_pct = (win_rate * b - (1 - win_rate)) / b

            # Use half-Kelly for safety
            kelly_pct = max(0, kelly_pct * 0.5)
            kelly_pct = min(kelly_pct, self.risk_rules.max_position_size)

            return int((current_capital * kelly_pct) / current_price)

        return 0

    def validate_signal(
        self,
        signal: StrategySignal,
        current_positions: Dict[str, Any],
        portfolio_value: float
    ) -> bool:
        """
        Validate signal against risk management rules

        Args:
            signal: Trading signal to validate
            current_positions: Currently open positions
            portfolio_value: Total portfolio value

        Returns:
            True if signal passes validation
        """
        # Check max open positions
        if len(current_positions) >= self.risk_rules.max_open_positions:
            return False

        # Check minimum risk/reward ratio
        if signal.stop_loss and signal.target_price:
            risk = abs(signal.price - signal.stop_loss)
            reward = abs(signal.target_price - signal.price)
            if risk > 0 and (reward / risk) < self.risk_rules.min_risk_reward:
                return False

        # Check max position value
        if signal.position_value:
            max_value = portfolio_value * self.risk_rules.max_position_size
            if signal.position_value > max_value:
                return False

        return True

    def set_parameters(self, **kwargs):
        """Set strategy parameters"""
        self.parameters.update(kwargs)

    def get_config(self) -> Dict[str, Any]:
        """Get strategy configuration as dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "position_sizing_method": self.position_sizing_method.value,
            "risk_rules": {
                "max_position_size": self.risk_rules.max_position_size,
                "risk_per_trade": self.risk_rules.risk_per_trade,
                "max_open_positions": self.risk_rules.max_open_positions,
                "min_risk_reward": self.risk_rules.min_risk_reward,
            },
            "parameters": self.parameters
        }


class PatternBasedStrategy(Strategy):
    """
    Strategy based on pattern detection (VCP, Cup & Handle, etc.)
    Uses existing pattern detector from core.pattern_detector
    """

    def __init__(
        self,
        name: str = "Pattern Based Strategy",
        pattern_types: Optional[List[str]] = None,
        min_pattern_score: float = 7.0,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.pattern_types = pattern_types or ["vcp", "cup_and_handle"]
        self.min_pattern_score = min_pattern_score
        self.set_parameters(
            pattern_types=self.pattern_types,
            min_pattern_score=min_pattern_score
        )

    def generate_signals(
        self,
        data: pd.DataFrame,
        ticker: str,
        current_positions: Dict[str, Any]
    ) -> List[StrategySignal]:
        """Generate signals based on pattern detection"""
        from app.core.pattern_detector import PatternDetector

        signals = []

        # Initialize pattern detector
        detector = PatternDetector(data, ticker)

        # Check for patterns
        for pattern_type in self.pattern_types:
            if pattern_type == "vcp":
                result = detector.detect_vcp()
            elif pattern_type == "cup_and_handle":
                result = detector.detect_cup_and_handle()
            elif pattern_type == "sma50_pullback":
                result = detector.detect_sma50_pullback()
            else:
                continue

            # Generate signal if pattern found with sufficient score
            if result.get("detected", False) and result.get("score", 0) >= self.min_pattern_score:
                current_price = data['close'].iloc[-1]

                # Create buy signal
                signal = StrategySignal(
                    signal_type=SignalType.BUY,
                    timestamp=data.index[-1],
                    price=current_price,
                    ticker=ticker,
                    stop_loss=result.get("stop_price"),
                    target_price=result.get("target_price"),
                    confidence=result.get("score", 0) / 10.0,
                    reason=f"{pattern_type} pattern detected (score: {result.get('score')})",
                    metadata={"pattern_result": result}
                )
                signals.append(signal)

        # Check for exit signals on open positions
        if ticker in current_positions:
            position = current_positions[ticker]
            current_price = data['close'].iloc[-1]

            # Exit if target hit
            if position.get("target_price") and current_price >= position["target_price"]:
                signals.append(StrategySignal(
                    signal_type=SignalType.EXIT,
                    timestamp=data.index[-1],
                    price=current_price,
                    ticker=ticker,
                    exit_reason=ExitReason.TARGET_HIT,
                    reason="Target price reached"
                ))

            # Exit if stop loss hit
            elif position.get("stop_loss") and current_price <= position["stop_loss"]:
                signals.append(StrategySignal(
                    signal_type=SignalType.EXIT,
                    timestamp=data.index[-1],
                    price=current_price,
                    ticker=ticker,
                    exit_reason=ExitReason.STOP_LOSS,
                    reason="Stop loss triggered"
                ))

        return signals


class IndicatorBasedStrategy(Strategy):
    """
    Strategy based on technical indicators (RSI, MACD, Moving Averages, etc.)
    """

    def __init__(
        self,
        name: str = "Indicator Based Strategy",
        use_rsi: bool = True,
        rsi_oversold: float = 30,
        rsi_overbought: float = 70,
        use_macd: bool = True,
        use_ma_cross: bool = True,
        fast_ma: int = 20,
        slow_ma: int = 50,
        **kwargs
    ):
        super().__init__(name, **kwargs)
        self.set_parameters(
            use_rsi=use_rsi,
            rsi_oversold=rsi_oversold,
            rsi_overbought=rsi_overbought,
            use_macd=use_macd,
            use_ma_cross=use_ma_cross,
            fast_ma=fast_ma,
            slow_ma=slow_ma
        )

    def generate_signals(
        self,
        data: pd.DataFrame,
        ticker: str,
        current_positions: Dict[str, Any]
    ) -> List[StrategySignal]:
        """Generate signals based on technical indicators"""
        signals = []

        # Ensure we have required indicators
        if 'rsi' not in data.columns or 'macd' not in data.columns:
            return signals

        current_price = data['close'].iloc[-1]
        current_time = data.index[-1]

        # Entry signals (if not in position)
        if ticker not in current_positions:
            buy_conditions = []

            # RSI oversold
            if self.parameters.get("use_rsi") and data['rsi'].iloc[-1] < self.parameters["rsi_oversold"]:
                buy_conditions.append("RSI oversold")

            # MACD bullish crossover
            if self.parameters.get("use_macd"):
                if len(data) > 1:
                    macd_prev = data['macd'].iloc[-2]
                    macd_signal_prev = data['macd_signal'].iloc[-2]
                    macd_curr = data['macd'].iloc[-1]
                    macd_signal_curr = data['macd_signal'].iloc[-1]

                    if macd_prev < macd_signal_prev and macd_curr > macd_signal_curr:
                        buy_conditions.append("MACD bullish crossover")

            # Moving average crossover
            if self.parameters.get("use_ma_cross"):
                fast_ma = self.parameters["fast_ma"]
                slow_ma = self.parameters["slow_ma"]

                if f'sma_{fast_ma}' in data.columns and f'sma_{slow_ma}' in data.columns:
                    if len(data) > 1:
                        fast_prev = data[f'sma_{fast_ma}'].iloc[-2]
                        slow_prev = data[f'sma_{slow_ma}'].iloc[-2]
                        fast_curr = data[f'sma_{fast_ma}'].iloc[-1]
                        slow_curr = data[f'sma_{slow_ma}'].iloc[-1]

                        if fast_prev < slow_prev and fast_curr > slow_curr:
                            buy_conditions.append(f"MA{fast_ma}/{slow_ma} golden cross")

            # Generate buy signal if conditions met
            if len(buy_conditions) >= 2:  # Require at least 2 confirmations
                # Calculate stop loss (e.g., below recent swing low or 5%)
                stop_loss = current_price * 0.95
                target_price = current_price * 1.15  # 15% target

                signal = StrategySignal(
                    signal_type=SignalType.BUY,
                    timestamp=current_time,
                    price=current_price,
                    ticker=ticker,
                    stop_loss=stop_loss,
                    target_price=target_price,
                    confidence=min(len(buy_conditions) / 3, 1.0),
                    reason=", ".join(buy_conditions)
                )
                signals.append(signal)

        # Exit signals (if in position)
        else:
            position = current_positions[ticker]
            exit_conditions = []

            # RSI overbought
            if self.parameters.get("use_rsi") and data['rsi'].iloc[-1] > self.parameters["rsi_overbought"]:
                exit_conditions.append("RSI overbought")

            # MACD bearish crossover
            if self.parameters.get("use_macd"):
                if len(data) > 1:
                    macd_prev = data['macd'].iloc[-2]
                    macd_signal_prev = data['macd_signal'].iloc[-2]
                    macd_curr = data['macd'].iloc[-1]
                    macd_signal_curr = data['macd_signal'].iloc[-1]

                    if macd_prev > macd_signal_prev and macd_curr < macd_signal_curr:
                        exit_conditions.append("MACD bearish crossover")

            # Generate exit signal if conditions met
            if exit_conditions or current_price >= position.get("target_price", float('inf')):
                signal = StrategySignal(
                    signal_type=SignalType.EXIT,
                    timestamp=current_time,
                    price=current_price,
                    ticker=ticker,
                    exit_reason=ExitReason.SIGNAL if exit_conditions else ExitReason.TARGET_HIT,
                    reason=", ".join(exit_conditions) if exit_conditions else "Target reached"
                )
                signals.append(signal)

        return signals
