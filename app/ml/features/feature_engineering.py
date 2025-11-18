"""
Feature engineering for ML pattern detection.

Computes 20+ technical indicators and features from OHLCV data.
"""

import pandas as pd
import numpy as np
from typing import Optional
from scipy import stats as scipy_stats


class FeatureEngineer:
    """Computes technical indicators and features for ML models."""

    def __init__(self):
        self.feature_names = []

    def compute_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Compute all features from OHLCV data.

        Args:
            df: DataFrame with columns: open, high, low, close, volume

        Returns:
            DataFrame with all computed features
        """
        if df.empty or len(df) < 50:
            return pd.DataFrame()

        features_df = df.copy()

        # Price action features
        features_df = self._compute_price_features(features_df)

        # Volume features
        features_df = self._compute_volume_features(features_df)

        # Technical indicators
        features_df = self._compute_technical_indicators(features_df)

        # Trend features
        features_df = self._compute_trend_features(features_df)

        # Volatility features
        features_df = self._compute_volatility_features(features_df)

        # Pattern-specific features
        features_df = self._compute_pattern_features(features_df)

        # Market context features
        features_df = self._compute_market_context_features(features_df)

        # Drop rows with NaN values (from indicator calculation)
        features_df = features_df.dropna()

        return features_df

    def _compute_price_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute price action features."""
        # Basic price metrics
        df['price_range'] = df['high'] - df['low']
        df['body'] = abs(df['close'] - df['open'])
        df['upper_wick'] = df['high'] - df[['close', 'open']].max(axis=1)
        df['lower_wick'] = df[['close', 'open']].min(axis=1) - df['low']

        # Price changes
        df['price_change'] = df['close'].pct_change()
        df['price_change_5'] = df['close'].pct_change(periods=5)
        df['price_change_10'] = df['close'].pct_change(periods=10)
        df['price_change_20'] = df['close'].pct_change(periods=20)

        # High/low ranges
        df['high_low_ratio'] = df['high'] / df['low']
        df['close_high_ratio'] = df['close'] / df['high']
        df['close_low_ratio'] = df['close'] / df['low']

        # Distance from highs/lows
        df['dist_from_52w_high'] = (df['high'].rolling(252).max() - df['close']) / df['close']
        df['dist_from_52w_low'] = (df['close'] - df['low'].rolling(252).min()) / df['close']

        return df

    def _compute_volume_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute volume-based features."""
        # Volume changes
        df['volume_change'] = df['volume'].pct_change()
        df['volume_ma_5'] = df['volume'].rolling(5).mean()
        df['volume_ma_20'] = df['volume'].rolling(20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_ma_20']

        # On-Balance Volume (OBV)
        df['obv'] = (np.sign(df['close'].diff()) * df['volume']).cumsum()
        df['obv_ma_20'] = df['obv'].rolling(20).mean()
        df['obv_slope'] = df['obv'].diff(5) / 5

        # Volume-price correlation
        df['vp_corr_10'] = df['close'].rolling(10).corr(df['volume'])
        df['vp_corr_20'] = df['close'].rolling(20).corr(df['volume'])

        # Volume profile
        df['volume_z_score'] = (df['volume'] - df['volume'].rolling(20).mean()) / df['volume'].rolling(20).std()

        return df

    def _compute_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute standard technical indicators."""
        # Moving Averages
        df['sma_10'] = df['close'].rolling(10).mean()
        df['sma_20'] = df['close'].rolling(20).mean()
        df['sma_50'] = df['close'].rolling(50).mean()
        df['sma_200'] = df['close'].rolling(200).mean()

        # EMA
        df['ema_12'] = df['close'].ewm(span=12).mean()
        df['ema_26'] = df['close'].ewm(span=26).mean()

        # MACD
        df['macd'] = df['ema_12'] - df['ema_26']
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # RSI
        df['rsi'] = self._compute_rsi(df['close'], 14)
        df['rsi_ma'] = df['rsi'].rolling(5).mean()

        # Bollinger Bands
        bb_period = 20
        df['bb_middle'] = df['close'].rolling(bb_period).mean()
        bb_std = df['close'].rolling(bb_period).std()
        df['bb_upper'] = df['bb_middle'] + (2 * bb_std)
        df['bb_lower'] = df['bb_middle'] - (2 * bb_std)
        df['bb_width'] = (df['bb_upper'] - df['bb_lower']) / df['bb_middle']
        df['bb_position'] = (df['close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])

        # Stochastic
        df['stoch_k'] = self._compute_stochastic(df, 14)
        df['stoch_d'] = df['stoch_k'].rolling(3).mean()

        # ADX (Average Directional Index)
        df = self._compute_adx(df, 14)

        # ATR (Average True Range)
        df['atr'] = self._compute_atr(df, 14)
        df['atr_percent'] = df['atr'] / df['close']

        return df

    def _compute_trend_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute trend-related features."""
        # Price position relative to SMAs
        df['price_sma_10_ratio'] = df['close'] / df['sma_10']
        df['price_sma_20_ratio'] = df['close'] / df['sma_20']
        df['price_sma_50_ratio'] = df['close'] / df['sma_50']
        df['price_sma_200_ratio'] = df['close'] / df['sma_200']

        # SMA relationships
        df['sma_10_20_cross'] = (df['sma_10'] > df['sma_20']).astype(int)
        df['sma_50_200_cross'] = (df['sma_50'] > df['sma_200']).astype(int)

        # Linear regression slope
        df['lr_slope_10'] = df['close'].rolling(10).apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[0] if len(x) == 10 else np.nan
        )
        df['lr_slope_20'] = df['close'].rolling(20).apply(
            lambda x: np.polyfit(np.arange(len(x)), x, 1)[0] if len(x) == 20 else np.nan
        )

        # Trend strength
        df['trend_strength_10'] = abs(df['lr_slope_10']) / df['close']
        df['trend_strength_20'] = abs(df['lr_slope_20']) / df['close']

        return df

    def _compute_volatility_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute volatility features."""
        # Historical volatility
        df['volatility_10'] = df['price_change'].rolling(10).std()
        df['volatility_20'] = df['price_change'].rolling(20).std()
        df['volatility_50'] = df['price_change'].rolling(50).std()

        # Volatility ratio
        df['volatility_ratio'] = df['volatility_10'] / df['volatility_50']

        # Parkinson's volatility (high-low)
        df['parkinson_vol'] = np.sqrt(
            (1 / (4 * np.log(2))) * ((np.log(df['high'] / df['low'])) ** 2).rolling(20).mean()
        )

        # Garman-Klass volatility
        df['gk_vol'] = np.sqrt(
            0.5 * ((np.log(df['high'] / df['low'])) ** 2).rolling(20).mean() -
            (2 * np.log(2) - 1) * ((np.log(df['close'] / df['open'])) ** 2).rolling(20).mean()
        )

        return df

    def _compute_pattern_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute pattern-specific features."""
        # Pivot points
        df['pivot'] = (df['high'] + df['low'] + df['close']) / 3
        df['r1'] = 2 * df['pivot'] - df['low']
        df['s1'] = 2 * df['pivot'] - df['high']

        # Higher highs / Lower lows
        df['higher_high'] = (df['high'] > df['high'].shift(1)).astype(int)
        df['lower_low'] = (df['low'] < df['low'].shift(1)).astype(int)

        # Consolidation detection
        df['consolidation_10'] = (df['high'].rolling(10).max() - df['low'].rolling(10).min()) / df['close']
        df['consolidation_20'] = (df['high'].rolling(20).max() - df['low'].rolling(20).min()) / df['close']

        # Breakout potential
        df['near_resistance'] = (df['high'].rolling(20).max() - df['close']) / df['close']
        df['near_support'] = (df['close'] - df['low'].rolling(20).min()) / df['close']

        return df

    def _compute_market_context_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute market context features."""
        # Price momentum
        df['momentum_5'] = df['close'] - df['close'].shift(5)
        df['momentum_10'] = df['close'] - df['close'].shift(10)
        df['momentum_20'] = df['close'] - df['close'].shift(20)

        # Rate of change
        df['roc_5'] = (df['close'] / df['close'].shift(5) - 1) * 100
        df['roc_10'] = (df['close'] / df['close'].shift(10) - 1) * 100
        df['roc_20'] = (df['close'] / df['close'].shift(20) - 1) * 100

        # Money flow index (simplified)
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        money_flow = typical_price * df['volume']
        df['mfi'] = self._compute_mfi(df, 14)

        return df

    # Helper methods for indicator calculation

    def _compute_rsi(self, series: pd.Series, period: int = 14) -> pd.Series:
        """Compute Relative Strength Index."""
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _compute_stochastic(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Compute Stochastic Oscillator %K."""
        low_min = df['low'].rolling(period).min()
        high_max = df['high'].rolling(period).max()
        stoch_k = 100 * (df['close'] - low_min) / (high_max - low_min)
        return stoch_k

    def _compute_atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Compute Average True Range."""
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(period).mean()
        return atr

    def _compute_adx(self, df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Compute Average Directional Index."""
        # Calculate +DM and -DM
        df['high_diff'] = df['high'].diff()
        df['low_diff'] = -df['low'].diff()

        df['plus_dm'] = np.where(
            (df['high_diff'] > df['low_diff']) & (df['high_diff'] > 0),
            df['high_diff'],
            0
        )
        df['minus_dm'] = np.where(
            (df['low_diff'] > df['high_diff']) & (df['low_diff'] > 0),
            df['low_diff'],
            0
        )

        # Calculate ATR
        atr = self._compute_atr(df, period)

        # Calculate +DI and -DI
        plus_di = 100 * (df['plus_dm'].rolling(period).mean() / atr)
        minus_di = 100 * (df['minus_dm'].rolling(period).mean() / atr)

        # Calculate DX and ADX
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di)
        df['adx'] = dx.rolling(period).mean()
        df['plus_di'] = plus_di
        df['minus_di'] = minus_di

        # Clean up temporary columns
        df.drop(['high_diff', 'low_diff', 'plus_dm', 'minus_dm'], axis=1, inplace=True)

        return df

    def _compute_mfi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Compute Money Flow Index."""
        typical_price = (df['high'] + df['low'] + df['close']) / 3
        money_flow = typical_price * df['volume']

        positive_flow = money_flow.where(typical_price > typical_price.shift(1), 0).rolling(period).sum()
        negative_flow = money_flow.where(typical_price < typical_price.shift(1), 0).rolling(period).sum()

        mfi_ratio = positive_flow / negative_flow
        mfi = 100 - (100 / (1 + mfi_ratio))

        return mfi

    def get_feature_names(self, df: pd.DataFrame) -> list[str]:
        """Get list of feature column names (excluding OHLCV)."""
        base_columns = {'open', 'high', 'low', 'close', 'volume'}
        return [col for col in df.columns if col not in base_columns]
