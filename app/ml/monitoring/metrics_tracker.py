"""
Monitoring and metrics tracking for ML models.

Tracks model performance, predictions, and drift over time.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
import pandas as pd


class MLMetricsTracker:
    """Tracks ML model performance metrics over time."""

    def __init__(self, metrics_dir: str = "metrics/ml"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.predictions_file = self.metrics_dir / "predictions.jsonl"
        self.metrics_file = self.metrics_dir / "daily_metrics.json"
        self.drift_file = self.metrics_dir / "drift_metrics.json"

    def log_prediction(
        self,
        model_name: str,
        model_version: str,
        ticker: str,
        prediction: int,
        probability: float,
        features: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ):
        """
        Log a single prediction.

        Args:
            model_name: Name of the model
            model_version: Version of the model
            ticker: Stock ticker
            prediction: Predicted label (0 or 1)
            probability: Prediction probability
            features: Input features
            metadata: Additional metadata
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model_name": model_name,
            "model_version": model_version,
            "ticker": ticker,
            "prediction": prediction,
            "probability": float(probability),
            "features": features,
            "metadata": metadata or {}
        }

        # Append to predictions file
        with open(self.predictions_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def log_actual_outcome(
        self,
        prediction_id: str,
        actual_label: int,
        success_metric: Optional[float] = None
    ):
        """
        Log actual outcome for a prediction.

        Args:
            prediction_id: ID of the prediction
            actual_label: Actual label (0 or 1)
            success_metric: Actual performance metric
        """
        outcome_entry = {
            "timestamp": datetime.now().isoformat(),
            "prediction_id": prediction_id,
            "actual_label": actual_label,
            "success_metric": success_metric
        }

        outcomes_file = self.metrics_dir / "outcomes.jsonl"
        with open(outcomes_file, 'a') as f:
            f.write(json.dumps(outcome_entry) + '\n')

    def compute_daily_metrics(self, date: Optional[str] = None) -> Dict:
        """
        Compute daily metrics for predictions.

        Args:
            date: Date to compute metrics for (None = today)

        Returns:
            Dictionary with daily metrics
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        # Load predictions for the day
        predictions = self._load_predictions(date)

        if not predictions:
            return {}

        # Group by model
        metrics_by_model = defaultdict(list)

        for pred in predictions:
            model_key = f"{pred['model_name']}_{pred['model_version']}"
            metrics_by_model[model_key].append(pred)

        # Compute metrics for each model
        daily_metrics = {
            "date": date,
            "models": {}
        }

        for model_key, preds in metrics_by_model.items():
            model_metrics = {
                "num_predictions": len(preds),
                "avg_probability": np.mean([p['probability'] for p in preds]),
                "prediction_distribution": {
                    "positive": sum(1 for p in preds if p['prediction'] == 1),
                    "negative": sum(1 for p in preds if p['prediction'] == 0)
                },
                "high_confidence": sum(1 for p in preds if abs(p['probability'] - 0.5) > 0.3),
                "low_confidence": sum(1 for p in preds if abs(p['probability'] - 0.5) <= 0.3)
            }

            daily_metrics["models"][model_key] = model_metrics

        # Save daily metrics
        self._save_daily_metrics(date, daily_metrics)

        return daily_metrics

    def compute_accuracy_over_time(
        self,
        model_name: str,
        model_version: str,
        days: int = 30
    ) -> Dict:
        """
        Compute model accuracy over time.

        Args:
            model_name: Name of the model
            model_version: Version of the model
            days: Number of days to look back

        Returns:
            Dictionary with accuracy metrics over time
        """
        # Load predictions and outcomes
        predictions = self._load_recent_predictions(days)
        outcomes = self._load_outcomes()

        # Filter by model
        model_key = f"{model_name}_{model_version}"
        model_preds = [p for p in predictions if
                      f"{p['model_name']}_{p['model_version']}" == model_key]

        # Match with outcomes
        matched = []
        outcome_dict = {o['prediction_id']: o for o in outcomes}

        for pred in model_preds:
            pred_id = pred.get('prediction_id')
            if pred_id in outcome_dict:
                matched.append({
                    'prediction': pred['prediction'],
                    'actual': outcome_dict[pred_id]['actual_label'],
                    'timestamp': pred['timestamp']
                })

        if not matched:
            return {}

        # Compute metrics
        predictions_array = np.array([m['prediction'] for m in matched])
        actuals_array = np.array([m['actual'] for m in matched])

        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        metrics = {
            "model_name": model_name,
            "model_version": model_version,
            "period_days": days,
            "num_predictions": len(matched),
            "accuracy": float(accuracy_score(actuals_array, predictions_array)),
            "precision": float(precision_score(actuals_array, predictions_array, zero_division=0)),
            "recall": float(recall_score(actuals_array, predictions_array, zero_division=0)),
            "f1_score": float(f1_score(actuals_array, predictions_array, zero_division=0))
        }

        return metrics

    def detect_data_drift(
        self,
        model_name: str,
        baseline_days: int = 30,
        recent_days: int = 7
    ) -> Dict:
        """
        Detect data drift by comparing feature distributions.

        Args:
            model_name: Name of the model
            baseline_days: Days for baseline period
            recent_days: Days for recent period

        Returns:
            Dictionary with drift metrics
        """
        # Load predictions
        baseline_preds = self._load_recent_predictions(baseline_days)
        recent_preds = self._load_recent_predictions(recent_days)

        # Filter by model
        baseline_preds = [p for p in baseline_preds if p['model_name'] == model_name]
        recent_preds = [p for p in recent_preds if p['model_name'] == model_name]

        if not baseline_preds or not recent_preds:
            return {}

        # Compare feature distributions
        drift_metrics = {
            "model_name": model_name,
            "baseline_period_days": baseline_days,
            "recent_period_days": recent_days,
            "baseline_samples": len(baseline_preds),
            "recent_samples": len(recent_preds),
            "feature_drift": {}
        }

        # Extract features
        baseline_features = self._extract_features(baseline_preds)
        recent_features = self._extract_features(recent_preds)

        # Compute drift for each feature
        for feature_name in baseline_features.keys():
            if feature_name in recent_features:
                baseline_vals = baseline_features[feature_name]
                recent_vals = recent_features[feature_name]

                # KS test for distribution shift
                from scipy import stats
                ks_stat, p_value = stats.ks_2samp(baseline_vals, recent_vals)

                drift_metrics["feature_drift"][feature_name] = {
                    "ks_statistic": float(ks_stat),
                    "p_value": float(p_value),
                    "drifted": p_value < 0.05,  # Significant drift at 5% level
                    "baseline_mean": float(np.mean(baseline_vals)),
                    "recent_mean": float(np.mean(recent_vals)),
                    "mean_change_pct": float((np.mean(recent_vals) - np.mean(baseline_vals)) /
                                           np.mean(baseline_vals) * 100)
                    if np.mean(baseline_vals) != 0 else 0
                }

        # Overall drift score
        drifted_features = sum(1 for f in drift_metrics["feature_drift"].values() if f["drifted"])
        total_features = len(drift_metrics["feature_drift"])

        drift_metrics["overall_drift_score"] = drifted_features / total_features if total_features > 0 else 0
        drift_metrics["drifted_features_count"] = drifted_features
        drift_metrics["total_features"] = total_features

        # Save drift metrics
        self._save_drift_metrics(drift_metrics)

        return drift_metrics

    def _load_predictions(self, date: str) -> List[Dict]:
        """Load predictions for a specific date."""
        if not self.predictions_file.exists():
            return []

        predictions = []
        with open(self.predictions_file, 'r') as f:
            for line in f:
                try:
                    pred = json.loads(line)
                    if pred['timestamp'].startswith(date):
                        predictions.append(pred)
                except json.JSONDecodeError:
                    continue

        return predictions

    def _load_recent_predictions(self, days: int) -> List[Dict]:
        """Load predictions from the last N days."""
        if not self.predictions_file.exists():
            return []

        cutoff_date = datetime.now() - timedelta(days=days)
        predictions = []

        with open(self.predictions_file, 'r') as f:
            for line in f:
                try:
                    pred = json.loads(line)
                    pred_date = datetime.fromisoformat(pred['timestamp'])
                    if pred_date >= cutoff_date:
                        predictions.append(pred)
                except (json.JSONDecodeError, ValueError):
                    continue

        return predictions

    def _load_outcomes(self) -> List[Dict]:
        """Load all outcomes."""
        outcomes_file = self.metrics_dir / "outcomes.jsonl"

        if not outcomes_file.exists():
            return []

        outcomes = []
        with open(outcomes_file, 'r') as f:
            for line in f:
                try:
                    outcomes.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        return outcomes

    def _extract_features(self, predictions: List[Dict]) -> Dict[str, List[float]]:
        """Extract features from predictions."""
        features = defaultdict(list)

        for pred in predictions:
            if pred.get('features'):
                for feature_name, value in pred['features'].items():
                    if isinstance(value, (int, float)):
                        features[feature_name].append(value)

        return dict(features)

    def _save_daily_metrics(self, date: str, metrics: Dict):
        """Save daily metrics to file."""
        # Load existing metrics
        all_metrics = {}
        if self.metrics_file.exists():
            with open(self.metrics_file, 'r') as f:
                all_metrics = json.load(f)

        # Add new metrics
        all_metrics[date] = metrics

        # Save
        with open(self.metrics_file, 'w') as f:
            json.dump(all_metrics, f, indent=2)

    def _save_drift_metrics(self, drift_metrics: Dict):
        """Save drift metrics to file."""
        # Load existing drift metrics
        all_drift = []
        if self.drift_file.exists():
            with open(self.drift_file, 'r') as f:
                all_drift = json.load(f)

        # Add new drift metrics
        drift_metrics['computed_at'] = datetime.now().isoformat()
        all_drift.append(drift_metrics)

        # Keep only last 30 drift checks
        all_drift = all_drift[-30:]

        # Save
        with open(self.drift_file, 'w') as f:
            json.dump(all_drift, f, indent=2)

    def get_summary(self, days: int = 7) -> Dict:
        """
        Get summary of ML metrics for the last N days.

        Args:
            days: Number of days to summarize

        Returns:
            Summary dictionary
        """
        predictions = self._load_recent_predictions(days)

        if not predictions:
            return {
                "period_days": days,
                "total_predictions": 0
            }

        # Group by model
        by_model = defaultdict(list)
        for pred in predictions:
            model_key = f"{pred['model_name']}_{pred['model_version']}"
            by_model[model_key].append(pred)

        summary = {
            "period_days": days,
            "total_predictions": len(predictions),
            "models": {}
        }

        for model_key, preds in by_model.items():
            summary["models"][model_key] = {
                "num_predictions": len(preds),
                "avg_probability": float(np.mean([p['probability'] for p in preds])),
                "positive_predictions": sum(1 for p in preds if p['prediction'] == 1),
                "negative_predictions": sum(1 for p in preds if p['prediction'] == 0)
            }

        return summary
