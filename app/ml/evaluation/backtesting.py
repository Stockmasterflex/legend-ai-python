"""
Backtesting framework for ML pattern detection models.

Evaluates model performance on out-of-sample data and compares to rule-based approach.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional, Any
from datetime import datetime
from pathlib import Path
import json

from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, precision_recall_curve,
    confusion_matrix, classification_report
)


class Backtester:
    """Backtesting framework for pattern detection models."""

    def __init__(self):
        self.results_dir = Path('results/backtesting')
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def backtest_model(
        self,
        model: Any,
        X_test: np.ndarray,
        y_test: np.ndarray,
        test_patterns: List[Dict],
        threshold: float = 0.5
    ) -> Dict:
        """
        Backtest a single model.

        Args:
            model: Trained model
            X_test: Test features
            y_test: Test labels
            test_patterns: Test patterns with metadata
            threshold: Classification threshold

        Returns:
            Dictionary with comprehensive backtest results
        """
        # Get predictions
        y_pred_proba = model.predict_proba(X_test)
        y_pred = (y_pred_proba > threshold).astype(int)

        # Basic metrics
        metrics = self._compute_metrics(y_test, y_pred, y_pred_proba)

        # Confusion matrix analysis
        cm_analysis = self._analyze_confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix_analysis'] = cm_analysis

        # ROC and PR curves
        curves = self._compute_curves(y_test, y_pred_proba)
        metrics['curves'] = curves

        # Threshold analysis
        threshold_analysis = self._analyze_thresholds(y_test, y_pred_proba)
        metrics['threshold_analysis'] = threshold_analysis

        # Pattern-level analysis
        pattern_analysis = self._analyze_patterns(
            test_patterns, y_test, y_pred, y_pred_proba
        )
        metrics['pattern_analysis'] = pattern_analysis

        # Trading performance simulation
        trading_metrics = self._simulate_trading(test_patterns, y_pred, y_pred_proba)
        metrics['trading_performance'] = trading_metrics

        return metrics

    def _compute_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict:
        """Compute basic classification metrics."""
        return {
            'accuracy': float(accuracy_score(y_true, y_pred)),
            'precision': float(precision_score(y_true, y_pred, zero_division=0)),
            'recall': float(recall_score(y_true, y_pred, zero_division=0)),
            'f1_score': float(f1_score(y_true, y_pred, zero_division=0)),
            'auc_roc': float(roc_auc_score(y_true, y_pred_proba)),
            'n_samples': len(y_true),
            'n_positive': int(np.sum(y_true == 1)),
            'n_negative': int(np.sum(y_true == 0)),
            'positive_rate': float(np.mean(y_true))
        }

    def _analyze_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ) -> Dict:
        """Analyze confusion matrix."""
        cm = confusion_matrix(y_true, y_pred)

        tn, fp, fn, tp = cm.ravel() if cm.size == 4 else (0, 0, 0, 0)

        return {
            'confusion_matrix': cm.tolist(),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'true_positives': int(tp),
            'false_positive_rate': float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0,
            'false_negative_rate': float(fn / (fn + tp)) if (fn + tp) > 0 else 0.0,
            'true_negative_rate': float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0,
            'true_positive_rate': float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        }

    def _compute_curves(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict:
        """Compute ROC and Precision-Recall curves."""
        # ROC curve
        fpr, tpr, roc_thresholds = roc_curve(y_true, y_pred_proba)

        # Precision-Recall curve
        precision, recall, pr_thresholds = precision_recall_curve(y_true, y_pred_proba)

        return {
            'roc_curve': {
                'fpr': fpr.tolist(),
                'tpr': tpr.tolist(),
                'thresholds': roc_thresholds.tolist()
            },
            'pr_curve': {
                'precision': precision.tolist(),
                'recall': recall.tolist(),
                'thresholds': pr_thresholds.tolist()
            }
        }

    def _analyze_thresholds(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict:
        """Analyze performance at different thresholds."""
        thresholds = np.arange(0.1, 1.0, 0.1)
        threshold_metrics = []

        for threshold in thresholds:
            y_pred = (y_pred_proba > threshold).astype(int)

            metrics = {
                'threshold': float(threshold),
                'accuracy': float(accuracy_score(y_true, y_pred)),
                'precision': float(precision_score(y_true, y_pred, zero_division=0)),
                'recall': float(recall_score(y_true, y_pred, zero_division=0)),
                'f1_score': float(f1_score(y_true, y_pred, zero_division=0))
            }

            threshold_metrics.append(metrics)

        # Find optimal threshold (maximize F1)
        optimal = max(threshold_metrics, key=lambda x: x['f1_score'])

        return {
            'thresholds': threshold_metrics,
            'optimal_threshold': optimal
        }

    def _analyze_patterns(
        self,
        patterns: List[Dict],
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict:
        """Analyze performance by pattern type."""
        df = pd.DataFrame(patterns)
        df['y_true'] = y_true
        df['y_pred'] = y_pred
        df['y_pred_proba'] = y_pred_proba

        pattern_metrics = {}

        for pattern_type in df['pattern_type'].unique():
            pattern_df = df[df['pattern_type'] == pattern_type]

            if len(pattern_df) == 0:
                continue

            y_t = pattern_df['y_true'].values
            y_p = pattern_df['y_pred'].values
            y_pp = pattern_df['y_pred_proba'].values

            pattern_metrics[pattern_type] = {
                'n_samples': len(pattern_df),
                'accuracy': float(accuracy_score(y_t, y_p)),
                'precision': float(precision_score(y_t, y_p, zero_division=0)),
                'recall': float(recall_score(y_t, y_p, zero_division=0)),
                'f1_score': float(f1_score(y_t, y_p, zero_division=0)),
                'auc': float(roc_auc_score(y_t, y_pp)) if len(np.unique(y_t)) > 1 else None
            }

        return pattern_metrics

    def _simulate_trading(
        self,
        patterns: List[Dict],
        y_pred: np.ndarray,
        y_pred_proba: np.ndarray
    ) -> Dict:
        """Simulate trading performance based on predictions."""
        df = pd.DataFrame(patterns)
        df['y_pred'] = y_pred
        df['y_pred_proba'] = y_pred_proba

        # Only consider patterns predicted as positive
        positive_predictions = df[df['y_pred'] == 1]

        if len(positive_predictions) == 0:
            return {
                'n_trades': 0,
                'win_rate': 0.0,
                'avg_return': 0.0,
                'total_return': 0.0
            }

        # Calculate returns for predicted positive patterns
        returns = []
        for _, pattern in positive_predictions.iterrows():
            success_metric = pattern.get('success_metric', 0)
            returns.append(success_metric)

        returns = np.array(returns)

        winning_trades = np.sum(returns > 0)
        losing_trades = np.sum(returns <= 0)

        return {
            'n_trades': len(positive_predictions),
            'n_winning': int(winning_trades),
            'n_losing': int(losing_trades),
            'win_rate': float(winning_trades / len(positive_predictions)),
            'avg_return': float(np.mean(returns)),
            'median_return': float(np.median(returns)),
            'std_return': float(np.std(returns)),
            'total_return': float(np.sum(returns)),
            'max_return': float(np.max(returns)),
            'min_return': float(np.min(returns)),
            'sharpe_ratio': float(np.mean(returns) / np.std(returns)) if np.std(returns) > 0 else 0.0
        }

    def compare_to_baseline(
        self,
        ml_metrics: Dict,
        baseline_predictions: Optional[np.ndarray] = None,
        y_test: Optional[np.ndarray] = None
    ) -> Dict:
        """
        Compare ML model to rule-based baseline.

        Args:
            ml_metrics: ML model metrics
            baseline_predictions: Baseline model predictions
            y_test: True labels

        Returns:
            Comparison metrics
        """
        if baseline_predictions is None or y_test is None:
            return {'comparison_available': False}

        baseline_metrics = {
            'accuracy': float(accuracy_score(y_test, baseline_predictions)),
            'precision': float(precision_score(y_test, baseline_predictions, zero_division=0)),
            'recall': float(recall_score(y_test, baseline_predictions, zero_division=0)),
            'f1_score': float(f1_score(y_test, baseline_predictions, zero_division=0))
        }

        # Calculate improvements
        improvements = {
            'accuracy_improvement': ml_metrics['accuracy'] - baseline_metrics['accuracy'],
            'precision_improvement': ml_metrics['precision'] - baseline_metrics['precision'],
            'recall_improvement': ml_metrics['recall'] - baseline_metrics['recall'],
            'f1_improvement': ml_metrics['f1_score'] - baseline_metrics['f1_score']
        }

        return {
            'comparison_available': True,
            'baseline_metrics': baseline_metrics,
            'ml_metrics': {
                'accuracy': ml_metrics['accuracy'],
                'precision': ml_metrics['precision'],
                'recall': ml_metrics['recall'],
                'f1_score': ml_metrics['f1_score']
            },
            'improvements': improvements
        }

    def save_backtest_results(
        self,
        results: Dict,
        model_name: str
    ):
        """Save backtest results to disk."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = self.results_dir / f'backtest_{model_name}_{timestamp}.json'

        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"Backtest results saved to {results_file}")

    def generate_report(self, results: Dict) -> str:
        """Generate a human-readable backtest report."""
        report = []
        report.append("=" * 80)
        report.append("BACKTEST REPORT")
        report.append("=" * 80)

        # Basic metrics
        report.append("\nPerformance Metrics:")
        report.append(f"  Accuracy:  {results['accuracy']:.4f}")
        report.append(f"  Precision: {results['precision']:.4f}")
        report.append(f"  Recall:    {results['recall']:.4f}")
        report.append(f"  F1 Score:  {results['f1_score']:.4f}")
        report.append(f"  AUC-ROC:   {results['auc_roc']:.4f}")

        # Confusion matrix
        cm = results['confusion_matrix_analysis']
        report.append("\nConfusion Matrix:")
        report.append(f"  True Positives:  {cm['true_positives']}")
        report.append(f"  True Negatives:  {cm['true_negatives']}")
        report.append(f"  False Positives: {cm['false_positives']}")
        report.append(f"  False Negatives: {cm['false_negatives']}")
        report.append(f"  FPR: {cm['false_positive_rate']:.4f}")
        report.append(f"  FNR: {cm['false_negative_rate']:.4f}")

        # Trading performance
        if 'trading_performance' in results:
            tp = results['trading_performance']
            report.append("\nSimulated Trading Performance:")
            report.append(f"  Number of Trades: {tp['n_trades']}")
            report.append(f"  Win Rate:         {tp['win_rate']:.2%}")
            report.append(f"  Avg Return:       {tp['avg_return']:.2f}%")
            report.append(f"  Total Return:     {tp['total_return']:.2f}%")
            report.append(f"  Sharpe Ratio:     {tp['sharpe_ratio']:.4f}")

        # Pattern analysis
        if 'pattern_analysis' in results:
            report.append("\nPerformance by Pattern Type:")
            for pattern_type, metrics in results['pattern_analysis'].items():
                report.append(f"\n  {pattern_type}:")
                report.append(f"    Samples:   {metrics['n_samples']}")
                report.append(f"    Accuracy:  {metrics['accuracy']:.4f}")
                report.append(f"    Precision: {metrics['precision']:.4f}")
                report.append(f"    Recall:    {metrics['recall']:.4f}")
                report.append(f"    F1 Score:  {metrics['f1_score']:.4f}")

        # Optimal threshold
        if 'threshold_analysis' in results:
            opt = results['threshold_analysis']['optimal_threshold']
            report.append("\nOptimal Threshold:")
            report.append(f"  Threshold: {opt['threshold']:.2f}")
            report.append(f"  F1 Score:  {opt['f1_score']:.4f}")

        report.append("\n" + "=" * 80)

        return "\n".join(report)


class ModelComparator:
    """Compare performance of multiple models."""

    def __init__(self):
        self.results_dir = Path('results/comparison')
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def compare_models(
        self,
        model_results: Dict[str, Dict]
    ) -> pd.DataFrame:
        """
        Compare multiple models.

        Args:
            model_results: Dictionary mapping model names to backtest results

        Returns:
            DataFrame with comparison
        """
        comparison_data = []

        for model_name, results in model_results.items():
            row = {
                'Model': model_name,
                'Accuracy': results['accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1 Score': results['f1_score'],
                'AUC-ROC': results['auc_roc']
            }

            # Add trading metrics if available
            if 'trading_performance' in results:
                tp = results['trading_performance']
                row['Win Rate'] = tp['win_rate']
                row['Avg Return'] = tp['avg_return']
                row['Sharpe Ratio'] = tp['sharpe_ratio']

            comparison_data.append(row)

        df = pd.DataFrame(comparison_data)
        df = df.sort_values('F1 Score', ascending=False)

        return df

    def save_comparison(
        self,
        comparison_df: pd.DataFrame,
        filename: Optional[str] = None
    ):
        """Save comparison to disk."""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'model_comparison_{timestamp}.csv'

        filepath = self.results_dir / filename
        comparison_df.to_csv(filepath, index=False)

        print(f"Model comparison saved to {filepath}")
