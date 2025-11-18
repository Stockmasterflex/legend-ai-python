"""
Model Evaluation Module

Provides comprehensive model evaluation including confusion matrices, ROC curves,
feature importance, and prediction examples.
"""

from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.metrics import (
    confusion_matrix,
    classification_report,
    roc_curve,
    auc,
    roc_auc_score,
    precision_recall_curve,
    average_precision_score,
    mean_squared_error,
    mean_absolute_error,
    r2_score,
    mean_absolute_percentage_error,
    explained_variance_score,
)
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """Comprehensive model evaluation toolkit"""

    def __init__(self, task_type: str = "classification"):
        """
        Initialize ModelEvaluator

        Args:
            task_type: 'classification' or 'regression'
        """
        self.task_type = task_type
        self.evaluation_results: Dict[str, Any] = {}

    def evaluate_classification(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: Optional[np.ndarray] = None,
        class_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Comprehensive classification evaluation

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_pred_proba: Predicted probabilities (for ROC/AUC)
            class_names: Names of classes

        Returns:
            Dictionary with all evaluation metrics
        """
        results = {}

        # Classification report
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        results["classification_report"] = report

        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        results["confusion_matrix"] = cm

        # Overall metrics
        results["accuracy"] = report["accuracy"]
        results["macro_avg_precision"] = report["macro avg"]["precision"]
        results["macro_avg_recall"] = report["macro avg"]["recall"]
        results["macro_avg_f1"] = report["macro avg"]["f1-score"]
        results["weighted_avg_precision"] = report["weighted avg"]["precision"]
        results["weighted_avg_recall"] = report["weighted avg"]["recall"]
        results["weighted_avg_f1"] = report["weighted avg"]["f1-score"]

        # ROC-AUC (if probabilities provided)
        if y_pred_proba is not None:
            try:
                unique_classes = np.unique(y_true)
                n_classes = len(unique_classes)

                if n_classes == 2:
                    # Binary classification
                    if y_pred_proba.ndim == 2:
                        y_scores = y_pred_proba[:, 1]
                    else:
                        y_scores = y_pred_proba

                    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
                    roc_auc = auc(fpr, tpr)

                    results["roc_curve"] = {"fpr": fpr, "tpr": tpr, "thresholds": thresholds}
                    results["roc_auc"] = roc_auc

                    # Precision-Recall curve
                    precision, recall, pr_thresholds = precision_recall_curve(y_true, y_scores)
                    avg_precision = average_precision_score(y_true, y_scores)

                    results["pr_curve"] = {
                        "precision": precision,
                        "recall": recall,
                        "thresholds": pr_thresholds,
                    }
                    results["average_precision"] = avg_precision

                else:
                    # Multi-class classification
                    y_true_bin = label_binarize(y_true, classes=unique_classes)
                    roc_auc = roc_auc_score(y_true_bin, y_pred_proba, average="weighted", multi_class="ovr")
                    results["roc_auc"] = roc_auc

            except Exception as e:
                logger.warning(f"Could not calculate ROC-AUC: {e}")

        self.evaluation_results = results
        return results

    def evaluate_regression(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> Dict[str, Any]:
        """
        Comprehensive regression evaluation

        Args:
            y_true: True values
            y_pred: Predicted values

        Returns:
            Dictionary with all evaluation metrics
        """
        results = {}

        # Calculate metrics
        results["mse"] = mean_squared_error(y_true, y_pred)
        results["rmse"] = np.sqrt(results["mse"])
        results["mae"] = mean_absolute_error(y_true, y_pred)
        results["r2"] = r2_score(y_true, y_pred)
        results["explained_variance"] = explained_variance_score(y_true, y_pred)

        try:
            results["mape"] = mean_absolute_percentage_error(y_true, y_pred)
        except Exception:
            results["mape"] = None

        # Residuals
        residuals = y_true - y_pred
        results["residuals_mean"] = np.mean(residuals)
        results["residuals_std"] = np.std(residuals)

        self.evaluation_results = results
        return results

    def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_pred_proba: Optional[np.ndarray] = None,
        class_names: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate model based on task type

        Args:
            y_true: True labels/values
            y_pred: Predicted labels/values
            y_pred_proba: Predicted probabilities (classification only)
            class_names: Names of classes (classification only)

        Returns:
            Dictionary with evaluation results
        """
        if self.task_type == "classification":
            return self.evaluate_classification(y_true, y_pred, y_pred_proba, class_names)
        else:
            return self.evaluate_regression(y_true, y_pred)

    def plot_confusion_matrix(
        self,
        y_true: Optional[np.ndarray] = None,
        y_pred: Optional[np.ndarray] = None,
        class_names: Optional[List[str]] = None,
        normalize: bool = False,
        save_path: Optional[str] = None,
    ) -> plt.Figure:
        """
        Plot confusion matrix

        Args:
            y_true: True labels (if None, uses cached results)
            y_pred: Predicted labels (if None, uses cached results)
            class_names: Names of classes
            normalize: Whether to normalize the confusion matrix
            save_path: Path to save the plot

        Returns:
            Matplotlib figure
        """
        if y_true is not None and y_pred is not None:
            cm = confusion_matrix(y_true, y_pred)
        elif "confusion_matrix" in self.evaluation_results:
            cm = self.evaluation_results["confusion_matrix"]
        else:
            raise ValueError("No confusion matrix available")

        if normalize:
            cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]

        fig, ax = plt.subplots(figsize=(10, 8))

        sns.heatmap(
            cm,
            annot=True,
            fmt=".2f" if normalize else "d",
            cmap="Blues",
            xticklabels=class_names if class_names else "auto",
            yticklabels=class_names if class_names else "auto",
            ax=ax,
        )

        ax.set_xlabel("Predicted Label", fontsize=12)
        ax.set_ylabel("True Label", fontsize=12)
        ax.set_title(
            "Normalized Confusion Matrix" if normalize else "Confusion Matrix",
            fontsize=14,
            fontweight="bold",
        )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Confusion matrix saved to {save_path}")

        return fig

    def plot_roc_curve(
        self,
        y_true: Optional[np.ndarray] = None,
        y_pred_proba: Optional[np.ndarray] = None,
        save_path: Optional[str] = None,
    ) -> Optional[plt.Figure]:
        """
        Plot ROC curve

        Args:
            y_true: True labels (if None, uses cached results)
            y_pred_proba: Predicted probabilities (if None, uses cached results)
            save_path: Path to save the plot

        Returns:
            Matplotlib figure or None if not applicable
        """
        if self.task_type != "classification":
            logger.warning("ROC curve only applicable for classification")
            return None

        if y_true is not None and y_pred_proba is not None:
            fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
            roc_auc = auc(fpr, tpr)
        elif "roc_curve" in self.evaluation_results:
            fpr = self.evaluation_results["roc_curve"]["fpr"]
            tpr = self.evaluation_results["roc_curve"]["tpr"]
            roc_auc = self.evaluation_results["roc_auc"]
        else:
            logger.warning("No ROC curve data available")
            return None

        fig, ax = plt.subplots(figsize=(10, 8))

        ax.plot(fpr, tpr, color="darkorange", lw=2, label=f"ROC curve (AUC = {roc_auc:.3f})")
        ax.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--", label="Random Classifier")

        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("False Positive Rate", fontsize=12)
        ax.set_ylabel("True Positive Rate", fontsize=12)
        ax.set_title("Receiver Operating Characteristic (ROC) Curve", fontsize=14, fontweight="bold")
        ax.legend(loc="lower right", fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"ROC curve saved to {save_path}")

        return fig

    def plot_precision_recall_curve(
        self,
        y_true: Optional[np.ndarray] = None,
        y_pred_proba: Optional[np.ndarray] = None,
        save_path: Optional[str] = None,
    ) -> Optional[plt.Figure]:
        """
        Plot Precision-Recall curve

        Args:
            y_true: True labels (if None, uses cached results)
            y_pred_proba: Predicted probabilities (if None, uses cached results)
            save_path: Path to save the plot

        Returns:
            Matplotlib figure or None if not applicable
        """
        if self.task_type != "classification":
            logger.warning("PR curve only applicable for classification")
            return None

        if y_true is not None and y_pred_proba is not None:
            precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
            avg_precision = average_precision_score(y_true, y_pred_proba)
        elif "pr_curve" in self.evaluation_results:
            precision = self.evaluation_results["pr_curve"]["precision"]
            recall = self.evaluation_results["pr_curve"]["recall"]
            avg_precision = self.evaluation_results["average_precision"]
        else:
            logger.warning("No PR curve data available")
            return None

        fig, ax = plt.subplots(figsize=(10, 8))

        ax.plot(recall, precision, color="darkorange", lw=2, label=f"PR curve (AP = {avg_precision:.3f})")

        ax.set_xlim([0.0, 1.0])
        ax.set_ylim([0.0, 1.05])
        ax.set_xlabel("Recall", fontsize=12)
        ax.set_ylabel("Precision", fontsize=12)
        ax.set_title("Precision-Recall Curve", fontsize=14, fontweight="bold")
        ax.legend(loc="lower left", fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"PR curve saved to {save_path}")

        return fig

    def plot_feature_importance(
        self,
        model: Any,
        feature_names: List[str],
        top_n: int = 20,
        save_path: Optional[str] = None,
    ) -> Optional[plt.Figure]:
        """
        Plot feature importance

        Args:
            model: Trained model with feature_importances_ attribute
            feature_names: Names of features
            top_n: Number of top features to display
            save_path: Path to save the plot

        Returns:
            Matplotlib figure or None if not applicable
        """
        if not hasattr(model, "feature_importances_"):
            logger.warning("Model does not have feature_importances_ attribute")
            return None

        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1][:top_n]

        fig, ax = plt.subplots(figsize=(12, 8))

        ax.barh(range(top_n), importances[indices], color="steelblue")
        ax.set_yticks(range(top_n))
        ax.set_yticklabels([feature_names[i] for i in indices])
        ax.set_xlabel("Importance", fontsize=12)
        ax.set_title(f"Top {top_n} Feature Importances", fontsize=14, fontweight="bold")
        ax.invert_yaxis()
        ax.grid(axis="x", alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Feature importance plot saved to {save_path}")

        return fig

    def plot_residuals(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        save_path: Optional[str] = None,
    ) -> Optional[plt.Figure]:
        """
        Plot residuals for regression tasks

        Args:
            y_true: True values
            y_pred: Predicted values
            save_path: Path to save the plot

        Returns:
            Matplotlib figure or None if not applicable
        """
        if self.task_type != "regression":
            logger.warning("Residual plots only applicable for regression")
            return None

        residuals = y_true - y_pred

        fig, axes = plt.subplots(1, 2, figsize=(14, 5))

        # Residuals vs Predicted
        axes[0].scatter(y_pred, residuals, alpha=0.5, edgecolors="k")
        axes[0].axhline(y=0, color="r", linestyle="--", linewidth=2)
        axes[0].set_xlabel("Predicted Values", fontsize=12)
        axes[0].set_ylabel("Residuals", fontsize=12)
        axes[0].set_title("Residuals vs Predicted Values", fontsize=14, fontweight="bold")
        axes[0].grid(True, alpha=0.3)

        # Residuals distribution
        axes[1].hist(residuals, bins=50, color="steelblue", edgecolor="black", alpha=0.7)
        axes[1].axvline(x=0, color="r", linestyle="--", linewidth=2)
        axes[1].set_xlabel("Residuals", fontsize=12)
        axes[1].set_ylabel("Frequency", fontsize=12)
        axes[1].set_title("Distribution of Residuals", fontsize=14, fontweight="bold")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Residual plots saved to {save_path}")

        return fig

    def plot_prediction_error(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        save_path: Optional[str] = None,
    ) -> Optional[plt.Figure]:
        """
        Plot prediction error (actual vs predicted)

        Args:
            y_true: True values
            y_pred: Predicted values
            save_path: Path to save the plot

        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        ax.scatter(y_true, y_pred, alpha=0.5, edgecolors="k")

        # Perfect prediction line
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        ax.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2, label="Perfect Prediction")

        ax.set_xlabel("True Values", fontsize=12)
        ax.set_ylabel("Predicted Values", fontsize=12)
        ax.set_title("Actual vs Predicted Values", fontsize=14, fontweight="bold")
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        # Add R² score
        if self.task_type == "regression":
            r2 = r2_score(y_true, y_pred)
            ax.text(
                0.05,
                0.95,
                f"R² = {r2:.4f}",
                transform=ax.transAxes,
                fontsize=12,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
            )

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            logger.info(f"Prediction error plot saved to {save_path}")

        return fig

    def get_prediction_examples(
        self,
        X: pd.DataFrame,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        n_examples: int = 10,
        example_type: str = "random",
    ) -> pd.DataFrame:
        """
        Get prediction examples

        Args:
            X: Feature DataFrame
            y_true: True labels/values
            y_pred: Predicted labels/values
            n_examples: Number of examples to return
            example_type: Type of examples
                - 'random': Random samples
                - 'best': Best predictions
                - 'worst': Worst predictions
                - 'correct': Correctly predicted (classification)
                - 'incorrect': Incorrectly predicted (classification)

        Returns:
            DataFrame with examples
        """
        if self.task_type == "classification":
            correct = y_true == y_pred

            if example_type == "random":
                indices = np.random.choice(len(X), min(n_examples, len(X)), replace=False)
            elif example_type == "correct":
                indices = np.where(correct)[0]
                indices = np.random.choice(indices, min(n_examples, len(indices)), replace=False)
            elif example_type == "incorrect":
                indices = np.where(~correct)[0]
                indices = np.random.choice(indices, min(n_examples, len(indices)), replace=False)
            else:
                indices = np.random.choice(len(X), min(n_examples, len(X)), replace=False)

        else:  # regression
            errors = np.abs(y_true - y_pred)

            if example_type == "random":
                indices = np.random.choice(len(X), min(n_examples, len(X)), replace=False)
            elif example_type == "best":
                indices = np.argsort(errors)[:n_examples]
            elif example_type == "worst":
                indices = np.argsort(errors)[-n_examples:][::-1]
            else:
                indices = np.random.choice(len(X), min(n_examples, len(X)), replace=False)

        # Create examples DataFrame
        examples = X.iloc[indices].copy()
        examples["true_value"] = y_true[indices]
        examples["predicted_value"] = y_pred[indices]

        if self.task_type == "classification":
            examples["correct"] = correct[indices]
        else:
            examples["error"] = np.abs(y_true[indices] - y_pred[indices])
            examples["relative_error"] = examples["error"] / (np.abs(y_true[indices]) + 1e-10)

        return examples

    def generate_evaluation_report(self) -> str:
        """
        Generate a comprehensive evaluation report

        Returns:
            String report
        """
        if not self.evaluation_results:
            return "No evaluation results available"

        report = ["=" * 80, "MODEL EVALUATION REPORT", "=" * 80, ""]

        if self.task_type == "classification":
            report.append(f"Task Type: Classification")
            report.append(f"Accuracy: {self.evaluation_results.get('accuracy', 'N/A'):.4f}")
            report.append("")
            report.append("Weighted Averages:")
            report.append(f"  Precision: {self.evaluation_results.get('weighted_avg_precision', 'N/A'):.4f}")
            report.append(f"  Recall: {self.evaluation_results.get('weighted_avg_recall', 'N/A'):.4f}")
            report.append(f"  F1-Score: {self.evaluation_results.get('weighted_avg_f1', 'N/A'):.4f}")

            if "roc_auc" in self.evaluation_results:
                report.append("")
                report.append(f"ROC-AUC Score: {self.evaluation_results['roc_auc']:.4f}")

        else:  # regression
            report.append(f"Task Type: Regression")
            report.append(f"R² Score: {self.evaluation_results.get('r2', 'N/A'):.4f}")
            report.append(f"RMSE: {self.evaluation_results.get('rmse', 'N/A'):.4f}")
            report.append(f"MAE: {self.evaluation_results.get('mae', 'N/A'):.4f}")

            if self.evaluation_results.get('mape') is not None:
                report.append(f"MAPE: {self.evaluation_results['mape']:.4f}")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)
