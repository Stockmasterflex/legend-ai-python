"""
Training Dashboard Module

Provides real-time training monitoring, loss curves, validation metrics, and early stopping.
"""

from typing import Dict, List, Optional, Any, Callable
import pandas as pd
import numpy as np
from datetime import datetime
import time
import logging
from dataclasses import dataclass, field
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
)
import xgboost as xgb
import lightgbm as lgb

logger = logging.getLogger(__name__)


@dataclass
class TrainingMetrics:
    """Container for training metrics"""
    epoch: int
    train_loss: Optional[float] = None
    val_loss: Optional[float] = None
    train_score: Optional[float] = None
    val_score: Optional[float] = None
    learning_rate: Optional[float] = None
    timestamp: datetime = field(default_factory=datetime.now)
    additional_metrics: Dict[str, float] = field(default_factory=dict)


class TrainingDashboard:
    """Real-time training monitoring and early stopping"""

    def __init__(
        self,
        task_type: str = "classification",
        metric: str = "auto",
        patience: int = 10,
        min_delta: float = 0.001,
        verbose: bool = True,
    ):
        """
        Initialize Training Dashboard

        Args:
            task_type: 'classification' or 'regression'
            metric: Metric to monitor ('auto', 'accuracy', 'f1', 'mse', 'r2', etc.)
            patience: Number of epochs to wait before early stopping
            min_delta: Minimum change to qualify as improvement
            verbose: Whether to print training progress
        """
        self.task_type = task_type
        self.patience = patience
        self.min_delta = min_delta
        self.verbose = verbose

        # Auto-select metric if needed
        if metric == "auto":
            self.metric = "accuracy" if task_type == "classification" else "r2"
        else:
            self.metric = metric

        # Training state
        self.history: List[TrainingMetrics] = []
        self.best_score: Optional[float] = None
        self.best_epoch: Optional[int] = None
        self.epochs_without_improvement: int = 0
        self.should_stop: bool = False
        self.start_time: Optional[float] = None
        self.total_epochs: int = 0

    def start_training(self):
        """Initialize training session"""
        self.history = []
        self.best_score = None
        self.best_epoch = None
        self.epochs_without_improvement = 0
        self.should_stop = False
        self.start_time = time.time()
        self.total_epochs = 0
        logger.info("Training session started")

    def log_epoch(
        self,
        epoch: int,
        train_loss: Optional[float] = None,
        val_loss: Optional[float] = None,
        train_score: Optional[float] = None,
        val_score: Optional[float] = None,
        learning_rate: Optional[float] = None,
        **kwargs,
    ):
        """
        Log metrics for an epoch

        Args:
            epoch: Epoch number
            train_loss: Training loss
            val_loss: Validation loss
            train_score: Training score (accuracy, r2, etc.)
            val_score: Validation score
            learning_rate: Current learning rate
            **kwargs: Additional metrics
        """
        metrics = TrainingMetrics(
            epoch=epoch,
            train_loss=train_loss,
            val_loss=val_loss,
            train_score=train_score,
            val_score=val_score,
            learning_rate=learning_rate,
            additional_metrics=kwargs,
        )

        self.history.append(metrics)
        self.total_epochs = epoch + 1

        # Check for early stopping
        self._check_early_stopping(val_score if val_score else train_score, epoch)

        # Print progress
        if self.verbose:
            self._print_progress(metrics)

    def _check_early_stopping(self, score: Optional[float], epoch: int):
        """Check if training should stop early"""
        if score is None:
            return

        # Determine if higher is better
        higher_is_better = self.metric in ["accuracy", "precision", "recall", "f1", "r2"]

        # Check for improvement
        if self.best_score is None:
            self.best_score = score
            self.best_epoch = epoch
            self.epochs_without_improvement = 0
        else:
            if higher_is_better:
                improved = (score - self.best_score) > self.min_delta
            else:
                improved = (self.best_score - score) > self.min_delta

            if improved:
                self.best_score = score
                self.best_epoch = epoch
                self.epochs_without_improvement = 0
            else:
                self.epochs_without_improvement += 1

        # Check if should stop
        if self.epochs_without_improvement >= self.patience:
            self.should_stop = True
            if self.verbose:
                logger.info(
                    f"Early stopping triggered at epoch {epoch}. "
                    f"Best score: {self.best_score:.4f} at epoch {self.best_epoch}"
                )

    def _print_progress(self, metrics: TrainingMetrics):
        """Print training progress"""
        elapsed = time.time() - self.start_time if self.start_time else 0
        msg = f"Epoch {metrics.epoch + 1:3d} | "

        if metrics.train_loss is not None:
            msg += f"Train Loss: {metrics.train_loss:.4f} | "
        if metrics.val_loss is not None:
            msg += f"Val Loss: {metrics.val_loss:.4f} | "
        if metrics.train_score is not None:
            msg += f"Train {self.metric}: {metrics.train_score:.4f} | "
        if metrics.val_score is not None:
            msg += f"Val {self.metric}: {metrics.val_score:.4f} | "
        if metrics.learning_rate is not None:
            msg += f"LR: {metrics.learning_rate:.6f} | "

        msg += f"Time: {elapsed:.1f}s"

        if self.epochs_without_improvement > 0:
            msg += f" | No improvement: {self.epochs_without_improvement}/{self.patience}"

        print(msg)

    def get_history_dataframe(self) -> pd.DataFrame:
        """
        Get training history as DataFrame

        Returns:
            DataFrame with training history
        """
        if not self.history:
            return pd.DataFrame()

        records = []
        for h in self.history:
            record = {
                "epoch": h.epoch,
                "train_loss": h.train_loss,
                "val_loss": h.val_loss,
                "train_score": h.train_score,
                "val_score": h.val_score,
                "learning_rate": h.learning_rate,
                "timestamp": h.timestamp,
            }
            record.update(h.additional_metrics)
            records.append(record)

        return pd.DataFrame(records)

    def get_best_epoch_info(self) -> Dict:
        """Get information about the best epoch"""
        return {
            "best_epoch": self.best_epoch,
            "best_score": self.best_score,
            "metric": self.metric,
        }

    def train_with_monitoring(
        self,
        model: Any,
        X_train: pd.DataFrame,
        y_train: pd.Series,
        X_val: Optional[pd.DataFrame] = None,
        y_val: Optional[pd.Series] = None,
        **fit_params,
    ) -> Any:
        """
        Train model with real-time monitoring

        Args:
            model: Model to train
            X_train: Training features
            y_train: Training target
            X_val: Validation features (optional)
            y_val: Validation target (optional)
            **fit_params: Additional parameters for model.fit()

        Returns:
            Trained model
        """
        self.start_training()

        # Check if model supports callbacks for real-time monitoring
        model_type = type(model).__name__

        if "XGB" in model_type:
            # XGBoost with callbacks
            eval_set = [(X_train, y_train)]
            if X_val is not None and y_val is not None:
                eval_set.append((X_val, y_val))

            # Custom callback for logging
            def xgb_callback(env):
                epoch = env.iteration
                train_metric = env.evaluation_result_list[0][1] if env.evaluation_result_list else None
                val_metric = env.evaluation_result_list[1][1] if len(env.evaluation_result_list) > 1 else None

                self.log_epoch(
                    epoch=epoch,
                    train_score=train_metric,
                    val_score=val_metric,
                )

                if self.should_stop:
                    raise KeyboardInterrupt("Early stopping")

            try:
                model.fit(
                    X_train,
                    y_train,
                    eval_set=eval_set,
                    verbose=False,
                    callbacks=[xgb_callback],
                    **fit_params,
                )
            except KeyboardInterrupt:
                logger.info("Training stopped early")

        elif "LGBM" in model_type:
            # LightGBM with callbacks
            eval_set = [(X_train, y_train)]
            if X_val is not None and y_val is not None:
                eval_set.append((X_val, y_val))

            # Custom callback
            def lgb_callback(env):
                epoch = env.iteration
                train_metric = list(env.evaluation_result_list[0].values())[0] if env.evaluation_result_list else None
                val_metric = list(env.evaluation_result_list[1].values())[0] if len(env.evaluation_result_list) > 1 else None

                self.log_epoch(
                    epoch=epoch,
                    train_score=train_metric,
                    val_score=val_metric,
                )

                if self.should_stop:
                    raise KeyboardInterrupt("Early stopping")

            try:
                model.fit(
                    X_train,
                    y_train,
                    eval_set=eval_set,
                    callbacks=[lgb_callback],
                    **fit_params,
                )
            except KeyboardInterrupt:
                logger.info("Training stopped early")

        else:
            # Standard scikit-learn model (no epoch-based training)
            # Train and evaluate once
            model.fit(X_train, y_train, **fit_params)

            # Calculate metrics
            train_pred = model.predict(X_train)
            train_score = self._calculate_score(y_train, train_pred)

            val_score = None
            if X_val is not None and y_val is not None:
                val_pred = model.predict(X_val)
                val_score = self._calculate_score(y_val, val_pred)

            self.log_epoch(
                epoch=0,
                train_score=train_score,
                val_score=val_score,
            )

        return model

    def _calculate_score(self, y_true, y_pred) -> float:
        """Calculate score based on metric"""
        if self.task_type == "classification":
            if self.metric == "accuracy":
                return accuracy_score(y_true, y_pred)
            elif self.metric == "precision":
                return precision_score(y_true, y_pred, average="weighted", zero_division=0)
            elif self.metric == "recall":
                return recall_score(y_true, y_pred, average="weighted", zero_division=0)
            elif self.metric == "f1":
                return f1_score(y_true, y_pred, average="weighted", zero_division=0)
            else:
                return accuracy_score(y_true, y_pred)
        else:  # regression
            if self.metric == "mse":
                return mean_squared_error(y_true, y_pred)
            elif self.metric == "mae":
                return mean_absolute_error(y_true, y_pred)
            elif self.metric == "r2":
                return r2_score(y_true, y_pred)
            else:
                return r2_score(y_true, y_pred)

    def plot_training_curves(self, save_path: Optional[str] = None):
        """
        Plot training and validation curves

        Args:
            save_path: Path to save the plot (if None, displays plot)

        Returns:
            Matplotlib figure
        """
        import matplotlib.pyplot as plt

        df = self.get_history_dataframe()

        if df.empty:
            logger.warning("No training history to plot")
            return None

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Loss curves
        if "train_loss" in df.columns and df["train_loss"].notna().any():
            axes[0].plot(df["epoch"], df["train_loss"], label="Train Loss", marker="o")
            if "val_loss" in df.columns and df["val_loss"].notna().any():
                axes[0].plot(df["epoch"], df["val_loss"], label="Val Loss", marker="o")
            axes[0].set_xlabel("Epoch")
            axes[0].set_ylabel("Loss")
            axes[0].set_title("Training and Validation Loss")
            axes[0].legend()
            axes[0].grid(True, alpha=0.3)

        # Score curves
        if "train_score" in df.columns and df["train_score"].notna().any():
            axes[1].plot(df["epoch"], df["train_score"], label=f"Train {self.metric}", marker="o")
            if "val_score" in df.columns and df["val_score"].notna().any():
                axes[1].plot(df["epoch"], df["val_score"], label=f"Val {self.metric}", marker="o")

            # Mark best epoch
            if self.best_epoch is not None:
                axes[1].axvline(self.best_epoch, color="red", linestyle="--", alpha=0.5, label="Best Epoch")

            axes[1].set_xlabel("Epoch")
            axes[1].set_ylabel(self.metric.capitalize())
            axes[1].set_title(f"Training and Validation {self.metric.capitalize()}")
            axes[1].legend()
            axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Training curves saved to {save_path}")

        return fig

    def get_summary(self) -> Dict:
        """Get training summary"""
        elapsed = time.time() - self.start_time if self.start_time else 0

        return {
            "total_epochs": self.total_epochs,
            "best_epoch": self.best_epoch,
            "best_score": self.best_score,
            "metric": self.metric,
            "early_stopped": self.should_stop,
            "training_time_seconds": elapsed,
            "epochs_per_second": self.total_epochs / elapsed if elapsed > 0 else 0,
        }
