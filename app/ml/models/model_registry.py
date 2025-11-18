"""
Model registry for managing ML model versions.

Provides version control, metadata tracking, and model lifecycle management.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import shutil
from dataclasses import dataclass, asdict


@dataclass
class ModelMetadata:
    """Metadata for a trained model."""
    model_id: str
    model_type: str
    version: str
    created_at: str
    created_by: str
    training_data_info: Dict[str, Any]
    performance_metrics: Dict[str, float]
    hyperparameters: Dict[str, Any]
    feature_names: List[str]
    n_features: int
    n_training_samples: int
    tags: List[str]
    description: Optional[str] = None
    parent_version: Optional[str] = None
    status: str = "active"  # active, archived, deprecated


class ModelRegistry:
    """Central registry for managing ML model versions."""

    def __init__(self, registry_path: str = "models/registry"):
        self.registry_path = Path(registry_path)
        self.registry_path.mkdir(parents=True, exist_ok=True)
        self.index_file = self.registry_path / "index.json"
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        """Load the model registry index."""
        if self.index_file.exists():
            with open(self.index_file, 'r') as f:
                return json.load(f)
        return {"models": {}, "versions": {}}

    def _save_index(self):
        """Save the model registry index."""
        with open(self.index_file, 'w') as f:
            json.dump(self.index, f, indent=2)

    def register_model(
        self,
        model_name: str,
        model_type: str,
        version: str,
        model_path: str,
        metadata: ModelMetadata,
        promote_to_production: bool = False
    ) -> str:
        """
        Register a new model version in the registry.

        Args:
            model_name: Name of the model
            model_type: Type of model (rf, xgboost, nn, ensemble)
            version: Version identifier
            model_path: Path to model files
            metadata: Model metadata
            promote_to_production: Whether to promote to production

        Returns:
            Model ID
        """
        model_id = f"{model_name}_{version}"

        # Create version entry
        version_entry = {
            "model_id": model_id,
            "model_name": model_name,
            "model_type": model_type,
            "version": version,
            "model_path": str(model_path),
            "metadata": asdict(metadata),
            "registered_at": datetime.now().isoformat(),
            "production": promote_to_production,
            "downloads": 0,
            "predictions_count": 0
        }

        # Add to index
        if model_name not in self.index["models"]:
            self.index["models"][model_name] = {
                "model_type": model_type,
                "versions": [],
                "latest_version": version,
                "production_version": version if promote_to_production else None,
                "created_at": datetime.now().isoformat()
            }

        self.index["models"][model_name]["versions"].append(version)
        self.index["models"][model_name]["latest_version"] = version

        if promote_to_production:
            self.index["models"][model_name]["production_version"] = version

        self.index["versions"][model_id] = version_entry

        self._save_index()

        print(f"Registered model: {model_id}")
        if promote_to_production:
            print(f"  Promoted to production")

        return model_id

    def get_model(
        self,
        model_name: str,
        version: Optional[str] = None,
        use_production: bool = False
    ) -> Optional[Dict]:
        """
        Get model information from registry.

        Args:
            model_name: Name of the model
            version: Specific version (None = latest)
            use_production: Use production version

        Returns:
            Model information dictionary
        """
        if model_name not in self.index["models"]:
            return None

        model_info = self.index["models"][model_name]

        # Determine version to use
        if use_production:
            version = model_info.get("production_version")
        elif version is None:
            version = model_info.get("latest_version")

        if version is None:
            return None

        model_id = f"{model_name}_{version}"
        return self.index["versions"].get(model_id)

    def list_models(self, model_type: Optional[str] = None) -> List[Dict]:
        """
        List all registered models.

        Args:
            model_type: Filter by model type

        Returns:
            List of model information
        """
        models = []

        for model_name, info in self.index["models"].items():
            if model_type is None or info["model_type"] == model_type:
                models.append({
                    "model_name": model_name,
                    "model_type": info["model_type"],
                    "latest_version": info["latest_version"],
                    "production_version": info.get("production_version"),
                    "num_versions": len(info["versions"]),
                    "created_at": info["created_at"]
                })

        return models

    def list_versions(self, model_name: str) -> List[Dict]:
        """
        List all versions of a model.

        Args:
            model_name: Name of the model

        Returns:
            List of version information
        """
        if model_name not in self.index["models"]:
            return []

        versions = []
        model_info = self.index["models"][model_name]

        for version in model_info["versions"]:
            model_id = f"{model_name}_{version}"
            version_info = self.index["versions"].get(model_id)

            if version_info:
                versions.append({
                    "version": version,
                    "model_id": model_id,
                    "registered_at": version_info["registered_at"],
                    "production": version_info["production"],
                    "performance": version_info["metadata"]["performance_metrics"]
                })

        return versions

    def promote_to_production(
        self,
        model_name: str,
        version: str
    ) -> bool:
        """
        Promote a model version to production.

        Args:
            model_name: Name of the model
            version: Version to promote

        Returns:
            True if successful
        """
        if model_name not in self.index["models"]:
            return False

        model_id = f"{model_name}_{version}"
        if model_id not in self.index["versions"]:
            return False

        # Demote current production version
        current_prod = self.index["models"][model_name].get("production_version")
        if current_prod:
            old_model_id = f"{model_name}_{current_prod}"
            if old_model_id in self.index["versions"]:
                self.index["versions"][old_model_id]["production"] = False

        # Promote new version
        self.index["models"][model_name]["production_version"] = version
        self.index["versions"][model_id]["production"] = True

        self._save_index()

        print(f"Promoted {model_id} to production")
        return True

    def archive_model(self, model_name: str, version: str) -> bool:
        """
        Archive a model version.

        Args:
            model_name: Name of the model
            version: Version to archive

        Returns:
            True if successful
        """
        model_id = f"{model_name}_{version}"

        if model_id not in self.index["versions"]:
            return False

        # Don't archive production version
        if self.index["versions"][model_id]["production"]:
            print(f"Cannot archive production version: {model_id}")
            return False

        self.index["versions"][model_id]["metadata"]["status"] = "archived"
        self._save_index()

        print(f"Archived {model_id}")
        return True

    def delete_model(
        self,
        model_name: str,
        version: str,
        delete_files: bool = False
    ) -> bool:
        """
        Delete a model version from registry.

        Args:
            model_name: Name of the model
            version: Version to delete
            delete_files: Whether to delete model files

        Returns:
            True if successful
        """
        model_id = f"{model_name}_{version}"

        if model_id not in self.index["versions"]:
            return False

        # Don't delete production version
        if self.index["versions"][model_id]["production"]:
            print(f"Cannot delete production version: {model_id}")
            return False

        version_info = self.index["versions"][model_id]

        # Delete files if requested
        if delete_files:
            model_path = Path(version_info["model_path"])
            if model_path.exists():
                if model_path.is_dir():
                    shutil.rmtree(model_path)
                else:
                    model_path.unlink()

        # Remove from index
        del self.index["versions"][model_id]

        # Update model versions list
        if model_name in self.index["models"]:
            versions = self.index["models"][model_name]["versions"]
            if version in versions:
                versions.remove(version)

            # Update latest version
            if versions:
                self.index["models"][model_name]["latest_version"] = versions[-1]
            else:
                # No more versions, remove model
                del self.index["models"][model_name]

        self._save_index()

        print(f"Deleted {model_id}")
        return True

    def compare_versions(
        self,
        model_name: str,
        version1: str,
        version2: str
    ) -> Dict:
        """
        Compare two model versions.

        Args:
            model_name: Name of the model
            version1: First version
            version2: Second version

        Returns:
            Comparison dictionary
        """
        model_id1 = f"{model_name}_{version1}"
        model_id2 = f"{model_name}_{version2}"

        if model_id1 not in self.index["versions"] or model_id2 not in self.index["versions"]:
            return {}

        v1_info = self.index["versions"][model_id1]
        v2_info = self.index["versions"][model_id2]

        comparison = {
            "version1": version1,
            "version2": version2,
            "performance_comparison": {},
            "metadata_comparison": {}
        }

        # Compare performance metrics
        metrics1 = v1_info["metadata"]["performance_metrics"]
        metrics2 = v2_info["metadata"]["performance_metrics"]

        for metric in metrics1.keys():
            if metric in metrics2:
                comparison["performance_comparison"][metric] = {
                    "version1": metrics1[metric],
                    "version2": metrics2[metric],
                    "difference": metrics2[metric] - metrics1[metric],
                    "improvement": ((metrics2[metric] - metrics1[metric]) / metrics1[metric] * 100)
                    if metrics1[metric] != 0 else 0
                }

        # Compare metadata
        comparison["metadata_comparison"] = {
            "n_features": {
                "version1": v1_info["metadata"]["n_features"],
                "version2": v2_info["metadata"]["n_features"]
            },
            "n_training_samples": {
                "version1": v1_info["metadata"]["n_training_samples"],
                "version2": v2_info["metadata"]["n_training_samples"]
            }
        }

        return comparison

    def get_best_model(
        self,
        model_name: str,
        metric: str = "f1_score"
    ) -> Optional[Dict]:
        """
        Get the best performing model version based on a metric.

        Args:
            model_name: Name of the model
            metric: Metric to optimize

        Returns:
            Best model information
        """
        if model_name not in self.index["models"]:
            return None

        versions = self.list_versions(model_name)

        if not versions:
            return None

        # Find version with best metric
        best_version = max(
            versions,
            key=lambda v: v["performance"].get(metric, 0)
        )

        return self.get_model(model_name, best_version["version"])

    def get_statistics(self) -> Dict:
        """
        Get registry statistics.

        Returns:
            Statistics dictionary
        """
        total_models = len(self.index["models"])
        total_versions = len(self.index["versions"])

        model_types = {}
        production_models = 0

        for model_name, info in self.index["models"].items():
            model_type = info["model_type"]
            model_types[model_type] = model_types.get(model_type, 0) + 1

            if info.get("production_version"):
                production_models += 1

        return {
            "total_models": total_models,
            "total_versions": total_versions,
            "production_models": production_models,
            "models_by_type": model_types,
            "registry_path": str(self.registry_path),
            "index_file": str(self.index_file)
        }
