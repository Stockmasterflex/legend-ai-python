"""
Manual pattern labeling system for ML training.

Provides tools for manually reviewing and labeling patterns.
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path
import json
from datetime import datetime


class ManualLabeler:
    """Manual labeling interface for pattern validation."""

    def __init__(self, data_dir: str = 'data/ml_training'):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.labels_file = self.data_dir / 'manual_labels.json'
        self.labels = self._load_labels()

    def _load_labels(self) -> Dict:
        """Load existing manual labels."""
        if self.labels_file.exists():
            with open(self.labels_file, 'r') as f:
                return json.load(f)
        return {'patterns': []}

    def _save_labels(self):
        """Save manual labels to disk."""
        with open(self.labels_file, 'w') as f:
            json.dump(self.labels, f, indent=2)

    def add_label(
        self,
        ticker: str,
        pattern_type: str,
        window_start: str,
        window_end: str,
        label: int,
        notes: Optional[str] = None,
        quality_score: Optional[int] = None
    ):
        """
        Add a manual label for a pattern.

        Args:
            ticker: Stock ticker
            pattern_type: Type of pattern
            window_start: Start date of pattern window
            window_end: End date of pattern window
            label: 1 for successful, 0 for failed
            notes: Optional notes about the pattern
            quality_score: Optional quality score (1-5)
        """
        label_entry = {
            'ticker': ticker,
            'pattern_type': pattern_type,
            'window_start': window_start,
            'window_end': window_end,
            'label': label,
            'notes': notes,
            'quality_score': quality_score,
            'labeled_at': datetime.now().isoformat(),
            'labeled_by': 'manual'
        }

        self.labels['patterns'].append(label_entry)
        self._save_labels()

    def get_labels(self, pattern_type: Optional[str] = None) -> List[Dict]:
        """
        Get manual labels, optionally filtered by pattern type.

        Args:
            pattern_type: Optional pattern type filter

        Returns:
            List of manual labels
        """
        patterns = self.labels['patterns']

        if pattern_type:
            patterns = [p for p in patterns if p['pattern_type'] == pattern_type]

        return patterns

    def export_for_training(self) -> pd.DataFrame:
        """
        Export manual labels in format suitable for training.

        Returns:
            DataFrame with manual labels
        """
        if not self.labels['patterns']:
            return pd.DataFrame()

        df = pd.DataFrame(self.labels['patterns'])
        return df

    def get_label_statistics(self) -> Dict:
        """
        Get statistics about manual labels.

        Returns:
            Dictionary with label statistics
        """
        patterns = self.labels['patterns']

        if not patterns:
            return {
                'total': 0,
                'by_pattern_type': {},
                'by_label': {},
                'average_quality': None
            }

        df = pd.DataFrame(patterns)

        stats = {
            'total': len(patterns),
            'by_pattern_type': df['pattern_type'].value_counts().to_dict(),
            'by_label': df['label'].value_counts().to_dict(),
            'average_quality': df['quality_score'].mean() if 'quality_score' in df.columns else None
        }

        return stats

    def create_labeling_batch(
        self,
        pattern_data: List[Dict],
        batch_size: int = 50,
        output_file: Optional[str] = None
    ):
        """
        Create a batch of patterns for manual labeling.

        Args:
            pattern_data: List of pattern detections to label
            batch_size: Number of patterns per batch
            output_file: Optional output file path
        """
        # Sample patterns for labeling
        import random
        batch = random.sample(pattern_data, min(batch_size, len(pattern_data)))

        # Create labeling template
        labeling_template = {
            'batch_created': datetime.now().isoformat(),
            'batch_size': len(batch),
            'instructions': {
                'label': '1 for successful pattern, 0 for failed',
                'quality_score': '1-5 rating of pattern quality',
                'notes': 'Any observations about the pattern'
            },
            'patterns': []
        }

        for pattern in batch:
            labeling_template['patterns'].append({
                'ticker': pattern.get('ticker'),
                'pattern_type': pattern.get('pattern_type'),
                'window_start': pattern.get('window_start'),
                'window_end': pattern.get('window_end'),
                'detected_score': pattern.get('score'),
                'label': None,  # To be filled manually
                'quality_score': None,  # To be filled manually
                'notes': ''  # To be filled manually
            })

        # Save batch
        if output_file is None:
            output_file = self.data_dir / f'labeling_batch_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        with open(output_file, 'w') as f:
            json.dump(labeling_template, f, indent=2)

        print(f"Created labeling batch with {len(batch)} patterns at {output_file}")
        print("Please review and label the patterns, then import using import_labeled_batch()")

    def import_labeled_batch(self, batch_file: str):
        """
        Import a completed labeling batch.

        Args:
            batch_file: Path to labeled batch file
        """
        with open(batch_file, 'r') as f:
            batch = json.load(f)

        imported = 0
        for pattern in batch['patterns']:
            if pattern['label'] is not None:
                self.add_label(
                    ticker=pattern['ticker'],
                    pattern_type=pattern['pattern_type'],
                    window_start=pattern['window_start'],
                    window_end=pattern['window_end'],
                    label=pattern['label'],
                    notes=pattern.get('notes'),
                    quality_score=pattern.get('quality_score')
                )
                imported += 1

        print(f"Imported {imported} labeled patterns from {batch_file}")


class LabelQualityChecker:
    """Checks quality and consistency of labels."""

    @staticmethod
    def check_inter_annotator_agreement(labels1: List[Dict], labels2: List[Dict]) -> float:
        """
        Calculate inter-annotator agreement (Cohen's Kappa).

        Args:
            labels1: First set of labels
            labels2: Second set of labels

        Returns:
            Cohen's Kappa score
        """
        # Match labels by ticker, pattern_type, and window
        matched_labels = []

        for l1 in labels1:
            key1 = (l1['ticker'], l1['pattern_type'], l1['window_start'], l1['window_end'])

            for l2 in labels2:
                key2 = (l2['ticker'], l2['pattern_type'], l2['window_start'], l2['window_end'])

                if key1 == key2:
                    matched_labels.append((l1['label'], l2['label']))
                    break

        if not matched_labels:
            return 0.0

        # Calculate Cohen's Kappa
        from sklearn.metrics import cohen_kappa_score
        labels_a = [m[0] for m in matched_labels]
        labels_b = [m[1] for m in matched_labels]

        kappa = cohen_kappa_score(labels_a, labels_b)
        return kappa

    @staticmethod
    def check_label_consistency(labels: List[Dict]) -> Dict:
        """
        Check for inconsistencies in labeling.

        Args:
            labels: List of labels to check

        Returns:
            Dictionary with consistency metrics
        """
        # Group by pattern type
        from collections import defaultdict

        by_pattern = defaultdict(list)
        for label in labels:
            by_pattern[label['pattern_type']].append(label['label'])

        # Calculate metrics
        consistency = {}

        for pattern_type, pattern_labels in by_pattern.items():
            total = len(pattern_labels)
            success_rate = sum(pattern_labels) / total if total > 0 else 0

            consistency[pattern_type] = {
                'total': total,
                'success_rate': success_rate,
                'failure_rate': 1 - success_rate
            }

        return consistency
