"""
Data collection pipeline for ML pattern detection.

Collects historical data and labels patterns for training.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import asyncio
from dataclasses import dataclass, asdict
import json
from pathlib import Path

from app.services.market_data import MarketDataService
from app.core.detectors.vcp_detector import VCPDetector
from app.core.detectors.cup_handle_detector import CupHandleDetector
from app.core.detectors.triangle_detector import TriangleDetector
from app.core.detectors.wedge_detector import WedgeDetector
from app.core.detectors.head_shoulders_detector import HeadShouldersDetector
from app.core.detectors.double_top_bottom_detector import DoubleTopBottomDetector
from app.ml.features.feature_engineering import FeatureEngineer


@dataclass
class LabeledPattern:
    """Labeled pattern instance for training."""
    ticker: str
    pattern_type: str
    window_start: str
    window_end: str
    features: Dict[str, float]
    label: int  # 1 for successful pattern, 0 for failed
    success_metric: Optional[float] = None  # % gain after breakout
    confidence_score: Optional[float] = None
    metadata: Optional[Dict] = None


class DataCollector:
    """Collects and labels historical pattern data for ML training."""

    def __init__(self, market_data_service: MarketDataService):
        self.market_data = market_data_service
        self.feature_engineer = FeatureEngineer()
        self.detectors = {
            'VCP': VCPDetector(),
            'CUP_HANDLE': CupHandleDetector(),
            'TRIANGLE': TriangleDetector(),
            'WEDGE': WedgeDetector(),
            'HEAD_SHOULDERS': HeadShouldersDetector(),
            'DOUBLE_TOP_BOTTOM': DoubleTopBottomDetector(),
        }
        self.data_dir = Path('data/ml_training')
        self.data_dir.mkdir(parents=True, exist_ok=True)

    async def collect_historical_data(
        self,
        tickers: List[str],
        years: int = 10,
        interval: str = '1day'
    ) -> pd.DataFrame:
        """
        Collect historical OHLCV data for multiple tickers.

        Args:
            tickers: List of ticker symbols
            years: Number of years of historical data
            interval: Time interval (1day, 1hour, etc.)

        Returns:
            DataFrame with multi-ticker historical data
        """
        all_data = []

        for ticker in tickers:
            try:
                # Fetch historical data
                data = await self.market_data.get_historical_data(
                    ticker=ticker,
                    interval=interval,
                    outputsize='full'
                )

                if data and 'values' in data:
                    df = pd.DataFrame(data['values'])
                    df['ticker'] = ticker
                    df['datetime'] = pd.to_datetime(df['datetime'])

                    # Convert to numeric
                    for col in ['open', 'high', 'low', 'close', 'volume']:
                        df[col] = pd.to_numeric(df[col], errors='coerce')

                    # Filter to requested time period
                    cutoff_date = datetime.now() - timedelta(days=years * 365)
                    df = df[df['datetime'] >= cutoff_date]

                    all_data.append(df)

                await asyncio.sleep(0.1)  # Rate limiting

            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
                continue

        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            return combined_df
        return pd.DataFrame()

    async def detect_patterns_in_history(
        self,
        df: pd.DataFrame,
        pattern_types: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Detect patterns in historical data using rule-based detectors.

        Args:
            df: Historical OHLCV data
            pattern_types: List of pattern types to detect (None = all)

        Returns:
            List of detected pattern instances
        """
        if pattern_types is None:
            pattern_types = list(self.detectors.keys())

        detected_patterns = []

        # Group by ticker
        for ticker, ticker_df in df.groupby('ticker'):
            ticker_df = ticker_df.sort_values('datetime').reset_index(drop=True)

            # Use sliding window to detect patterns at different time points
            window_size = 100
            step_size = 20

            for i in range(0, len(ticker_df) - window_size, step_size):
                window_df = ticker_df.iloc[i:i + window_size].copy()

                for pattern_name in pattern_types:
                    detector = self.detectors.get(pattern_name)
                    if detector is None:
                        continue

                    try:
                        result = detector.detect(window_df)

                        if result and result.score > 0.5:  # Only high-confidence detections
                            detected_patterns.append({
                                'ticker': ticker,
                                'pattern_type': pattern_name,
                                'window_start': str(window_df.iloc[0]['datetime']),
                                'window_end': str(window_df.iloc[-1]['datetime']),
                                'score': result.score,
                                'entry': result.entry,
                                'stop': result.stop,
                                'target': result.target,
                                'window_index': i
                            })
                    except Exception as e:
                        # Skip patterns that fail detection
                        continue

        return detected_patterns

    def label_pattern_success(
        self,
        df: pd.DataFrame,
        pattern_info: Dict,
        lookforward_days: int = 30
    ) -> Tuple[int, float]:
        """
        Label whether a detected pattern was successful.

        A pattern is successful if:
        1. Price reached target before hitting stop loss
        2. Positive return within lookforward period

        Args:
            df: Historical data for the ticker
            pattern_info: Pattern detection information
            lookforward_days: Days to look forward for success

        Returns:
            Tuple of (label, success_metric) where label is 0/1
        """
        ticker = pattern_info['ticker']
        window_end = pd.to_datetime(pattern_info['window_end'])

        # Get data after pattern detection
        ticker_df = df[df['ticker'] == ticker].copy()
        ticker_df['datetime'] = pd.to_datetime(ticker_df['datetime'])
        ticker_df = ticker_df.sort_values('datetime')

        future_df = ticker_df[ticker_df['datetime'] > window_end].head(lookforward_days)

        if future_df.empty:
            return 0, 0.0

        entry = pattern_info.get('entry')
        stop = pattern_info.get('stop')
        target = pattern_info.get('target')

        if entry is None or stop is None or target is None:
            return 0, 0.0

        # Check if target was reached before stop loss
        max_price = future_df['high'].max()
        min_price = future_df['low'].min()

        target_reached = max_price >= target
        stop_hit = min_price <= stop

        # Success if target reached before stop, or target reached at all
        if target_reached and not stop_hit:
            success_metric = ((target - entry) / entry) * 100
            return 1, success_metric
        elif target_reached:
            # Target reached but stop also hit - partial success
            success_metric = ((target - entry) / entry) * 100 * 0.5
            return 1, success_metric
        elif stop_hit:
            # Stop hit first - failure
            success_metric = ((stop - entry) / entry) * 100
            return 0, success_metric
        else:
            # Neither reached - check overall performance
            final_price = future_df.iloc[-1]['close']
            success_metric = ((final_price - entry) / entry) * 100

            # Consider success if > 5% gain
            label = 1 if success_metric > 5.0 else 0
            return label, success_metric

    async def create_labeled_dataset(
        self,
        tickers: List[str],
        years: int = 10,
        examples_per_pattern: int = 100
    ) -> List[LabeledPattern]:
        """
        Create labeled dataset for ML training.

        Args:
            tickers: List of ticker symbols
            years: Years of historical data
            examples_per_pattern: Target number of examples per pattern type

        Returns:
            List of labeled pattern instances
        """
        # Collect historical data
        print(f"Collecting {years} years of data for {len(tickers)} tickers...")
        df = await self.collect_historical_data(tickers, years)

        if df.empty:
            return []

        # Detect patterns
        print("Detecting patterns in historical data...")
        detected_patterns = await self.detect_patterns_in_history(df)
        print(f"Found {len(detected_patterns)} pattern instances")

        # Label patterns and compute features
        labeled_patterns = []

        for pattern_info in detected_patterns:
            try:
                # Label success
                label, success_metric = self.label_pattern_success(df, pattern_info)

                # Get pattern window data
                ticker = pattern_info['ticker']
                window_start = pd.to_datetime(pattern_info['window_start'])
                window_end = pd.to_datetime(pattern_info['window_end'])

                ticker_df = df[df['ticker'] == ticker].copy()
                ticker_df['datetime'] = pd.to_datetime(ticker_df['datetime'])

                window_df = ticker_df[
                    (ticker_df['datetime'] >= window_start) &
                    (ticker_df['datetime'] <= window_end)
                ].copy()

                if window_df.empty:
                    continue

                # Compute features
                features_df = self.feature_engineer.compute_all_features(window_df)

                if features_df.empty:
                    continue

                # Use features from the last row (pattern completion point)
                feature_row = features_df.iloc[-1]
                feature_names = self.feature_engineer.get_feature_names(features_df)
                features_dict = {name: float(feature_row[name]) for name in feature_names if name in feature_row.index}

                # Create labeled pattern
                labeled_pattern = LabeledPattern(
                    ticker=ticker,
                    pattern_type=pattern_info['pattern_type'],
                    window_start=pattern_info['window_start'],
                    window_end=pattern_info['window_end'],
                    features=features_dict,
                    label=label,
                    success_metric=success_metric,
                    confidence_score=pattern_info.get('score'),
                    metadata={
                        'entry': pattern_info.get('entry'),
                        'stop': pattern_info.get('stop'),
                        'target': pattern_info.get('target')
                    }
                )

                labeled_patterns.append(labeled_pattern)

            except Exception as e:
                print(f"Error labeling pattern: {e}")
                continue

        # Balance dataset if needed
        labeled_patterns = self._balance_dataset(labeled_patterns, examples_per_pattern)

        # Save to disk
        self._save_labeled_dataset(labeled_patterns)

        return labeled_patterns

    def _balance_dataset(
        self,
        patterns: List[LabeledPattern],
        examples_per_pattern: int
    ) -> List[LabeledPattern]:
        """Balance dataset across pattern types and success/failure."""
        from collections import defaultdict

        # Group by pattern type and label
        grouped = defaultdict(lambda: {'success': [], 'failure': []})

        for pattern in patterns:
            key = 'success' if pattern.label == 1 else 'failure'
            grouped[pattern.pattern_type][key].append(pattern)

        # Sample from each group
        balanced = []

        for pattern_type, groups in grouped.items():
            success_patterns = groups['success']
            failure_patterns = groups['failure']

            # Take up to examples_per_pattern / 2 from each
            n_per_class = min(examples_per_pattern // 2, min(len(success_patterns), len(failure_patterns)))

            if n_per_class > 0:
                balanced.extend(np.random.choice(success_patterns, n_per_class, replace=False))
                balanced.extend(np.random.choice(failure_patterns, n_per_class, replace=False))

        return balanced

    def _save_labeled_dataset(self, patterns: List[LabeledPattern]):
        """Save labeled dataset to disk."""
        if not patterns:
            return

        # Convert to list of dicts
        data = [asdict(p) for p in patterns]

        # Save as JSON
        filepath = self.data_dir / f'labeled_patterns_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Saved {len(patterns)} labeled patterns to {filepath}")

        # Also save as CSV for easy inspection
        csv_filepath = filepath.with_suffix('.csv')
        df = pd.DataFrame(data)
        df.to_csv(csv_filepath, index=False)
        print(f"Saved CSV to {csv_filepath}")

    def load_labeled_dataset(self, filepath: Optional[str] = None) -> List[LabeledPattern]:
        """Load labeled dataset from disk."""
        if filepath is None:
            # Load most recent file
            json_files = list(self.data_dir.glob('labeled_patterns_*.json'))
            if not json_files:
                return []
            filepath = max(json_files, key=lambda p: p.stat().st_mtime)

        with open(filepath, 'r') as f:
            data = json.load(f)

        patterns = [LabeledPattern(**item) for item in data]
        return patterns
