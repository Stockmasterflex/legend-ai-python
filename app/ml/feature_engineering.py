"""
Feature Engineering for Price Forecasting
Extracts technical indicators, volume profiles, sentiment, and market regime
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Any
from app.core.indicators import sma, ema, rsi
import logging

logger = logging.getLogger(__name__)


class FeatureEngineer:
    """
    Comprehensive feature engineering for price prediction models
    """

    def __init__(self):
        self.feature_names: List[str] = []

    def calculate_technical_indicators(
        self, df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Calculate comprehensive technical indicators

        Args:
            df: DataFrame with OHLCV data (columns: open, high, low, close, volume)

        Returns:
            DataFrame with added technical indicator columns
        """
        df = df.copy()

        # Price-based indicators
        df['returns'] = df['close'].pct_change()
        df['log_returns'] = np.log(df['close'] / df['close'].shift(1))

        # Moving Averages
        for period in [5, 10, 20, 50, 100, 200]:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
            df[f'ema_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
            df[f'price_to_sma_{period}'] = df['close'] / df[f'sma_{period}']

        # Bollinger Bands
        for period in [20, 50]:
            sma_val = df['close'].rolling(window=period).mean()
            std_val = df['close'].rolling(window=period).std()
            df[f'bb_upper_{period}'] = sma_val + (2 * std_val)
            df[f'bb_lower_{period}'] = sma_val - (2 * std_val)
            df[f'bb_width_{period}'] = (df[f'bb_upper_{period}'] - df[f'bb_lower_{period}']) / sma_val
            df[f'bb_position_{period}'] = (df['close'] - df[f'bb_lower_{period}']) / (df[f'bb_upper_{period}'] - df[f'bb_lower_{period}'])

        # RSI
        for period in [14, 21]:
            # Use pandas for easier calculation
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            df[f'rsi_{period}'] = 100 - (100 / (1 + rs))

        # MACD
        df['macd_line'] = df['close'].ewm(span=12, adjust=False).mean() - df['close'].ewm(span=26, adjust=False).mean()
        df['macd_signal'] = df['macd_line'].ewm(span=9, adjust=False).mean()
        df['macd_histogram'] = df['macd_line'] - df['macd_signal']

        # Stochastic Oscillator
        for period in [14, 21]:
            low_min = df['low'].rolling(window=period).min()
            high_max = df['high'].rolling(window=period).max()
            df[f'stoch_{period}'] = 100 * (df['close'] - low_min) / (high_max - low_min)
            df[f'stoch_signal_{period}'] = df[f'stoch_{period}'].rolling(window=3).mean()

        # ATR (Average True Range)
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        for period in [14, 21]:
            df[f'atr_{period}'] = df['tr'].rolling(window=period).mean()
            df[f'atr_percent_{period}'] = df[f'atr_{period}'] / df['close']

        # ADX (Average Directional Index)
        df['dm_plus'] = np.where(
            (df['high'] - df['high'].shift(1)) > (df['low'].shift(1) - df['low']),
            np.maximum(df['high'] - df['high'].shift(1), 0),
            0
        )
        df['dm_minus'] = np.where(
            (df['low'].shift(1) - df['low']) > (df['high'] - df['high'].shift(1)),
            np.maximum(df['low'].shift(1) - df['low'], 0),
            0
        )

        for period in [14]:
            atr = df['tr'].rolling(window=period).mean()
            di_plus = 100 * (df['dm_plus'].rolling(window=period).mean() / atr)
            di_minus = 100 * (df['dm_minus'].rolling(window=period).mean() / atr)
            dx = 100 * abs(di_plus - di_minus) / (di_plus + di_minus)
            df[f'adx_{period}'] = dx.rolling(window=period).mean()
            df[f'di_plus_{period}'] = di_plus
            df[f'di_minus_{period}'] = di_minus

        # Momentum indicators
        for period in [5, 10, 20]:
            df[f'momentum_{period}'] = df['close'] - df['close'].shift(period)
            df[f'roc_{period}'] = ((df['close'] - df['close'].shift(period)) / df['close'].shift(period)) * 100

        # Price patterns
        df['high_low_ratio'] = df['high'] / df['low']
        df['close_position'] = (df['close'] - df['low']) / (df['high'] - df['low'])

        return df

    def calculate_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate volume-based features and profiles

        Args:
            df: DataFrame with OHLCV data

        Returns:
            DataFrame with added volume features
        """
        df = df.copy()

        # Volume moving averages
        for period in [5, 10, 20, 50]:
            df[f'volume_sma_{period}'] = df['volume'].rolling(window=period).mean()
            df[f'volume_ratio_{period}'] = df['volume'] / df[f'volume_sma_{period}']

        # Volume trends
        df['volume_change'] = df['volume'].pct_change()
        df['volume_momentum'] = df['volume'] - df['volume'].shift(5)

        # OBV (On-Balance Volume)
        df['obv'] = (np.sign(df['close'].diff()) * df['volume']).fillna(0).cumsum()
        df['obv_ema'] = df['obv'].ewm(span=20, adjust=False).mean()

        # Volume Price Trend
        df['vpt'] = (df['volume'] * ((df['close'] - df['close'].shift(1)) / df['close'].shift(1))).fillna(0).cumsum()

        # Money Flow Index
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        money_flow = typical_price * df['volume']

        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0)
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0)

        for period in [14]:
            positive_mf = positive_flow.rolling(window=period).sum()
            negative_mf = negative_flow.rolling(window=period).sum()
            mfi = 100 - (100 / (1 + positive_mf / negative_mf))
            df[f'mfi_{period}'] = mfi

        # Volume weighted average price (VWAP)
        df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
        df['price_to_vwap'] = df['close'] / df['vwap']

        # Volume profile - relative to price movement
        df['volume_price_correlation'] = df['volume'].rolling(window=20).corr(df['close'])

        return df

    def detect_market_regime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detect market regime: bullish, bearish, ranging, or volatile

        Args:
            df: DataFrame with price and indicator data

        Returns:
            DataFrame with market regime columns
        """
        df = df.copy()

        # Trend detection
        if 'sma_50' in df.columns and 'sma_200' in df.columns:
            df['trend_long'] = np.where(df['sma_50'] > df['sma_200'], 1, -1)

        if 'sma_20' in df.columns and 'sma_50' in df.columns:
            df['trend_medium'] = np.where(df['sma_20'] > df['sma_50'], 1, -1)

        if 'ema_10' in df.columns and 'ema_20' in df.columns:
            df['trend_short'] = np.where(df['ema_10'] > df['ema_20'], 1, -1)

        # Volatility regime
        if 'atr_14' in df.columns:
            atr_percentile = df['atr_14'].rolling(window=100).apply(
                lambda x: pd.Series(x).rank(pct=True).iloc[-1] if len(x) > 0 else 0.5
            )
            df['volatility_regime'] = np.where(atr_percentile > 0.75, 'high',
                                              np.where(atr_percentile < 0.25, 'low', 'normal'))

        # ADX for trend strength
        if 'adx_14' in df.columns:
            df['trend_strength'] = np.where(df['adx_14'] > 25, 'strong',
                                           np.where(df['adx_14'] < 20, 'weak', 'moderate'))

        # Overall market regime classification
        conditions = []
        regimes = []

        # Strong bullish: uptrend + strong trend + not too volatile
        if all(col in df.columns for col in ['trend_long', 'adx_14']):
            conditions.append((df['trend_long'] == 1) & (df['adx_14'] > 25))
            regimes.append('bullish')

        # Strong bearish: downtrend + strong trend
        if all(col in df.columns for col in ['trend_long', 'adx_14']):
            conditions.append((df['trend_long'] == -1) & (df['adx_14'] > 25))
            regimes.append('bearish')

        # Ranging: weak trend
        if 'adx_14' in df.columns:
            conditions.append(df['adx_14'] < 20)
            regimes.append('ranging')

        # Volatile: high volatility
        if 'volatility_regime' in df.columns:
            conditions.append(df['volatility_regime'] == 'high')
            regimes.append('volatile')

        # Default to neutral
        df['market_regime'] = 'neutral'
        for condition, regime in zip(conditions, regimes):
            df.loc[condition, 'market_regime'] = regime

        return df

    def create_lagged_features(self, df: pd.DataFrame, columns: List[str], lags: List[int]) -> pd.DataFrame:
        """
        Create lagged features for time series

        Args:
            df: DataFrame with features
            columns: Column names to create lags for
            lags: List of lag periods

        Returns:
            DataFrame with lagged features
        """
        df = df.copy()

        for col in columns:
            if col in df.columns:
                for lag in lags:
                    df[f'{col}_lag_{lag}'] = df[col].shift(lag)

        return df

    def create_rolling_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        windows: List[int]
    ) -> pd.DataFrame:
        """
        Create rolling statistical features

        Args:
            df: DataFrame with features
            columns: Column names to create rolling stats for
            windows: List of window sizes

        Returns:
            DataFrame with rolling features
        """
        df = df.copy()

        for col in columns:
            if col in df.columns:
                for window in windows:
                    df[f'{col}_rolling_mean_{window}'] = df[col].rolling(window=window).mean()
                    df[f'{col}_rolling_std_{window}'] = df[col].rolling(window=window).std()
                    df[f'{col}_rolling_min_{window}'] = df[col].rolling(window=window).min()
                    df[f'{col}_rolling_max_{window}'] = df[col].rolling(window=window).max()

        return df

    def prepare_features(
        self,
        df: pd.DataFrame,
        include_lagged: bool = True,
        include_rolling: bool = True,
        sentiment_data: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        """
        Complete feature engineering pipeline

        Args:
            df: DataFrame with OHLCV data
            include_lagged: Whether to include lagged features
            include_rolling: Whether to include rolling features
            sentiment_data: Optional sentiment scores to include

        Returns:
            DataFrame with all engineered features
        """
        logger.info("Starting feature engineering pipeline")

        # Calculate technical indicators
        df = self.calculate_technical_indicators(df)

        # Calculate volume features
        df = self.calculate_volume_features(df)

        # Detect market regime
        df = self.detect_market_regime(df)

        # Add sentiment if provided
        if sentiment_data:
            df = self._add_sentiment_features(df, sentiment_data)

        # Create lagged features for key indicators
        if include_lagged:
            lag_columns = ['close', 'volume', 'returns', 'rsi_14', 'macd_histogram']
            df = self.create_lagged_features(df, lag_columns, lags=[1, 2, 3, 5, 10])

        # Create rolling features for volatility measures
        if include_rolling:
            roll_columns = ['returns', 'volume']
            df = self.create_rolling_features(df, roll_columns, windows=[5, 10, 20])

        # Store feature names (excluding original OHLCV)
        original_cols = ['open', 'high', 'low', 'close', 'volume', 'date', 'timestamp']
        self.feature_names = [col for col in df.columns if col not in original_cols]

        logger.info(f"Feature engineering complete. Generated {len(self.feature_names)} features")

        return df

    def _add_sentiment_features(self, df: pd.DataFrame, sentiment_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Add sentiment-based features

        Args:
            df: DataFrame with price data
            sentiment_data: Dictionary with sentiment scores

        Returns:
            DataFrame with sentiment features
        """
        df = df.copy()

        # Example sentiment features (placeholder - would be populated from real sentiment analysis)
        if 'news_sentiment' in sentiment_data:
            df['news_sentiment'] = sentiment_data['news_sentiment']

        if 'social_sentiment' in sentiment_data:
            df['social_sentiment'] = sentiment_data['social_sentiment']

        if 'analyst_rating' in sentiment_data:
            df['analyst_rating'] = sentiment_data['analyst_rating']

        return df

    def get_feature_importance_names(self) -> List[str]:
        """Get list of engineered feature names"""
        return self.feature_names

    def prepare_ml_dataset(
        self,
        df: pd.DataFrame,
        target_column: str = 'close',
        forecast_horizon: int = 1,
        test_size: float = 0.2
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Prepare dataset for ML training

        Args:
            df: DataFrame with features
            target_column: Column to predict
            forecast_horizon: How many periods ahead to predict
            test_size: Fraction of data to use for testing

        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        # Create target variable (future price)
        df = df.copy()
        df['target'] = df[target_column].shift(-forecast_horizon)

        # Remove rows with NaN values
        df = df.dropna()

        # Split features and target
        feature_cols = [col for col in df.columns if col not in [
            'target', 'open', 'high', 'low', 'close', 'volume',
            'date', 'timestamp', 'market_regime', 'volatility_regime', 'trend_strength'
        ]]

        X = df[feature_cols]
        y = df['target']

        # Train-test split (time-series aware - no shuffling)
        split_idx = int(len(df) * (1 - test_size))

        X_train = X.iloc[:split_idx]
        X_test = X.iloc[split_idx:]
        y_train = y.iloc[:split_idx]
        y_test = y.iloc[split_idx:]

        logger.info(f"Dataset prepared: Train size={len(X_train)}, Test size={len(X_test)}, Features={len(feature_cols)}")

        return X_train, X_test, y_train, y_test
