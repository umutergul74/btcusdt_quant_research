import os
import joblib
from typing import Any, Optional
from utils.logging_utils import setup_logger

logger = setup_logger("model_registry")

class ModelRegistry:
    """Manages saving and loading of model checkpoints and hyperparameter studies."""
    def __init__(self, project_root: str = "/content/drive/MyDrive/btcusdt_quant_research"):
        self.project_root = project_root
        self.checkpoint_dir = os.path.join(project_root, "models", "checkpoints")
        self.trained_dir = os.path.join(project_root, "models", "trained_models")
        
        # Fallback to local paths
        if not os.path.exists(os.path.join(project_root, "models")):
            self.checkpoint_dir = os.path.join(os.getcwd(), "models", "checkpoints")
            self.trained_dir = os.path.join(os.getcwd(), "models", "trained_models")

    def save_model(self, model: Any, name: str) -> bool:
        """Saves a trained model file."""
        path = os.path.join(self.trained_dir, f"{name}.joblib")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        try:
            joblib.dump(model, path)
            logger.info(f"Model saved to {path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save model {name}: {e}")
            return False

    def load_model(self, name: str) -> Optional[Any]:
        """Loads a trained model file."""
        path = os.path.join(self.trained_dir, f"{name}.joblib")
        if not os.path.exists(path):
            logger.warning(f"Model file not found: {path}")
            return None
        try:
            model = joblib.load(path)
            logger.info(f"Model loaded from {path}")
            return model
        except Exception as e:
            logger.error(f"Failed to load model {name}: {e}")
            return None
            
    def get_optuna_storage_url(self) -> str:
        """Returns the persistent SQLite storage URL for Optuna."""
        db_path = os.path.join(self.checkpoint_dir, "optuna_study.db")
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        return f"sqlite:///{db_path}"
