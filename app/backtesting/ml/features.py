"""
Feature Engineering
Comprehensive feature extraction for ML models
"""

from typing import Dict, List, Optional, Callable
import pandas as pd
import numpy as np
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class FeatureConfig:
    """Feature engineering configuration"""
    feature_groups: List[str] = None  # ["price", "technical", "volume", "pattern", "sentiment"]
    lookback_periods: List[int] = None  # [5, 10, 20, 50, 200]
    include_ratios: bool = True
    include_lagged: bool = True
    lag_periods: List[int] = None  # [1, 2, 3, 5]


class PriceFeatures:
    """Price-based features"""

    @staticmethod
    def calculate(data: pd.DataFrame, periods: List[int] = None) -> pd.DataFrame:
        """
        Calculate price-based features

        Args:
            data: OHLCV DataFrame
            periods: Lookback periods

        Returns:
            DataFrame with price features
        """
        if periods is None:
            periods = [5, 10, 20, 50, 200]

        features = pd.DataFrame(index=data.index)

        # Returns
        features["return_1d"] = data["close"].pct_change(1)
        features["return_5d"] = data["close"].pct_change(5)
        features["return_10d"] = data["close"].pct_change(10)
        features["return_20d"] = data["close"].pct_change(20)

        # Log returns
        features["log_return_1d"] = np.log(data["close"] / data["close"].shift(1))

        # Price position within range
        for period in periods:
            if period <= len(data):
                rolling_min = data["low"].rolling(period).min()
                rolling_max = data["high"].rolling(period).max()
                features[f"price_position_{period}d"] = (
                    (data["close"] - rolling_min) / (rolling_max - rolling_min)
                )

        # Gap features
        features["gap"] = (data["open"] - data["close"].shift(1)) / data["close"].shift(1)
        features["gap_up"] = (features["gap"] > 0).astype(int)
        features["gap_down"] = (features["gap"] < 0).astype(int)

        # Intraday range
        features["intraday_range"] = (data["high"] - data["low"]) / data["close"]
        features["upper_shadow"] = (data["high"] - data[["open", "close"]].max(axis=1)) / data["close"]
        features["lower_shadow"] = (data[["open", "close"]].min(axis=1) - data["low"]) / data["close"]

        # Body size
        features["body_size"] = abs(data["close"] - data["open"]) / data["close"]
        features["is_green"] = (data["close"] > data["open"]).astype(int)

        return features


class TechnicalFeatures:
    """Technical indicator features"""

    @staticmethod
    def calculate(data: pd.DataFrame, periods: List[int] = None) -> pd.DataFrame:
        """
        Calculate technical indicator features

        Args:
            data: OHLCV DataFrame
            periods: Lookback periods

        Returns:
            DataFrame with technical features
        """
        if periods is None:
            periods = [5, 10, 20, 50, 200]

        features = pd.DataFrame(index=data.index)

        # Moving averages
        for period in periods:
            if period <= len(data):
                features[f"sma_{period}"] = data["close"].rolling(period).mean()
                features[f"ema_{period}"] = data["close"].ewm(span=period, adjust=False).mean()

                # Price vs MA
                features[f"close_vs_sma_{period}"] = (
                    (data["close"] - features[f"sma_{period}"]) / features[f"sma_{period}"]
                )

        # RSI
        for period in [14, 28]:
            if period <= len(data):
                delta = data["close"].diff()
                gain = (delta.where(delta > 0, 0)).rolling(period).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
                rs = gain / loss
                features[f"rsi_{period}"] = 100 - (100 / (1 + rs))

        # MACD
        if 26 <= len(data):
            ema12 = data["close"].ewm(span=12, adjust=False).mean()
            ema26 = data["close"].ewm(span=26, adjust=False).mean()
            features["macd"] = ema12 - ema26
            features["macd_signal"] = features["macd"].ewm(span=9, adjust=False).mean()
            features["macd_histogram"] = features["macd"] - features["macd_signal"]

        # Bollinger Bands
        for period in [20]:
            if period <= len(data):
                sma = data["close"].rolling(period).mean()
                std = data["close"].rolling(period).std()
                features[f"bb_upper_{period}"] = sma + (2 * std)
                features[f"bb_lower_{period}"] = sma - (2 * std)
                features[f"bb_width_{period}"] = (features[f"bb_upper_{period}"] - features[f"bb_lower_{period}"]) / sma
                features[f"bb_position_{period}"] = (data["close"] - features[f"bb_lower_{period}"]) / (
                    features[f"bb_upper_{period}"] - features[f"bb_lower_{period}"]
                )

        # ATR (Average True Range)
        for period in [14]:
            if period <= len(data):
                high_low = data["high"] - data["low"]
                high_close = abs(data["high"] - data["close"].shift())
                low_close = abs(data["low"] - data["close"].shift())
                true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
                features[f"atr_{period}"] = true_range.rolling(period).mean()
                features[f"atr_pct_{period}"] = features[f"atr_{period}"] / data["close"]

        # Momentum
        for period in [10, 20]:
            if period <= len(data):
                features[f"momentum_{period}"] = data["close"] - data["close"].shift(period)

        # Rate of Change (ROC)
        for period in [10, 20]:
            if period <= len(data):
                features[f"roc_{period}"] = (
                    (data["close"] - data["close"].shift(period)) / data["close"].shift(period) * 100
                )

        # Stochastic Oscillator
        for period in [14]:
            if period <= len(data):
                low_min = data["low"].rolling(period).min()
                high_max = data["high"].rolling(period).max()
                features[f"stoch_k_{period}"] = (
                    (data["close"] - low_min) / (high_max - low_min) * 100
                )
                features[f"stoch_d_{period}"] = features[f"stoch_k_{period}"].rolling(3).mean()

        return features


class VolumeFeatures:
    """Volume-based features"""

    @staticmethod
    def calculate(data: pd.DataFrame, periods: List[int] = None) -> pd.DataFrame:
        """
        Calculate volume features

        Args:
            data: OHLCV DataFrame
            periods: Lookback periods

        Returns:
            DataFrame with volume features
        """
        if periods is None:
            periods = [5, 10, 20, 50]

        features = pd.DataFrame(index=data.index)

        # Volume ratios
        for period in periods:
            if period <= len(data):
                features[f"volume_sma_{period}"] = data["volume"].rolling(period).mean()
                features[f"volume_ratio_{period}"] = data["volume"] / features[f"volume_sma_{period}"]

        # Volume change
        features["volume_change_1d"] = data["volume"].pct_change(1)
        features["volume_change_5d"] = data["volume"].pct_change(5)

        # OBV (On-Balance Volume)
        obv = (np.sign(data["close"].diff()) * data["volume"]).fillna(0).cumsum()
        features["obv"] = obv
        for period in [10, 20]:
            if period <= len(data):
                features[f"obv_sma_{period}"] = obv.rolling(period).mean()

        # Volume-weighted features
        features["vwap_1d"] = (data["close"] * data["volume"]).rolling(1).sum() / data["volume"].rolling(1).sum()

        # Money Flow Index (MFI)
        for period in [14]:
            if period <= len(data):
                typical_price = (data["high"] + data["low"] + data["close"]) / 3
                money_flow = typical_price * data["volume"]

                positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(period).sum()
                negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(period).sum()

                mfi_ratio = positive_flow / negative_flow
                features[f"mfi_{period}"] = 100 - (100 / (1 + mfi_ratio))

        return features


class PatternFeatures:
    """Pattern recognition features"""

    @staticmethod
    def calculate(data: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate pattern features

        Args:
            data: OHLCV DataFrame

        Returns:
            DataFrame with pattern features
        """
        features = pd.DataFrame(index=data.index)

        # Trend features
        features["higher_high"] = ((data["high"] > data["high"].shift(1)) &
                                   (data["high"].shift(1) > data["high"].shift(2))).astype(int)
        features["lower_low"] = ((data["low"] < data["low"].shift(1)) &
                                 (data["low"].shift(1) < data["low"].shift(2))).astype(int)

        # Candlestick patterns (simplified)
        body = abs(data["close"] - data["open"])
        body_avg = body.rolling(20).mean()

        # Doji
        features["doji"] = (body < body_avg * 0.1).astype(int)

        # Hammer
        lower_shadow = data[["open", "close"]].min(axis=1) - data["low"]
        features["hammer"] = ((lower_shadow > body * 2) & (data["close"] > data["open"])).astype(int)

        # Shooting star
        upper_shadow = data["high"] - data[["open", "close"]].max(axis=1)
        features["shooting_star"] = ((upper_shadow > body * 2) & (data["close"] < data["open"])).astype(int)

        # Engulfing
        features["bullish_engulfing"] = (
            (data["close"] > data["open"]) &
            (data["close"].shift(1) < data["open"].shift(1)) &
            (data["close"] > data["open"].shift(1)) &
            (data["open"] < data["close"].shift(1))
        ).astype(int)

        return features


class FeatureEngineer:
    """
    Comprehensive feature engineering pipeline
    """

    def __init__(self, config: Optional[FeatureConfig] = None):
        """
        Initialize feature engineer

        Args:
            config: Feature configuration
        """
        self.config = config or FeatureConfig()

        if self.config.feature_groups is None:
            self.config.feature_groups = ["price", "technical", "volume", "pattern"]

        if self.config.lookback_periods is None:
            self.config.lookback_periods = [5, 10, 20, 50, 200]

        if self.config.lag_periods is None:
            self.config.lag_periods = [1, 2, 3, 5]

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Transform OHLCV data into ML features

        Args:
            data: OHLCV DataFrame

        Returns:
            DataFrame with engineered features
        """
        all_features = [data[["open", "high", "low", "close", "volume"]].copy()]

        # Price features
        if "price" in self.config.feature_groups:
            logger.debug("Calculating price features...")
            price_features = PriceFeatures.calculate(data, self.config.lookback_periods)
            all_features.append(price_features)

        # Technical features
        if "technical" in self.config.feature_groups:
            logger.debug("Calculating technical features...")
            technical_features = TechnicalFeatures.calculate(data, self.config.lookback_periods)
            all_features.append(technical_features)

        # Volume features
        if "volume" in self.config.feature_groups:
            logger.debug("Calculating volume features...")
            volume_features = VolumeFeatures.calculate(data, self.config.lookback_periods)
            all_features.append(volume_features)

        # Pattern features
        if "pattern" in self.config.feature_groups:
            logger.debug("Calculating pattern features...")
            pattern_features = PatternFeatures.calculate(data)
            all_features.append(pattern_features)

        # Combine all features
        features_df = pd.concat(all_features, axis=1)

        # Add lagged features
        if self.config.include_lagged:
            features_df = self._add_lagged_features(features_df)

        # Add ratios
        if self.config.include_ratios:
            features_df = self._add_ratio_features(features_df)

        # Remove rows with NaN (from rolling calculations)
        features_df = features_df.dropna()

        logger.info(f"Generated {len(features_df.columns)} features from {len(data)} rows")

        return features_df

    def _add_lagged_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Add lagged versions of key features"""
        key_features = ["close", "volume", "return_1d"]

        for feature in key_features:
            if feature in features.columns:
                for lag in self.config.lag_periods:
                    features[f"{feature}_lag_{lag}"] = features[feature].shift(lag)

        return features

    def _add_ratio_features(self, features: pd.DataFrame) -> pd.DataFrame:
        """Add ratio features between correlated metrics"""
        # Example ratios (extend as needed)
        if "sma_20" in features.columns and "sma_50" in features.columns:
            features["sma_20_50_ratio"] = features["sma_20"] / features["sma_50"]

        if "volume_sma_20" in features.columns and "volume_sma_50" in features.columns:
            features["volume_20_50_ratio"] = features["volume_sma_20"] / features["volume_sma_50"]

        return features

    def create_labels(
        self,
        data: pd.DataFrame,
        target_type: str = "classification",
        forward_period: int = 5,
        threshold: float = 0.02,
    ) -> pd.Series:
        """
        Create labels for supervised learning

        Args:
            data: OHLCV DataFrame
            target_type: "classification" or "regression"
            forward_period: Days to look forward
            threshold: For classification, % threshold for up/down

        Returns:
            Series with labels
        """
        if target_type == "classification":
            # Binary: 1 = price up by threshold, 0 = otherwise
            future_return = data["close"].pct_change(forward_period).shift(-forward_period)
            labels = (future_return > threshold).astype(int)

        elif target_type == "regression":
            # Continuous: future return
            labels = data["close"].pct_change(forward_period).shift(-forward_period)

        else:
            raise ValueError(f"Unknown target_type: {target_type}")

        return labels

    def get_feature_names(self, features: pd.DataFrame) -> List[str]:
        """Get list of feature names"""
        # Exclude OHLCV columns
        exclude = ["open", "high", "low", "close", "volume"]
        return [col for col in features.columns if col not in exclude]
