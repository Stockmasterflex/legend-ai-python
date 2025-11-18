"""
Model Deployment Module

Provides tools for saving/loading models, versioning, A/B testing, and rollback capabilities.
"""

from typing import Dict, List, Optional, Any, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import json
import joblib
import hashlib
import shutil
import logging
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)


class ModelStatus(str, Enum):
    """Model deployment status"""
    TRAINING = "training"
    STAGED = "staged"
    PRODUCTION = "production"
    ARCHIVED = "archived"
    FAILED = "failed"


@dataclass
class ModelMetadata:
    """Metadata for a deployed model"""
    model_id: str
    version: str
    name: str
    task_type: str
    algorithm: str
    created_at: datetime
    status: ModelStatus
    metrics: Dict[str, float]
    hyperparameters: Dict[str, Any]
    feature_names: List[str]
    target_name: str
    training_samples: int
    file_path: str
    checksum: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class ModelDeployment:
    """Comprehensive model deployment and versioning system"""

    def __init__(self, models_dir: str = "models"):
        """
        Initialize ModelDeployment

        Args:
            models_dir: Directory to store models
        """
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_file = self.models_dir / "models_metadata.json"
        self.models_metadata: Dict[str, ModelMetadata] = {}
        self._load_metadata()

    def _load_metadata(self):
        """Load models metadata from disk"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, "r") as f:
                    data = json.load(f)
                    for model_id, meta_dict in data.items():
                        meta_dict["created_at"] = datetime.fromisoformat(meta_dict["created_at"])
                        meta_dict["status"] = ModelStatus(meta_dict["status"])
                        self.models_metadata[model_id] = ModelMetadata(**meta_dict)
                logger.info(f"Loaded metadata for {len(self.models_metadata)} models")
            except Exception as e:
                logger.error(f"Error loading metadata: {e}")
                self.models_metadata = {}

    def _save_metadata(self):
        """Save models metadata to disk"""
        try:
            data = {}
            for model_id, metadata in self.models_metadata.items():
                meta_dict = asdict(metadata)
                meta_dict["created_at"] = metadata.created_at.isoformat()
                meta_dict["status"] = metadata.status.value
                data[model_id] = meta_dict

            with open(self.metadata_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("Metadata saved successfully")
        except Exception as e:
            logger.error(f"Error saving metadata: {e}")

    def _generate_model_id(self, name: str) -> str:
        """Generate unique model ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8]
        return f"{name}_{timestamp}_{random_suffix}"

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate file checksum"""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def save_model(
        self,
        model: Any,
        name: str,
        version: str,
        task_type: str,
        algorithm: str,
        metrics: Dict[str, float],
        hyperparameters: Dict[str, Any],
        feature_names: List[str],
        target_name: str,
        training_samples: int,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        status: ModelStatus = ModelStatus.STAGED,
    ) -> str:
        """
        Save a trained model with metadata

        Args:
            model: Trained model object
            name: Model name
            version: Model version
            task_type: 'classification' or 'regression'
            algorithm: Algorithm name
            metrics: Performance metrics
            hyperparameters: Model hyperparameters
            feature_names: List of feature names
            target_name: Target variable name
            training_samples: Number of training samples
            description: Optional model description
            tags: Optional tags for categorization
            status: Initial deployment status

        Returns:
            Model ID
        """
        model_id = self._generate_model_id(name)

        # Create model directory
        model_dir = self.models_dir / model_id
        model_dir.mkdir(parents=True, exist_ok=True)

        # Save model file
        model_file = model_dir / "model.pkl"
        joblib.dump(model, model_file)

        # Calculate checksum
        checksum = self._calculate_checksum(model_file)

        # Save feature names
        features_file = model_dir / "features.json"
        with open(features_file, "w") as f:
            json.dump({"features": feature_names, "target": target_name}, f, indent=2)

        # Create metadata
        metadata = ModelMetadata(
            model_id=model_id,
            version=version,
            name=name,
            task_type=task_type,
            algorithm=algorithm,
            created_at=datetime.now(),
            status=status,
            metrics=metrics,
            hyperparameters=hyperparameters,
            feature_names=feature_names,
            target_name=target_name,
            training_samples=training_samples,
            file_path=str(model_file),
            checksum=checksum,
            description=description,
            tags=tags or [],
        )

        self.models_metadata[model_id] = metadata
        self._save_metadata()

        logger.info(f"Model saved successfully: {model_id}")
        return model_id

    def load_model(self, model_id: str) -> Tuple[Any, ModelMetadata]:
        """
        Load a model by ID

        Args:
            model_id: Model ID

        Returns:
            Tuple of (model, metadata)
        """
        if model_id not in self.models_metadata:
            raise ValueError(f"Model not found: {model_id}")

        metadata = self.models_metadata[model_id]
        model_file = Path(metadata.file_path)

        if not model_file.exists():
            raise FileNotFoundError(f"Model file not found: {model_file}")

        # Verify checksum
        current_checksum = self._calculate_checksum(model_file)
        if current_checksum != metadata.checksum:
            logger.warning(f"Checksum mismatch for model {model_id}")

        model = joblib.load(model_file)
        logger.info(f"Model loaded successfully: {model_id}")

        return model, metadata

    def get_model_by_version(self, name: str, version: str) -> Optional[Tuple[Any, ModelMetadata]]:
        """
        Get model by name and version

        Args:
            name: Model name
            version: Model version

        Returns:
            Tuple of (model, metadata) or None if not found
        """
        for model_id, metadata in self.models_metadata.items():
            if metadata.name == name and metadata.version == version:
                return self.load_model(model_id)
        return None

    def get_production_model(self, name: str) -> Optional[Tuple[Any, ModelMetadata]]:
        """
        Get the production model by name

        Args:
            name: Model name

        Returns:
            Tuple of (model, metadata) or None if no production model exists
        """
        for model_id, metadata in self.models_metadata.items():
            if metadata.name == name and metadata.status == ModelStatus.PRODUCTION:
                return self.load_model(model_id)
        return None

    def promote_to_production(
        self,
        model_id: str,
        demote_current: bool = True,
    ) -> bool:
        """
        Promote a model to production

        Args:
            model_id: Model ID to promote
            demote_current: Whether to demote current production model

        Returns:
            Success status
        """
        if model_id not in self.models_metadata:
            raise ValueError(f"Model not found: {model_id}")

        metadata = self.models_metadata[model_id]

        # Demote current production model if requested
        if demote_current:
            for mid, meta in self.models_metadata.items():
                if meta.name == metadata.name and meta.status == ModelStatus.PRODUCTION:
                    meta.status = ModelStatus.ARCHIVED
                    logger.info(f"Demoted model {mid} from production to archived")

        # Promote new model
        metadata.status = ModelStatus.PRODUCTION
        self._save_metadata()

        logger.info(f"Model {model_id} promoted to production")
        return True

    def rollback_model(self, name: str, to_version: Optional[str] = None) -> Optional[str]:
        """
        Rollback to a previous model version

        Args:
            name: Model name
            to_version: Specific version to rollback to (if None, rollback to last archived)

        Returns:
            Model ID that was promoted, or None if rollback failed
        """
        # Find target model
        target_model_id = None

        if to_version:
            # Rollback to specific version
            for model_id, metadata in self.models_metadata.items():
                if metadata.name == name and metadata.version == to_version:
                    target_model_id = model_id
                    break
        else:
            # Rollback to last archived model
            archived_models = [
                (model_id, metadata)
                for model_id, metadata in self.models_metadata.items()
                if metadata.name == name and metadata.status == ModelStatus.ARCHIVED
            ]

            if archived_models:
                # Sort by creation date and get the most recent
                archived_models.sort(key=lambda x: x[1].created_at, reverse=True)
                target_model_id = archived_models[0][0]

        if target_model_id:
            self.promote_to_production(target_model_id, demote_current=True)
            logger.info(f"Rolled back to model {target_model_id}")
            return target_model_id
        else:
            logger.warning(f"No suitable model found for rollback")
            return None

    def delete_model(self, model_id: str, force: bool = False):
        """
        Delete a model

        Args:
            model_id: Model ID to delete
            force: Force deletion even if model is in production
        """
        if model_id not in self.models_metadata:
            raise ValueError(f"Model not found: {model_id}")

        metadata = self.models_metadata[model_id]

        # Prevent deletion of production models unless forced
        if metadata.status == ModelStatus.PRODUCTION and not force:
            raise ValueError("Cannot delete production model without force=True")

        # Delete model directory
        model_dir = Path(metadata.file_path).parent
        if model_dir.exists():
            shutil.rmtree(model_dir)

        # Remove from metadata
        del self.models_metadata[model_id]
        self._save_metadata()

        logger.info(f"Model deleted: {model_id}")

    def list_models(
        self,
        name: Optional[str] = None,
        status: Optional[ModelStatus] = None,
        tags: Optional[List[str]] = None,
    ) -> List[ModelMetadata]:
        """
        List models with optional filters

        Args:
            name: Filter by model name
            status: Filter by status
            tags: Filter by tags (any match)

        Returns:
            List of model metadata
        """
        models = list(self.models_metadata.values())

        if name:
            models = [m for m in models if m.name == name]

        if status:
            models = [m for m in models if m.status == status]

        if tags:
            models = [m for m in models if any(tag in m.tags for tag in tags)]

        # Sort by creation date (newest first)
        models.sort(key=lambda x: x.created_at, reverse=True)

        return models

    def compare_models(self, model_ids: List[str]) -> pd.DataFrame:
        """
        Compare multiple models

        Args:
            model_ids: List of model IDs to compare

        Returns:
            DataFrame with model comparison
        """
        comparison_data = []

        for model_id in model_ids:
            if model_id not in self.models_metadata:
                logger.warning(f"Model not found: {model_id}")
                continue

            metadata = self.models_metadata[model_id]

            record = {
                "model_id": model_id,
                "name": metadata.name,
                "version": metadata.version,
                "algorithm": metadata.algorithm,
                "status": metadata.status.value,
                "created_at": metadata.created_at,
                "training_samples": metadata.training_samples,
            }

            # Add metrics
            record.update(metadata.metrics)

            comparison_data.append(record)

        return pd.DataFrame(comparison_data)

    def setup_ab_test(
        self,
        model_a_id: str,
        model_b_id: str,
        test_name: str,
        split_ratio: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Setup A/B test between two models

        Args:
            model_a_id: First model ID
            model_b_id: Second model ID
            test_name: Name for the A/B test
            split_ratio: Ratio of traffic to model A (0-1)

        Returns:
            A/B test configuration
        """
        if model_a_id not in self.models_metadata:
            raise ValueError(f"Model A not found: {model_a_id}")
        if model_b_id not in self.models_metadata:
            raise ValueError(f"Model B not found: {model_b_id}")

        config = {
            "test_name": test_name,
            "model_a": {
                "model_id": model_a_id,
                "metadata": asdict(self.models_metadata[model_a_id]),
                "traffic_ratio": split_ratio,
            },
            "model_b": {
                "model_id": model_b_id,
                "metadata": asdict(self.models_metadata[model_b_id]),
                "traffic_ratio": 1 - split_ratio,
            },
            "created_at": datetime.now().isoformat(),
            "status": "active",
        }

        # Save A/B test config
        ab_test_file = self.models_dir / f"ab_test_{test_name}.json"
        with open(ab_test_file, "w") as f:
            # Convert datetime objects to strings for JSON serialization
            config_copy = config.copy()
            config_copy["model_a"]["metadata"]["created_at"] = config_copy["model_a"]["metadata"]["created_at"].isoformat()
            config_copy["model_a"]["metadata"]["status"] = config_copy["model_a"]["metadata"]["status"].value
            config_copy["model_b"]["metadata"]["created_at"] = config_copy["model_b"]["metadata"]["created_at"].isoformat()
            config_copy["model_b"]["metadata"]["status"] = config_copy["model_b"]["metadata"]["status"].value
            json.dump(config_copy, f, indent=2)

        logger.info(f"A/B test created: {test_name}")
        return config

    def predict_ab_test(
        self,
        test_name: str,
        X: pd.DataFrame,
        user_id: Optional[str] = None,
    ) -> Tuple[np.ndarray, str]:
        """
        Make prediction using A/B test

        Args:
            test_name: A/B test name
            X: Features for prediction
            user_id: Optional user ID for consistent routing

        Returns:
            Tuple of (predictions, model_id_used)
        """
        ab_test_file = self.models_dir / f"ab_test_{test_name}.json"

        if not ab_test_file.exists():
            raise ValueError(f"A/B test not found: {test_name}")

        with open(ab_test_file, "r") as f:
            config = json.load(f)

        # Determine which model to use
        if user_id:
            # Consistent hashing for same user
            hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
            use_model_a = (hash_value % 100) < (config["model_a"]["traffic_ratio"] * 100)
        else:
            # Random assignment
            use_model_a = np.random.random() < config["model_a"]["traffic_ratio"]

        model_id = config["model_a"]["model_id"] if use_model_a else config["model_b"]["model_id"]
        model, _ = self.load_model(model_id)

        predictions = model.predict(X)

        return predictions, model_id

    def export_model(
        self,
        model_id: str,
        export_path: str,
        include_metadata: bool = True,
    ):
        """
        Export model to a different location

        Args:
            model_id: Model ID to export
            export_path: Path to export to
            include_metadata: Whether to include metadata
        """
        if model_id not in self.models_metadata:
            raise ValueError(f"Model not found: {model_id}")

        metadata = self.models_metadata[model_id]
        export_dir = Path(export_path)
        export_dir.mkdir(parents=True, exist_ok=True)

        # Copy model file
        src_file = Path(metadata.file_path)
        dst_file = export_dir / "model.pkl"
        shutil.copy2(src_file, dst_file)

        if include_metadata:
            # Export metadata
            meta_dict = asdict(metadata)
            meta_dict["created_at"] = metadata.created_at.isoformat()
            meta_dict["status"] = metadata.status.value

            metadata_file = export_dir / "metadata.json"
            with open(metadata_file, "w") as f:
                json.dump(meta_dict, f, indent=2)

            # Copy features file
            features_file = src_file.parent / "features.json"
            if features_file.exists():
                shutil.copy2(features_file, export_dir / "features.json")

        logger.info(f"Model exported to {export_path}")

    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Get detailed model information

        Args:
            model_id: Model ID

        Returns:
            Dictionary with model information
        """
        if model_id not in self.models_metadata:
            raise ValueError(f"Model not found: {model_id}")

        metadata = self.models_metadata[model_id]
        model_file = Path(metadata.file_path)

        info = asdict(metadata)
        info["created_at"] = metadata.created_at.isoformat()
        info["status"] = metadata.status.value
        info["file_size_mb"] = model_file.stat().st_size / (1024 * 1024) if model_file.exists() else 0

        return info
