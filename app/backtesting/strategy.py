"""
Strategy Definition Framework
Supports YAML, Python, and Visual strategy definitions
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

import pandas as pd
import yaml


class SignalType(str, Enum):
    """Trading signal types"""

    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"


@dataclass
class Signal:
    """Trading signal"""

    type: SignalType
    ticker: str
    timestamp: datetime
    price: float
    quantity: Optional[int] = None
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    confidence: float = 1.0
    reason: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate signal"""
        if self.confidence < 0 or self.confidence > 1:
            raise ValueError("Confidence must be between 0 and 1")
        if self.price <= 0:
            raise ValueError("Price must be positive")


class Strategy(ABC):
    """
    Base strategy class
    All strategies must inherit from this class
    """

    def __init__(self, name: str, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize strategy

        Args:
            name: Strategy name
            parameters: Strategy parameters
        """
        self.name = name
        self.parameters = parameters or {}
        self.current_positions: Dict[str, Any] = {}
        self.historical_data: Dict[str, pd.DataFrame] = {}
        self.indicators: Dict[str, Dict[str, pd.Series]] = {}

    @abstractmethod
    async def on_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        timestamp: datetime,
        portfolio_value: float,
        cash: float,
    ) -> List[Signal]:
        """
        Called on each bar of data

        Args:
            ticker: Stock ticker
            data: Historical price data (OHLCV)
            timestamp: Current timestamp
            portfolio_value: Current portfolio value
            cash: Available cash

        Returns:
            List of trading signals
        """

    @abstractmethod
    async def calculate_position_size(
        self,
        signal: Signal,
        portfolio_value: float,
        cash: float,
        current_price: float,
    ) -> int:
        """
        Calculate position size for a signal

        Args:
            signal: Trading signal
            portfolio_value: Current portfolio value
            cash: Available cash
            current_price: Current price

        Returns:
            Number of shares to trade
        """

    async def on_order_filled(
        self,
        signal: Signal,
        filled_price: float,
        filled_quantity: int,
        commission: float,
        slippage: float,
    ):
        """
        Called when an order is filled

        Args:
            signal: Original signal
            filled_price: Actual fill price
            filled_quantity: Actual quantity filled
            commission: Commission paid
            slippage: Slippage cost
        """
        # Update current positions
        if signal.type in [SignalType.BUY]:
            self.current_positions[signal.ticker] = {
                "quantity": filled_quantity,
                "entry_price": filled_price,
                "entry_time": signal.timestamp,
            }
        elif signal.type in [SignalType.SELL, SignalType.CLOSE]:
            if signal.ticker in self.current_positions:
                del self.current_positions[signal.ticker]

    async def on_bar(
        self,
        ticker: str,
        bar: Dict[str, float],
        timestamp: datetime,
    ):
        """
        Called on each new bar (optional override)

        Args:
            ticker: Stock ticker
            bar: OHLCV data for current bar
            timestamp: Bar timestamp
        """

    def get_parameter(self, key: str, default: Any = None) -> Any:
        """Get strategy parameter with default"""
        return self.parameters.get(key, default)

    def set_parameter(self, key: str, value: Any):
        """Set strategy parameter"""
        self.parameters[key] = value

    def update_indicators(self, ticker: str, data: pd.DataFrame):
        """
        Update technical indicators for a ticker
        Override this method to calculate custom indicators

        Args:
            ticker: Stock ticker
            data: Historical price data
        """
        if ticker not in self.indicators:
            self.indicators[ticker] = {}

    def get_indicator(self, ticker: str, indicator_name: str) -> Optional[pd.Series]:
        """Get indicator value for a ticker"""
        return self.indicators.get(ticker, {}).get(indicator_name)


class YAMLStrategy(Strategy):
    """
    Strategy defined using YAML configuration
    """

    def __init__(
        self, name: str, yaml_config: str, parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize YAML strategy

        Args:
            name: Strategy name
            yaml_config: YAML configuration string
            parameters: Override parameters
        """
        super().__init__(name, parameters)
        self.config = yaml.safe_load(yaml_config)
        self._parse_config()

    def _parse_config(self):
        """Parse YAML configuration"""
        # Extract strategy parameters
        if "parameters" in self.config:
            for key, value in self.config["parameters"].items():
                if key not in self.parameters:
                    self.parameters[key] = value

        # Parse entry rules
        self.entry_rules = self.config.get("entry_rules", {})
        self.exit_rules = self.config.get("exit_rules", {})
        self.risk_management = self.config.get("risk_management", {})

    async def on_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        timestamp: datetime,
        portfolio_value: float,
        cash: float,
    ) -> List[Signal]:
        """Evaluate YAML rules and generate signals"""
        signals = []

        # Update indicators
        self.update_indicators(ticker, data)

        # Check entry rules
        if ticker not in self.current_positions:
            if self._evaluate_entry_rules(ticker, data, timestamp):
                signal = Signal(
                    type=SignalType.BUY,
                    ticker=ticker,
                    timestamp=timestamp,
                    price=data.iloc[-1]["close"],
                    reason="YAML entry rules satisfied",
                )
                signals.append(signal)

        # Check exit rules
        else:
            if self._evaluate_exit_rules(ticker, data, timestamp):
                signal = Signal(
                    type=SignalType.SELL,
                    ticker=ticker,
                    timestamp=timestamp,
                    price=data.iloc[-1]["close"],
                    reason="YAML exit rules satisfied",
                )
                signals.append(signal)

        return signals

    def _evaluate_entry_rules(
        self, ticker: str, data: pd.DataFrame, timestamp: datetime
    ) -> bool:
        """Evaluate entry rules from YAML config"""
        if not self.entry_rules:
            return False

        # Implement rule evaluation logic
        # This is a simplified version - can be extended with a full rule engine
        conditions = self.entry_rules.get("conditions", [])
        operator = self.entry_rules.get("operator", "AND")

        results = []
        for condition in conditions:
            result = self._evaluate_condition(condition, ticker, data)
            results.append(result)

        if operator == "AND":
            return all(results)
        elif operator == "OR":
            return any(results)
        else:
            return False

    def _evaluate_exit_rules(
        self, ticker: str, data: pd.DataFrame, timestamp: datetime
    ) -> bool:
        """Evaluate exit rules from YAML config"""
        if not self.exit_rules:
            return False

        conditions = self.exit_rules.get("conditions", [])
        operator = self.exit_rules.get("operator", "OR")

        results = []
        for condition in conditions:
            result = self._evaluate_condition(condition, ticker, data)
            results.append(result)

        if operator == "AND":
            return all(results)
        elif operator == "OR":
            return any(results)
        else:
            return False

    def _evaluate_condition(
        self, condition: Dict[str, Any], ticker: str, data: pd.DataFrame
    ) -> bool:
        """Evaluate a single condition"""
        indicator = condition.get("indicator")
        operator = condition.get("operator")
        value = condition.get("value")

        if indicator and operator and value is not None:
            ind_value = self.get_indicator(ticker, indicator)
            if ind_value is None or len(ind_value) == 0:
                return False

            current_value = ind_value.iloc[-1]

            if operator == ">":
                return current_value > value
            elif operator == "<":
                return current_value < value
            elif operator == ">=":
                return current_value >= value
            elif operator == "<=":
                return current_value <= value
            elif operator == "==":
                return current_value == value
            elif operator == "crosses_above":
                if len(ind_value) < 2:
                    return False
                return ind_value.iloc[-2] <= value < ind_value.iloc[-1]
            elif operator == "crosses_below":
                if len(ind_value) < 2:
                    return False
                return ind_value.iloc[-2] >= value > ind_value.iloc[-1]

        return False

    async def calculate_position_size(
        self,
        signal: Signal,
        portfolio_value: float,
        cash: float,
        current_price: float,
    ) -> int:
        """Calculate position size based on risk management rules"""
        risk_pct = self.risk_management.get("risk_per_trade", 0.02)  # Default 2%
        max_position_pct = self.risk_management.get(
            "max_position_size", 0.1
        )  # Default 10%

        # Calculate based on risk
        if signal.stop_loss:
            risk_per_share = abs(current_price - signal.stop_loss)
            if risk_per_share > 0:
                risk_amount = portfolio_value * risk_pct
                shares = int(risk_amount / risk_per_share)
            else:
                shares = 0
        else:
            # No stop loss, use max position size
            max_position_value = portfolio_value * max_position_pct
            shares = int(max_position_value / current_price)

        # Cap by available cash
        max_shares_by_cash = int(cash / current_price)
        shares = min(shares, max_shares_by_cash)

        return max(0, shares)

    def update_indicators(self, ticker: str, data: pd.DataFrame):
        """Calculate indicators specified in YAML config"""
        super().update_indicators(ticker, data)

        indicators_config = self.config.get("indicators", [])

        for ind_config in indicators_config:
            ind_name = ind_config.get("name")
            ind_type = ind_config.get("type")
            params = ind_config.get("parameters", {})

            if ind_type == "SMA":
                period = params.get("period", 20)
                self.indicators[ticker][ind_name] = (
                    data["close"].rolling(window=period).mean()
                )

            elif ind_type == "EMA":
                period = params.get("period", 20)
                self.indicators[ticker][ind_name] = (
                    data["close"].ewm(span=period, adjust=False).mean()
                )

            elif ind_type == "RSI":
                period = params.get("period", 14)
                delta = data["close"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
                rs = gain / loss
                self.indicators[ticker][ind_name] = 100 - (100 / (1 + rs))

            elif ind_type == "PRICE":
                self.indicators[ticker][ind_name] = data["close"]

            elif ind_type == "VOLUME":
                self.indicators[ticker][ind_name] = data["volume"]


class PythonStrategy(Strategy):
    """
    Strategy defined using Python code
    Executes user-provided Python code
    """

    def __init__(
        self, name: str, python_code: str, parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize Python strategy

        Args:
            name: Strategy name
            python_code: Python code defining the strategy
            parameters: Strategy parameters
        """
        super().__init__(name, parameters)
        self.python_code = python_code
        self._strategy_instance = None
        self._load_strategy()

    def _load_strategy(self):
        """Load and instantiate the Python strategy"""
        # Create a namespace for the strategy
        namespace = {
            "Strategy": Strategy,
            "Signal": Signal,
            "SignalType": SignalType,
            "pd": pd,
            "datetime": datetime,
        }

        # Execute the Python code
        exec(self.python_code, namespace)

        # Find the strategy class (should be named 'CustomStrategy')
        strategy_class = namespace.get("CustomStrategy")
        if strategy_class:
            self._strategy_instance = strategy_class(self.name, self.parameters)
        else:
            raise ValueError("Python code must define a 'CustomStrategy' class")

    async def on_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        timestamp: datetime,
        portfolio_value: float,
        cash: float,
    ) -> List[Signal]:
        """Delegate to Python strategy instance"""
        if self._strategy_instance:
            return await self._strategy_instance.on_data(
                ticker, data, timestamp, portfolio_value, cash
            )
        return []

    async def calculate_position_size(
        self,
        signal: Signal,
        portfolio_value: float,
        cash: float,
        current_price: float,
    ) -> int:
        """Delegate to Python strategy instance"""
        if self._strategy_instance:
            return await self._strategy_instance.calculate_position_size(
                signal, portfolio_value, cash, current_price
            )
        return 0


class VisualStrategy(Strategy):
    """
    Strategy defined using visual builder
    Uses a JSON configuration from the visual builder
    """

    def __init__(
        self,
        name: str,
        visual_config: Dict[str, Any],
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize visual strategy

        Args:
            name: Strategy name
            visual_config: Visual builder configuration (JSON)
            parameters: Strategy parameters
        """
        super().__init__(name, parameters)
        self.visual_config = visual_config
        self._parse_visual_config()

    def _parse_visual_config(self):
        """Parse visual builder configuration"""
        self.blocks = self.visual_config.get("blocks", [])
        self.connections = self.visual_config.get("connections", [])

        # Build execution graph
        self.entry_conditions = []
        self.exit_conditions = []
        self.risk_rules = {}

        for block in self.blocks:
            block_type = block.get("type")
            block_config = block.get("config", {})

            if block_type == "entry_condition":
                self.entry_conditions.append(block_config)
            elif block_type == "exit_condition":
                self.exit_conditions.append(block_config)
            elif block_type == "risk_management":
                self.risk_rules.update(block_config)

    async def on_data(
        self,
        ticker: str,
        data: pd.DataFrame,
        timestamp: datetime,
        portfolio_value: float,
        cash: float,
    ) -> List[Signal]:
        """Execute visual strategy blocks"""
        signals = []

        # Update indicators
        self.update_indicators(ticker, data)

        # Check entry conditions
        if ticker not in self.current_positions:
            if self._evaluate_visual_conditions(self.entry_conditions, ticker, data):
                signal = Signal(
                    type=SignalType.BUY,
                    ticker=ticker,
                    timestamp=timestamp,
                    price=data.iloc[-1]["close"],
                    reason="Visual entry conditions satisfied",
                )
                signals.append(signal)

        # Check exit conditions
        else:
            if self._evaluate_visual_conditions(self.exit_conditions, ticker, data):
                signal = Signal(
                    type=SignalType.SELL,
                    ticker=ticker,
                    timestamp=timestamp,
                    price=data.iloc[-1]["close"],
                    reason="Visual exit conditions satisfied",
                )
                signals.append(signal)

        return signals

    def _evaluate_visual_conditions(
        self,
        conditions: List[Dict[str, Any]],
        ticker: str,
        data: pd.DataFrame,
    ) -> bool:
        """Evaluate visual builder conditions"""
        if not conditions:
            return False

        results = []
        for condition in conditions:
            # Similar to YAML condition evaluation
            result = self._evaluate_condition(condition, ticker, data)
            results.append(result)

        # Default to AND logic
        return all(results)

    def _evaluate_condition(
        self, condition: Dict[str, Any], ticker: str, data: pd.DataFrame
    ) -> bool:
        """Evaluate a single visual condition"""
        # Similar to YAMLStrategy._evaluate_condition
        # Implement based on visual builder block structure
        return True  # Placeholder

    async def calculate_position_size(
        self,
        signal: Signal,
        portfolio_value: float,
        cash: float,
        current_price: float,
    ) -> int:
        """Calculate position size from visual risk rules"""
        risk_pct = self.risk_rules.get("risk_per_trade", 0.02)
        max_position_pct = self.risk_rules.get("max_position_size", 0.1)

        # Similar to YAMLStrategy position sizing
        if signal.stop_loss:
            risk_per_share = abs(current_price - signal.stop_loss)
            if risk_per_share > 0:
                risk_amount = portfolio_value * risk_pct
                shares = int(risk_amount / risk_per_share)
            else:
                shares = 0
        else:
            max_position_value = portfolio_value * max_position_pct
            shares = int(max_position_value / current_price)

        max_shares_by_cash = int(cash / current_price)
        shares = min(shares, max_shares_by_cash)

        return max(0, shares)

    def update_indicators(self, ticker: str, data: pd.DataFrame):
        """Calculate indicators from visual blocks"""
        super().update_indicators(ticker, data)

        for block in self.blocks:
            if block.get("type") == "indicator":
                ind_config = block.get("config", {})
                ind_name = ind_config.get("name")
                ind_type = ind_config.get("indicator_type")
                params = ind_config.get("parameters", {})

                # Calculate indicator (similar to YAML)
                if ind_type == "SMA":
                    period = params.get("period", 20)
                    self.indicators[ticker][ind_name] = (
                        data["close"].rolling(window=period).mean()
                    )
                # ... other indicators
